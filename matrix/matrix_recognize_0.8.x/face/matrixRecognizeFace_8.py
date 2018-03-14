#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
import json
import requests
import re
import xlrd
import xlwt
from xlutils.copy import copy
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )
#print sys.getdefaultencoding()
 
MATRIX_ADDRESS = "192.168.2.164"
MATRIX_PORT = "6601"

imgFile = "wangli_nanchang.txt"
#uriHeader = 'http://192.168.2.16:3002/'
#mountPath = '/mnt/ssd/DeepV/server/'
#photoPath = '/mnt/ssd/DeepV/server/zdb_data_backup/wangli_test_data/wangli_test_data'
xlsname = "auto.xls"
 
class AnalyzeMatrix():
    def __init__(self):
        self.img_list = []
        self.face_count = 0
        self.feature_count = 0

    def recImage(self,img_url):
        url = "http://%s:%s/rec/image"%(MATRIX_ADDRESS,MATRIX_PORT)
        source = {"Context": {"SessionId": "test123",
                              "Functions": [200,201,202,203,204,205],
                              "Type":2
                             },
                  "Image": {"Data": {"URI": img_url}
                           }
                 }
        jsource = json.dumps(source)
        resp = requests.post(url, data = jsource)
        status_code = resp.status_code
	if status_code != 200:
	    rdict = {}
	else:
            rdict = json.loads(resp.content)
	#print status_code
	return status_code,rdict


    def analyzeFace(self,datadict):
        face_dict = {}
        self.face_count += 1
        cutboard = []
        for item in ["X","Y","Width","Height"]:
            cutboard_item = datadict["Img"]["Cutboard"][item]
            cutboard.append(cutboard_item)
            face_dict["cutboard"] = cutboard
            if "Features" not in datadict:
                print "No Features"
                face_dict["feature"] = 0
            else:
                face_dict["feature"] = 1
            self.feature_count += 1
            #feature = face["Features"]
            attributes = datadict["Attributes"]
            lst_name = [u"性别",u"年龄",u"民族",u"眼镜",u"帽子"]
            lst = ["gender","age","nation","glasses","hat"]
            #for i,item in enumerate(lst):
            face_dict["attribute"] = ""
            for attribute in attributes:
                attribute_name = attribute["Name"]
                for i,item in enumerate(lst_name):
                    if attribute_name == item:
                        if attribute_name == u"年龄":
                            attribute_content = attribute["ValueInt"]
                        else:
                            attribute_content = attribute["ValueString"]
                        face_dict[lst[i]] = attribute_content
                        
        #print self.face_count
        #print self.feature_count
        return face_dict
            
		
    def saveToXlsx(self):
        workbook = xlwt.Workbook(encoding = 'utf-8')
        worksheet = workbook.add_sheet("Sheet1")
	row0 = ["ID",u"文件名",u"人脸ROI",u"feature",u"性别",u"年龄",u"民族",u"眼镜",u"帽子"]
	for i in range(0,len(row0)):
            worksheet.write(0,i,row0[i])
	#workbook.save(xlsname)
	return workbook,worksheet

    def addToXlsx(self,worksheet,row_num,face_dict):
	#data = xlrd.open_workbook(xlsname,formatting_info=True)
	#wb = copy(data)
	#ws = wb.get_sheet(0)
	for key in face_dict:
	    data = face_dict[key]
	    if isinstance(data,list):
		data = str(data)
	    worksheet.write(row_num,key,data)
	    #wb.save(xlsname)

    def dealImgPath(self, root_path):
	#print os.listdir(root_path)
        for sub_dir_name in os.listdir(root_path):
            temp_path = "%s/%s" %(root_path, sub_dir_name)
            #print "temp_path:%s" %(temp_path)
            if re.search("^\.", sub_dir_name) != None:
                #print "not deal it."
                continue
            if os.path.isfile(temp_path):
                if re.search("\.png", temp_path) == None:
                    continue
                #print temp_path
                self.img_list.append(temp_path)
            elif os.path.isdir(temp_path):
                self.dealImgPath(temp_path)
	#print img_list
	return self.img_list


    def run(self):
        row_num = 0
        workbook,worksheet = self.saveToXlsx()
        
        fd = open(imgFile,'r')
        for url in fd.readlines():
            img_url = url.strip()
            
	#img_lst = self.dealImgPath(photoPath)
	#print img_lst
	#for img in img_lst:
	    #img_url = uriHeader + img.split(mountPath)[1]
	    print img_url
	    status_code,rdict = self.recImage(img_url)
	    if len(rdict) == 0:
		print status_code
		#print img_url
		continue
	    status = rdict["Context"]["Status"]
            #print status
            if status != "200":
	        print status
                print rdict["Context"]["Message"]
	        continue
	    if "Faces" not in rdict["Result"]:
		print "not Faces:%s"%img_url
		continue
	    faces = rdict["Result"]["Faces"]
	    for face in faces:
	        face_dict = {}
	        data_dict = self.analyzeFace(face)
	        lst = ["id","img_url","cutboard","feature","gender","age","nation","glasses","hat"]
	        for i,item in enumerate(lst):
		    if item in data_dict:
			face_dict[i] = data_dict[item]
	        face_dict[0] = row_num + 1
	        face_dict[1] = img_url
	        row_num = row_num + 1
	        self.addToXlsx(worksheet,row_num,face_dict)
	    #break
	workbook.save(xlsname)
	print "----------------- Analyze End -----------------"


if __name__ == "__main__":
    p = AnalyzeMatrix()
    p.run()
