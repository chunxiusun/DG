#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
import sys
#import Image
import cv2
import xlwt
import copy
#from PIL import Image
#import Queue
import multiprocessing

THRESHOLD = 0.5
imagePath = "./images_all/"
imageFile = "./images_all/"
gFile = "./12groundtruth/"
tFile = "./12testresult_6/"
xlsxfile = "12_6.xls"

r_result = "./rate_result_6/"
os.system("rm -r %s"%r_result)
os.system("mkdir %s"%r_result)

v_image = "./visual_image_6/"
os.system("rm -r %s"%v_image)
os.system("mkdir %s"%v_image)

#q = Queue.Queue(maxsize=0)
lock = multiprocessing.Lock()

def recallRate(g_list,t_list,fd,fn):
    g_num = len(g_list)
    t_num = len(t_list)
    #iou = 0.0
    #iou_count = 0
    #recall rate
    recall_list = []
    for item in g_list:
        gframeid = item.split(",")[0]
        groi = item.split(",")[3:7]
        dct = {}
        flag = False
        for data in t_list:
            tframeid = data[0]
            troi = data[2:6]
            if gframeid == tframeid:
                ratio = CalRatio(groi, troi)
                if ratio >= THRESHOLD:
                    flag = True
                    dct[str(ratio)] = data #有多个符合条件的
                    #iou = iou + ratio
                    #iou_count += 1
        if flag == True:
            recall_list.append(item)
        
        if len(dct) == 0:
            continue
        else:
            c_list = sorted(dct.keys(),reverse=True) #相邻车的情况，取ratio最大的,从tlist中去除
            key = c_list[0]
            t_list.remove(dct[key])
    if g_num == 0:
        recall_rate = 0
        value = ""
    else:
        recall_rate = len(recall_list)*1.0/g_num
        value = "%0.2f%s"%(recall_rate*100,"%")
    fn.write("%s,"%value)
    fd.write("recall rate:%0.2f%s\n"%(recall_rate*100,"%"))
    #print "recall rate:%0.2f%s"%(recall_rate*100,"%")

def cc_recallRate(g_list_tmp,t_list_tmp,g_num,t_num,fd,fn):
    g_list=copy.deepcopy(g_list_tmp)
    t_list=copy.deepcopy(t_list_tmp)
            
    recall_list = []
    for img_id in g_list:
        for item in g_list[img_id]:
            groi = item.split(",")[3:7]
            dct = {}
            flag = False
            if img_id in t_list:
                for data in t_list[img_id]:
                    troi = data[2:6]
                    ratio = CalRatio(groi, troi)
                    if ratio >= THRESHOLD:
                        flag = True
                        dct[str(ratio)] = data #有多个符合条件的
            if flag == True:
                recall_list.append(item)
            
            if len(dct) == 0:
                continue
            else:
                c_list = sorted(dct.keys(),reverse=True) #相邻车的情况，取ratio最大的,从tlist中去除
                key = c_list[0]
                t_list[img_id].remove(dct[key])
    if g_num == 0:
        recall_rate = 0
        value = ""
    else:
        recall_rate = len(recall_list)*1.0/g_num
        value = "%0.2f%s"%(recall_rate*100,"%")
    fn.write("%s,"%value)
    fd.write("recall rate:%0.2f%s\n"%(recall_rate*100,"%"))

def accuracyRate(g_list,t_list,fd,fn):
    t_num = len(t_list)
    success_list = []
    for data in t_list:
        tframeid = data[0]
        troi = data[2:6]
        dct = {}
        flag = False
        for item in g_list:
            gframeid = item.split(",")[0]
            groi = item.split(",")[3:7]
            if gframeid == tframeid:
                ratio = CalRatio(groi, troi)
                if ratio >= THRESHOLD:
                    flag = True
                    dct[str(ratio)] = item #有多个符合条件的,去掉最符合条件的那个
        if flag == True:
            success_list.append(data)
        if len(dct) == 0:
            continue
        else:
            c_list = sorted(dct.keys(),reverse=True)
            key = c_list[0]
            g_list.remove(dct[key]) #有多个符合条件的,去掉最符合条件的那个
    if t_num == 0:
        accuracy_rate = 0
        value = ""
    else:
        accuracy_rate = len(success_list)*1.0/t_num
        value = "%0.2f%s"%(accuracy_rate*100,"%")
    fn.write("%s,"%value)
    fd.write("accuracy rate:%0.2f%s\n"%(accuracy_rate*100,"%"))
    #print "accuracy rate:%0.2f%s"%(accuracy_rate*100,"%")

