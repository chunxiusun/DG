#!/usr/bin/python
#coding:utf-8

# author:chunxiusun

import os
import numpy as np
import matplotlib.pyplot as plt

#os.system('rm sta.txt')

N = 10
res_unit = 'k'
#fname = 'mxadaptor_2'
flname = 'sta.txt'

filelist = ['./output/matrix_apps.log.131605','./output/matrix_apps.log.93634','./output/mxadaptor.log.93628','./output/mxadaptor.log.93633']
#filelist = ['./log/mxadaptor.log.93628','./log/mxadaptor.log.93628']

def get_top_result(fileName):
    global res_list,mem_list,cpu_list
    res_ls = []
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
	    res_ls.append(res)
	    cpu_list.append(cpu)
            mem_list.append(mem)
    res_list = analyze_RES(res_ls)
    #print res_list
    fd.close()

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

	if res_unit == 'm':
	    data = value/1024
	if res_unit == 'g':
	    data = value/1024/1024
	if res_unit == 't':
	    data = value/1024/1024/1024
	if res_unit == 'k':
	    data = value

	ls.append(data)
    return ls

def draw_plot(listname,title,xlabel,ylabel):
    y = []
    for i in range(0,len(listname),N):
	y.append(listname[i])
    #x = np.arange(0,len(y))
    x = np.arange(0,len(listname),N)
    for i in range(0,len(y)):
	if y[i] == max(y):
	    y_max = y[i]
	    x_max = x[i]
	if y[i] == min(y):
	    y_min = y[i]
	    x_min = x[i]
    y_avg = sum(y)/len(y)

    fd_out = open(flname,'a')
    fd_out.write("################## Result ######################\r\n")
    fd_out.write('%s %s Max:%0.2f%s\r\n' %(fname,title,y_max,ylabel))
    fd_out.write('%s %s Min:%0.2f%s\r\n' %(fname,title,y_min,ylabel))
    fd_out.write('%s %s Avg:%0.2f%s\r\n' %(fname,title,y_avg,ylabel))
    fd_out.write('\r\n')
    fd_out.close()
    print "################## Result ######################"
    print '%s %s Max:%0.2f%s' %(fname,title,y_max,ylabel)
    print '%s %s Min:%0.2f%s' %(fname,title,y_min,ylabel)
    print '%s %s Avg:%0.2f%s' %(fname,title,y_avg,ylabel)

    plt.ylim(0,y_max*1.2)
    line = plt.plot(x,y,linewidth=1.0)
    #lmax = plt.axhline(y=y_max, color='b')
    #lmin = plt.axhline(y=y_min, color='b')
    #lavg = plt.axhline(y=y_avg,color='r')
    #plt.text(0,y_max, r'%f'%(y_max))
    plt.text(0,y_avg, r'avg:%0.2f'%(y_avg))
    plt.annotate('max:%0.2f'%(y_max), xy = (x_max, y_max))
    plt.annotate('min:%0.2f'%(y_min), xy = (x_min, y_min))
    plt.title(title)
    label_x = plt.xlabel(xlabel)
    plt.setp(label_x, color='r', fontsize='medium')
    label_y = plt.ylabel('Usage(%s)'%(ylabel))
    plt.setp(label_y, color='r', fontsize='medium')
    #plt = legend()
    plt.savefig('%s-%s'%(fname,title))
    plt.show()

if __name__ == '__main__':
    i = 1
    for item in filelist:
	get_top_result(item)

	m = item.split('/')[-1].split('.')
	fname = m[0]+'_'+str(i)
	i = i+1
	draw_plot(cpu_list,'CPU','Time(s)','%')
	draw_plot(mem_list,'MEM','Time(s)','%')
	draw_plot(res_list,'RES','Time(s)','kb')
    #get_top_result('./matrix_apps.log.131605')
    #get_top_result('./matrix_apps.log.93634')
    #get_top_result('./mxadaptor.log.93628')
    #get_top_result('./mxadaptor.log.93633')

    #draw_plot(cpu_list,'CPU','Time(s)','Utilization rate(%)')
    #draw_plot(mem_list,'MEM','Time(s)','Utilization rate(%)')
    #draw_plot(res_list,'RES','Time(s)','Usage(kb)')
