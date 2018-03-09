#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
import Image
import cv2
import xlwt
#from PIL import Image
#import Queue
import multiprocessing

THRESHOLD = 0.5
imagePath = "./images/"
imageFile = "./images/"
gFile = "./12groundtruth/"
tFile = "./12testresult/"
xlsxfile = "12.xls"
r_result = "./rate_result/"
os.system("rm -r %s"%r_result)
os.system("mkdir %s"%r_result)

v_image = "./visual_image_classifiy/"
os.system("rm -r %s"%v_image)
os.system("mkdir %s"%v_image)

#q = Queue.Queue(maxsize=0)
lock = multiprocessing.Lock()

 
def dealGroundTruthInput(rootdir,filename):
    glist = []
    lst = os.listdir(rootdir)
    fd = open(filename,'r')
    for line in fd.readlines():
        gframeid = line.strip().split(",")[0]
        for i in range(0,len(lst)):
            #print lst[i]
            iframeid = lst[i].split(".")[0]
            if iframeid == gframeid:
                #print line
                glist.append(line.strip())
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


def visual(s_img,t_img,glist,tlist,i,filt=""):
     d = str(i)+filt
     os.system("mkdir %s/%s"%(t_img,d))
     fd = open(s_img,'r')
     for line in fd.readlines():
         s_name = line.strip()
         print s_name
         img = s_name.split("/")[-1]
     #for img in os.listdir(s_img):
         flag = False
         #s_name = "%s/%s"%(s_img,img)
         im = cv2.imread(s_name)
         im_copy = im.copy()
         frameid = img.split(".")[0]
         #for g in glist:
         #    data = g.split(",")
         #    gframeid = data[0]
         #    roi = data[3:7]
         #    if frameid == gframeid:
         #        flag = True
         #        x = eval(roi[0])
         #        y = eval(roi[1])
         #        x1 = eval(roi[0]) + eval(roi[2])
         #        y1 = eval(roi[1]) + eval(roi[3])
         #        cv2.rectangle(im_copy,(int(x),int(y)),(int(x1),int(y1)),(0,0,255),3)
         for t in tlist:
             data = t
             tframeid = data[0]
             ty = eval(data[1])
             roi = data[2:6]
             if frameid == tframeid:
                 flag = True
                 x = eval(roi[0])
                 y = eval(roi[1])
                 x1 = eval(roi[0]) + eval(roi[2])
                 y1 = eval(roi[1]) + eval(roi[3])
                 if ty == 1:
                     cv2.rectangle(im_copy,(int(x),int(y)),(int(x1),int(y1)),(0,255,0),3)
                 if ty == 2:
                     cv2.rectangle(im_copy,(int(x),int(y)),(int(x1),int(y1)),(0,0,255),3)
                 if ty == 3:
                     cv2.rectangle(im_copy,(int(x),int(y)),(int(x1),int(y1)),(255,0,0),3)
                 if ty == 4:
                     cv2.rectangle(im_copy,(int(x),int(y)),(int(x1),int(y1)),(255,0,255),3)
         if flag == True:
             cv2.imwrite("%s/%s/%s"%(t_img,d,img), im_copy)
         #break
     fd.close()
         

def run(i):
    print "\n" + "#"*20 + "video_%s"%str(i) + "#"*20
    imgdir = "%s/%s"%(imagePath,str(i))
    imgfile = "%s/%s.list"%(imageFile,str(i))
    #gfile = "%s/%s.txt"%(gFile,str(i))
    tfile = "%s/%s.txt"%(tFile,str(i))
    #glist = dealGroundTruthInput(imgdir,gfile)
    glist = []
    tlist = dealTestResultInput(tfile)
    visual(imgfile,v_image,glist,tlist,i)


if __name__ == '__main__':
    pool = multiprocessing.Pool(processes = 12)
    for i in range(1,13):
        pool.apply_async(run, (i,))
    pool.close()
    pool.join()

