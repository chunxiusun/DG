#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author:chunxiusun

import time
import xlrd
import logging
import logging.handlers
import os
import pdb
import datetime
from collections import Counter

THRESHOLD = 0.35

 
logger = logging.getLogger("MyLogger")
os.system("mkdir -p ./log")
log_name = "./log/analyze_car.log"
formatter = logging.Formatter(
    '%(asctime)s %(filename)s %(funcName)s [line:%(lineno)d] %(levelname)s: %(message)s')
handler = logging.handlers.RotatingFileHandler(log_name,
            maxBytes = 20971520, backupCount = 5)
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)
logger.info(
        "[[time.time:%s]]" % str(int(time.time())))
logger.info(
        "[[loadtest start at %s]]" % str(datetime.datetime.now()))

def get_rate(total_num,tlist,glist,rlist,attribute_list):
    iou = 0
    iou_count = 0
    success_list = []
    err_list = []
    repeat_dict = {}
    attribute_dict = {}
    for item in tlist:
        tframe_id = int(item[0])
        troi = eval(item[1])
        flag_iou = True
        capture_dict = {}
        for data in glist:
            gframe_id = int(data.split(",")[0])
            groi = data.split(",")[3:7]
            gid = data.split(",")[1]
            if gframe_id == tframe_id:
                ratio = CalRatio(groi, troi)
                if ratio >= THRESHOLD:
                   iou = iou + ratio
                   iou_count += 1
                   capture_dict[str(ratio)] = gid #相邻的车可能符合iou条件
                   flag_iou = False
        if flag_iou == True:
            err_list.append(item)
        else:
            success_list.append(item)

        #print capture_dict
        if len(capture_dict) == 0:
            continue
        else:
            capture_list = sorted(capture_dict.keys(),reverse=True) #相邻车的情况，取ratio最大的
            key = capture_list[0]
            g_id = capture_dict[key]
            if g_id not in repeat_dict:
                repeat_dict[g_id] = []
            repeat_dict[g_id].append(tframe_id)
        '''for row in rlist:
            r_id = row[0]
            if g_id == r_id:
                for index in range(len(attribute_list)):
                    attribute = attribute_list[index]
                    #print type(row[index+1]),type(line[index+2])
                    #print row[index+1].encode('utf-8','ignore') +',' + line[index+2]  # open this line
                    if row[index+1] in line[index+2].decode('utf-8','ignore') or row[index+1] == u"——" or row[index+1] == u"":
                        #pdb.set_trace()
                        #print row[index+1] +',' + line[index+2].decode('utf-8','ignore')
                        if attribute not in attribute_dict:
                            attribute_dict[attribute] = 0
                        attribute_dict[attribute] += 1'''
    
    #avg iou
    if iou_count == 0:
        iou_avg = 0
    else:
        iou_avg = iou*1.0/iou_count
    print "iou_avg:%s"%str(iou_avg)

    #attribute rate        
    #print attribute_dict
    '''for key in attribute_dict:
	attribute_rate = attribute_dict[key]*1.0/total_num
	print "%s_rate:%s"%(key,str(attribute_rate))'''

    #capture rate
    capture_rate = len(success_list)*1.0/total_num
    print "capture_rate:%0.2f%s"%(capture_rate*100,"%")

    #err rate
    err_rate = len(err_list)*1.0/total_num
    print "err_rate:%0.2f%s"%(err_rate*100,"%")

    #repeat rate
    re_count = 0
    for key in repeat_dict:
        re_count = re_count + len(repeat_dict[key])
    repeat_count = re_count - len(repeat_dict)
    repeat_rate = repeat_count*1.0/total_num
    print "repeat_rate:%0.2f%s"%(repeat_rate*100,"%")

    #lost rate
    lost_dict = {}
    for line in glist:
        gframe_id = int(line.split(",")[0])
        groi = line.split(",")[3:7]
        gid = line.split(",")[1]
        if gid not in lost_dict:
            lost_dict[gid] = []
        for item in tlist:
            tframe_id = int(item[0])
            troi = eval(item[1])
            if gframe_id == tframe_id:
                ratio = CalRatio(groi, troi)
                if ratio >= THRESHOLD:
                    lost_dict[gid].append(tframe_id)
    lost_count = 0
    for key in lost_dict:
        if lost_dict[key] == []:
            lost_count += 1
    lost_rate = lost_count*1.0/total_num
    print "lost_rate:%0.2f%s"%(lost_rate*100,"%")

