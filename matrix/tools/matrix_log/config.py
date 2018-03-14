#!/usr/bin/env python
# -*- coding: utf8 -*-

DETECT_FLAG = True
ALIGN_FLAG = True
QUALITY_FLAG = True
DRAW_PIC = True

#moniter
INTERVAL = 1
MONITER_TIME = 600
#PID_LIST = [xxx,xx,xxx]
network_interface = 'bond0'

#analyze
#cpu_filelist = ['./log/matrix_apps.log.10267']
detect_filelist = ['./FaceDetectProcessor']
align_filelist = ['./FaceAlignmentProcessor']
quality_filelist = ['./FaceQualityProcessor']
res_unit = 'T' #K,M,G,T
flow_unit = 'K' #K,M,G,T

#draw
N =10

