#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
from kafka import KafkaConsumer

kafkaServer = "192.168.2.19"
kafkaPort = "9092"
kafkaTopic = "face-topic"

dirName = "./data/"
fileName = "vsd"

#if os.path.exists(dirName):
 #   os.system("rm -r %s"%dirName)
os.system("mkdir %s"%dirName)

def kafkaConsumer():
    consumer = KafkaConsumer("%s"%(kafkaTopic),bootstrap_servers=['%s:%s'%(kafkaServer,kafkaPort)])
    count = 1
    for msg in consumer:
        filename = "%s%s_%d.txt"%(dirName,fileName,count)
        fd = open(filename,'w')
        fd.write(msg.value)
        print type(msg.value)
        fd.close()
        count += 1
        break
    exit()


if __name__ == '__main__':
    kafkaConsumer()
