#!/usr/bin/python
# -*- coding:utf-8 -*-

# author : chunxiusun

import sys 
sys.path.append('./gen-py')

import config
from init_parameter import *
from function import LibrafApi

import threading
import time
import random
import datetime

from logger import logger

from LibraFService import LibraFService
from LibraFService import ttypes

from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol


class FunctionSet(threading.Thread):
    def __init__(self, func_name):
        threading.Thread.__init__(self)
        self.func_name = func_name
	self.transport = None
        self.client = None
        logger.info('openTransport')
	try:
            self.transport = TSocket.TSocket(config.IP, config.PORT)
            self.transport = TTransport.TFramedTransport(self.transport)
            protocol = TBinaryProtocol.TBinaryProtocol(self.transport)
            self.client = LibraFService.Client(protocol)
            self.transport.open()    
            logger.info('openTransport success')
	except:
	    msg = 'Could not connect to %s:%s'%(config.IP,config.PORT)                                                                     
            logger.error(msg)
	    sys.exit(0)

	logger.info('set the passive mode')
	try:
	    work_mode = 16842752
	    resp = LibrafApi().set_get_WorkMode(self.client,work_mode)
	except ttypes.RpcLibraFException as e:                                                                                             
            logger.error(e.msg)
	logger.info('if calibrate,stop it')
	if self.client.CaliBusy():
	    logger.info('stop calibrate')
	    try:
	        LibrafApi().stopCalibrate(self.client)
	    except ttypes.RpcLibraFException as e:
                logger.error(e.msg)

    def __del__(self):
        logger.info('closeTransport')
        self.transport.close()                                                                                                             
        logger.info('closeTransport success')

    def func01_OSD(self):
        logger.info("func01 OSD...")
	logger.info('func01 begins:%s'%datetime.datetime.now())
	try:
	    text_type = init_RpcTextType()
	    font_prop = init_RpcFontProperties()
	    resp = LibrafApi().get_set_FontProperties(self.client,text_type,font_prop)
	except ttypes.RpcLibraFException as e:                                                                                             
            logger.error(e.msg)
	try:
	    osd_other = init_RpcOSDOther() 
	    resp = LibrafApi().get_set_OSDOthers(self.client,osd_other)
	except ttypes.RpcLibraFException as e:
            logger.error(e.msg)
	try:
	    text_type = init_RpcTextType()
	    align_type = init_RpcTextAlignType()
	    resp = LibrafApi().get_set_TextAlign(self.client,text_type,align_type)
	except ttypes.RpcLibraFException as e:
	    logger.error(e.msg)

    def func02_ImgMask(self):
	logger.info("func02 ImgMask...")
	logger.info('func02 begins:%s'%datetime.datetime.now())
	try:
            is_mask_on = True                                                                                                                  
            resp = LibrafApi().get_set_MaskOn(self.client,is_mask_on)
	except ttypes.RpcLibraFException as e:                                                                                             
            logger.error(e.msg)
	try:                                                                          
            img_masks = init_list_list_RpcPoint()
            resp = LibrafApi().get_set_ImageMasks(self.client,img_masks)
	except ttypes.RpcLibraFException as e:
            logger.error(e.msg)
	try:
	    is_mask_on = False
            resp = LibrafApi().get_set_MaskOn(self.client,is_mask_on)
	except ttypes.RpcLibraFException as e:
            logger.error(e.msg)

    def func03_LayoutProperties(self):
	logger.info("func03 LayoutProperties...")
	logger.info('func03 begins:%s'%datetime.datetime.now())
	layout_prop = init_RpcLayoutProp()
	try:
	    layout_prop.default_layout = True
	    resp = LibrafApi().get_set_LayoutProperties(self.client,layout_prop)
	except ttypes.RpcLibraFException as e:
            logger.error(e.msg)
	try:
	    layout_prop.default_layout = False
	    resp = LibrafApi().get_set_LayoutProperties(self.client,layout_prop)
	except ttypes.RpcLibraFException as e:
            logger.error(e.msg)
	try:
	    layout_prop.pip_on = False
            layout_prop.pip_fixed = True
	    resp = LibrafApi().get_set_LayoutProperties(self.client,layout_prop)
	except ttypes.RpcLibraFException as e:
            logger.error(e.msg)
	try:
	    layout_prop.pip_on = True
	    layout_prop.pip_fixed = False
	    resp = LibrafApi().get_set_LayoutProperties(self.client,layout_prop)
	except ttypes.RpcLibraFException as e:
	    logger.error(e.msg)

    def func04_SensorPropertiesAndIRCut(self):
        logger.info("func04 SensorPropertiesAndIRCut...")
	logger.info('func04 begins:%s'%datetime.datetime.now())
	sensor_type = init_RpcSensorType()
	sensor_prop = init_RpcSensorProp()
	try:
	    sensor_prop.exposure_auto = False
	    sensor_prop.shutter_auto = False
	    resp = LibrafApi().get_set_SensorProperties(self.client,sensor_type,sensor_prop)
	except ttypes.RpcLibraFException as e:                                                                                             
            logger.error(e.msg)
	try:
	    sensor_prop.exposure_auto = True
	    sensor_prop.shutter_auto = True
	    resp = LibrafApi().get_set_SensorProperties(self.client,sensor_type,sensor_prop)
	except ttypes.RpcLibraFException as e:
            logger.error(e.msg)
	#interval = init_RpcDayNightTime()
	#resp = LibrafApi().get_set_DayNight(self.client,interval)
 
    def func05_DetectionProperties(self):
	logger.info("func05 DetectionProperties...")
	logger.info('func05 begins:%s'%datetime.datetime.now())
	try:
	    det_roi = init_RpcDetectProp()
	    resp = LibrafApi().get_set_DetectionProperties(self.client,det_roi)
	except ttypes.RpcLibraFException as e:
	    logger.error(e.msg)

    def func06_SnapControl(self):
	logger.info("func06 SnapControl...")
	logger.info('func06 begins:%s'%datetime.datetime.now())
	try:
	    snap_type = init_RpcSnapType()
	    img_trans_prop = init_RpcImgTransProperties()
	    resp = LibrafApi().get_set_ImgTransProperties(self.client,snap_type,img_trans_prop)
	except ttypes.RpcLibraFException as e:                                                                                             
            logger.error(e.msg)
	try:
	    snap_type_list = init_list_RpcSnapType()
 	    resp = LibrafApi().get_set_ImgTransList(self.client,snap_type_list)
	except ttypes.RpcLibraFException as e:
            logger.error(e.msg)
	try:
	    snap_type_list = init_list_RpcSnapType()
	    resp = LibrafApi().get_set_DetTasks(self.client,snap_type_list)
	except ttypes.RpcLibraFException as e:
            logger.error(e.msg)


    def run(self):
        #print "run..."
	func_dict = {1:'self.func01_OSD()',
                     2:'self.func02_ImgMask()',
                     3:'self.func03_LayoutProperties()',
                     4:'self.func04_SensorPropertiesAndIRCut()',
                     5:'self.func05_DetectionProperties()',
                     6:'self.func06_SnapControl()'}
	for key,value in func_dict.items():
	    if self.func_name == key:
		eval(value)
	
       
        	


if __name__ == '__main__':
    pass