def cc_accuracyRate(g_list_tmp,t_list_tmp,g_num,t_num,fd,fn):
    g_list=copy.deepcopy(g_list_tmp)
    t_list=copy.deepcopy(t_list_tmp)
    
    success_list = []
    for img_id in t_list:
        for data in t_list[img_id]:
            troi = data[2:6]
            dct = {}
            flag = False
            if img_id in g_list:
                for item in g_list[img_id]:
                    groi = item.split(",")[3:7]
                    ratio = CalRatio(groi, troi)
                    if ratio >= THRESHOLD:
                        flag = True
                        dct[str(ratio)] = item #有多个符合条件的,去掉最符合条件的那个
            if flag == True:
                success_list.append(data)
            if len(dct) == 0:
                continue
            else:
                c_list = sorted(dct.keys(),reverse=True)
                key = c_list[0]
                g_list[img_id].remove(dct[key]) #有多个符合条件的,去掉最符合条件的那个
  

    if t_num == 0:
        accuracy_rate = 0
        value = ""
    else:
        accuracy_rate = len(success_list)*1.0/t_num
        value = "%0.2f%s"%(accuracy_rate*100,"%")
    fn.write("%s,"%value)
    fd.write("accuracy rate:%0.2f%s\n"%(accuracy_rate*100,"%"))
    #print "accuracy rate:%0.2f%s"%(accuracy_rate*100,"%")
    
def t_detect_classify(tlist,fd):
    vehicle = []
    pedestrian = []
    bicycle = []
    tricycle = []
    for item in tlist:
        ty = item[1]
        #del item[1]
        if ty == "1":
            vehicle.append(item)
        elif ty == "2":
            pedestrian.append(item)
        elif ty == "3":
            bicycle.append(item)
        elif ty == "4":
            tricycle.append(item)
    fd.write("test result classify:%d,%d,%d,%d\n"%(len(vehicle),len(pedestrian),len(bicycle),len(tricycle)))
    #print "test result classify:%d,%d,%d,%d"%(len(vehicle),len(pedestrian),len(bicycle),len(tricycle))
    return vehicle,pedestrian,bicycle,tricycle

def cc_t_detect_classify(tlist,fd):
    vehicle = {}
    pedestrian = {}
    bicycle = {}
    tricycle = {}
    num_vehicle=0
    num_pedestrian=0
    num_bicycle=0
    num_tricycle=0
    for img_id in tlist:
        vehicle[img_id]=[]
        pedestrian[img_id]=[]
        bicycle[img_id]=[]
        tricycle[img_id]=[]
        for item in tlist[img_id]:
            ty = item[1]
            #del item[1]
            if ty == "1":
                vehicle[img_id].append(item)
                num_vehicle+=1
            elif ty == "2":
                pedestrian[img_id].append(item)
                num_pedestrian+=1
            elif ty == "3":
                bicycle[img_id].append(item)
                num_bicycle+=1
            elif ty == "4":
                tricycle[img_id].append(item)
                num_tricycle+=1
    fd.write("test result classify:%d,%d,%d,%d\n"%(num_vehicle,num_pedestrian,num_bicycle,num_tricycle))
    return vehicle,pedestrian,bicycle,tricycle,num_vehicle,num_pedestrian,num_bicycle,num_tricycle

def g_detect_classify(glist,fd):
    vehicle = []
    pedestrian = []
    bicycle = []
    tricycle = []
    for item in glist:
        detect_type = item.split(",")[2]
        if detect_type == "1":                                                                                                             
            vehicle.append(item)                                                                                                           
        elif detect_type == "2":                                                                                                           
            pedestrian.append(item)                                                                                                        
        elif detect_type == "3":                                                                                                           
            bicycle.append(item)                                                                                                           
        elif detect_type == "4":                                                                                                           
            tricycle.append(item)
    fd.write("groundtruth classify:%d,%d,%d,%d\n"%(len(vehicle),len(pedestrian),len(bicycle),len(tricycle)))
    #print "groundtruth classify:%d,%d,%d,%d"%(len(vehicle),len(pedestrian),len(bicycle),len(tricycle))                                                 
    return vehicle,pedestrian,bicycle,tricycle

