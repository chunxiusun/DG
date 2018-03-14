#!/usr/bin/env python
# -*- coding: utf8 -*-

# author : chunxiusun

import os,re
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from config import *

def get_result(fileName,m):
    fd = open(fileName, 'r')
    count_list = []
    x = []
    for line in fd.readlines():
        line = line.strip()
	if line == '':
	    continue
	count = eval(line.split()[0])
	#print count
        count_list.append(count)
    fd.close()
    if DRAW_PIC:
	count_list,x = take_sample(count_list)
    print "################## %s ######################"%(m)
    print '%s Max:%0.2f' %(m,max(count_list))
    print '%s Min:%0.2f' %(m,min(count_list))
    print '%s Avg:%0.2f' %(m,sum(count_list)/len(count_list))
    print ''
    return count_list,x

def draw_plot(x_list,y_list,title,x,xlabel,y,ylabel,index):
    global plt
    y_max = max(y_list[0])
    y_min = min(y_list[0])
  
    #fig= plt.figure()
    #ax = plt.subplot(111)
    plt.ylim(y_min/1.2,y_max*1.2)
    plt.xlim(0,x_list[0][-1]*1.2)
    line1 = plt.plot(x_list[0],y_list[0],linewidth=1.0,label=title+'_'+str(index))
    #line2 = plt.plot(x_list[1],y_list[1],linewidth=1.0,label=label+'_2')

    plt.axhline(y=sum(y_list[0])/len(y_list[0]),color='r')
    #plt.axhline(y=sum(y_list[1])/len(y_list[1]),color='y')
    plt.text(0,sum(y_list[0])/len(y_list[0]), r'avg:%0.2f'%(int(sum(y_list[0])/len(y_list[0]))))
    #plt.text(0,sum(y_list[1])/len(y_list[1]), r'avg:%0.2f'%(sum(y_list[1])/len(y_list[1])))

    plt.annotate('max:%0.2f'%(max(y_list[0])), xy = (get_x_max(x_list[0],y_list[0]), max(y_list[0])))
    #plt.annotate('max:%0.2f'%(max(y_list[1])), xy = (get_x_max(x_list[1],y_list[1]), max(y_list[1])))
    plt.annotate('min:%0.2f'%(min(y_list[0])), xy = (get_x_min(x_list[0],y_list[0]), min(y_list[0])))
    #plt.annotate('min:%0.2f'%(min(y_list[1])), xy = (get_x_min(x_list[1],y_list[1]), min(y_list[1])))

    plt.title(title)
    label_x = plt.xlabel('%s(%s)'%(x,xlabel))
    plt.setp(label_x, color='r', fontsize='medium')
    label_y = plt.ylabel('%s(%s)'%(y,ylabel))
    plt.setp(label_y, color='r', fontsize='medium')
    #box=ax.get_position()
    #ax.set_position()
    #ax.legend(loc='upper left',bbox_to_anchor=(1.0,0.5))
    plt.legend(loc='upper left')
    #print index
    plt.savefig('%s_%s'%(title,index))
    #plt.show()
    #plt.draw()
    plt.clf()
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
    if DETECT_FLAG:
	i = 1
	for item in detect_filelist:
	    x_list = []
	    detect_y = []
	    #m = item.split('/')[-1].split('.')[0]
	    fname = "FaceDetectProcessor"
	    detect_list,x = get_result(item,fname)
	    x_list.append(x)
	    detect_y.append(detect_list)
	    if DRAW_PIC:
	        draw_plot(x_list,detect_y,'FaceDetectProcessor','Count','number','Time per batch','ms',i)
	    i = i+1
    if ALIGN_FLAG:                                                                                                                        
        i = 1                                                                                                                              
        for item in align_filelist:                                                                                                       
            x_list = []                                                                                                                    
            align_y = []                                                                                                                   
            #m = item.split('/')[-1].split('.')[0]                                                                                         
            fname = "FaceAlignmentProcessor"                                                                                                               
            align_list,x = get_result(item,fname)
            x_list.append(x)                                                                                                               
            align_y.append(align_list)
            if DRAW_PIC:                                                                                                                   
                draw_plot(x_list,align_y,'FaceAlignmentProcessor','Count','number','Time per batch','ms',i)
            i = i+1 
    if QUALITY_FLAG: 
        i = 1
        for item in quality_filelist: 
            x_list = []
            quality_y = []
            #m = item.split('/')[-1].split('.')[0]                                                                                         
            fname = "FaceQualityProcessor"
            quality_list,x = get_result(item,fname)
            x_list.append(x)                                                                                                               
            quality_y.append(quality_list)
            if DRAW_PIC:
                draw_plot(x_list,quality_y,'FaceQualityProcessor','Count','number','Time per batch','ms',i)
            i = i+1

if __name__ == '__main__':
    run()
