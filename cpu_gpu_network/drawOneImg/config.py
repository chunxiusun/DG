#!/usr/bin/env python
# -*- coding: utf8 -*-

CPU_FLAG = True
SYSTEM_CPU_FLAG = True
GPU_FLAG = True
NETWORK_FLAG = False
DRAW_PIC = True

#moniter
MATRIX = 'matrix_apps'
INTERVAL = 1
MONITER_TIME = 3600
#PID_LIST = [xxx,xx,xxx]
network_interface = 'bond0'

#analyze
#cpu_filelist = ['./log/matrix_apps.log.10267']
cpu_filelist = ['./log/matrix_apps.0.6.0.sun.log.22974']
gpu_filelist = ['./log/nvidia1.log','./log/nvidia2.log','./log/nvidia3.log','./log/nvidia4.log']
network_file = './log/if_stat.log'
res_unit = 'T' #K,M,G,T
flow_unit = 'K' #K,M,G,T

#draw
N =1

