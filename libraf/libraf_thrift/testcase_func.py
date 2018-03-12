#!/usr/bin/python
# -*- coding:utf-8 -*-
#author : chunxiusun

import sys
sys.path.append('./gen-py')
import os
if not os.path.exists("./output"):
    os.mkdir("./output")

import config
from init_parameter import *
from function import LibrafApi
import time
import unittest
import random
import datetime
import requests

from logger import logger

from LibraFService import LibraFService
from LibraFService import ttypes

from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol


def checkEqual(value1, value2, flag):
    if flag == 0:
        if value1 != value2:
            msg = "Not equal:%s, %s" %(value1, value2)
            logger.error(msg)
    if flag == 1:
	if abs(value1-value2) >= 1:
	    msg = "Not equal:%s, %s" %(value1, value2)
	    logger.error(msg)


class TestFunc(unittest.TestCase):
    @classmethod
    def setUpClass(self):
	print 'testcase_func starts:%s' % (datetime.datetime.now())
        global transport,client
        logger.info('openTransport')
	try:
            transport = TSocket.TSocket(config.IP, config.PORT)
            transport = TTransport.TFramedTransport(transport)
            protocol = TBinaryProtocol.TBinaryProtocol(transport)
            client = LibraFService.Client(protocol)
            transport.open()
            logger.info('openTransport success')
	except:
	    msg = 'Could not connect to %s:%s'%(config.IP,config.PORT)
	    print msg
	    logger.error(msg)
	    sys.exit(0)

        '''logger.info('if calibrate,stop it')
        if client.CaliBusy():
            logger.info('stop calibrate')
            try:
                LibrafApi().stopCalibrate(client)
            except ttypes.RpcLibraFException as e:
                logger.error(e.msg)
	logger.info('set the passive mode')
        try:
            work_mode = 16842752
            resp = LibrafApi().set_get_WorkMode(client,work_mode)
            logger.info('get WorkMode:%s'%(resp))
        except ttypes.RpcLibraFException as e:
            logger.error(e.msg)'''

    @classmethod
    def tearDownClass(self):
        logger.info('closeTransport')
        transport.close()
        logger.info('closeTransport success')
	print 'testcase_func end:%s' % (datetime.datetime.now())
	#logger.info('reset config')
	#print 'reset config'
	#p = "9000"
	#post_url = "http://%s:%s/api/restore/config"%(config.IP,p)
	#resp = requests.post(post_url)
	#code = resp.status_code
	#print 'resp status code:%s'%code
	#logger.info('resp status code:%s'%code)

    def test01_set_get_WorkMode(self):
	print 'test01 starts:%s' % (datetime.datetime.now())
	logger.info('test01 begins:%s'%datetime.datetime.now())
	work_mode = init_RpcWorkMode()
	logger.info('set_work_mode:%x' %(work_mode))
	resp = LibrafApi().set_get_WorkMode(client,work_mode)
	logger.info('reget_work_mode:%x' %(resp))

        checkEqual(resp, work_mode,0)

        self.assertEqual(resp,work_mode)
 

    def test02_SwitchToPassiveModeWithTimer(self):
	print 'test02 starts:%s' % (datetime.datetime.now())
	logger.info('test02 begins:%s'%datetime.datetime.now())
	LibrafApi().switchToPassiveModeWithTimer(client)

    #OSD
    def test03_get_set_FontProperties(self):
	print 'test03 starts:%s' % (datetime.datetime.now())
        logger.info('test03 begins:%s'%datetime.datetime.now())
	text_type = init_RpcTextType()
	font_prop = init_RpcFontProperties()
	logger.info('text_type:%s'%(text_type))
	logger.info('set FontProperties:%s'%(font_prop)) 
	resp = LibrafApi().get_set_FontProperties(client,text_type,font_prop)
	logger.info('reget FontProperties:%s'%(resp))

	checkEqual(resp.font_size, font_prop.font_size, 0)
	checkEqual(resp.is_display, font_prop.is_display, 0)

        self.assertEqual(resp.font_filename,font_prop.font_filename)
        self.assertEqual(resp.font_size,font_prop.font_size)
        self.assertEqual(resp.interval_scale,font_prop.interval_scale)
        self.assertEqual(resp.space_scale,font_prop.space_scale)
        self.assertEqual(resp.pos_ll,font_prop.pos_ll)
        #self.assertEqual(resp.text_align,font_prop.text_align)
        self.assertEqual(resp.font_color,font_prop.font_color)
        self.assertEqual(resp.outline_color,font_prop.outline_color)
        self.assertEqual(resp.is_display,font_prop.is_display)

    def test04_get_set_OSDOthers(self):
	print 'test04 starts:%s' % (datetime.datetime.now())
	logger.info('test04 begins:%s'%datetime.datetime.now())
	osd_other = init_RpcOSDOther()
	logger.info('set OSDOthers:%s'%(osd_other))
	resp = LibrafApi().get_set_OSDOthers(client,osd_other)
	logger.info('reget GetOSDOthers:%s'%(resp))

	checkEqual(resp.is_24hour, osd_other.is_24hour, 0)
	checkEqual(resp.show_weekday, osd_other.show_weekday, 0)
	checkEqual(resp.zh_str, osd_other.zh_str, 0)

	self.assertEqual(resp.is_24hour,osd_other.is_24hour)
        self.assertEqual(resp.show_weekday,osd_other.show_weekday)
        self.assertEqual(resp.zh_str,osd_other.zh_str)

    def test05_get_set_TextAlign(self):
	print 'test05 starts:%s' % (datetime.datetime.now())
	logger.info('test05 begins:%s'%datetime.datetime.now())
	text_type = init_RpcTextType()
	align_type = init_RpcTextAlignType()
	logger.info('text_type:%s'%(text_type))
	logger.info('set TextAlign:%s'%(align_type))
	resp = LibrafApi().get_set_TextAlign(client,text_type,align_type)
	logger.info('reget TextAlign:%s'%(resp))

	checkEqual(resp, align_type, 0)

	self.assertEqual(resp,align_type)

    #图像遮盖
    def test06_get_set_MaskOn(self):
	print 'test06 starts:%s' % (datetime.datetime.now())
	logger.info('test06 begins:%s'%datetime.datetime.now())
	is_mask_on = random.choice([True,False])
	#is_mask_on = True
	logger.info('set MaskOn:%s'%(is_mask_on))
	resp = LibrafApi().get_set_MaskOn(client,is_mask_on)
	logger.info('reget MaskOn:%s'%(resp))

	checkEqual(resp, is_mask_on, 0)

	self.assertEqual(resp,is_mask_on)

    def test07_get_set_ImageMasks(self):
	print 'test07 starts:%s' % (datetime.datetime.now())
	logger.info('test07 begins:%s'%datetime.datetime.now())
	img_masks = init_list_list_RpcPoint()
	logger.info('set ImageMasks:%s'%(img_masks))
	resp = LibrafApi().get_set_ImageMasks(client,img_masks)
	logger.info('reget ImageMasks:%s'%(resp))
	for i in range(0, len(resp)):
            for j in range(0, len(resp[i])):
		checkEqual(resp[i][j].x, img_masks[i][j].x, 1)
		checkEqual(resp[i][j].y, img_masks[i][j].y, 1)

                rx = round(resp[i][j].x,1)
                vx = round(img_masks[i][j].x,1)
                ry = round(resp[i][j].y,1)
                vy = round(img_masks[i][j].y,1)
                self.assertAlmostEqual(rx, vx)
                self.assertAlmostEqual(ry, vy)

    #图像布局
    def test08_get_set_LayoutProperties(self):
	print 'test08 starts:%s' % (datetime.datetime.now())
	logger.info('test08 begins:%s'%datetime.datetime.now())
	layout_prop = init_RpcLayoutProp()
	logger.info('set LayoutProperties:%s'%(layout_prop))
	resp = LibrafApi().get_set_LayoutProperties(client,layout_prop)
	logger.info('reget LayoutProperties:%s'%(resp))
	
	vx = round(layout_prop.pip_roi.x,1)
        vy = round(layout_prop.pip_roi.y,1)
        vheight = round(layout_prop.pip_roi.height,1)
        vwidth = round(layout_prop.pip_roi.width,1)
        rx = round(resp.pip_roi.x,1)
        ry = round(resp.pip_roi.y,1)
        rheight = round(resp.pip_roi.height,1)
        rwidth = round(resp.pip_roi.width,1)
	
	if layout_prop.default_layout == True:
	    #layout_prop.pip_on = True
	    #layout_prop.pip_fixed = True
	    vx = 0.6
	    vy = 0.0
	    vheight = 0.4
	    vwidth = 0.4
	    
	checkEqual(resp.pip_on, layout_prop.pip_on, 0)
	checkEqual(resp.pip_fixed, layout_prop.pip_fixed, 0)
	checkEqual(resp.snap_rows, layout_prop.snap_rows, 0)
	checkEqual(resp.snap_cols, layout_prop.snap_cols, 0)
	checkEqual(resp.default_layout, layout_prop.default_layout, 0)
	checkEqual(resp.pip_roi.x, layout_prop.pip_roi.x, 1)
	checkEqual(resp.pip_roi.y, layout_prop.pip_roi.y, 1)
	checkEqual(resp.pip_roi.height, layout_prop.pip_roi.height, 1)
	checkEqual(resp.pip_roi.width, layout_prop.pip_roi.width, 1)

        self.assertEqual(resp.pip_on, layout_prop.pip_on)
        self.assertEqual(resp.pip_fixed, layout_prop.pip_fixed)
        self.assertEqual(resp.snap_rows, layout_prop.snap_rows)
        self.assertEqual(resp.snap_cols, layout_prop.snap_cols)
        self.assertEqual(resp.default_layout, layout_prop.default_layout)
        self.assertEqual(rx,vx)
        self.assertEqual(ry,vy)
        self.assertEqual(rheight,vheight)
        self.assertEqual(rwidth,vwidth)

    #图像显示
    def test09_get_set_SensorProperties(self):
	print 'test09 starts:%s' % (datetime.datetime.now())
	logger.info('test09 begins:%s'%datetime.datetime.now())
	sensor_type = init_RpcSensorType()
	sensor_prop = init_RpcSensorProp()
	logger.info('sensor_type:%s'%(sensor_type))
        logger.info('set SensorProperties:%s'%(sensor_prop))
	try:
	    resp = LibrafApi().get_set_SensorProperties(client,sensor_type,sensor_prop)
	except ttypes.RpcLibraFException as e:
	    print e.msg
	    logger.info(e.msg)
	    self.assertEqual(e.msg,'SENSOR_OCCLUSION_ERROR')
	logger.info('reget SensorProperties:%s'%(resp))
	if sensor_prop.exposure_auto == True:
	    sensor_prop.exposure = 50.0
	if sensor_prop.shutter_auto == True:
	    if sensor_type == 1:
	        sensor_prop.shutter = 10000.0
	    elif sensor_type == 0:
		sensor_prop.shutter = 50000.0
	checkEqual(resp.exposure, sensor_prop.exposure, 1)
	checkEqual(resp.shutter, sensor_prop.shutter, 1)
	checkEqual(resp.shutter_auto, sensor_prop.shutter_auto, 0 )

	self.assertTrue(abs(resp.exposure-sensor_prop.exposure)<1)
        self.assertEqual(resp.exposure_auto,sensor_prop.exposure_auto)
        try:
	    self.assertTrue(abs(resp.shutter-sensor_prop.shutter)<1)
	except:
	    print sensor_type
	    print sensor_prop.exposure_auto
	    print resp.exposure
	    print sensor_prop.shutter_auto
	    print sensor_prop.shutter,resp.shutter
        self.assertEqual(resp.shutter_auto,sensor_prop.shutter_auto)
        #self.assertEqual(resp.fps,sensor_prop.fps)
        #self.assertEqual(resp.fps_auto,sensor_prop.fps_auto)
        #self.assertEqual(resp.resolution,sensor_prop.resolution)

    def test10_get_set_DayNight(self):
	print 'test10 starts:%s' % (datetime.datetime.now())
	logger.info('test10 begins:%s'%datetime.datetime.now())
	interval = init_RpcDayNightTime()
	logger.info('set DayNight:%s'%(interval))
	try:
	    resp = LibrafApi().get_set_DayNight(client,interval)
	except ttypes.RpcLibraFException as e:
	    print e.msg
	#except:
	    #print 'An unexpected exception'
	logger.info('reget DayNight:%s'%(resp))

	checkEqual(resp.is_auto,interval.is_auto,0)
	checkEqual(resp.is_bw,interval.is_bw,0)
	checkEqual(resp.start_tm,interval.start_tm,0)
	checkEqual(resp.end_tm,interval.end_tm,0)

	self.assertEqual(resp.is_auto,interval.is_auto)
	self.assertEqual(resp.is_bw,interval.is_bw)
	self.assertEqual(resp.start_tm,interval.start_tm)
	self.assertEqual(resp.end_tm,interval.end_tm)

    #检测区域
    def test11_get_set_DetectionProperties(self):
	print 'test11 starts:%s' % (datetime.datetime.now())
	logger.info('test11 begins:%s'%datetime.datetime.now())
	det_roi = init_RpcDetectProp()
	logger.info('set DetectionProperties:%s'%(det_roi))
	resp = LibrafApi().get_set_DetectionProperties(client,det_roi)
	logger.info('reget DetectionProperties:%s'%(resp))
	#self.assertEqual(resp.threshold, det_roi.threshold)
        #self.assertEqual(resp.dist, det_roi.dist)
        #self.assertAlmostEqual(0.1235555555, 0.1235555556)
        for i in range(0, len(resp.polygons)):
            for j in range(0, len(resp.polygons[i])):

		checkEqual(resp.polygons[i][j].x,det_roi.polygons[i][j].x,1)
		checkEqual(resp.polygons[i][j].y,det_roi.polygons[i][j].y,1)

                rx = resp.polygons[i][j].x
                vx = det_roi.polygons[i][j].x
                ry = resp.polygons[i][j].y
                vy = det_roi.polygons[i][j].y
                self.assertTrue(abs(rx-vx)<1)
                self.assertTrue(abs(ry-vy)<1)

    #抓拍设置
    def test12_get_set_ImgTransProperties(self):
	print 'test12 starts:%s' % (datetime.datetime.now())
	logger.info('test12 begins:%s'%datetime.datetime.now())
	snap_type = init_RpcSnapType()
	img_trans_prop = init_RpcImgTransProperties()
	logger.info('snap_type:%s'%(snap_type))
	logger.info('set ImgTransProperties:%s'%(img_trans_prop))
	resp = LibrafApi().get_set_ImgTransProperties(client,snap_type,img_trans_prop)
	logger.info('reget ImgTransProperties:%s'%(resp))

	checkEqual(resp.format,img_trans_prop.format,0)
	checkEqual(resp.ip,img_trans_prop.ip,0)
	checkEqual(resp.port,img_trans_prop.port,0)

	self.assertEqual(resp.format,img_trans_prop.format)
        self.assertEqual(resp.ip,img_trans_prop.ip)
        self.assertEqual(resp.port,img_trans_prop.port)
	self.assertEqual(resp.is_snap_trans,img_trans_prop.is_snap_trans)
	self.assertEqual(resp.is_fovea_trans,img_trans_prop.is_fovea_trans)

    def test13_get_set_ImgTransList(self):
	print 'test13 starts:%s' % (datetime.datetime.now())
	logger.info('test13 begins:%s'%datetime.datetime.now())
	snap_type_list = init_list_RpcSnapType()
	snap_type_list = random.choice([snap_type_list,[]])
	logger.info('set ImgTransList:%s'%(snap_type_list))
	resp = LibrafApi().get_set_ImgTransList(client,snap_type_list)
	logger.info('reget ImgTransList:%s'%(resp))

	checkEqual(sorted(resp),sorted(snap_type_list),0)

        self.assertEqual(resp,snap_type_list)

    def test14_get_set_DetTasks(self):
	print 'test14 starts:%s' % (datetime.datetime.now())
	logger.info('test14 begins:%s'%datetime.datetime.now())
	snap_type_list = init_list_RpcSnapType()
	logger.info('set DetTasks:%s'%(snap_type_list))
	resp = LibrafApi().get_set_DetTasks(client,snap_type_list)
	logger.info('reget DetTasks:%s'%(resp))

	checkEqual(sorted(resp),sorted(snap_type_list),0)

        self.assertEqual(resp,snap_type_list)

    #目标检测敏感度
    def test15_get_set_BGMSensitivity(self):
	print 'test15 starts:%s' % (datetime.datetime.now())
	logger.info('test15 begins:%s'%datetime.datetime.now())
	sen = random.uniform(0,10)
	logger.info('set BGMSensitivity:%f'%(sen))
	resp = LibrafApi().get_set_BGMSensitivity(client,sen)
	logger.info('reget BGMSensitivity:%f'%(resp))

	checkEqual(resp,sen,1)

	self.assertTrue(abs(resp-sen)<1)

    def test16_LearnBGM(self):
	print 'test16 starts:%s' % (datetime.datetime.now())
	logger.info('test16 begins:%s'%datetime.datetime.now())
	logger.info('start LearnBGM')
        LibrafApi().learnBGM(client)
        while True:
            time.sleep(1)
            state = LibrafApi().learnBGMState(client)
            logger.info('LearnBGMState:%s'%(state))
            if state == -1 or state == 100:
                break
	resp = client.GetBGMSensitivity()
	print 'get BGMSensitivity:%f'%(resp)
	logger.info('get BGMSensitivity:%f'%(resp))

    #摄像机校准
    def test17_AutoCalibrate(self):
	print 'test17 starts:%s' % (datetime.datetime.now())
	logger.info('test17 begins:%s'%datetime.datetime.now())
	is_auto = True
	#logger.info('is_auto'%(str(is_auto)))
	while client.CaliBusy():
            time.sleep(2)
            logger.info('Please waitting...')
        logger.info('Auto calibrate begins')
        LibrafApi().autoCalibrate(client,is_auto)
        cali_busy = LibrafApi().caliBusy(client)
        logger.info('CaliBusy:%r' %(cali_busy))
        self.assertTrue(cali_busy)
        while client.CaliBusy():
            time.sleep(2)
            cali_state = LibrafApi().caliState(client)
            logger.info('calibrate percentage:%d' %(cali_state))
            #if state > 10:
                #client.Calibrate(True)
                #self.assertRaises(ttypes.RpcLibraFException,client.Calibrate,True)#???需确认
            self.assertTrue(cali_state in range(0,101) or cali_state == -1)
        cali_state = LibrafApi().caliState(client)
        logger.info('CaliState:%d' %(cali_state))
        self.assertTrue(cali_state==100 or cali_state==-1)

    def test18_StopCalibrate(self):
	print 'test18 starts:%s' % (datetime.datetime.now())
	logger.info('test18 begins:%s'%datetime.datetime.now())
	if client.CaliBusy():
            logger.info('CaliBusy is True, StopCali')
            LibrafApi().stopCalibrate(client)
            cali_busy = LibrafApi().caliBusy(client)
            logger.info('CaliBusy:%r' %(cali_busy))
            self.assertFalse(cali_busy)
            cali_state = LibrafApi().caliState(client)
            logger.info('CaliState:%d' %(cali_state))
            self.assertEqual(cali_state,-1)
        else:
            logger.info('CaliBusy is False, StartCali')
	    is_auto = True
            LibrafApi().autoCalibrate(client,is_auto)
            cali_busy = LibrafApi().caliBusy(client)
            logger.info('CaliBusy:%r' %(cali_busy))
            self.assertTrue(cali_busy)
            time.sleep(30)
            cali_state = LibrafApi().caliState(client)
            logger.info('calibrate percentage:%d' %(cali_state))
            logger.info('StopCali')
            LibrafApi().stopCalibrate(client)
            cali_busy = LibrafApi().caliBusy(client)
            logger.info('CaliBusy:%r' %(cali_busy))
            self.assertFalse(cali_busy)
            cali_state = LibrafApi().caliState(client)
            logger.info('CaliState:%d' %(cali_state))
            self.assertEqual(cali_state,-1)

    def test19_IsBlocking(self):
	print 'test19 starts:%s' % (datetime.datetime.now())
	logger.info('test19 begins:%s'%datetime.datetime.now())
	if client.CaliBusy():
            logger.info('CaliBusy is True')
            is_blocking = LibrafApi().isBlocking(client)
            logger.info('IsBlocking:%r' %(is_blocking))
            self.assertTrue(is_blocking)
            logger.info('StopCali')
            LibrafApi().stopCalibrate(client)
            is_blocking = LibrafApi().isBlocking(client)
            logger.info('IsBlocking:%r' %(is_blocking))
            self.assertFalse(is_blocking)
        else:
            logger.info('CaliBusy is False')
            is_blocking = LibrafApi().isBlocking(client)
            logger.info('IsBlocking:%r' %(is_blocking))
            self.assertFalse(is_blocking)
            logger.info('StartCali')
	    is_auto = True
            LibrafApi().autoCalibrate(client,is_auto)
            is_blocking = LibrafApi().isBlocking(client)
            logger.info('IsBlocking:%r' %(is_blocking))
            time.sleep(5)
            logger.info('StopCali')
            LibrafApi().stopCalibrate(client)
            self.assertTrue(is_blocking)

    def test20_GetAlignROI(self):
	print 'test20 starts:%s' % (datetime.datetime.now())
	logger.info('test20 begins:%s'%datetime.datetime.now())
	resp = LibrafApi().getAlignROI(client)
        logger.info('x=%f'%(resp.x))
        logger.info('y=%f'%(resp.y))
        logger.info('height=%f'%(resp.height))
        logger.info('width=%f'%(resp.width))

    #电机操作
    def test21_SetLookAtPointOnStream(self):
	print 'test21 starts:%s' % (datetime.datetime.now())
	logger.info('test21 begins:%s'%datetime.datetime.now())
	point = init_set_stream_RpcPoint()
	logger.info('v.x=%f,v.y=%f'%(point.x,point.y))
	try:
	    LibrafApi().setLookAtPointOnStream(client,point)
	except ttypes.RpcLibraFException as e:
            print e.msg
            logger.info(e.msg)
	    self.assertTrue(e.msg in ['MOTOR_INVALID_ANGLE','MOTOR_OCCLUSION_ERROR'])
            #if e.msg != 'MOTOR_INVALID_ANGLE' and e.msg != 'MOTOR_OCCLUSION_ERROR':
             #   raise Exception('An unexpected exception')

    def test22_MoveLookAtPointOnStream(self):
	print 'test22 starts:%s' % (datetime.datetime.now())
	logger.info('test22 begins:%s'%datetime.datetime.now())
	point = init_move_stream_RpcPoint()
        logger.info('v.x=%f,v.y=%f'%(point.x,point.y))
	try:
	    LibrafApi().moveLookAtPointOnStream(client,point)
	except ttypes.RpcLibraFException as e:
            print e.msg
            logger.info(e.msg)
	    self.assertTrue(e.msg in ['MOTOR_INVALID_ANGLE','MOTOR_OCCLUSION_ERROR'])
            #if e.msg != 'MOTOR_INVALID_ANGLE' and e.msg != 'MOTOR_OCCLUSION_ERROR':
             #   raise Exception('An unexpected exception')

    def test23_SetLookAtPoint(self):
	print 'test23 starts:%s' % (datetime.datetime.now())
	logger.info('test23 begins:%s'%datetime.datetime.now())
	point = init_set_RpcPoint()
	logger.info('v.x=%f,v.y=%f'%(point.x,point.y))
	try:
	    LibrafApi().setLookAtPoint(client,point)
	except ttypes.RpcLibraFException as e:
	    print e.msg
	    logger.info(e.msg)
	    self.assertTrue(e.msg in ['MOTOR_INVALID_ANGLE','MOTOR_OCCLUSION_ERROR']) 
	    #if e.msg != 'MOTOR_INVALID_ANGLE' and e.msg != 'MOTOR_OCCLUSION_ERROR':
             #   raise Exception('An unexpected exception')

    def test24_RotateMotorWithGivenStepLevel(self):
	print 'test24 starts:%s' % (datetime.datetime.now())
	logger.info('test24 begins:%s'%datetime.datetime.now())
	rot_type = init_RpcRotateType()
	level = init_RpcRotateStep()
	logger.info('rot_type:%s'%(rot_type))
	logger.info('level:%s'%(level))
	try:
	    LibrafApi().rotateMotorWithGivenStepLevel(client,rot_type,level)
	    time.sleep(0.3)
	except ttypes.RpcLibraFException as e:
	    print e.msg
	    logger.info(e.msg)
	    self.assertTrue(e.msg in ['MOTOR_INVALID_ANGLE','MOTOR_OCCLUSION_ERROR'])
	    #if e.msg != 'MOTOR_INVALID_ANGLE' and e.msg != 'MOTOR_OCCLUSION_ERROR':
		#raise Exception('An unexpected exception')
	    
	    

    #图片
    def test25_GetRawImg(self):
	print 'test25 starts:%s' % (datetime.datetime.now())
	logger.info('test25 begins:%s'%datetime.datetime.now())
	sensor_type = init_RpcSensorType()
	logger.info('RpcSensorType:%s' %(sensor_type))
	cnt = 2
        while(cnt):
            logger.info('cnt:%d' %(cnt))
            logger.info('Start GetRawImg')
            rpc_mat = LibrafApi().getRawImg(client,sensor_type)
            imgData = rpc_mat.data
            logger.info('Save RawImg')
            fd = open('./output/raw_img'+str(cnt)+'.png', 'wb')
            fd.write(imgData)
            fd.close()
            cnt -= 1

    def test26_GetStreamImg(self):
	print 'test26 starts:%s' % (datetime.datetime.now())
	logger.info('test26 begins:%s'%datetime.datetime.now())
	cnt = 2
        while(cnt):
            logger.info('cnt:%d' %(cnt))
            logger.info('Start GetStreamImg')
            rpc_mat = LibrafApi().getStreamImg(client)
            imgData = rpc_mat.data
            logger.info('Save StreamImg')
            fd = open('./output/stream_img'+str(cnt)+'.png', 'wb')
            fd.write(imgData)
            fd.close()
            cnt -= 1

    def test27_GetFullSzRawImg(self):
	print 'test27 starts:%s' % (datetime.datetime.now())
	logger.info('test27 begins:%s'%datetime.datetime.now())
	sensor_type = init_RpcSensorType()
        logger.info('RpcSensorType:%s' %(sensor_type))
	cnt = 2
        while(cnt):
            logger.info('cnt:%d' %(cnt))
            logger.info('Start GetFullSzRawImg')
            rpc_mat = LibrafApi().getFullSzRawImg(client,sensor_type)
            imgData = rpc_mat.data
            logger.info('Save RawImg')
            fd = open('./output/fullsz_img'+str(cnt)+'.png', 'wb')
            fd.write(imgData)
            fd.close()
            cnt -= 1

    #码流
    def test28_get_set_TwoStreamProperties(self):
	print 'test28 starts:%s' % (datetime.datetime.now())
	logger.info('test28 begins:%s'%datetime.datetime.now())
	stream_prop = init_RpcTwoStreamProperties()
	logger.info('set TwoStreamProperties:%s'%(stream_prop))
	try:
	    resp = LibrafApi().get_set_TwoStreamProperties(client,stream_prop)
	except:
	    raise Exception('An unexpected exception')
	logger.info('reget TwoStreamProperties:%s'%(resp))
        self.assertEqual(resp.main_res,stream_prop.main_res)
        self.assertEqual(resp.main_bitrate_variable,stream_prop.main_bitrate_variable)
        self.assertEqual(resp.main_bitrate,stream_prop.main_bitrate)
        self.assertEqual(resp.main_fps,stream_prop.main_fps)
        self.assertEqual(resp.main_kframe_interval,stream_prop.main_kframe_interval)
        self.assertEqual(resp.sub_bitrate_variable,stream_prop.sub_bitrate_variable)
        self.assertEqual(resp.sub_bitrate,stream_prop.sub_bitrate)
        self.assertEqual(resp.sub_fps,stream_prop.sub_fps)
        self.assertEqual(resp.sub_kframe_interval,stream_prop.sub_kframe_interval)
	self.assertEqual(resp.is_sub_on,stream_prop.is_sub_on)
	
    #设置相机光圈电压值
    def test29_get_set_IrisOffset(self):
        logger.info('test29 begins:%s'%datetime.datetime.now())
        #sensor_type = init_RpcSensorType()
        sensor_type = ttypes.RpcSensorType.RPC_FOVEA
        logger.info('RpcSensorType:%s' %(sensor_type))
        offset = random.randint(-10,10)
        logger.info('set offset:%d'%(offset))
        resp = LibrafApi().get_set_IrisOffset(client,sensor_type,offset)
        self.assertEqual(resp,offset)

    #智能视频流类型
    def test30_get_set_SmartStreamType(self):
	logger.info('test30 begins:%s'%datetime.datetime.now())
	smart_stream_type = init_RpcSmartStreamType()
	logger.info('RpcSmartStreamType:%s' %(smart_stream_type))
	resp = LibrafApi().get_set_SmartStreamType(client,smart_stream_type)
	self.assertEqual(resp,smart_stream_type)

    #去畸变广角图片类型
    def test31_GetUndistortWideImg(self):
	logger.info('test31 begins:%s'%datetime.datetime.now())
	undistort_type = init_RpcUndistortImgType()
	logger.info('RpcUndistortImgType:%s' %(undistort_type))
	cnt = 1
	num = 1 
        while(cnt):
	    logger.info('num:%d' %(num))
            logger.info('cnt:%d' %(cnt))
            logger.info('Start GetUndistortWideImg')
	    #print num
	    num = num + 1
	    try:
                rpc_mat = LibrafApi().getUndistortWideImg(client,undistort_type)
                imgData = rpc_mat.data
                logger.info('Save RawImg')
                fd = open('./output/UndistortWideImg_'+str(undistort_type)+'_'+str(cnt)+'.png', 'wb')
                fd.write(imgData)
                fd.close()
                cnt -= 1
	    except ttypes.RpcLibraFException as e:
                print e.msg
                logger.info(e.msg)
		cnt -= 1
		self.assertEqual(e.msg,"OPERATION_OCCLUSION_ERROR")

    #在视频中画出检测框
    def test32_get_set_DrawBBS(self):
	logger.info('test32 begins:%s'%datetime.datetime.now())
	is_draw_bbs = random.choice([True,False])
	logger.info('set is_draw_bbs:%s' %(is_draw_bbs))
	resp = LibrafApi().get_set_DrawBBS(client,is_draw_bbs)
	logger.info('get is_draw_bbs:%s' %(resp))
	self.assertEqual(resp,is_draw_bbs)

    def test33_get_set_DrawView(self):
	logger.info('test33 begins:%s'%datetime.datetime.now())
	is_draw_view = random.choice([True,False])
	logger.info('set is_draw_view:%s' %(is_draw_view))
	resp = LibrafApi().get_set_DrawView(client,is_draw_view)
	logger.info('get is_draw_view:%s' %(resp))
	self.assertEqual(resp,is_draw_view)

    def test34_get_set_SnapProps(self):
	logger.info('test34 begins:%s'%datetime.datetime.now())
	snap_props = init_RpcSnapProps()
	logger.info('set snap_props:%s' %(snap_props))
	resp = LibrafApi().get_set_SnapProps(client,snap_props)
	logger.info('get snap_props:%s' %(resp))
	self.assertEqual(resp.server_port,snap_props.server_port)
	for key in resp.snap_props:
	    self.assertEqual(resp.snap_props[key].ip,snap_props.snap_props[key].ip)
	    self.assertEqual(resp.snap_props[key].port,snap_props.snap_props[key].port)
	    self.assertEqual(resp.snap_props[key].is_snap_trans,snap_props.snap_props[key].is_snap_trans)
	    self.assertEqual(resp.snap_props[key].is_fovea_trans,snap_props.snap_props[key].is_fovea_trans)
	    self.assertEqual(resp.snap_props[key].format,snap_props.snap_props[key].format)

    def test35_GetSnapConnectionInfo(self):
	logger.info('test35 begins:%s'%datetime.datetime.now())
	resp = LibrafApi().getSnapConnectInfo(client)
	logger.info('get SnapConnectionInfo:%s' %(resp))
	print resp

    def test36_GetSnapPublicKey(self):
	logger.info('test36 begins:%s'%datetime.datetime.now())
	resp = LibrafApi().getSnapPublicKey(client)
	logger.info('get SnapPublicKey:%s' %(resp))
	print resp

    def test37_ResetSnapPriveteKey(self):
	logger.info('test37 begins:%s'%datetime.datetime.now())
	resp = LibrafApi().resetSnapPriveteKey(client)
	logger.info('reset SnapPublicKey:%s' %(resp))
	print resp

    def test38_get_set_Compatible(self):
	logger.info('test38 begins:%s'%datetime.datetime.now())
	compatible = random.choice([True,False])
	logger.info('set compatible:%s' %(compatible))
	resp = LibrafApi().get_set_Compatible(client,compatible)
	logger.info('get compatible:%s' %(resp))
	self.assertEqual(resp,compatible)

    def test39_get_set_DrawDetGrid(self):
	logger.info('test39 begins:%s'%datetime.datetime.now())
	is_draw = random.choice([True,False])
	logger.info('set is_draw:%s' %(is_draw))
	resp = LibrafApi().get_set_DrawDetGrid(client,is_draw)
	logger.info('get is_draw:%s' %(resp))
	self.assertEqual(resp,is_draw)

