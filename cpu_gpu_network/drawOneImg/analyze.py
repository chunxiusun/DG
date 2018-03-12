#!/usr/bin/env python
# -*- coding: utf8 -*-

# author:chunxiusun

import os,re
import numpy as np
import matplotlib.pyplot as plt
from config import *

def get_cpu_result(fileName,fname):
    res_list = []
    mem_list = []
    cpu_list = []
    row_count = 0  
    row_count_next = 0
    fd = open(fileName,'r')
    fd_split = fd.read().splitlines()
    for row in fd_split:
        row_count_next = row_count + 1  
        row_count = row_count + 1 
        if 'PID' not in row:
            continue
        if row_count_next == len(fd_split):
            break
        row_next = fd_split[row_count_next]
        if row_next:
            res = row_next.strip().split()[5]
            cpu = eval(row_next.strip().split()[8])
            mem = eval(row_next.strip().split()[9])
            res_list.append(res)
            cpu_list.append(cpu)
            mem_list.append(mem)
    res_list = analyze_RES(res_list)
    fd.close()
    print "################## %s ######################"%(fname)
    print '%s CPU Max:%0.2f%s' %(fname,max(cpu_list),'%')
    print '%s CPU Min:%0.2f%s' %(fname,min(cpu_list),'%')
    print '%s CPU Avg:%0.2f%s' %(fname,sum(cpu_list)/len(cpu_list),'%')
    print ''
    print '%s MEM Max:%0.2f%s' %(fname,max(mem_list),'%')
    print '%s MEM Min:%0.2f%s' %(fname,min(mem_list),'%')
    print '%s MEM Avg:%0.2f%s' %(fname,sum(mem_list)/len(mem_list),'%')
    print ''
    print '%s RES Max:%0.2f%sB' %(fname,max(res_list),res_unit)
    print '%s RES Min:%0.2f%sB' %(fname,min(res_list),res_unit)
    print '%s RES Avg:%0.2f%sB' %(fname,sum(res_list)/len(res_list),res_unit)
    print ''
    return cpu_list,mem_list,res_list

def get_gpu_result(fileName,m):
    fd = open(fileName, 'r')
    mem_list = []
    gpu_list = []
    for line in fd.readlines():
        line = line.strip()
        if re.search('([0-9]+)MiB.*/', line) == None:
            continue
        mem_1 = int(re.search('([0-9]+)MiB.*/', line).group(1))
        if re.search('/ ([0-9]+)MiB.*', line) == None:
            continue
        mem_2 = int(re.search('/ ([0-9]+)MiB.*', line).group(1))
        mem_usage = (mem_1 *1.0 / mem_2)*100
        mem_list.append(mem_usage)
        if re.search('MiB |.* ([0-9]+)%.*|', line) == None:
            continue
        gpu_util = eval(re.search('MiB |.* ([0-9]+)%.*|', line).group(1))
        gpu_list.append(gpu_util)
    fd.close()
    print "################## GPU_%s ######################"%(m)
    print 'Memory-Usage Max:%0.2f%s' %(max(mem_list),'%')
    print 'Memory-Usage Min:%0.2f%s' %(min(mem_list),'%')
    print 'Memory-Usage Avg:%0.2f%s' %(sum(mem_list)/len(mem_list),'%')
    print ''
    print 'GPU-Util Max:%0.2f%s' %(max(gpu_list),'%')
    print 'GPU-Util Min:%0.2f%s' %(min(gpu_list),'%')
    print 'GPU-Util Avg:%0.2f%s' %(sum(gpu_list)/len(gpu_list),'%')
    print ''
    return mem_list,gpu_list

def get_network_result(filename):
    in_list = []
    out_list = []
    fd = open(filename,'r')
    for line in fd.readlines():
        in_list.append(line.split()[-2])
        out_list.append(line.split()[-1])
    in_list = analyze_unit(in_list[2:])
    out_list = analyze_unit(out_list[2:])
    #print in_list,out_list
    fd.close()
    print "################## Network ######################"
    print 'Incoming Max:%0.2f%sB/s' %(max(in_list),flow_unit)
    print 'Incoming Min:%0.2f%sB/s' %(min(in_list),flow_unit)
    print 'Incoming Avg:%0.2f%sB/s' %(sum(in_list)/len(in_list),flow_unit)
    print ''
    print 'Outgoing Max:%0.2f%sB/s' %(max(out_list),flow_unit)
    print 'Outgoing Min:%0.2f%sB/s' %(min(out_list),flow_unit)
    print 'Outgoing Avg:%0.2f%sB/s' %(sum(out_list)/len(out_list),flow_unit)
    print ''
    return in_list,out_list

def analyze_RES(listname):
    ls = []
    for item in listname:
        if 'm' in item:
            value = eval(item.split('m')[0])*1024
        elif 'g' in item:
            value = eval(item.split('g')[0])*1024*1024
        elif 't' in item:
            value = eval(item.split('t')[0])*1024*1024*1024
        else:
            value = eval(item)

        if res_unit == 'M':
            data = value/1024
        if res_unit == 'G':
            data = value/1024/1024
        if res_unit == 'T':
            data = value/1024/1024/1024
        if res_unit == 'K':
            data = value

        ls.append(data)
    return ls

def analyze_unit(listname):
    ls = []
    for item in listname:
        if flow_unit == 'K':
            data = eval(item)
        if flow_unit == 'M':
            data = eval(item)/1024
        if flow_unit == 'G':
            data = eval(item)/1024/1024
        if flow_unit == 'T':
            data = eval(item)/1024/1024/1024
        ls.append(data)
    return ls

def run():
    if CPU_FLAG:
	i = 1
	for item in cpu_filelist:
	    m = item.split('/')[-1].split('.')[0]
	    fname = m+'_'+str(i)
	    i = i+1
	    cpu_list,mem_list,res_list = get_cpu_result(item,fname)
    if GPU_FLAG:
	m = 1
	for item in gpu_filelist:
	    mem_list,gpu_list = get_gpu_result(item,m)
	    m += 1
    if NETWORK_FLAG:
	in_list,out_list = get_network_result(network_file)

if __name__ == '__main__':
    run()
