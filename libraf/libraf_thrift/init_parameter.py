#!/usr/bin/python
# -*- coding:utf-8 -*-

# author : chunxiusun

import sys 
sys.path.append('./gen-py')

import random
import string

from LibraFService import ttypes

def init_RpcSensorType():
    lst = [ttypes.RpcSensorType.RPC_WIDE,ttypes.RpcSensorType.RPC_FOVEA]
    sensor_type = random.choice(lst)
    return sensor_type

def init_RpcTextType():
    #RpcTimeText=0,RpcDescText=1,RpcSnapText=2
    l = [ttypes.RpcTextType.RpcTimeText,ttypes.RpcTextType.RpcDescText]
    text_type = random.choice(l)
    return text_type

def init_RpcSnapType():
    #RpcFace = 0,RpcBody = 1,RpcCar = 2
    l = [ttypes.RpcSnapType.RpcFace,ttypes.RpcSnapType.RpcBody]
    snap_type = random.choice(l)
    return snap_type

def init_RpcFontProperties():
    font_prop = ttypes.RpcFontProperties()
    font_prop.font_filename ="../data/truetype/simsun.ttf"
    font_prop.font_size = random.choice([50,40,30]) #60 40 20
    font_prop.interval_scale = 0.1
    font_prop.space_scale = 0.5
    font_prop.pos_ll = ttypes.RpcPoint()#undo
    font_prop.pos_ll.x = 0.5
    font_prop.pos_ll.y = 0.5
    #RPC_UPPERLEFT_ALIGN=0,RPC_LOWERLEFT_ALIGN=1,RPC_UPPERRIGHT_ALIGN=2,RPC_LOWERRIGHT_ALIGN=3
    font_prop.text_align = random.choice([0,1,2,3])
    #font_prop.text_align = 2#undo
    font_prop.font_color = ttypes.RpcColor()
    font_prop.font_color.val0 = 0
    font_prop.font_color.val1 = 0
    font_prop.font_color.val2 = 0
    font_prop.outline_color = ttypes.RpcColor()
    font_prop.outline_color.val0 = 255
    font_prop.outline_color.val1 = 255
    font_prop.outline_color.val2 = 255
    font_prop.is_display = random.choice([True,False])#True or False
    return font_prop

def init_RpcOSDOther():
    osd_other = ttypes.RpcOSDOther()
    osd_other.is_24hour = random.choice([True,False])#True
    osd_other.show_weekday = random.choice([True,False])
    s = 'adcdefqwe123@#$?*&'
    str1 = string.join(random.sample(s,8)).replace(" ","")
    str2 = '格灵深瞳人眼相机'
    osd_other.zh_str = random.choice([str1,str2])
    return osd_other

def init_RpcTextAlignType():
    #RPC_UPPERLEFT_ALIGN=0,RPC_LOWERLEFT_ALIGN=1,RPC_UPPERRIGHT_ALIGN=2,RPC_LOWERRIGHT_ALIGN=3
    align_type = random.choice([0,1,2,3])
    return align_type

def init_list_list_RpcPoint():
    img_masks = []
    counts = random.choice([1,2,3,4,5])
    edges = random.choice([3,4,5,6,7,8,9,10])
    for i in range(0,counts):
        l = []
        l = [ttypes.RpcPoint(y=0.16, x=0.38), ttypes.RpcPoint(y=0.57, x=0.28), ttypes.RpcPoint(y=0.5, x=0.66)]
        '''for j in range(0,edges):
            item = ttypes.RpcPoint()
            item.x = random.uniform(0,0.99)
            item.y = random.uniform(0,0.99)
            l.append(item)'''
        img_masks.append(l)
    return img_masks

