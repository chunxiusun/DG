#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
import cv2


imgFile = "02_new_1000.txt"
newFile = "result_02_new_1000.txt"
imageUrl = "/home/dell/python/sun/image/01/"#"http://192.168.2.16:6001/nanchang/yingshiyun/person_1w/"
newDir = "02_new_1000"

os.system("mkdir %s"%newDir)

def draw(lst,imgdir):
    fd = open(imgFile,'r')
    for line in fd.readlines():
        img_name = line.strip().split('/')[-1]
        s_name = "%s/%s"%(imageUrl,img_name)
        print s_name
        im = cv2.imread(s_name)
        try:
            im_copy = im.copy()
        except Exception as e:
            print e
            continue
        for item in lst:
            if item[0] == img_name:
                ty = item[1]
                cutboard = eval(item[2])
                x = cutboard[0]
                y = cutboard[1]
                x1 = cutboard[0] + cutboard[2]
                y1 = cutboard[1] + cutboard[3]
                if ty == "Vehicle":
                    cv2.rectangle(im_copy,(int(x),int(y)),(int(x1),int(y1)),(0,255,0),3)
                if ty == "Pedestrian":
                    cv2.rectangle(im_copy,(int(x),int(y)),(int(x1),int(y1)),(0,0,255),3)
                if ty == "NonMotorVehicle":
                    cv2.rectangle(im_copy,(int(x),int(y)),(int(x1),int(y1)),(255,0,0),3)
        cv2.imwrite("%s/%s"%(imgdir,img_name), im_copy)
def dealFile(filename):
    data_list = []
    with open(filename,'r') as fd: 
        for line in fd.readlines():
            lst = []
            data = line.strip().split(";")
            if len(data) < 3:
                print line
                continue
            for i in range(3):
                lst.append(data[i])
            data_list.append(lst)
    return data_list

if __name__ == '__main__':
    new = dealFile(newFile)
    draw(new,newDir)
    