def cc_g_detect_classify(glist,fd):
    vehicle = {}
    pedestrian = {}
    bicycle = {}
    tricycle = {}
    num_vehicle=0
    num_pedestrian=0
    num_bicycle=0
    num_tricycle=0
    for img_id in glist:
        vehicle[img_id]=[]
        pedestrian[img_id]=[]
        bicycle[img_id]=[]
        tricycle[img_id]=[]
        for item in glist[img_id]:
            detect_type = item.split(",")[2]
            if detect_type == "1":                                                                                                             
                vehicle[img_id].append(item)
                num_vehicle+=1                                                                                                           
            elif detect_type == "2":                                                                                                           
                pedestrian[img_id].append(item)  
                num_pedestrian+=1                                                                                                      
            elif detect_type == "3":                                                                                                           
                bicycle[img_id].append(item) 
                num_bicycle+=1                                                                                                          
            elif detect_type == "4":                                                                                                           
                tricycle[img_id].append(item)
                num_tricycle+=1

    fd.write("groundtruth classify:%d,%d,%d,%d\n"%(num_vehicle,num_pedestrian,num_bicycle,num_tricycle))
    return vehicle,pedestrian,bicycle,tricycle,num_vehicle,num_pedestrian,num_bicycle,num_tricycle

'''
def dealFilter(lst,rootdir,fd,n):
    lst32 = []
    lst3248 = []
    lst48 = []
    #other = []
    for item in lst:
        if n == "g":
            frameid = item.strip().split(",")[0]
            roi = item.strip().split(",")[3:7]
        elif n == "t":
            frameid = item[0]
            roi = item[2:6]
        img = "%s/%s.jpg"%(rootdir,frameid)
        a1,a2 = getResolutionRatio(img)
        w = eval(roi[2])
        h = eval(roi[3])
        nw = w * a1
        nh = h * a2
        if nw <= 32 and nh <= 64:
            lst32.append(item)
        #elif nw > 32 and nw <= 48 and nh > 64 and nh <= 96:
         #   lst3248.append(item)
        elif nw > 48 and nh > 96:
            lst48.append(item)
        else:
            lst3248.append(item)
    s = ""
    if n == "g":
        s = "groundtruth filter"
    elif n == "t":
        s = "test result filter"
    fd.write("%s 32:%d 3248:%d 48:%d\n"%(s,len(lst32),len(lst3248),len(lst48)))
    #print "%s 32:%d 3248:%d 48:%d"%(s,len(lst32),len(lst3248),len(lst48))
    return lst32,lst3248,lst48

'''

def cc_dealFilter(lst,rootdir,fd,n):
    lst32 = {}
    lst3248 = {}
    lst48 = {}
    num_lst32=0
    num_lst3248=0
    num_lst48=0
    for item in lst:
        frameid=item
        lst32[item]=[]
        lst3248[item]=[]
        lst48[item]=[]
        img = "%s/%s.jpg"%(rootdir,frameid)
        w_1920,h_1080 = getResolutionRatio(img)  ## w_1920=img_width/1920
        for box in lst[item]:
            if n == "g":
                roi = box.strip().split(",")[3:7]
            else :##n == "t"
                roi = box[2:6]
            w = eval(roi[2])
            h = eval(roi[3])
            nw = w / (w_1920+0.0001)
            nh = h / (h_1080+0.0001)  ## new geight when img resizes to 1920x1080
            if nw <= 32 and nh <= 64:
                lst32[item].append(box)
                num_lst32+=1
            elif nw > 48 and nh > 96:
                lst48[item].append(box)
                num_lst48+=1
            else:
                lst3248[item].append(box)  ## danger
                num_lst3248+=1
    s = ""
    if n == "g":
        s = "groundtruth filter"
    elif n == "t":
        s = "test result filter"
    fd.write("%s 32:%d 3248:%d 48:%d\n"%(s,num_lst32,num_lst3248,num_lst48))
    #print "%s 32:%d 3248:%d 48:%d"%(s,len(lst32),len(lst3248),len(lst48))
    return lst32,lst3248,lst48,num_lst32,num_lst3248,num_lst48

##images is img_list, filename is groundtruth_list of img_list
def dealGroundTruthInput(images,filename):
    glist = []
    if os.path.isdir(images):
        lst = os.listdir(images)
        fd = open(filename,'r')
        for line in fd.readlines():
            gframeid = line.strip().split(",")[0]
            for i in range(0,len(lst)):
                iframeid = lst[i].split(".")[0]
                if iframeid == gframeid:
                    glist.append(line.strip())
        fd.close()
    elif os.path.isfile(images):
        lst = []
        fi = open(images,'r')
        for line in fi.readlines():
            iframeid = line.strip().split("/")[-1].split(".")[0]
            lst.append(iframeid)
        fi.close()
        fd = open(filename,'r')
        for line in fd.readlines():
            gframeid = line.strip().split(",")[0]
            for i in range(0,len(lst)):##slow
                iframeid = lst[i]
                if iframeid == gframeid:
                    glist.append(line.strip())
        fd.close()
    return glist

