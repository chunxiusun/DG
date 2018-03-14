#!/usr/bin/env python
# -*- coding: utf8 -*-

# author : chunxiusun

import commands

pid_cmd = "ps -ef|grep \"matrix_apps\"|grep -v grep |awk  '{print $2}'"
pids_return = commands.getstatusoutput(pid_cmd)
MATRIX_PID = pids_return[1].split("\n")[0]
print MATRIX_PID

CPU_FLAG = True
GPU_FLAG = True
NETWORK_FLAG = False
DRAW_PIC = True

#moniter
MATRIX = 'matrix_apps'
INTERVAL = 1
MONITER_TIME = 600
#PID_LIST = [xxx,xx,xxx]
network_interface = 'bond0'

#analyze
#cpu_filelist = ['./log/matrix_apps.log.10267']
cpu_filelist = ['./log/matrix_apps.log.%s'%(str(MATRIX_PID))]
gpu_filelist = ['./log/nvidia1.log']
network_file = './log/if_stat.log'
res_unit = 'G' #K,M,G,T
flow_unit = 'K' #K,M,G,T

#draw
N =1

