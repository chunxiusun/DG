#!/usr/bin/env python
# -*- coding: utf8 -*-

# author : chunxiusun

import commands, os,time
from config import *

os.system('rm -r ./log')
os.system('mkdir ./log')

def get_pid(keyWord):
    pid_cmd = "ps -ef|grep \"%s\"|grep -v grep |awk  '{print $2}'" %(keyWord)
    #print pid_cmd
    pids_return = commands.getstatusoutput(pid_cmd)
    #print pids_return
    #print pids_return[1]
    if pids_return[0] != 0:
	print "get pid error,exit...."
	return
    pids = pids_return[1].split("\n")
    #print len(pids)
    return pids

def get_top_log(keyWord):
    pids = get_pid(keyWord)
    for pid in pids:
	keyWord_temp = keyWord.replace(" ","_")
	top_cmd = "top -p %s -b -d %d -n %d >> ./log/%s.log.%s&" \
                   %(pid, INTERVAL, MONITER_TIME, keyWord_temp, pid)
	print "top_cmd:"+top_cmd
	print "stat CPU start"
	os.system(top_cmd)
	print "stat CPU complete"

def get_gpu_log():
    timelen = MONITER_TIME
    print "stat GPU start"
    while timelen:
	print "stat GPU ..."
	os.system('nvidia-smi > tmp.txt')
	os.system("sed -n '9p' tmp.txt >> ./log/nvidia1.log")
	os.system("sed -n '12p' tmp.txt >> ./log/nvidia2.log")
	os.system("sed -n '15p' tmp.txt >> ./log/nvidia3.log")
	os.system("sed -n '18p' tmp.txt >> ./log/nvidia4.log")
	time.sleep(INTERVAL)
	timelen = timelen - INTERVAL
    print "stat GPU complete"

def get_network_log():
    number = MONITER_TIME/INTERVAL
    print "stat Network times:%s"%(number)
    print "stat Network start"
    network_cmd = "ifstat -tn -i %s -a %d %d >> ./log/if_stat.log" \
                  %(network_interface, INTERVAL, number)
    print "network_cmd:"+network_cmd
    os.system(network_cmd)
    print "stat Network complete"

def run():
    if CPU_FLAG:
	get_top_log(MATRIX)
	#get_top_log('mxadaptor')
    if GPU_FLAG:
	get_gpu_log()
    if NETWORK_FLAG:
	get_network_log()

if __name__ == '__main__':
    run()