def cc_dealGroundTruthInput(images,filename):
    glist = {}
    if os.path.isdir(images):
        lst = os.listdir(images)
        fd = open(filename,'r')
        ### not finished ###
    elif os.path.isfile(images):
        lst = []
        fi = open(images,'r')
        for line in fi.readlines():
            iframeid = line.strip().split("/")[-1].split(".")[0] ### line = /home/chencheng/tools/chunxiu_mAP/images_all/1/001673.jpg
            lst.append(iframeid)
        fi.close()
        fd = open(filename,'r')
        for line in fd.readlines():
            gframeid = line.strip().split(",")[0] ### line = 001673,74,1,475.5,7.5,215,177, means iframeid,?,class,xmin,ymin,width,height
            
            if gframeid in lst:
                if gframeid in glist:
                    glist[gframeid].append(line.strip())
                else:
                    glist[gframeid] = [line.strip()]
        
        fd.close()
    

    return glist





def dealTestResultInput(filename):
    tlist = []
    fd = open(filename,'r')
    for line in fd.readlines():
        data = line.strip().split(" ")
        frameid = data[0].split("/")[-1].split(".")[0]
        for i in range(2,len(data),6):
           lst = []
           lst.append(frameid)
           lst.append(data[i])
           lst.append(data[i+1])
           lst.append(data[i+2])
           lst.append(data[i+3])
           lst.append(data[i+4])
           tlist.append(lst)
    return tlist 

def cc_dealTestResultInput(filename):
    tlist = {}
    fd = open(filename,'r')
    for line in fd.readlines():
        data = line.strip().split(" ")   ### line = /home/chencheng/tools/chunxiu_mAP/images_all/1/001673.jpg 0.999969 1 472 303 450 498 \
        ### 0.999878 1 6 406 343 294 0.999870 1 254 132 299 267 0.999160 1 682 86 246 201 0.998409 1 3 92 228 207 0.990335 1 486 10 204 178 \
        ### 0.978699 1 236 0 217 141 means score,class,xmin,ymin,width,height

        frameid = data[0].split("/")[-1].split(".")[0]
        tlist[frameid]=[]
        for i in range(2,len(data),6):
           lst = []
           lst.append(frameid)
           lst.append(data[i]) ##class
           lst.append(data[i+1]) ##xmin
           lst.append(data[i+2]) ##ymin
           lst.append(data[i+3]) ##width
           lst.append(data[i+4]) ##height
           tlist[frameid].append(lst)
        #print('tlist[frameid]:{}'.format(tlist[frameid]))
        #sys.exit()
    return tlist 

def getResolutionRatio(img):
    #im = Image.open(img)
    h,w,c=cv2.imread(img).shape
    aw = w*1.0/1920
    ah = h*1.0/1080
    return aw,ah


def CalRatio(pos1, pos2):
    ratio = 0.0
    x1 = float(pos1[0])
    x2 = float(pos2[0])
    y1 = float(pos1[1])
    y2 = float(pos2[1])
    width1 = float(pos1[2])
    width2 = float(pos2[2])
    height1 = float(pos1[3])
    height2 = float(pos2[3])

    startx = min(x1, x2)
    endx = max(x1+width1, x2+width2)
    width = width1 + width2 - (endx - startx)

    starty = min(y1, y2)
    endy = max(y1+height1, y2+height2)
    height = height1 + height2 - (endy - starty)

    if (width <= 0) or (height <= 0):
        ratio = 0.0
    else:
        area = width * height
        area1 = width1 * height1
        area2 = width2 * height2
        ratio = area*1.0 / (area1 + area2 - area)
    return ratio

