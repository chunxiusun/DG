#!/usr/bin/python
#coding:utf-8

# author:chunxiusun

import os
import numpy as np
import matplotlib.pyplot as plt

#os.system('rm sta.txt')

N =10
res_unit = 'M'#K,M,G,T
f_out = 'sta.txt'

#filelist = ['./matrix_apps.log.131605','./matrix_apps.log.93634','./mxadaptor.log.93628','./mxadaptor.log.93633']
#filelist = ['./matrix_apps.log.131605','./matrix_apps.log.93634']
filelist = ['./log/mxadaptor.log.93628','./log/mxadaptor.log.93633']

def get_top_result(fileName):
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
    #print res_list
    fd.close()
    return cpu_list,mem_list,res_list

def take_sample(listname,title,unit):
    y = []
    for i in range(0,len(listname),N):
	y.append(listname[i])
    #x = np.arange(0,len(y))
    x = np.arange(0,len(listname),N)

    fd_out = open(f_out,'a')
    fd_out.write("################## %s ######################\r\n"%(fname))
    fd_out.write('%s %s Max:%0.2f%s\r\n' %(fname,title,max(y),unit))
    fd_out.write('%s %s Min:%0.2f%s\r\n' %(fname,title,min(y),unit))
    fd_out.write('%s %s Avg:%0.2f%s\r\n' %(fname,title,sum(y)/len(y),unit))
    fd_out.write('\r\n')
    fd_out.close()
    print "################## %s ######################"%(fname)
    print '%s %s Max:%0.2f%s' %(fname,title,max(y),unit)
    print '%s %s Min:%0.2f%s' %(fname,title,min(y),unit)
    print '%s %s Avg:%0.2f%s' %(fname,title,sum(y)/len(y),unit)
    
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
    plt.savefig('%s-%s'%(label,title))
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

if __name__ == '__main__':
    x_list = []
    y_list = []
    i = 1
    for item in filelist:
	m = item.split('/')[-1].split('.')[0]
	fname = m+'_'+str(i)
	i = i+1

	cpu_list,mem_list,res_list = get_top_result(item)

	#x,y = take_sample(cpu_list,'CPU','%')
	#x,y = take_sample(mem_list,'MEM','%')
	x,y = take_sample(res_list,'RES','%sB'%(res_unit))
	x_list.append(x)
	y_list.append(y)

    #draw_plot(x_list,y_list,'CPU','Time(s)','%',m)
    #draw_plot(x_list,y_list,'MEM','Time(s)','%',m)
    draw_plot(x_list,y_list,'RES','Time(s)','%sB'%(res_unit.upper()),m)