def detect_classify(filename):
    vehicle = []
    pedestrian = []
    bicycle = []
    tricycle = []
    fd = open(filename,'r')
    for line in fd.readlines():
        data = line.strip()
        detect_type = data.split(",")[2]
        if detect_type == "1":
            vehicle.append(data)
        elif detect_type == "2":
            pedestrian.append(data)
        elif detect_type == "3":
            bicycle.append(data)
        elif detect_type == "4":
            tricycle.append(data)
    fd.close()
    print len(vehicle),len(pedestrian),len(bicycle),len(tricycle)
    return vehicle,pedestrian,bicycle,tricycle

def test_result_to_list(filename):
    flist = []
    fd = open(filename,"r")
    for line in fd.readlines():
        lst = []
        for i in [1,3]:
            data = line.split(";")[i]
            lst.append(data)
        flist.append(lst)
    fd.close()
    return flist

def deal_no_moto(filename):
    blist = []
    clist = []
    fd = open(filename,"r")
    for line in fd.readlines():
        lst = []
        for i in [1,3]:
            data = line.split(";")[i]
            lst.append(data)
        if u"三轮车" in line.decode('utf-8','ignore'):
            clist.append(lst)
        else:
            blist.append(lst)
    fd.close()
    return blist,clist

def vehicle_result_to_list(filename,tp):
    flist = []
    if tp == "xlsx":
        data = xlrd.open_workbook(filename)
        #pdb.set_trace()
        table = data.sheets()[0] 
        nrows = table.nrows
        for i in range(2,nrows):
            lst = []
            for j in [1,2,4,5,6]:
                if j == 1:
                    data = table.row_values(i)[j].split("_")[0]
                else:
                    data = table.row_values(i)[j]
                lst.append(data)
            flist.append(lst)
    elif tp == "txt":
        fd = open(filename,"r")
        for line in fd.readlines():
            lst = []
            for k in [0,1,7,5,2,6]:
                data = line.split(";")[k]
                lst.append(data)
            flist.append(lst)
        fd.close()
    return flist

def total_num(lst):
    file_list = []
    for item in lst:
        car_id = item.split(",")[1]
        if car_id not in file_list:
            file_list.append(car_id)
    num = len(file_list)
    print "total_num:%d"%num
    return num

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


if __name__ == '__main__':
    for i in range(8,9):
        print "video_%s"%str(i)
        gfile = "./12groundtruth/%s.txt"%str(i)
        vfile = "./12testResult/%s.txt_car"%str(i)
        pfile = "./12testResult/%s.txt_pedestrian"%str(i)
        nvfile = "./12testResult/%s.txt_no_moto"%str(i)
        g_vehicle,g_pedestrian,g_bicycle,g_tricycle = detect_classify(gfile)
        t_vehicle = test_result_to_list(vfile)
        t_pedestrian = test_result_to_list(pfile)
        t_bicycle,t_tricycle = deal_no_moto(nvfile)
        
        if len(g_vehicle) == 0:
            print "No Vehicles"
        else:
            print "#"*20 + "vehicle" + "#"*20
            total_vehicle = total_num(g_vehicle)
            rlist = []
            attribute_list = ["plate","car_type","main_broad","color"]
            get_rate(total_vehicle,t_vehicle,g_vehicle,rlist,attribute_list)
        
        if len(g_pedestrian) == 0:
            print "No Pedestrians"
        else:
            print "#"*20 + "pedestrian" + "#"*20
            total_pedestrian = total_num(g_pedestrian)
            rlist = []
            attribute_list = []
            get_rate(total_pedestrian,t_pedestrian,g_pedestrian,rlist,attribute_list)

        if len(g_bicycle) == 0:
            print "No Bicycles"
        else:
            print "#"*20 + "bicycle" + "#"*20
            total_bicycle = total_num(g_bicycle)
            rlist = []
            attribute_list = []
            get_rate(total_bicycle,t_bicycle,g_bicycle,rlist,attribute_list)

        if len(g_tricycle) == 0:
            print "No Tricycles"
        else:
            print "#"*20 + "tricycle" + "#"*20
            total_tricycle = total_num(g_tricycle)
            rlist = []
            attribute_list = []
            get_rate(total_tricycle,t_tricycle,g_tricycle,rlist,attribute_list)

