#!/usr/bin/python
#-*- coding:utf-8 -*-
# author:chunxiusun

import os,re
import numpy as np
import matplotlib.pyplot as plt

#os.system('rm sta.txt')

N =1
f_out = 'sta.txt'
filelist = ['./nvidia1.log','./nvidia2.log']

def get_nvidia_result(fileName):
    fd = open(fileName, 'r')
    mem_list = []
    gpu_list = []
    for line in fd.readlines():
        line = line.strip()
        #print line
        if re.search('([0-9]+)MiB.*/', line) == None:
            continue
        mem_1 = int(re.search('([0-9]+)MiB.*/', line).group(1))
        #print mem_1
        if re.search('/ ([0-9]+)MiB.*', line) == None:
            continue
        mem_2 = int(re.search('/ ([0-9]+)MiB.*', line).group(1))
        #print mem_2
        mem_usage = mem_1 *1.0 / mem_2
        #print 'mem_usage:%f' %(mem_usage)
        mem_list.append(mem_usage)
        if re.search('MiB |.* ([0-9]+)%.*|', line) == None:
            continue
        gpu_util = eval(re.search('MiB |.* ([0-9]+)%.*|', line).group(1))
        #print gpu_util
        gpu_list.append(gpu_util)
    fd.close()
    return mem_list,gpu_list

def take_sample(listname,title,unit,m):
    y = []
    for i in range(0,len(listname),N):
        y.append(listname[i])
    #x = np.arange(0,len(y))
    x = np.arange(0,len(listname),N)

    fd_out = open(f_out,'a')
    fd_out.write("################## %s_%d ######################\r\n"%(title,m))
    fd_out.write('%s Max:%0.2f%s\r\n' %(title,max(y),unit))
    fd_out.write('%s Min:%0.2f%s\r\n' %(title,min(y),unit))
    fd_out.write('%s Avg:%0.2f%s\r\n' %(title,sum(y)/len(y),unit))
    fd_out.write('\r\n')
    fd_out.close()
    print "################## %s_%d ######################"%(title,m)
    print '%s Max:%0.2f%s' %(title,max(y),unit)
    print '%s Min:%0.2f%s' %(title,min(y),unit)
    print '%s Avg:%0.2f%s' %(title,sum(y)/len(y),unit)
    
    return x,y

def draw_plot(x_list,y_list,title,xlabel,ylabel,label):
    global plt
    if max(y_list[0]) >= max(y_list[1]):
        y_max = max(y_list[0])
    else:
        y_max = max(y_list[1])
    if min(y_list[0]) >= min(y_list[1]):
        y_min = min(y_list[1])
    else:
        y_min = min(y_list[0])
  
    #fig= plt.figure()
    #ax = plt.subplot(111)
    plt.ylim(y_min/1.2,y_max*1.2)
    plt.xlim(0,x_list[0][-1]*1.2)

    line1 = plt.plot(x_list[0],y_list[0],linewidth=1.0,label=label+'_1')
    line2 = plt.plot(x_list[1],y_list[1],linewidth=1.0,label=label+'_2')

    plt.axhline(y=sum(y_list[0])/len(y_list[0]),color='r')
    plt.axhline(y=sum(y_list[1])/len(y_list[1]),color='y')
    plt.text(0,sum(y_list[0])/len(y_list[0]), r'avg:%0.2f'%(sum(y_list[0])/len(y_list[0])))
    plt.text(0,sum(y_list[1])/len(y_list[1]), r'avg:%0.2f'%(sum(y_list[1])/len(y_list[1])))

    plt.annotate('max:%0.2f'%(max(y_list[0])), xy = (get_x_max(x_list[0],y_list[0]), max(y_list[0])))
    plt.annotate('max:%0.2f'%(max(y_list[1])), xy = (get_x_max(x_list[1],y_list[1]), max(y_list[1])))
    plt.annotate('min:%0.2f'%(min(y_list[0])), xy = (get_x_min(x_list[0],y_list[0]), min(y_list[0])))
    plt.annotate('min:%0.2f'%(min(y_list[1])), xy = (get_x_min(x_list[1],y_list[1]), min(y_list[1])))

    plt.title(title)
    label_x = plt.xlabel(xlabel)
    plt.setp(label_x, color='r', fontsize='medium')
    label_y = plt.ylabel('Usage(%s)'%(ylabel))
    plt.setp(label_y, color='r', fontsize='medium')
    #box=ax.get_position()
    #ax.set_position()
    #ax.legend(loc='upper left',bbox_to_anchor=(1.0,0.5))
    plt.legend(loc='upper right')
    plt.savefig('%s'%(title))
    plt.show()

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

if __name__ == '__main__':
    x_list = []
    y_list = []
    m = 1
    for item in filelist:
        mem_list,gpu_list = get_nvidia_result(item)
        x,y = take_sample(mem_list,'MEM','%',m)
        #x,y = take_sample(gpu_list,'GPU','%',m)
        x_list.append(x)
        y_list.append(y)
	m += 1

    draw_plot(x_list,y_list,'MEM','Time(s)','%','MEM')
    #draw_plot(x_list,y_list,'GPU','Time(s)','%','GPU')
