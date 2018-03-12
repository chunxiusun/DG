#!/usr/bin/python
# -*- coding:utf-8 -*-

import sys
sys.path.append('./gen-py')

import config
from init_parameter import *
from function import LibrafApi
import time
import unittest
import random
import datetime

from logger import logger

from LibraFService import LibraFService
from LibraFService import ttypes

from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

flag = random.choice([0,1])
logger.info('flag is:%s'%flag)

def checkEqual(value, flag):
    if flag == 0:
        if value != 'CATCHALL_BUSY':
            msg = "Not equal:%s, CATCHALL_BUSY" %(value)
            logger.error(msg)
    if flag == 1:
	if value != 'CALIBRATION_BUSY':
	    msg = "Not equal:%s, CALIBRATION_BUSY" %(value)
	    logger.error(msg)


class TestAbnormal(unittest.TestCase):
    @classmethod
    def setUpClass(self):
	print 'testcase_abnormal starts:%s' % (datetime.datetime.now())
        global transport,client,flag
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
	if flag == 0:
	    if client.CaliBusy():
	        logger.info('stop calibrate')
	        LibrafApi().stopCalibrate(client)
	    work_mode = ttypes.RpcWorkMode.RPC_CORE_CATCHALL_WORKMODE
	    logger.info('set work_mode = ttypes.RpcWorkMode.RPC_CORE_CATCHALL_WORKMODE')
	    LibrafApi().set_get_WorkMode(client,work_mode)
	if flag == 1:
            logger.info("detection calibrate abnormal")
	    if client.CaliBusy():
	        pass    
	    else:
	       work_mode = ttypes.RpcWorkMode.RPC_CORE_PASSIVE_WORKMODE
	       LibrafApi().set_get_WorkMode(client,work_mode)
	       LibrafApi().autoCalibrate(client,True)

    @classmethod
    def tearDownClass(self):
        logger.info('closeTransport')
	if client.CaliBusy(): 
	    LibrafApi().stopCalibrate(client)
        transport.close()
        logger.info('closeTransport success')
	print 'testcase_abnormal end:%s' % (datetime.datetime.now())

    def test01_set_get_WorkMode(self):
	print 'test01 begins:%s'%datetime.datetime.now()
	logger.info('test01 begins:%s'%datetime.datetime.now())
	work_mode = ttypes.RpcWorkMode.RPC_CORE_CATCHALL_WORKMODE
	logger.info('set_work_mode:%x' %(work_mode))
	try:
	    LibrafApi().set_get_WorkMode(client,work_mode)
	    logger.info('Can be set up')
	except ttypes.RpcLibraFException as e:
	    logger.info(e.msg)
	    checkEqual(e.msg,flag)
	    
    def test02_SwitchToPassiveModeWithTimer(self):
	print 'test02 begins:%s'%datetime.datetime.now()
	logger.info('test02 begins:%s'%datetime.datetime.now())
	try:
	    LibrafApi().switchToPassiveModeWithTimer(client)
	    logger.info('Can be set up')
	except ttypes.RpcLibraFException as e:
	    logger.info(e.msg)
	    checkEqual(e.msg,flag)

    #OSD
    def test03_get_set_FontProperties(self):
	print 'test03 begins:%s'%datetime.datetime.now()
        logger.info('test03 begins:%s'%datetime.datetime.now())
	text_type = init_RpcTextType()
	font_prop = init_RpcFontProperties()
	logger.info('text_type:%s'%(text_type))
	logger.info('set FontProperties:%s'%(font_prop))
	try:
	    LibrafApi().get_set_FontProperties(client,text_type,font_prop)
	    logger.info('Can be set up')
	except ttypes.RpcLibraFException as e:
	    logger.info(e.msg)
	    checkEqual(e.msg,flag)

    def test04_get_set_OSDOthers(self):
	print 'test04 begins:%s'%datetime.datetime.now()
	logger.info('test04 begins:%s'%datetime.datetime.now())
	osd_other = init_RpcOSDOther()
	logger.info('set OSDOthers:%s'%(osd_other))
	try:
	    LibrafApi().get_set_OSDOthers(client,osd_other)
	    logger.info('Can be set up')
	except ttypes.RpcLibraFException as e: 
	    logger.info(e.msg)
	    checkEqual(e.msg,flag)

    def test05_get_set_TextAlign(self):
	print 'test05 begins:%s'%datetime.datetime.now()
	logger.info('test05 begins:%s'%datetime.datetime.now())
	text_type = init_RpcTextType()
	align_type = init_RpcTextAlignType()
	logger.info('text_type:%s'%(text_type))
	logger.info('set TextAlign:%s'%(align_type))  
	try:
	    LibrafApi().get_set_TextAlign(client,text_type,align_type)
	    logger.info('Can be set up')
	except ttypes.RpcLibraFException as e:
	    logger.info(e.msg) 
	    checkEqual(e.msg,flag) 

    #图像遮盖
    def test06_get_set_MaskOn(self):
	print 'test06 begins:%s'%datetime.datetime.now()
	logger.info('test06 begins:%s'%datetime.datetime.now())
	is_mask_on = random.choice([True,False])
	logger.info('set MaskOn:%s'%(is_mask_on))
	try:
	    LibrafApi().get_set_MaskOn(client,is_mask_on)
	    logger.info('Can be set up')
	except ttypes.RpcLibraFException as e:
 	    logger.info(e.msg)
	    checkEqual(e.msg,flag)

    def test07_get_set_ImageMasks(self):
	print 'test07 begins:%s'%datetime.datetime.now()
	logger.info('test07 begins:%s'%datetime.datetime.now())
	img_masks = init_list_list_RpcPoint()
	logger.info('set ImageMasks:%s'%(img_masks))
	LibrafApi().get_set_MaskOn(client,True)
	try:
	    LibrafApi().get_set_ImageMasks(client,img_masks)
	    logger.info('Can be set up')
	except ttypes.RpcLibraFException as e:
	    logger.info(e.msg)
	    checkEqual(e.msg,flag)

    #图像布局
    def test08_get_set_LayoutProperties(self):
	print 'test08 begins:%s'%datetime.datetime.now()
	logger.info('test08 begins:%s'%datetime.datetime.now())
	layout_prop = init_RpcLayoutProp()
	logger.info('set LayoutProperties:%s'%(layout_prop)) 
	try:
	    LibrafApi().get_set_LayoutProperties(client,layout_prop)
	    logger.info('Can be set up')
	except ttypes.RpcLibraFException as e:
	    logger.info(e.msg)
	    checkEqual(e.msg,flag)

    #图像显示
    def test09_get_set_SensorProperties(self):
	print 'test09 begins:%s'%datetime.datetime.now()
	logger.info('test09 begins:%s'%datetime.datetime.now())
	sensor_type = init_RpcSensorType()
	sensor_prop = init_RpcSensorProp()
	logger.info('sensor_type:%s'%(sensor_type))
	logger.info('set SensorProperties:%s'%(sensor_prop))
	try:
	    LibrafApi().get_set_SensorProperties(client,sensor_type,sensor_prop)
	    logger.info('Can be set up')
        except ttypes.RpcLibraFException as e:
	    logger.info(e.msg)
	    checkEqual(e.msg,flag)

    def test10_get_set_DayNight(self):
	print 'test10 begins:%s'%datetime.datetime.now()
	logger.info('test10 begins:%s'%datetime.datetime.now())
	interval = init_RpcDayNightTime()
	logger.info('set DayNight:%s'%(interval))
	try:
	    LibrafApi().get_set_DayNight(client,interval)
	    logger.info('Can be set up')
	except ttypes.RpcLibraFException as e:
	    logger.info(e.msg)
	    checkEqual(e.msg,flag)

    #检测区域
    def test11_get_set_DetectionProperties(self):
	print 'test11 begins:%s'%datetime.datetime.now()
	logger.info('test11 begins:%s'%datetime.datetime.now())
	det_roi = init_RpcDetectProp()
	logger.info('set DetectionProperties:%s'%(det_roi))
	try:
 	    LibrafApi().get_set_DetectionProperties(client,det_roi)
	    logger.info('Can be set up')
	except ttypes.RpcLibraFException as e:
            logger.info(e.msg)
            checkEqual(e.msg,flag)
 
   #抓拍设置
    def test12_get_set_ImgTransProperties(self):
	print 'test12 begins:%s'%datetime.datetime.now()
	logger.info('test12 begins:%s'%datetime.datetime.now())
	snap_type = init_RpcSnapType()
	img_trans_prop = init_RpcImgTransProperties()
	logger.info('snap_type:%s'%(snap_type)) 
	logger.info('set ImgTransProperties:%s'%(img_trans_prop))   
	try: 
	    LibrafApi().get_set_ImgTransProperties(client,snap_type,img_trans_prop)
	    logger.info('Can be set up')
   	except ttypes.RpcLibraFException as e:
            logger.info(e.msg)
            checkEqual(e.msg,flag)

    def test13_get_set_ImgTransList(self):
	print 'test13 begins:%s'%datetime.datetime.now()
	logger.info('test13 begins:%s'%datetime.datetime.now())
	snap_type_list = init_list_RpcSnapType()
	snap_type_list = random.choice([snap_type_list,[]])
	logger.info('set ImgTransList:%s'%(snap_type_list))
	try:
	    LibrafApi().get_set_ImgTransList(client,snap_type_list)
	    logger.info('Can be set up')
	except ttypes.RpcLibraFException as e:
            logger.info(e.msg)
            checkEqual(e.msg,flag)

    def test14_get_set_DetTasks(self):
	print 'test14 begins:%s'%datetime.datetime.now()
	logger.info('test14 begins:%s'%datetime.datetime.now())
	snap_type_list = init_list_RpcSnapType()
	logger.info('set DetTasks:%s'%(snap_type_list))
	try:
	    LibrafApi().get_set_DetTasks(client,snap_type_list)
	    logger.info('Can be set up')
	except ttypes.RpcLibraFException as e:
            logger.info(e.msg)
            checkEqual(e.msg,flag)

    #目标检测敏感度
    def test15_get_set_BGMSensitivity(self):
	print 'test15 begins:%s'%datetime.datetime.now()
	logger.info('test15 begins:%s'%datetime.datetime.now())
	sen = random.uniform(0,10)
	logger.info('set BGMSensitivity:%f'%(sen))
	try:
	    LibrafApi().get_set_BGMSensitivity(client,sen)
	    logger.info('Can be set up')
	except ttypes.RpcLibraFException as e:
            logger.info(e.msg)
            checkEqual(e.msg,flag)

    def test16_LearnBGM(self):
	print 'test16 begins:%s'%datetime.datetime.now()
	logger.info('test16 begins:%s'%datetime.datetime.now())
	logger.info('start LearnBGM')
        try:
	    LibrafApi().learnBGM(client)
	    logger.info('Can be set up')
	except ttypes.RpcLibraFException as e:
            logger.info(e.msg)
            checkEqual(e.msg,flag)

    #摄像机校准
    def test17_AutoCalibrate(self):
	print 'test17 begins:%s'%datetime.datetime.now()
	logger.info('test17 begins:%s'%datetime.datetime.now())
	is_auto = True
        logger.info('Auto calibrate begins')
        try:
	    LibrafApi().autoCalibrate(client,is_auto)
	    logger.info('Can be set up')
        except ttypes.RpcLibraFException as e:
            logger.info(e.msg)
            checkEqual(e.msg,flag)
    def test18_StopCalibrate(self):
	print 'test18 begins:%s'%datetime.datetime.now()
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
	print 'test19 begins:%s'%datetime.datetime.now()
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
	print 'test20 begins:%s'%datetime.datetime.now()
	logger.info('test20 begins:%s'%datetime.datetime.now())
	try:
	    LibrafApi().getAlignROI(client)
	    logger.info('Can be set up')
	except ttypes.RpcLibraFException as e:
            logger.info(e.msg)
            checkEqual(e.msg,flag)
    #电机操作
    def test21_SetLookAtPointOnStream(self):
	print 'test21 begins:%s'%datetime.datetime.now()
	logger.info('test21 begins:%s'%datetime.datetime.now())
	point = init_set_stream_RpcPoint()
	logger.info('v.x=%f,v.y=%f'%(point.x,point.y))
	try:
	    LibrafApi().setLookAtPointOnStream(client,point)
   	    logger.info('Can be set up')
	except ttypes.RpcLibraFException as e:
            logger.info(e.msg)
            checkEqual(e.msg,flag)

    def test22_MoveLookAtPointOnStream(self):
	print 'test22 begins:%s'%datetime.datetime.now()
	logger.info('test22 begins:%s'%datetime.datetime.now())
	point = init_move_stream_RpcPoint()
	logger.info('v.x=%f,v.y=%f'%(point.x,point.y)) 
	try:
	    LibrafApi().moveLookAtPointOnStream(client,point)
	    logger.info('Can be set up')
        except ttypes.RpcLibraFException as e:
            logger.info(e.msg)
            checkEqual(e.msg,flag)
    def test23_SetLookAtPoint(self):
	print 'test23 begins:%s'%datetime.datetime.now()
	logger.info('test23 begins:%s'%datetime.datetime.now())
	point = init_set_RpcPoint()
	logger.info('v.x=%f,v.y=%f'%(point.x,point.y))
	try:
	    LibrafApi().setLookAtPoint(client,point)
	    logger.info('Can be set up')
        except ttypes.RpcLibraFException as e:
            logger.info(e.msg)
            checkEqual(e.msg,flag)
    def test24_RotateMotorWithGivenStepLevel(self):
	print 'test24 begins:%s'%datetime.datetime.now()
	logger.info('test24 begins:%s'%datetime.datetime.now())
	rot_type = init_RpcRotateType()
	level = init_RpcRotateStep()
	logger.info('rot_type:%s'%(rot_type))
	logger.info('level:%s'%(level))  
	try:
	    LibrafApi().rotateMotorWithGivenStepLevel(client,rot_type,level)
	    time.sleep(0.3)
	    logger.info('Can be set up')
	except ttypes.RpcLibraFException as e:
            logger.info(e.msg)
            checkEqual(e.msg,flag)

    #图片
    def test25_GetRawImg(self):
	print 'test25 begins:%s'%datetime.datetime.now()
	logger.info('test25 begins:%s'%datetime.datetime.now())
	sensor_type = init_RpcSensorType()
	cnt = 2
        while(cnt):
            logger.info('cnt:%d' %(cnt))
            logger.info('Start GetRawImg')
            try:
	        rpc_mat = LibrafApi().getRawImg(client,sensor_type)
	        logger.info('Can be set up')
                imgData = rpc_mat.data
                logger.info('Save RawImg')
                fd = open('./output/imgout'+str(cnt)+'.png', 'wb')
                fd.write(imgData)
                fd.close()
                cnt -= 1
	    except ttypes.RpcLibraFException as e:
	  	logger.info(e.msg)
		checkEqual(e.msg,flag)	

    def test26_GetStreamImg(self):
	print 'test26 begins:%s'%datetime.datetime.now()
	logger.info('test26 begins:%s'%datetime.datetime.now())
	cnt = 2
        while(cnt):
            logger.info('cnt:%d' %(cnt))
            logger.info('Start GetStreamImg')
            try:
		rpc_mat = LibrafApi().getStreamImg(client)
	   	logger.info('Can be set up')
                imgData = rpc_mat.data
                logger.info('Save StreamImg')
                fd = open('./output/stream_img'+str(cnt)+'.png', 'wb')
                fd.write(imgData)
                fd.close()
                cnt -= 1
	    except ttypes.RpcLibraFException as e:
		logger.info(e.msg)
	 	checkEqual(e.msg,flag)

    def test27_GetFullSzRawImg(self):
	print 'test27 begins:%s'%datetime.datetime.now()
	logger.info('test27 begins:%s'%datetime.datetime.now())
	sensor_type = init_RpcSensorType()
	cnt = 2
        while(cnt):
            logger.info('cnt:%d' %(cnt))
            logger.info('Start GetRawImg')
            try:
		rpc_mat = LibrafApi().getFullSzRawImg(client,sensor_type)
                logger.info('Can be set up')
		imgData = rpc_mat.data
                logger.info('Save RawImg')
                fd = open('./output/fullsz_img'+str(cnt)+'.png', 'wb')
                fd.write(imgData)
                fd.close()
                cnt -= 1
	    except ttypes.RpcLibraFException as e:
		logger.info(e.msg)
		checkEqual(e.msg,flag)

    #码流
    def test28_get_set_TwoStreamProperties(self):
	print 'test28 begins:%s'%datetime.datetime.now()
	logger.info('test28 begins:%s'%datetime.datetime.now())
	stream_prop = init_RpcTwoStreamProperties()
	logger.info('set TwoStreamProperties:%s'%(stream_prop)) 
	try:
	    LibrafApi().get_set_TwoStreamProperties(client,stream_prop)
	    logger.info('Can be set up')
	except ttypes.RpcLibraFException as e:
	    logger.info(e.msg)
	    checkEqual(e.msg,flag)
	

