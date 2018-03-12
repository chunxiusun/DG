#!/usr/bin/env python
# -*- coding: utf8 -*-

# author:chunxiusun

import os,re
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from config import *

def get_cpu_result(fileName,fname):
    res_list = []
    mem_list = []
    cpu_list = []
    x = []
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
    if DRAW_PIC:
	cpu_list,x = take_sample(cpu_list)
	mem_list,x = take_sample(mem_list)
	res_list,x = take_sample(res_list)
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
    return cpu_list,mem_list,res_list,x

def get_gpu_result(fileName,m):
    fd = open(fileName, 'r')
    mem_list = []
    gpu_list = []
    x = []
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
    if DRAW_PIC:
	mem_list,x = take_sample(mem_list)
	gpu_list,x = take_sample(gpu_list)
    print "################## GPU_%s ######################"%(m)
    print 'Memory-Usage Max:%0.2f%s' %(max(mem_list),'%')
    print 'Memory-Usage Min:%0.2f%s' %(min(mem_list),'%')
    print 'Memory-Usage Avg:%0.2f%s' %(sum(mem_list)/len(mem_list),'%')
    print ''
    print 'GPU-Util Max:%0.2f%s' %(max(gpu_list),'%')
    print 'GPU-Util Min:%0.2f%s' %(min(gpu_list),'%')
    print 'GPU-Util Avg:%0.2f%s' %(sum(gpu_list)/len(gpu_list),'%')
    print ''
    return mem_list,gpu_list,x

def get_network_result(filename):
    in_list = []
    out_list = []
    x = []
    fd = open(filename,'r')
    for line in fd.readlines():
        in_list.append(line.split()[-2])
        out_list.append(line.split()[-1])
    in_list = analyze_unit(in_list[2:])
    out_list = analyze_unit(out_list[2:])
    #print in_list,out_list
    fd.close()
    if DRAW_PIC:
	in_list,x = take_sample(in_list)
	out_list,x = take_sample(out_list)
    print "################## Network ######################"
    print 'Incoming Max:%0.2f%sB/s' %(max(in_list),flow_unit)
    print 'Incoming Min:%0.2f%sB/s' %(min(in_list),flow_unit)
    print 'Incoming Avg:%0.2f%sB/s' %(sum(in_list)/len(in_list),flow_unit)
    print ''
    print 'Outgoing Max:%0.2f%sB/s' %(max(out_list),flow_unit)
    print 'Outgoing Min:%0.2f%sB/s' %(min(out_list),flow_unit)
    print 'Outgoing Avg:%0.2f%sB/s' %(sum(out_list)/len(out_list),flow_unit)
    print ''
    return in_list,out_list,x

def get_system_cpu_result(fileName):
    user_cpu_list = []
    sys_cpu_list = []
    mem_list = []
    x = []
    #row_count = 0
    #row_count_next = 0
    fd = open(fileName,'r')
    #fd_split = fd.read().splitlines()
    for line in fd.readlines():
        #row_count_next = row_count + 1
        #row_count = row_count + 1
        if '%Cpu(s)' in line:
            user_cpu = eval(line.split()[1])
	    sys_cpu = eval(line.split()[3])
	    #print user_cpu,sys_cpu
	    user_cpu_list.append(user_cpu)
	    sys_cpu_list.append(sys_cpu)
	if 'KiB Mem' in line:
	    t_mem = eval(line.split()[2].split('+')[0])
	    u_mem = eval(line.split()[3])
	    #print t_mem,u_mem
	    mem = u_mem*1.0/t_mem
	    #print mem
	    mem_list.append(mem)
    fd.close()
    if DRAW_PIC:
        user_cpu_list,x = take_sample(user_cpu_list)
	sys_cpu_list,x = take_sample(sys_cpu_list)
        mem_list,x = take_sample(mem_list)
    print "################## SYSTEM CPU ######################"
    print 'USER CPU Max:%0.2f%s' %(max(user_cpu_list),'%')
    print 'USER CPU Min:%0.2f%s' %(min(user_cpu_list),'%')
    print 'USER CPU Avg:%0.2f%s' %(sum(user_cpu_list)/len(user_cpu_list),'%')
    print ''
    print 'SYS CPU  Max:%0.2f%s' %(max(sys_cpu_list),'%')                                                                            
    print 'SYS CPU  Min:%0.2f%s' %(min(sys_cpu_list),'%')                                                                            
    print 'SYS CPU  Avg:%0.2f%s' %(sum(sys_cpu_list)/len(sys_cpu_list),'%')                                                              
    print ''
    print 'MEM Max:%0.2f%s' %(max(mem_list),'%')
    print 'MEM Min:%0.2f%s' %(min(mem_list),'%')
    print 'MEM Avg:%0.2f%s' %(sum(mem_list)/len(mem_list),'%')
    print ''
    return user_cpu_list,mem_list,sys_cpu_list,x

