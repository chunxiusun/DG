#!/usr/bin/env python
#-*- coding:utf-8 -*-
#author : chunxiusun

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
 
MATRIX_ADDRESS = "192.168.2.16"
MATRIX_PORT = "6801"

uriHeader = 'http://192.168.2.16:3002/'
mountPath = '/mnt/ssd/DeepV/server/'
photoPath = '/mnt/ssd/DeepV/server/zdb_data_backup/wangli_test_data/wangli_test_data'
#img_url = "ftp://192.168.2.16/matrix_cases/double.jpg"
xlsname = "autoFilterNoPlate.xls"
 
class AnalyzeMatrix():
    def __init__(self):
        self.img_list = []

    def recImage(self,img_url):
        url = "http://%s:%s/rec/image"%(MATRIX_ADDRESS,MATRIX_PORT)
        source = {"Context": {"SessionId": "test123",
                              "Functions": [1,10,11,12,13,14,15,16,170,171,172,2,20,21,3],
                              "Type":3,
                              "Storage":{"Address":"192.168.2.119:9004",
                                         "DBType":0
                                        },
                               "Params":[{"key":"AttributeFilter",
                                          "value": "0"
                                         }]
                             },
                  "Image": {"Data": {"URI": img_url}}
                  }
        jsource = json.dumps(source)
        resp = requests.post(url, data = jsource)
        status_code = resp.status_code
	if status_code != 200:
	    rdict = {}
	else:
            rdict = json.loads(resp.content,encoding="UTF-8")
	#print status_code
	return status_code,rdict


    def analyzeVehicle(self,datadict):
	vehicle_dict = {}
	if "Plates" not in datadict:
	    print "no Plates"
	    return vehicle_dict
	#basedata
        #img_uri = datadict["Result"]["Image"]["Data"]["URI"]
        #print img_uri
	cartype = datadict["ModelType"]["Type"]        
	vehicle_dict["cartype"] = cartype
	brand = datadict["ModelType"]["Brand"]
	vehicle_dict["brand"] = brand
	subrand = datadict["ModelType"]["SubBrand"]
	vehicle_dict["subrand"] = subrand
	modelyear = datadict["ModelType"]["ModelYear"]
	vehicle_dict["modelyear"] = modelyear
	color = datadict["Color"]["ColorName"]
	vehicle_dict["color"] = color
	cutboard = []
	for item in ["X","Y","Width","Height"]:
	    cutboard_item = datadict["Img"]["Cutboard"][item]
	    cutboard.append(cutboard_item)
	vehicle_dict["cutboard"] = cutboard
	#print vehicle_dict

	#plates
	if "Plates" in datadict:
	    plates = datadict["Plates"]
	    #platetext_list = []
	    platetexts = ""
	    #platecolor_list = []
	    platecolors = ""
	    platetype_list = []
	    plate_cutboard_list = []
	    for i,plate in enumerate(plates):
	        platetext = plate["PlateText"]
		platetext = "\"" + platetext + "\""
		if i != 0:
		    platetexts = platetexts + ","
		platetexts = platetexts + platetext
	        #platetext_list.append(platetext)
	        platecolor = plate["Color"]["ColorName"]
		platecolor = "\"" + platecolor + "\""
		if i != 0:
		    platecolors = platecolors + ","
		platecolors = platecolors + platecolor
	        #platecolor_list.append(platecolor)
	        platetype = plate["TypeName"]
	        platetype_list.append(platetype)
	        plate_cutboard = []
                for item in ["X","Y","Width","Height"]:
                    cutboard_item = plate["Cutboard"][item]
                    plate_cutboard.append(cutboard_item)
                #print plate_cutboard
	        plate_cutboard_list.append(plate_cutboard)
	    platetexts = "[" + platetexts + "]"
	    platecolors = "[" + platecolors + "]"
	    vehicle_dict["platetexts"] = platetexts
	    #vehicle_dict["platetext_list"] = platetext_list
	    vehicle_dict["platecolors"] = platecolors
	    #vehicle_dict["platecolor_list"] = platecolor_list
	    vehicle_dict["platetype_list"] = platetype_list
	    vehicle_dict["plate_cutboard_list"] = plate_cutboard_list
	#print vehicle_dict

	#symbols
	if "Symbols" in datadict:
	    symbols = datadict["Symbols"]
	    for symbol in symbols:
	        #print symbol["SymbolName"]
	        sub_symbols = symbol["Symbols"]
	        sub_symbol_num = len(sub_symbols)
	        sub_cutboard_list = []
	        for sub_symbol in sub_symbols:
		    sub_cutboard = []
		    for item in ["X","Y","Width","Height"]:
		        sub_cutboard_item = sub_symbol["Cutboard"][item]
		        sub_cutboard.append(sub_cutboard_item)
		    sub_cutboard_list.append(sub_cutboard)

	        lst = ["window","label","sun_visor","tableware","safety_belt","pendant","tissue_box",
		       "left_safety_belt","right_safety_belt","left_sun_visor","right_sun_visor"]
	        for i,item in enumerate(lst):
		    if symbol["SymbolId"] == i:
		        vehicle_dict["%s_num"%item] = sub_symbol_num
		        vehicle_dict["%s_cutboard_list"%item] = sub_cutboard_list
	#print vehicle_dict
	return vehicle_dict
		
	#passengers
	'''if "Passengers" in datadict:
	    passengers = datadict["Passengers"]
	    for passenger in passengers:
	        categorys = passenger["PassengerAttr"]["Category"]
		for category in categorys:
		    if category["ID"] == 11:
		        items = category["Items"]
			    for item in items:
				if item["ID"] == 48:
				    break'''
				
	    #if passenger["Driver"]:
		
    def saveToXlsx(self):
        workbook = xlwt.Workbook(encoding = 'utf-8')
        worksheet = workbook.add_sheet("Sheet1")
	row0 = ["ID",u"文件名",u"车辆ROI",u"主品牌",u"子品牌",u"年款",u"车型",u"车身颜色",
               u"车牌",u"安全带",u"年检标",u"遮阳板",u"纸巾盒",u"挂坠",u"摆件",u"安全带个数",
               u"年检标个数",u"遮阳板个数",u"纸巾盒个数",u"挂坠个数",u"摆件个数",u"车牌颜色"]
	for i in range(0,len(row0)):
            worksheet.write(0,i,row0[i])
	#workbook.save(xlsname)
	return workbook,worksheet

    def addToXlsx(self,worksheet,row_num,vehicle_dict):
	#data = xlrd.open_workbook(xlsname,formatting_info=True)
	#wb = copy(data)
	#ws = wb.get_sheet(0)
	for key in vehicle_dict:
	    data = vehicle_dict[key]
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
                #print "-------------------"
                #print temp_path
                self.img_list.append(temp_path)
            elif os.path.isdir(temp_path):
                #print "in iter..."
                #self.batch_run(temp_path)
                self.dealImgPath(temp_path)
	#print img_list
	return self.img_list


    def run(self):
	row_num = 0
	workbook,worksheet = self.saveToXlsx()
	img_lt = self.dealImgPath(photoPath)
	#print img_lt
	for img in img_lt:
	    img_url = uriHeader + img.split(mountPath)[1]
	    print img_url
	    #img_url = 'ftp://192.168.2.16/matrix_cases/plate/gang.jpg'
	    status_code,rdict = self.recImage(img_url)
	    if len(rdict) == 0:
		print status_code
		print img_url
		continue
	    status = rdict["Context"]["Status"]
            #print status
            if status != "200":
	        print status
                print rdict["Context"]["Message"]
	        continue
	    if "Vehicles" not in rdict["Result"]:
		print "not Vehicles:%s"%img_url
		continue
	    vehicles = rdict["Result"]["Vehicles"]
	    for i in range(0,len(vehicles)):
	        vehicle_dict = {}
	        vehicledict = rdict["Result"]["Vehicles"][i]
	        vehicle_type = vehicledict["VehicleType"]
                #print vehicle_type
                if vehicle_type != 1:
                    print "Non-motor vehicles"
		    continue
	        data_dict = self.analyzeVehicle(vehicledict)
		if len(data_dict) == 0:
		    continue
	        lst = ["id","img_url","cutboard","brand","subrand","modelyear","cartype","color","platetexts",
                   "safety_belt_cutboard_list","label_cutboard_list","sun_visor_cutboard_list","tissue_box_cutboard_list",
                   "pendant_cutboard_list","tableware_cutboard_list","safety_belt_num","label_num","sun_visor_num",
                   "tissue_box_num","pendant_num","tableware_num","platecolors"]
	        for i,item in enumerate(lst):
		    if item in data_dict:
			vehicle_dict[i] = data_dict[item]
		    elif "num" in item:
			vehicle_dict[i] = 0
	            #for key in data_dict:
		        #if key == item:
		            #vehicle_dict[i] = data_dict[key]
	        vehicle_dict[0] = row_num + 1
	        vehicle_dict[1] = img_url
	        #print vehicle_dict
	        row_num = row_num + 1
	        self.addToXlsx(worksheet,row_num,vehicle_dict)
	workbook.save(xlsname)
	print "----------------- Analyze End -----------------"


if __name__ == "__main__":
    p = AnalyzeMatrix()
    p.run()
