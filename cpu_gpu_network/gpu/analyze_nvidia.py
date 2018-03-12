#!/usr/bin/python
#-*- coding:utf-8 -*-

# author:chunxiusun

import re

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
        print mem_1
        if re.search('/ ([0-9]+)MiB.*', line) == None:
            continue
        mem_2 = int(re.search('/ ([0-9]+)MiB.*', line).group(1))
        print mem_2
        mem_usage = mem_1 *1.0 / mem_2
        print 'mem_usage:%f' %(mem_usage)
        mem_list.append(mem_usage)
        if re.search('MiB |.* ([0-9]+)%.*|', line) == None:
            continue
        gpu_util = eval(re.search('MiB |.* ([0-9]+)%.*|', line).group(1))
        #print gpu_util
        gpu_list.append(gpu_util)

    print "################## Result ######################"
    print 'Memory-Usage Max:%f' %(max(mem_list))
    print 'Memory-Usage Min:%f' %(min(mem_list))
    print 'Memory-Usage Avg:%f' %(sum(mem_list)*1.0/len(mem_list))
    print 'GPU-Util Max:%f' %(max(gpu_list)*1.0/100)
    print 'GPU-Util Min:%f' %(min(gpu_list)*1.0/100)
    print 'GPU-Util Avg:%f' %(sum(gpu_list)*1.0/(len(gpu_list)*100.0))
    fd.close()

if __name__ == '__main__':
    get_nvidia_result('nvidia1.log')
    get_nvidia_result('nvidia2.log')
    #get_nvidia_result('./log/case3/nvidia1.log')
    #get_nvidia_result('./log/case3/nvidia2.log')
