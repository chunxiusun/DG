#!/usr/bin/python
#-*- coding:utf-8 -*-

# author : chunxiusun

import os
import re
import json
import requests
import base64
import numpy as np

matrix = '192.168.2.18'
port = '6801'
photoPath = '/mnt/ssd/DeepV/server/Brand_Data/dayfront/SrcData2/changzhou/02/'
uriHeader = 'http://192.168.2.16:3002/'
mountPath = '/mnt/ssd/DeepV/server/'

img_list = []
img_url = ""

def featuretofloat():
    matrix_url = "http://%s:%s/rec/image"%(matrix,port)
    dict_source = {"Context": {"SessionId": "test123",
                             "Functions": [1,10,11,12,13,14,15,16,170,171,172,3,4],
                             "Type":3,
                             "Storage":{"RepoInfo":"dg"}
                            },
                 "Image": {"Data": {"URI": img_url}
                          } 
                 }
    post_data = json.dumps(dict_source)
    resp = requests.post(matrix_url,data=post_data)
    resp_dict = json.loads(resp.content)
    for vehicle in resp_dict["Result"]["Vehicles"]:
	feature = vehicle["Features"]
        a = base64.b64decode(feature)
        array = np.frombuffer(a,dtype=np.float32)
        print len(array)
        print array
        #print (array.shape)

def dealImgPath(root_path):
    global img_list    
    for sub_dir_name in os.listdir(root_path):    
        temp_path = "%s/%s" %(root_path, sub_dir_name)
	#print temp_path    
        if re.search("^\.", sub_dir_name) != None:    
            continue    
        if os.path.isfile(temp_path):    
            if re.search("\.jpg", temp_path) == None:    
                continue    
            img_list.append(temp_path)    
        elif os.path.isdir(temp_path):    
            dealImgPath(temp_path)                                                                                                              
    #print img_list                                                                                                                    
    return img_list

if __name__ == '__main__':
    img_ls = dealImgPath(photoPath)
    for img in img_ls:
	img_url = uriHeader + img.split(mountPath)[1]
	print img_url
	featuretofloat()
