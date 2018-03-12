#!/usr/bin/env python
# -*- coding: utf8 -*-

# author : chunxiusun

import os,re
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

START_PROC_FLAG = True
CAPTURED_ADD_FEATURE_PROC_FLAG = True
CAPTURED_INFORM_PROC_FLAG = True
CAPTURED_STORAGE_PROC_FLAG = True
WARNED_INFORM_PROC_FLAG = True
WARNED_STORAGE_PROC_FLAG = True
DRAW_PIC = True

#analyze
filelist = ["START_PROC.txt","CAPTURED_ADD_FEATURE_PROC.txt","CAPTURED_INFORM_PROC.txt",\
            "CAPTURED_STORAGE_PROC.txt","WARNED_INFORM_PROC.txt","WARNED_STORAGE_PROC.txt"]

#draw
N =30

def get_count_result(fileName,fname):
    y = []
    x = []
    fd = open(fileName,'r')
    fd_split = fd.read().splitlines()
    n = 1
    count = 0
    row = 0
    for line in fd_split:
        row += 1
        count += eval(line.strip().split()[0])
        t = int(line.strip().split()[1].replace(":",""))
        #print len(fd_split)
        if row == len(fd_split):
            c = int(count/n)
            y.append(c)
            break
        if n == N:
            c = int(count/n)
            y.append(c)
            n = 1
            count = 0
            continue
        if n == 1:
            x.append(t)
        n += 1
    print y
    print x
    #x = np.arange(0,len(y))
        
    print "################## %s ######################"%(fname)
    print '%s Max:%0.2f%s' %(fname,max(y),'%')
    print '%s Min:%0.2f%s' %(fname,min(y),'%')
    print '%s Avg:%0.2f%s' %(fname,sum(y)/len(y),'%')
    print ''
    return y,x


def draw_plot(x_list,y_list,title,xlabel,ylabel):
    global plt
    y_max = 0
    y_min = 1000000000000
    for lst in y_list:
        if max(lst) >= y_max:
            y_max = max(lst)
        if min(lst) <= y_min:
            y_min = min(lst)

    x_max = 0
    x_min = 100000000000
    for lst in x_list:
        if max(lst) >= x_max:
            x_max = max(lst)
        if min(lst) <= x_min:
            x_min = min(lst)

    print x_max,x_min  
    #fig= plt.figure()
    #ax = plt.subplot(111)
    plt.ylim(y_min/1.1,y_max*1.1)
    plt.xlim(x_min,x_max)
    lst = ["START_PROC","CAPTURED_ADD_FEATURE_PROC","CAPTURED_INFORM_PROC","CAPTURED_STORAGE_PROC","WARNED_INFORM_PROC","WARNED_STORAGE_PROC"]
    for i in range(0,len(y_list)):
        line = plt.plot(x_list[i],y_list[i],linewidth=1.0,label=lst[i])
        #plt.axhline(y=sum(y_list[i])/len(y_list[i]),color='r')
        #plt.text(0,sum(y_list[i])/len(y_list[i]), r'avg:%0.2f'%(sum(y_list[i])/len(y_list[i])))
        plt.annotate('%d'%(max(y_list[i])), xy = (get_x_max(x_list[i],y_list[i]), max(y_list[i])))
        plt.annotate('%d'%(min(y_list[i])), xy = (get_x_min(x_list[i],y_list[i]), min(y_list[i])))

    plt.title(title)
    label_x = plt.xlabel(xlabel)
    plt.setp(label_x, color='r', fontsize='medium')
    label_y = plt.ylabel('Count/s')
    plt.setp(label_y, color='r', fontsize='medium')
    #box=ax.get_position()
    #ax.set_position()
    #ax.legend(loc='upper left',bbox_to_anchor=(1.0,0.5))
    plt.legend(loc='upper left')
    plt.savefig('%s'%(title))
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


def run():
    x_list = []
    y_list = []
    for item in filelist:
	fname = item.split('.')[0]
	y,x = get_count_result(item,fname)
	x_list.append(x)
	y_list.append(y)
    if DRAW_PIC:
	draw_plot(x_list,y_list,'bingo','Time','%')

if __name__ == '__main__':
    run()
