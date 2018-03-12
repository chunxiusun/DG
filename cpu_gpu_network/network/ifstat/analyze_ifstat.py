#!/usr/bin/python
#-*- coding:utf-8 -*-
# author:chunxiusun

import os
import numpy as np
import matplotlib.pyplot as plt

os.system('rm sta.txt')

f_in = 'if_stat.log'
f_out = 'sta.txt'
unit = 'M' #K,M,G,T
N = 10

def get_ifstat_result(filename):
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
    return in_list,out_list

def take_sample(listname,fname,unit):
    y = []
    for i in range(0,len(listname),N):
        y.append(listname[i])
    #x = np.arange(0,len(y))
    x = np.arange(0,len(listname),N)

    fd_out = open(f_out,'a')
    fd_out.write("################## %s ######################\r\n"%(fname))
    fd_out.write('%s Max:%0.2f%s\r\n' %(fname,max(y),unit))
    fd_out.write('%s Min:%0.2f%s\r\n' %(fname,min(y),unit))
    fd_out.write('%s Avg:%0.2f%s\r\n' %(fname,sum(y)/len(y),unit))
    fd_out.write('\r\n')
    fd_out.close()
    print "################## %s ######################"%(fname)
    print '%s Max:%0.2f%s' %(fname,max(y),unit)
    print '%s Min:%0.2f%s' %(fname,min(y),unit)
    print '%s Avg:%0.2f%s' %(fname,sum(y)/len(y),unit)
    
    return x,y

def draw_plot(x_list,y_list,title,xlabel,ylabel):
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

    line1 = plt.plot(x_list[0],y_list[0],linewidth=1.0,label='Incoming')
    line2 = plt.plot(x_list[1],y_list[1],linewidth=1.0,label='Outgoing')

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
    label_y = plt.ylabel('Rate of flow(%s)'%(ylabel))
    plt.setp(label_y, color='r', fontsize='medium')
    #box=ax.get_position()
    #ax.set_position()
    #ax.legend(loc='upper left',bbox_to_anchor=(1.0,0.5))
    plt.legend(loc='upper left')
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

def analyze_unit(listname):
    ls = []
    for item in listname:
        if unit == 'K':
            data = eval(item)
        if unit == 'M':
            data = eval(item)/1024
        if unit == 'G':
            data = eval(item)/1024/1024
        if unit == 'T':
            data = eval(item)/1024/1024/1024
        ls.append(data)
    return ls

if __name__ == '__main__':
    x_list = []
    y_list = []
    in_list,out_list = get_ifstat_result(f_in)

    x,y = take_sample(in_list,'Incoming','%sB/s'%(unit))
    x_list.append(x),y_list.append(y)
    x,y = take_sample(out_list,'Outgoing','%sB/s'%(unit))
    x_list.append(x),y_list.append(y)

    draw_plot(x_list,y_list,'Network','Time(s)','%sB/s'%(unit))