def visual(s_img,t_img,glist,tlist,i,filt=""):
     d = str(i)+filt
     os.system("mkdir %s/%s"%(t_img,d))
     fd = open(s_img,'r')
     for line in fd.readlines():
         s_name = line.strip()
         img = s_name.split("/")[-1]
     #for img in os.listdir(s_img):
         flag = False
         #s_name = "%s/%s"%(s_img,img)
         im = cv2.imread(s_name)
         im_copy = im.copy()
         frameid = img.split(".")[0]
         for g in glist:
             data = g.split(",")
             gframeid = data[0]
             roi = data[3:7]
             if frameid == gframeid:
                 flag = True
                 x = eval(roi[0])
                 y = eval(roi[1])
                 x1 = eval(roi[0]) + eval(roi[2])
                 y1 = eval(roi[1]) + eval(roi[3])
                 cv2.rectangle(im_copy,(int(x),int(y)),(int(x1),int(y1)),(0,0,255),3)
         for t in tlist:
             data = t
             tframeid = data[0]
             roi = data[2:6]
             if frameid == tframeid:
                 flag = True
                 x = eval(roi[0])
                 y = eval(roi[1])
                 x1 = eval(roi[0]) + eval(roi[2])
                 y1 = eval(roi[1]) + eval(roi[3])
                 cv2.rectangle(im_copy,(int(x),int(y)),(int(x1),int(y1)),(0,255,0),3)
         if flag == True:
             cv2.imwrite("%s/%s/%s"%(t_img,d,img), im_copy)
         #break
     fd.close()

def cc_visual(s_img,t_img,glist,tlist,i,filt=""):
     d = str(i)+filt
     os.system("mkdir %s/%s"%(t_img,d))
     fd = open(s_img,'r')
     lines = fd.readlines()
     for i in range(500):
         line = lines[i]
         s_name = line.strip()
         img = s_name.split("/")[-1]
         flag = False
         im = cv2.imread(s_name)
         im_copy = im.copy()
         frameid = img.split(".")[0]
         if glist.has_key(frameid):
             for g in glist[frameid]:
                 data = g.split(",")
                 roi = data[3:7]
                 flag = True
                 x = eval(roi[0])
                 y = eval(roi[1])
                 x1 = eval(roi[0]) + eval(roi[2])
                 y1 = eval(roi[1]) + eval(roi[3])
                 cv2.rectangle(im_copy,(int(x),int(y)),(int(x1),int(y1)),(0,0,255),3)

         if tlist.has_key(frameid):
             for t in tlist[frameid]:
                 data = t
                 tframeid = data[0]
                 roi = data[2:6]
                 flag = True
                 x = eval(roi[0])
                 y = eval(roi[1])
                 x1 = eval(roi[0]) + eval(roi[2])
                 y1 = eval(roi[1]) + eval(roi[3])
                 cv2.rectangle(im_copy,(int(x),int(y)),(int(x1),int(y1)),(0,255,0),3)
         if flag == True:
             cv2.imwrite("%s/%s/%s"%(t_img,d,img), im_copy)
         #break
     fd.close()
         

