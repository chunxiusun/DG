#!/usr/bin/python
#-*- coding:utf-8 -*-
#author : chunxiusun

import os,sys
import time
import json
import zmq
import threading

from logger import logger

index_file = 'index_UN1607150037.txt'
face_num = 5
thread_num = 2
send_num = 10

class IsdTest(threading.Thread):
    def __init__(self):
	threading.Thread.__init__(self)
        self.setDaemon(True)
	self.timeCount = 0
	self.sendCount = 1
	self.sendAll = 1

    def zmqClient(self):
	global send_num
        context = zmq.Context()
        socket1 = context.socket(zmq.PUB)
        socket1.connect("tcp://192.168.2.22:9900")
        time.sleep(5)

	row_num = (face_num+1)*2+1
	self.timeCount = int(time.time()*1000)
	while True:
	    begin = int(time.time()*1000)
            row = 0
    	    fdr = open(index_file,'r')
    	    for line in fdr.readlines():
        	line = line.strip()
		logger.info("line:%s"%line)
        	row = row + 1
		if 'timestamp' in line:
	    	    data_dict = eval(line)
	    	    data_dict["timestamp"] = str(int(time.time()*1000000))
	    	    data = json.dumps(data_dict)
	    	    logger.info("send ImageInfo:%s"%data)
        	elif 'Images' in line:
	    	    fdr1 = open(line,'rb')
	    	    data = fdr1.read()
	    	    fdr1.close()
        	else:
	    	    data = line
        	if row != row_num:
            	    socket1.send(data, zmq.SNDMORE)
        	else:
	    	    socket1.send(data)
		    break
    	    fdr.close()
	    print "send count:%s"%self.sendCount
	    if self.sendCount == (send_num/thread_num):
		now_time = int(time.time()*1000)
		elapse = now_time - self.timeCount
		print "elapse:%sms"%elapse
		if elapse <= 1000:
		    sleep_time = (1000 - elapse)*1.0/1000
		    print "sleep times:%ss"%sleep_time
		    time.sleep(sleep_time)
		    self.timeCount = int(time.time()*1000)
		    self.sendCount = 0
		    print "send All:%s"%self.sendAll
		    self.sendAll = self.sendAll + 1
		    #break
	    self.sendCount = self.sendCount + 1
	    #end = int(time.time()*1000)
	    #elapse = end - begin
	    #print elapse
	    #if (end - time_count) >= 1000:
		#break
	    #time.sleep(2)
	    #break

    def run(self):
	self.zmqClient()

def run():
    query_list = []
    for i in range(thread_num):
	t = IsdTest()
	query_list.append(t)

    for i in range(thread_num):
	query_list[i].start()

    #for i in range(thread_num):
	#query_list[i].join()
    while True:
        time.sleep(36000)
    sys.exit(0)
    
if __name__ == '__main__':
    run()