if __name__ == '__main__':
    suite = unittest.TestSuite()

    if flag == 1:
        suite.addTest(TestAbnormal("test01_set_get_WorkMode"))
        suite.addTest(TestAbnormal("test02_SwitchToPassiveModeWithTimer"))
    
    '''ls = ["test03_get_set_FontProperties","test04_get_set_OSDOthers",\
          "test05_get_set_TextAlign","test06_get_set_MaskOn",\
          "test07_get_set_ImageMasks","test09_get_set_SensorProperties",\
          "test13_get_set_ImgTransList","test14_get_set_DetTasks",\
          "test15_get_set_BGMSensitivity","test16_LearnBGM",\
          "test17_AutoCalibrate","test20_GetAlignROI",\
          "test21_SetLookAtPointOnStream","test22_MoveLookAtPointOnStream",\
          "test23_SetLookAtPoint","test24_RotateMotorWithGivenStepLevel",\
          "test25_GetRawImg","test26_GetStreamImg","test27_GetFullSzRawImg"]
    random.shuffle(ls)
    for func in ls:    
        suite.addTest(TestAbnormal(func))'''

    suite.addTest(TestAbnormal("test03_get_set_FontProperties"))
    suite.addTest(TestAbnormal("test04_get_set_OSDOthers"))
    suite.addTest(TestAbnormal("test05_get_set_TextAlign"))
    suite.addTest(TestAbnormal("test06_get_set_MaskOn"))
    suite.addTest(TestAbnormal("test07_get_set_ImageMasks"))
    #suite.addTest(TestAbnormal("test08_get_set_LayoutProperties"))
    suite.addTest(TestAbnormal("test09_get_set_SensorProperties"))
    suite.addTest(TestAbnormal("test10_get_set_DayNight"))
    #suite.addTest(TestAbnormal("test11_get_set_DetectionProperties"))
    #suite.addTest(TestAbnormal("test12_get_set_ImgTransProperties"))
    suite.addTest(TestAbnormal("test13_get_set_ImgTransList"))
    suite.addTest(TestAbnormal("test14_get_set_DetTasks"))
    suite.addTest(TestAbnormal("test15_get_set_BGMSensitivity"))
    suite.addTest(TestAbnormal("test16_LearnBGM"))
    suite.addTest(TestAbnormal("test17_AutoCalibrate"))
    #suite.addTest(TestAbnormal("test18_StopCalibrate"))
    #suite.addTest(TestAbnormal("test19_IsBlocking"))
    suite.addTest(TestAbnormal("test20_GetAlignROI"))
    suite.addTest(TestAbnormal("test21_SetLookAtPointOnStream"))
    suite.addTest(TestAbnormal("test22_MoveLookAtPointOnStream"))
    suite.addTest(TestAbnormal("test23_SetLookAtPoint"))
    suite.addTest(TestAbnormal("test24_RotateMotorWithGivenStepLevel"))
    suite.addTest(TestAbnormal("test25_GetRawImg"))
    suite.addTest(TestAbnormal("test26_GetStreamImg"))
    suite.addTest(TestAbnormal("test27_GetFullSzRawImg"))
    #suite.addTest(TestAbnormal("test28_get_set_TwoStreamProperties"))'''
    


    runner = unittest.TextTestRunner()
    runner.run(suite)