def run(i):
    rate_file = "%s/%s.txt"%(r_result,str(i))
    #print rate_file
    now_file = "%s/%s_%s.txt"%(r_result,str(i),str(i))
    fd = open(rate_file,'w')
    fn = open(now_file,'w')
    #print "\n" + "#"*20 + "video_%s"%str(i) + "#"*20
    imgdir = "%s/%s"%(imagePath,str(i))
    imgfile = "%s/%s.list"%(imageFile,str(i))
    gfile = "%s/%s.txt"%(gFile,str(i))
    tfile = "%s/%s.txt"%(tFile,str(i))
    #glist = dealGroundTruthInput(imgdir,gfile)
    glist = cc_dealGroundTruthInput(imgfile,gfile) ##imgfile is img_list, gfile is groundtruth_list of img_list
    tlist = cc_dealTestResultInput(tfile)  ##tfile is test result txt
    #visual(imgdir,v_image,glist,tlist,i)
    
    cc_visual(imgfile,v_image,glist,tlist,i)  ## draw test_box and grondtruth in img

    fd.write("*"*10 + " all " + "*"*10 + "\n")
    g_vehicle,g_pedestrian,g_bicycle,g_tricycle,num_g_vehicle,num_g_pedestrian,num_g_bicycle,num_g_tricycle = cc_g_detect_classify(glist,fd)
    t_vehicle,t_pedestrian,t_bicycle,t_tricycle,num_t_vehicle,num_t_pedestrian,num_t_bicycle,num_t_tricycle = cc_t_detect_classify(tlist,fd)
    
    
    #'''
    fd.write("##vehicle##\n")
    if num_g_vehicle == 0:
        fd.write("No Vehicles:%d,%d\n"%(num_g_vehicle,num_t_vehicle))
        fn.write(",,")
    else:
        cc_recallRate(g_vehicle,t_vehicle,num_g_vehicle,num_t_vehicle,fd,fn)
        cc_accuracyRate(g_vehicle,t_vehicle,num_g_vehicle,num_t_vehicle,fd,fn)
    #'''
    '''
    fd.write("##pedestrian##\n")
    if num_g_pedestrian == 0:
        fd.write("No Pedestrian:%d,%d\n"%(num_g_pedestrian,num_t_pedestrian))
        fn.write(",,")
    else:
        cc_recallRate(g_pedestrian,t_pedestrian,num_g_pedestrian,num_t_pedestrian,fd,fn)
        cc_accuracyRate(g_pedestrian,t_pedestrian,num_g_pedestrian,num_t_pedestrian,fd,fn)

    fd.write("##bicycle##\n")
    if num_g_bicycle == 0:
        fd.write("No Bicycle:%d,%d\n"%(num_g_bicycle,num_t_bicycle))
        fn.write(",,")
    else:
        cc_recallRate(g_bicycle,t_bicycle,num_g_bicycle,num_t_bicycle,fd,fn)
        cc_accuracyRate(g_bicycle,t_bicycle,num_g_bicycle,num_t_bicycle,fd,fn)
    '''
    #'''
    fd.write("##tricycle##\n")
    if num_g_tricycle == 0:
        fd.write("No Tricycle:%d,%d\n"%(num_g_tricycle,num_t_tricycle))
        fn.write(",,")
    else:
        cc_recallRate(g_tricycle,t_tricycle,num_g_tricycle,num_t_tricycle,fd,fn)
        cc_accuracyRate(g_tricycle,t_tricycle,num_g_tricycle,num_t_tricycle,fd,fn)
    #'''
    fd.write("\n" + "*"*10 + " filter " + "*"*10 + "\n")

    classes = ["pedestrian","bicycle"]
    for ty in classes:
        glst32,glst3248,glst48 = {},{},{}
        tlst32,tlst3248,tlst48 = {},{},{}
        gnum_lst32,gnum_lst3248,gnum_lst48=0,0,0
        tnum_lst32,tnum_lst3248,tnum_lst48=0,0,0
        fd.write("="*5 + ty + "="*5 + "\n")
        g_type = "g_%s"%ty
        t_type = "t_%s"%ty
        glst32,glst3248,glst48,gnum_lst32,gnum_lst3248,gnum_lst48 = cc_dealFilter(eval(g_type),imgdir,fd,"g")
        tlst32,tlst3248,tlst48,tnum_lst32,tnum_lst3248,tnum_lst48 = cc_dealFilter(eval(t_type),imgdir,fd,"t")
        fd.write("## %d ##\n"%48)
        if gnum_lst48==0:
            fd.write("No %s:%d,%d\n"%(ty,gnum_lst48,tnum_lst48))
            fn.write(",,")
        else:
            cc_recallRate(glst48,tlst48,gnum_lst48,tnum_lst48,fd,fn)
            cc_accuracyRate(glst48,tlst48,gnum_lst48,tnum_lst48,fd,fn)


    #visual(imgdir,v_image,glst48,tlst48,i,"_%s"%item)
    #visual(imgfile,v_image,glst48,tlst48,i,"_%s"%item)
    
    fd.close()
    fn.close()



## txt result to xls result 
def saveExcel():
    workbook = xlwt.Workbook(encoding='utf-8')
    worksheet = workbook.add_sheet("Sheet1",cell_overwrite_ok=True)
    dct = {0:"图片",1:"机动车",3:"行人",5:"二轮车",7:"三轮车"}
    for key,value in dct.iteritems():
        worksheet.write(0,key,value)
    for i in [1,3,5,7]:
        worksheet.write(1,i,"检出率")
    for j in [2,4,6,8]:
        worksheet.write(1,j,"准确率")
    for i in range(1,13):
        worksheet.write(i+1,0,i)
        filename = "%s/%s_%s.txt"%(r_result,str(i),str(i))
        fd = open(filename,'r')
        for line in fd.readlines():
            lst = [0,1,4,5,6,7,2,3]
            rate = line.strip().split(",")
            for j,item in enumerate(lst):
                worksheet.write(i+1,j+1,rate[item])
            break
    workbook.save(xlsxfile)

if __name__ == '__main__':
    num_proc=12
    pool = multiprocessing.Pool(processes = num_proc)
    for i in range(1,1+num_proc):
        pool.apply_async(run, (i,))
        print(i)
    pool.close()
    pool.join()
    saveExcel()
