#!/usr/bin/python
#-*- coding:utf-8 -*-

# author : chunxiusun

import os
import re

uriHeader = 'http://192.168.2.16:6001/'
mountPath = '/home/dell/python/sun/image/'
photoPath = '/home/dell/python/sun/image/deepdata/DangerVehicles/'
img_form = '.jpg'
img_url_file = 'img_url_http.txt'
img_list = []

def dealImgPath(root_path):
    for sub_dir_name in os.listdir(root_path):
        temp_path = "%s/%s" %(root_path, sub_dir_name)
        #print "temp_path:%s" %(temp_path)                                                                                             
        if re.search("^\.", sub_dir_name) != None:
            #print "not deal it."                                                                                                      
            continue
        if os.path.isfile(temp_path):
            if re.search("\%s"%(img_form), temp_path) == None:
                continue
            img_list.append(temp_path)
        elif os.path.isdir(temp_path):
            #print "in iter..."                                                                                                        
            dealImgPath(temp_path)                                                                                                
    #print img_list                                                                                                                    
    return img_list

def localToHttp():
    img_list = dealImgPath(photoPath)
    #print img_list
    fw = open(img_url_file,'w')
    for img in img_list:
        img_url = uriHeader + img.split(mountPath)[1]
        print img_url
	fw.write(img_url + '\n')
    fw.close()

if __name__ == '__main__':
    localToHttp()
