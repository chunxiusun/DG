#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
import cv2


oldFile = "result_nanchang_person_1w_0.8.3.1.txt"
newFile = "result_nanchang_person_1w.txt"
imageUrl = "/home/dell/python/sun/image/nanchang/yingshiyun/person_1w/"#"http://192.168.2.16:6001/nanchang/yingshiyun/person_1w/"
oldDir = "person_1w_0.8.3.1"
newDir = "person_1w"

os.system("mkdir %s"%oldDir)
os.system("mkdir %s"%newDir)

def draw(lst,imgdir):
    for item in lst:
        s_name = "%s/%s"%(imageUrl,item[0])
        ty = item[1]
        cutboard = eval(item[2])
        print s_name
        im = cv2.imread(s_name)
        im_copy = im.copy()
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
        cv2.imwrite("%s/%s"%(imgdir,item[0]), im_copy)
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
    #old = dealFile(oldFile)
    new = dealFile(newFile)
    #draw(old,oldDir)
    draw(new,newDir)
    