def init_RpcLayoutProp():
    layout_prop = ttypes.RpcLayoutProp()
    layout_prop.default_layout = random.choice([True,False])# True or False
    layout_prop.pip_on = random.choice([True,False])
    layout_prop.pip_fixed = random.choice([True,False])
    layout_prop.snap_rows = random.randint(1,2)
    if layout_prop.snap_rows == 1:
        layout_prop.snap_cols = 8
    else:
        layout_prop.snap_cols = 10
    #layout_prop.snap_cols = random.randint(1,10)
    layout_prop.pip_roi = ttypes.RpcRect()
    layout_prop.pip_roi.x = random.uniform(0,0.99)
    layout_prop.pip_roi.y = random.uniform(0,0.99)
    layout_prop.pip_roi.height = random.uniform(0,1-layout_prop.pip_roi.y)
    layout_prop.pip_roi.width = random.uniform(0,1-layout_prop.pip_roi.x)
    return layout_prop

def init_RpcSensorProp():
    sensor_prop = ttypes.RpcSensorProp()
    sensor_prop.exposure = random.uniform(50,100)
    #sensor_prop.exposure = 50.0
    sensor_prop.exposure_auto = random.choice([True,False])
    sensor_prop.shutter = random.uniform(200,40000)
    #sensor_prop.shutter = 1000000
    sensor_prop.shutter_auto = random.choice([True,False])
    #sensor_prop.fps = random.uniform(0,0.99)
    sensor_prop.fps = 20.0
    sensor_prop.fps_auto = True
    sensor_prop.resolution = ttypes.RpcResolution()
    #sensor_prop.resolution.width = random.randint(1,3)
    sensor_prop.resolution.width = 0
    #sensor_prop.resolution.height = random.randint(1,3)
    sensor_prop.resolution.height = 0
    return sensor_prop

def init_RpcDayNightTime():
    interval = ttypes.RpcDayNightTime()
    interval.is_auto = False #auto switch: 19:00 - 7:00 is night
    interval.is_bw = random.choice([True,False]) #true: do not filter infrared ray during night; false: filter
    start_h = random.choice([16,17,18,19,20,21,22,23])
    start_m = random.choice([00,15,30,45])
    interval.start_tm = start_h*100 + start_m #hour*100 + min
    end_h = random.choice([3,4,5,6,7,8,9,10,11])
    interval.end_tm = end_h*100 + start_m #hour*100 + min
    return interval

def init_RpcDetectProp():
    det_roi = ttypes.RpcDetectProp()
    det_roi.threshold = 0.0 #undo
    det_roi.dist = 20 #undo
    counts = random.randint(1,5)
    edges = random.randint(3,10)
    det_roi.polygons = []
    for i in range(0,counts):
        l = []
        l = [ttypes.RpcPoint(y=0.5157407522201538, x=0.02395833283662796), \
             ttypes.RpcPoint(y=0.5222222208976746, x=0.9635416865348816), \
             ttypes.RpcPoint(y=0.8425925970077515, x=0.9536458253860474),\
             ttypes.RpcPoint(y=0.8037037253379822, x=0.05156249925494194)]
        '''for j in range(0,edges):
            item = ttypes.RpcPoint()
            item.x = random.uniform(0,0.99)
            item.y = random.uniform(0,0.99)
            l.append(item)'''
        det_roi.polygons.append(l)
    return det_roi

def init_RpcImgTransProperties():
    img_trans_prop = ttypes.RpcImgTransProperties()
    img_trans_prop.format = 4 #RPC_JPEG = 0
    img_trans_prop.ip = random.choice(["192.168.2.16","192.168.2.137","192.168.4.41"])
    img_trans_prop.port = random.randint(1,9999)#9900
    img_trans_prop.is_snap_trans = random.choice([True,False])
    img_trans_prop.is_fovea_trans = random.choice([True,False])
    return img_trans_prop

def init_list_RpcSnapType():
    l = [[0],[1],[0,1]]
    snap_type_list = random.choice(l)#[0,1]#RpcFace = 0,RpcBody = 1,RpcCar = 2
    return snap_type_list

def init_set_stream_RpcPoint():
    point = ttypes.RpcPoint()
    point.x = random.uniform(0,1)
    point.y = random.uniform(0.3,0.6)
    return point

