#!/usr/bin/python
#-*- coding:utf-8 -*-
#author : chunxiusun

import os
import json
import zmq

os.system('mkdir Images')

index_file = 'index.txt'
img_dir = './Images/'
if not os.path.exists(img_dir):
    os.mkdir(img_dir)

def zmqServer():
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    #socket.bind("tcp://0.0.0.0:9800")
    #socket.setsockopt(zmq.SUBSCRIBE,'')
    #socket = context.socket(zmq.PUB)
    socket.connect("tcp://192.168.17.174:9800")

    count = 10
    while count:
        n = 0
	f = open(index_file,'a+')
        while True:
	    n = n + 1
            message = socket.recv()
	    if "name" in message:
	        n = 2  
            more = socket.getsockopt(zmq.RCVMORE)
            if more:
	        if n == 1:
		    print "ID:%s"%(message)
		    f.write('%s\n'%message)
	        if n == 2:
		    msg = eval(message)
		    img_name = msg["name"]
		    print img_name
		    timestamp = msg["timestamp"]
		    print timestamp
		    cut_board = msg["bounding-boxes"]
		    print cut_board
		    roi_x = cut_board[0]["x"]
		    roi_y = cut_board[0]["y"]
		    roi_w = cut_board[0]["w"]
		    roi_h = cut_board[0]["h"]
		    roi = "x"+str(roi_x )+"y"+str(roi_y)+"w"+str(roi_w)+"h"+str(roi_h)
		    img = img_dir+ img_name + '_' + timestamp + '_' + roi + '.jpg'
		    f.write(message)
	        if n == 3:
		    fd = open(img, 'wb')
		    fd.write(message)
		    fd.close()
		    print img
		    f.write('%s\n'%img)
            else:  
	        fd = open(img, 'wb')
	        fd.write(message)
	        fd.close()
	        print img
	        f.write('%s\n'%img)
	        print ""
	        break # Last message part
	f.close()
	count = count - 1
        #break 
        #time.sleep(1)


if __name__ == '__main__':
    zmqServer()
