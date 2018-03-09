#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os,time
#from kafka import KafkaConsumer
from kafka import KafkaClient,SimpleConsumer

kafkaServer = "192.168.2.19"
kafkaPort = "9092"
kafkaTopic = "face-importer"

dirName = "./data/"
fileName = "libraf"

#if os.path.exists(dirName):
 #   os.system("rm -r %s"%dirName)
os.system("mkdir %s"%dirName)

def kafkaConsumer():
    #consumer = KafkaConsumer("%s"%(kafkaTopic),bootstrap_servers=['%s:%s'%(kafkaServer,kafkaPort)])
    kafka = KafkaClient("%s:%s"%(kafkaServer,kafkaPort))
    consumer = SimpleConsumer(kafka,"sun",kafkaTopic)
    count = 1
    for msg in consumer:
        #print msg.message.value
        filename = "%s%s_%d.txt"%(dirName,fileName,count)
        fd = open(filename,'w')
        fd.write(msg.message.value)
        print type(msg.message.value)
        fd.close()
        count += 1
        time.sleep(1)
        #break
    exit()


if __name__ == '__main__':
    kafkaConsumer()