def init_move_stream_RpcPoint():
    point = ttypes.RpcPoint()
    point.x = random.uniform(-0.6,0.6)
    point.y = random.uniform(-0.6,0.6)
    return point

def init_set_RpcPoint():
    point = ttypes.RpcPoint()
    point.x = random.uniform(0,0.99)
    point.y = random.uniform(0,0.99)
    return point

def init_RpcRotateType():
    lst = []
    lst.append(ttypes.RpcRotateType.RpcMoveLeft)
    lst.append(ttypes.RpcRotateType.RpcMoveRight)
    lst.append(ttypes.RpcRotateType.RpcMoveUp)
    lst.append(ttypes.RpcRotateType.RpcMoveDown)
    lst.append(ttypes.RpcRotateType.RpcMoveUpLeft)
    lst.append(ttypes.RpcRotateType.RpcMoveUpRight)
    lst.append(ttypes.RpcRotateType.RpcMoveDownLeft)
    lst.append(ttypes.RpcRotateType.RpcMoveDownRight)
    rot_type = random.choice(lst)
    return rot_type


def init_RpcRotateStep():
    #Rpc1Level = 0,Rpc2Level = 1,Rpc3Level = 2,Rpc4Level = 3,Rpc5Level = 4,Rpc6Level = 5
    l = [ttypes.RpcRotateStep.Rpc1Level,ttypes.RpcRotateStep.Rpc2Level,\
         ttypes.RpcRotateStep.Rpc3Level,ttypes.RpcRotateStep.Rpc4Level,\
         ttypes.RpcRotateStep.Rpc5Level,ttypes.RpcRotateStep.Rpc6Level]
    level = random.choice(l)
    return level

def init_RpcWorkMode():
    lst = [ttypes.RpcWorkMode.RPC_CORE_PASSIVE_WORKMODE,ttypes.RpcWorkMode.RPC_CORE_CATCHALL_WORKMODE]
    work_mode = random.choice(lst)
    #set_work_mode = ttypes.RpcWorkMode.RPC_CORE_PASSIVE_WORKMODE
    return work_mode

def init_RpcTwoStreamProperties():
    stream_prop = ttypes.RpcTwoStreamProperties()
    stream_prop.main_res = random.choice([0,1,2,3,4])#RPC_FHD = 0,RPC_UXGA = 1,RPC_XGA = 2,RPC_VGA = 3,RPC_HD = 4
    #stream_prop.main_res = 1
    stream_prop.main_bitrate_variable = False #False
    stream_prop.main_bitrate = random.choice([8192,4096,2048,1024,512])
    stream_prop.main_fps = random.randint(1,20)
    stream_prop.main_kframe_interval = random.randint(1,100)
    stream_prop.sub_bitrate_variable = False
    stream_prop.sub_bitrate = random.choice([8192,4096,2048,1024,512])
    stream_prop.sub_fps = random.randint(1,20)
    stream_prop.sub_kframe_interval = random.randint(1,100)
    stream_prop.is_sub_on = random.choice([True,False])
    return stream_prop

def init_RpcSmartStreamType():
    smart_stream_type = random.choice([0,1,2])#0:人脸墙在顶部,1:人脸墙在下方,2:无人脸墙
    return smart_stream_type

def init_RpcUndistortImgType():
    undistort_type = random.choice([0,3])#0:RPC_UNDISTORT_1080P,1:RPC_UNDISTORT_720P,2:RPC_UNDISTORT_540P,3:RPC_UNDISTORT_CROP
    return undistort_type

def init_RpcSnapProps():
    snap_prop = ttypes.RpcSnapProps()
    snap_type_list = [0,1]#RpcFace = 0,RpcBody = 1,RpcCar = 2
    snap_prop.snap_props = {}
    for snap_type in snap_type_list:
	snap_prop.snap_props[snap_type] = init_RpcImgTransProperties()
    snap_prop.server_port = random.randint(1,9999)
    return snap_prop

