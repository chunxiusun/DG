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
 
MATRIX_ADDRESS = "192.168.2.134"
MATRIX_PORT = "6801"

VEHICLE_FLAG = 1 #0:not analyze,1:analyze
BIKE_FLAG = 1
TRICYCLE_FLAG = 1
PEDESTRIAN_FLAG = 1

uriHeader = 'http://192.168.2.16:3002/'
mountPath = '/mnt/ssd/DeepV/server/'
photoPath = '/mnt/ssd/DeepV/server/zdb_data_backup/wangli_test_data/wangli_test_data'
 
class AnalyzeMatrix():
    def __init__(self):
        self.img_list = []
	self.img_url = ""
	self.row_num_1 = 1
	self.row_num_2 = 1
	self.row_num_3 = 1
	self.row_num_4 = 1

    def dealImgPath(self, root_path):                                                                                                      
        for sub_dir_name in os.listdir(root_path):                                                                                         
            temp_path = "%s/%s" %(root_path, sub_dir_name)                                                                                 
            #print "temp_path:%s" %(temp_path)                                                                                             
            if re.search("^\.", sub_dir_name) != None:                                                                                     
                #print "not deal it."                                                                                                      
                continue                                                                                                                   
            if os.path.isfile(temp_path):                                                                                                  
                if re.search("\.png", temp_path) == None:                                                                                  
                    continue                                                                                                               
                self.img_list.append(temp_path)                                                                                            
            elif os.path.isdir(temp_path):                                                                                                 
                #print "in iter..."                                                                                                        
                self.dealImgPath(temp_path)                                                                                                
        #print img_list                                                                                                                    
        return self.img_list

    def recImage(self):
        url = "http://%s:%s/rec/image"%(MATRIX_ADDRESS,MATRIX_PORT)
        source = {"Context": {"SessionId": "test123",
                              "Functions": [1,10,11,12,13,14,15,16,170,171,172,2,20,21,3,4],
                              "Type":3,
                              "Storage":{"Address":"192.168.2.119:9004",
                                         "DBType":0
                                        },
                               "Params":[{"key":"AttributeFilter",
                                          "value": "0"
                                         }]
                             },
                  "Image": {"Data": {"URI": self.img_url}}
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

    def analyzeVehicle(self,datadict):
	vehicle_dict = {}
	#if "Plates" not in datadict:
	    #print "no Plates:%s"%self.img_url
	    #return vehicle_dict
	#basedata
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
	#return vehicle_dict
		
	#passengers
	vehicle_dict["driver_no_safety_belt"] = 0
	vehicle_dict["codriver_no_safety_belt"] = 0
	vehicle_dict["driver_phone"] = 0
	if "Passengers" in datadict:
	    passengers = datadict["Passengers"]
	    #vehicle_dict["driver_no_safety_belt"] = 0
	    #vehicle_dict["codriver_no_safety_belt"] = 0
	    #vehicle_dict["driver_phone"] = 0
	    for passenger in passengers:
	        categorys = passenger["PassengerAttr"]["Category"]
		for category in categorys:
		    if category["Id"] == 11:
		        items = category["Items"]
			for item in items:
			    if item["Id"] == 48:
				#print passenger["Driver"]
				if passenger["Driver"] == True:
				    vehicle_dict["driver_no_safety_belt"] = 1
				else:
				    vehicle_dict["codriver_no_safety_belt"] = 1
			    if item["Id"] == 47 and passenger["Driver"] == True:
				vehicle_dict["driver_phone"] = 1
	#print vehicle_dict
	return vehicle_dict

    def runVehicle(self,rdict,worksheet):
	if "Vehicles" not in rdict["Result"]:
	    #print "no Vehicles:%s"%self.img_url
	    return
	vehicles = rdict["Result"]["Vehicles"]
	for i in range(0,len(vehicles)):
	    vehicle_dict = {}
	    vehicledict = rdict["Result"]["Vehicles"][i]
	    vehicle_type = vehicledict["VehicleType"]
            #print vehicle_type
            if vehicle_type != 1:
                #print "not vehicles:%s"%self.img_url
		continue
	    data_dict = self.analyzeVehicle(vehicledict)
	    if len(data_dict) == 0:
		continue
	    lst = ["id","img_url","cutboard","brand","subrand","modelyear","cartype","color","platetexts",
                   "safety_belt_cutboard_list","label_cutboard_list","sun_visor_cutboard_list","tissue_box_cutboard_list",
                   "pendant_cutboard_list","tableware_cutboard_list","safety_belt_num","label_num","sun_visor_num",
                   "tissue_box_num","pendant_num","tableware_num","platecolors","driver_no_safety_belt",
                   "codriver_no_safety_belt","driver_phone"]
	    for i,item in enumerate(lst):
		if item in data_dict:
		    vehicle_dict[i] = data_dict[item]
		elif "num" in item:
		    vehicle_dict[i] = 0
	    vehicle_dict[0] = self.row_num_1
	    vehicle_dict[1] = self.img_url
	    #print vehicle_dict
	    self.addToXlsx(worksheet,self.row_num_1,vehicle_dict)
	    self.row_num_1 = self.row_num_1 + 1

    def analyzeNonMotorvehicle(self,datadict):
	nonMotorvehicle_dict = {}
	nonMotorvehicle_dict["nMVehicle_type"] = datadict["NMVehicleTypeName"]
	#Cutboard
	cutboard = []                                                                                                                      
        for item in ["X","Y","Width","Height"]:                                                                                            
            cutboard_item = datadict["Img"]["Cutboard"][item]                                                                              
            cutboard.append(cutboard_item)
        nonMotorvehicle_dict["cutboard"] = cutboard
	#NMVehicleGesture
	l = [u"正面",u"侧右面",u"侧左面",u"后面"]
	for i,item in enumerate(l):
	    if datadict["NMVehicleGesture"] == i:
		nonMotorvehicle_dict["nMVehicle_gesture"] = item
	#NMVehicle
	nMVehicle_list = datadict["NMVehicle"]
	for nMVehicle in nMVehicle_list:
	    if nMVehicle["Id"] == 8:
		nMVehicle_colors = ""
		for i,item in enumerate(nMVehicle["Items"]):
		    nMVehicle_color = item["Name"]
		    #print nMVehicle_color
		    #nMVehicle_color = "\"" + nMVehicle_color + "\""
                    if i != 0:
                        nMVehicle_colors = nMVehicle_colors + ","
                    nMVehicle_colors = nMVehicle_colors + nMVehicle_color
		#nMVehicle_colors = "[" + nMVehicle_colors + "]"
		#print nMVehicle_colors
		nonMotorvehicle_dict["nMVehicle_colors"] = nMVehicle_colors

	#Passenger
	passenger_list = datadict["Passenger"]
	for passenger in passenger_list:
	    gender = passenger["Sex"]["Name"]
	    #print gender
	    nonMotorvehicle_dict["gender"] = gender
	    attributes = passenger["Attribute"]
	    for attribute in attributes:
		items = attribute["Items"]
		item_names = ""
		for i,item in enumerate(items):
		    item_name = item["Name"]
		    #item_name = "\"" + item_name + "\""
		    if i != 0:
			item_names = item_names + ","
		    item_names = item_names + item_name
		#item_names = "[" + item_names + "]"
		lst = ["nation","head_features","attached_items","upper_body_color","upper_body_style"]
		for i,item in enumerate(lst):
		    if attribute["Id"] == (i + 3):
			nonMotorvehicle_dict[item] = item_names
	#print nonMotorvehicle_dict
	return nonMotorvehicle_dict

    def runBike(self,rdict,worksheet):
	if "NonMotorVehicles" not in rdict["Result"]:
	    #print "no NonMotorVehicles:%s"%self.img_url
	    return
	nonMotorVehicles = rdict["Result"]["NonMotorVehicles"]
	for i in range(0,len(nonMotorVehicles)):
	    nonMotorvehicle_dict = {}
	    nonMotorvehicledict = rdict["Result"]["NonMotorVehicles"][i]
	    nmvehicle_type = nonMotorvehicledict["NMVehicleType"]
	    #print nmvehicle_type
	    if nmvehicle_type != 3 and nmvehicle_type != 7:
		#print "not nmvehicles:%s"%self.img_url
		continue
	    data_dict = self.analyzeNonMotorvehicle(nonMotorvehicledict)
	    lst = ["id","img_url","cutboard","nMVehicle_type","nMVehicle_gesture","nMVehicle_colors","gender","nation",
                   "head_features","attached_items","upper_body_color","upper_body_style"]
	    for i,item in enumerate(lst):                                                                                              
                if item in data_dict:                                                                                                  
                    nonMotorvehicle_dict[i] = data_dict[item]
	    nonMotorvehicle_dict[0] = self.row_num_2                                                                                        
            nonMotorvehicle_dict[1] = self.img_url                                                                                                  
            #print vehicle_dict                                                                                                        
            self.addToXlsx(worksheet,self.row_num_2,nonMotorvehicle_dict)
	    self.row_num_2 = self.row_num_2 + 1

    def runTricycle(self,rdict,worksheet):
	if "NonMotorVehicles" not in rdict["Result"]:
            #print "no tricycles:%s"%self.img_url
	    return
        nonMotorVehicles = rdict["Result"]["NonMotorVehicles"]
        for i in range(0,len(nonMotorVehicles)):
            nonMotorvehicle_dict = {}
            nonMotorvehicledict = rdict["Result"]["NonMotorVehicles"][i]
            nmvehicle_type = nonMotorvehicledict["NMVehicleType"]
            #print nmvehicle_type
            if nmvehicle_type != 4:
                #print "not tricycles:%s"%self.img_url
                continue
            data_dict = self.analyzeNonMotorvehicle(nonMotorvehicledict)
            lst = ["id","img_url","cutboard","nMVehicle_type","nMVehicle_gesture","nMVehicle_colors","gender","nation",
                   "head_features","attached_items","upper_body_color","upper_body_style"]
            for i,item in enumerate(lst):
                if item in data_dict:
                    nonMotorvehicle_dict[i] = data_dict[item]
            nonMotorvehicle_dict[0] = self.row_num_3
            nonMotorvehicle_dict[1] = self.img_url
            self.addToXlsx(worksheet,self.row_num_3,nonMotorvehicle_dict)
	    self.row_num_3 = self.row_num_3 + 1

    def analyzePedestrian(self,datadict):
	pedestrian_dict = {}
	#Cutboard
        cutboard = []    
        for item in ["X","Y","Width","Height"]:                                                                                                
            cutboard_item = datadict["Img"]["Cutboard"][item]                                                                                  
            cutboard.append(cutboard_item)
        pedestrian_dict["cutboard"] = cutboard
	#Sex
	sex = datadict["PedesAttr"]["Sex"]["Name"]
	pedestrian_dict["sex"] = sex
	#Age
	age = datadict["PedesAttr"]["Age"]["Name"]
	pedestrian_dict["age"] = age
	#National
	nation = datadict["PedesAttr"]["National"]["Name"]
	pedestrian_dict["nation"] = nation
	#Category
	for category in datadict["PedesAttr"]["Category"]:
	    items = category["Items"]
	    item_names = ""
	    for i,item in enumerate(items):
		item_name = item["Name"]
                #item_name = "\"" + item_name + "\""                                                                       
                if i != 0:                                                                                                             
                    item_names = item_names + ","                                                                          
                item_names = item_names + item_name                                                                  
            #item_names = "[" + item_names + "]"                                                                           
            lst = ["head_features","attached_items","upper_body_color","upper_body_style","upper_body_class","lower_body_color",
                   "lower_body_style","lower_body_class"]
	    for i,item in enumerate(lst):
		if category["Id"] == i:
		    pedestrian_dict[item] = item_names
	return pedestrian_dict

    def runPedestrian(self,rdict,worksheet):
	if "Pedestrian" not in rdict["Result"]:
	    #print "no pedestrians:%s"%self.img_url
	    return
	pedestrians = rdict["Result"]["Pedestrian"]
	for i in range(0,len(pedestrians)):
	    pedestrian_dict = {}
	    pedestriandict = rdict["Result"]["Pedestrian"][i]
	    data_dict = self.analyzePedestrian(pedestriandict)
	    lst = ["id","img_url","cutboard","sex","age","nation","head_features","attached_items","upper_body_color",
                   "upper_body_style","upper_body_class","lower_body_color","lower_body_style","lower_body_class"]
	    for i,item in enumerate(lst):
                if item in data_dict:
                    pedestrian_dict[i] = data_dict[item]
            pedestrian_dict[0] = self.row_num_4
            pedestrian_dict[1] = self.img_url
            #print pedestrian_dict                                                                                                        
            self.addToXlsx(worksheet,self.row_num_4,pedestrian_dict)
	    self.row_num_4 = self.row_num_4 + 1

    def run(self):
	if VEHICLE_FLAG == 1:
	    workbook1 = xlwt.Workbook(encoding = 'utf-8')
            worksheet1 = workbook1.add_sheet("Sheet1")
            row0 = ["ID",u"文件名",u"车辆ROI",u"主品牌",u"子品牌",u"年款",u"车型",u"车身颜色",
                   u"车牌",u"安全带",u"年检标",u"遮阳板",u"纸巾盒",u"挂坠",u"摆件",u"安全带个数",
                   u"年检标个数",u"遮阳板个数",u"纸巾盒个数",u"挂坠个数",u"摆件个数",u"车牌颜色",
                   u"主驾无安全带",u"副驾无安全带",u"主驾打电话"]
            for i in range(0,len(row0)):
                worksheet1.write(0,i,row0[i])
	if BIKE_FLAG == 1:
	    workbook2 = xlwt.Workbook(encoding = 'utf-8')
            worksheet2 = workbook2.add_sheet("Sheet1")
            row0 = ["ID",u"文件名","ROI",u"车分类",u"车姿态",u"车身颜色",u"乘客性别",u"乘客民族",u"头部特征",u"附属物品",u"上身颜色",
                   u"上身款式"]
            for i in range(0,len(row0)):
                worksheet2.write(0,i,row0[i])
	if TRICYCLE_FLAG == 1:
	    workbook3 = xlwt.Workbook(encoding = 'utf-8')
            worksheet3 = workbook3.add_sheet("Sheet1")
            row0 = ["ID",u"文件名","ROI",u"车分类",u"车姿态",u"车身颜色",u"乘客性别",u"乘客民族",u"头部特征",u"附属物品",u"上身颜色",
                   u"上身款式"]
            for i in range(0,len(row0)):
                worksheet3.write(0,i,row0[i])

	if PEDESTRIAN_FLAG == 1:
	    workbook4 = xlwt.Workbook(encoding = 'utf-8')
	    worksheet4 = workbook4.add_sheet("Sheet1")
	    row0 = ["ID",u"文件名","ROI",u"性别",u"年龄",u"民族",u"头部特征",u"附属物品",u"上身颜色",u"上身纹理",u"上身类别",
                   u"下身颜色",u"下身纹理",u"下身类别"]
	    for i in range(0,len(row0)):
		worksheet4.write(0,i,row0[i])

	img_lst = self.dealImgPath(photoPath)
        #print img_lst
	#img_lst = ['ftp://192.168.2.16/matrix_cases/tricycle/207.jpg','ftp://192.168.2.16/matrix_cases/tricycle/208.jpg',
         #          'ftp://192.168.2.16/matrix_cases/tricycle/219.jpg','ftp://192.168.2.16/matrix_cases/bike/254.jpg',
          #         'ftp://192.168.2.16/matrix_cases/bike/427.jpg']
        for img in img_lst:
	    self.img_url = img
            self.img_url = uriHeader + img.split(mountPath)[1]
            print self.img_url
            #self.img_url = 'http://192.168.2.16:3002/zdb_data_backup/wangli_test_data/wangli_test_data/day/Selection_079.png'
            status_code,rdict = self.recImage()
            if len(rdict) == 0:
                print "status_code:%s"%status_code
                print "img_url:%s"%self.img_url
                continue
            status = rdict["Context"]["Status"]
            #print status
            if status != "200":
                print "status:%s"%status
                print "Message:%s"%rdict["Context"]["Message"]
		print "img_url:%s"%self.img_url
                continue
	    if VEHICLE_FLAG == 1:
		self.runVehicle(rdict,worksheet1)
	    if BIKE_FLAG == 1:
		self.runBike(rdict,worksheet2)
	    if TRICYCLE_FLAG == 1:
		self.runTricycle(rdict,worksheet3)
	    if PEDESTRIAN_FLAG == 1:
		self.runPedestrian(rdict,worksheet4)
	    #break
	if VEHICLE_FLAG == 1:
	    workbook1.save("vehicles.xls")
	    print "----------------- Analyze Vehicles End -----------------"
	if BIKE_FLAG == 1:
	    workbook2.save("bikes.xls")
	    print "------------------- Analyze Bikes End ------------------"
	if TRICYCLE_FLAG == 1:
	    workbook3.save("tricycles.xls")
	    print "---------------- Analyze Tricycles End -----------------"
	    
	if PEDESTRIAN_FLAG == 1:
	    workbook4.save("pedestrians.xls")
	    print "---------------- Analyze Pedestrians End -----------------"

if __name__ == "__main__":
    p = AnalyzeMatrix()
    p.run()