if __name__ == '__main__':
    suite = unittest.TestSuite()

    #suite.addTest(TestFunc("test01_set_get_WorkMode"))
    #suite.addTest(TestFunc("test02_SwitchToPassiveModeWithTimer"))

    '''ls = ["test03_get_set_FontProperties","test04_get_set_OSDOthers",\
          "test05_get_set_TextAlign","test06_get_set_MaskOn",\
          "test07_get_set_ImageMasks","test08_get_set_LayoutProperties",\
          "test09_get_set_SensorProperties","test10_get_set_DayNight",\
          "test11_get_set_DetectionProperties","test12_get_set_ImgTransProperties",\
          "test13_get_set_ImgTransList","test14_get_set_DetTasks",\
          "test15_get_set_BGMSensitivity","test16_LearnBGM",\
          "test20_GetAlignROI","test21_SetLookAtPointOnStream",\
          "test22_MoveLookAtPointOnStream","test23_SetLookAtPoint",\
          "test24_RotateMotorWithGivenStepLevel","test25_GetRawImg",\
          "test26_GetStreamImg","test27_GetFullSzRawImg",\
          "test30_get_set_SmartStreamType","test31_GetUndistortWideImg"]
    random.shuffle(ls)
    for func in ls:    
	suite.addTest(TestFunc(func))'''

    #suite.addTest(TestFunc("test03_get_set_FontProperties"))
    #suite.addTest(TestFunc("test04_get_set_OSDOthers"))
    #suite.addTest(TestFunc("test05_get_set_TextAlign"))
    #suite.addTest(TestFunc("test06_get_set_MaskOn"))
    #suite.addTest(TestFunc("test07_get_set_ImageMasks"))
    #suite.addTest(TestFunc("test08_get_set_LayoutProperties"))
    #suite.addTest(TestFunc("test09_get_set_SensorProperties"))
    #suite.addTest(TestFunc("test10_get_set_DayNight"))
    #suite.addTest(TestFunc("test11_get_set_DetectionProperties"))
    #suite.addTest(TestFunc("test12_get_set_ImgTransProperties"))
    #suite.addTest(TestFunc("test13_get_set_ImgTransList"))
    #suite.addTest(TestFunc("test14_get_set_DetTasks"))
    #suite.addTest(TestFunc("test15_get_set_BGMSensitivity"))
    #suite.addTest(TestFunc("test16_LearnBGM"))
    ##suite.addTest(TestFunc("test17_AutoCalibrate"))
    ##suite.addTest(TestFunc("test18_StopCalibrate"))
    ##suite.addTest(TestFunc("test19_IsBlocking"))
    #suite.addTest(TestFunc("test20_GetAlignROI"))
    #suite.addTest(TestFunc("test21_SetLookAtPointOnStream"))
    #suite.addTest(TestFunc("test22_MoveLookAtPointOnStream"))
    #suite.addTest(TestFunc("test23_SetLookAtPoint"))
    #suite.addTest(TestFunc("test24_RotateMotorWithGivenStepLevel"))
    #suite.addTest(TestFunc("test25_GetRawImg"))
    #suite.addTest(TestFunc("test26_GetStreamImg"))
    #suite.addTest(TestFunc("test27_GetFullSzRawImg"))
    #suite.addTest(TestFunc("test28_get_set_TwoStreamProperties"))
    #suite.addTest(TestFunc("test29_get_set_IrisOffset"))
    #suite.addTest(TestFunc("test30_get_set_SmartStreamType"))
    #suite.addTest(TestFunc("test31_GetUndistortWideImg"))
    #suite.addTest(TestFunc("test32_get_set_DrawBBS"))
    #suite.addTest(TestFunc("test33_get_set_DrawView"))
    #suite.addTest(TestFunc("test34_get_set_SnapProps"))
    #suite.addTest(TestFunc("test35_GetSnapConnectionInfo"))
    #suite.addTest(TestFunc("test36_GetSnapPublicKey"))
    #suite.addTest(TestFunc("test36_GetSnapPublicKey"))
    #suite.addTest(TestFunc("test38_get_set_Compatible"))
    suite.addTest(TestFunc("test39_get_set_DrawDetGrid"))


    runner = unittest.TextTestRunner()
    runner.run(suite)