def draw_plot(x_list,y_list,title,xlabel,ylabel,index,label=''):
    global plt
    '''if max(y_list[0]) >= max(y_list[1]):
        y_max = max(y_list[0])
    else:
        y_max = max(y_list[1])
    if min(y_list[0]) >= min(y_list[1]):
        y_min = min(y_list[1])
    else:
        y_min = min(y_list[0])'''
    y_max = max(y_list[0])
    y_min = min(y_list[0])
  
    #fig= plt.figure()
    #ax = plt.subplot(111)
    plt.ylim(y_min/1.2,y_max*1.2)
    plt.xlim(0,x_list[0][-1]*1.2)

    if title == 'Network':
	line1 = plt.plot(x_list[0],y_list[0],linewidth=1.0,label='Incoming')
	#line2 = plt.plot(x_list[1],y_list[1],linewidth=1.0,label='Outgoing')
    else:
	line1 = plt.plot(x_list[0],y_list[0],linewidth=1.0,label=label+'_'+str(index))
        #line2 = plt.plot(x_list[1],y_list[1],linewidth=1.0,label=label+'_2')

    plt.axhline(y=sum(y_list[0])/len(y_list[0]),color='r')
    #plt.axhline(y=sum(y_list[1])/len(y_list[1]),color='y')
    plt.text(0,sum(y_list[0])/len(y_list[0]), r'avg:%0.2f'%(sum(y_list[0])/len(y_list[0])))
    #plt.text(0,sum(y_list[1])/len(y_list[1]), r'avg:%0.2f'%(sum(y_list[1])/len(y_list[1])))

    plt.annotate('max:%0.2f'%(max(y_list[0])), xy = (get_x_max(x_list[0],y_list[0]), max(y_list[0])))
    #plt.annotate('max:%0.2f'%(max(y_list[1])), xy = (get_x_max(x_list[1],y_list[1]), max(y_list[1])))
    plt.annotate('min:%0.2f'%(min(y_list[0])), xy = (get_x_min(x_list[0],y_list[0]), min(y_list[0])))
    #plt.annotate('min:%0.2f'%(min(y_list[1])), xy = (get_x_min(x_list[1],y_list[1]), min(y_list[1])))

    plt.title(title)
    label_x = plt.xlabel(xlabel)
    plt.setp(label_x, color='r', fontsize='medium')
    label_y = plt.ylabel('Usage(%s)'%(ylabel))
    plt.setp(label_y, color='r', fontsize='medium')
    #box=ax.get_position()
    #ax.set_position()
    #ax.legend(loc='upper left',bbox_to_anchor=(1.0,0.5))
    plt.legend(loc='upper left')
    if title == 'Network':
	plt.savefig('%s'%(title))
    else:
        plt.savefig('%s-%s_%s'%(label,title,index))
    #plt.show()
    #plt.draw()
    #plt.clf()
    plt.close()

def get_x_max(x_name,y_name):
    for i in range(0,len(y_name)):
        if y_name[i] == max(y_name):
            x_max = x_name[i]
    return x_max

def get_x_min(x_name,y_name):
    for i in range(0,len(y_name)):
        if y_name[i] == min(y_name):
            x_min = x_name[i]
    return x_min

def take_sample(listname):
    y = []
    for i in range(0,len(listname),N):
        y.append(listname[i])
    x = np.arange(0,len(listname),N)
    return y,x

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
            data = value*1.0/1024
        if res_unit == 'G':
            data = value*1.0/1024/1024
        if res_unit == 'T':
            data = value*1.0/1024/1024/1024
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
            data = eval(item)*1.0/1024
        if flow_unit == 'G':
            data = eval(item)*1.0/1024/1024
        if flow_unit == 'T':
            data = eval(item)*1.0/1024/1024/1024
        ls.append(data)
    return ls

def run():
    if CPU_FLAG:
	i = 1
	for item in cpu_filelist:
	    x_list = []
	    cpu_y = []
	    mem_y = []
	    res_y = []
	    m = item.split('/')[-1].split('.')[0]
	    fname = m+'_'+str(i)
	    cpu_list,mem_list,res_list,x = get_cpu_result(item,fname)
	    x_list.append(x)
	    cpu_y.append(cpu_list)
	    mem_y.append(mem_list)
	    res_y.append(res_list)
	    if DRAW_PIC:
	        draw_plot(x_list,cpu_y,'CPU','Time(s)','%',i,m)
	        draw_plot(x_list,mem_y,'MEM','Time(s)','%',i,m)
	        draw_plot(x_list,res_y,'RES','Time(s)','%sB'%(res_unit),i,m)
	    i = i+1
    if SYSTEM_CPU_FLAG:
	i = 1
	for item in cpu_filelist:
            x_list = []
            user_cpu_y = []
            mem_y = []
            sys_cpu_y = []
            m = item.split('/')[-1].split('.')[0]
            fname = m+'_'+str(i)
            user_cpu_list,mem_list,sys_cpu_list,x = get_system_cpu_result(item)
            x_list.append(x)
            user_cpu_y.append(user_cpu_list)
            mem_y.append(mem_list)
            sys_cpu_y.append(sys_cpu_list)
            if DRAW_PIC:
                draw_plot(x_list,user_cpu_y,'USER_CPU','Time(s)','%',i,"user_cpu")
                draw_plot(x_list,mem_y,'MEM','Time(s)','%',i,"mem")
                draw_plot(x_list,sys_cpu_y,'SYS_CPU','Time(s)','%',i,"sys_cpu")
            i = i+1 
    if GPU_FLAG:
	m = 1
	for item in gpu_filelist:
	    x_list = []
	    mem_y = []
	    gpu_y = []
	    mem_list,gpu_list,x = get_gpu_result(item,m)
	    x_list.append(x)
	    mem_y.append(mem_list)
	    gpu_y.append(gpu_list)
	    if DRAW_PIC:
	        draw_plot(x_list,mem_y,'MEM','Time(s)','%',m,'MEM')
	        draw_plot(x_list,gpu_y,'GPU','Time(s)','%',m,'GPU')
	    m = m + 1
    if NETWORK_FLAG:
	x_list = []
	y_list = []
	in_list,out_list,x = get_network_result(network_file)
	x_list.append(x)
	x_list.append(x)
	y_list.append(in_list)
	y_list.append(out_list)
	if DRAW_PIC:
	    draw_plot(x_list,y_list,'Network','Time(s)','%sB/s'%(flow_unit))

if __name__ == '__main__':
    run()
