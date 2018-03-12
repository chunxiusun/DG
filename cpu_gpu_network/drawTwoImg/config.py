#!/usr/bin/env python
# -*- coding: utf8 -*-

# author:chunxiusun

CPU_FLAG = True
GPU_FLAG = True
NETWORK_FLAG = False
DRAW_PIC = True

#moniter
INTERVAL = 1
MONITER_TIME = 30
#PID_LIST = [xxx,xx,xxx]
network_interface = 'bond0'

#analyze
#cpu_filelist = ['./log/matrix_apps.log.10267']
cpu_filelist = ['./log/mxadaptor.log.93628','./log/mxadaptor.log.93633']
gpu_filelist = ['./log/nvidia1.log','./log/nvidia2.log']
network_file = './log/if_stat.log'
res_unit = 'T' #K,M,G,T
flow_unit = 'K' #K,M,G,T

#draw
N =1

