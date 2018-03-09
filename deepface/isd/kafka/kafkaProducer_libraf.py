#!/usr/bin/env python
#-*- coding:utf-8 -*-

import time,threading
import uuid
from kafka import KafkaClient
from kafka.producer import SimpleProducer
from kafka.errors import KafkaError
import importer_pb2
import matrix_pb2

IP = "192.168.2.19"
PORT = "9092"
kafkaTopic = "face-importer"

sensorId = "1dd5522c-e27e-4223-b9a7-0bfd707baea4"
fileName = "./data/libraf.txt"
threadNum = 1
sendNumPerSencond = 1


class IsdTest(threading.Thread):
    def __init__(self,result):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.result = result
        self.timeCount = 0
        self.sendCount = 1
        self.sendAll = 1

    def kafkaProducer(self):
        client = KafkaClient(hosts=["%s:%s"%(IP,PORT)], timeout=30)  
        producer = SimpleProducer(client, async=False)
        self.timeCount = int(time.time()*1000)
        while True:
            self.result.RecResult.Id = str(uuid.uuid1())
            self.result.RecResult.Meta.Timestamp = int(time.time()*1000)
            self.result.RecResult.Image.Id = str(uuid.uuid1())
            self.result.RecResult.Objects[0].Id = str(uuid.uuid1())
            self.result.RecResult.Objects[1].Id = str(uuid.uuid1())
            data = self.result.SerializeToString()
            producer.send_messages(kafkaTopic, data)
            print "send count:%s"%self.sendCount
            if self.sendCount == sendNumPerSencond:
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
            #break 
        producer.stop()
        client.close()

    def run(self):                                                                                                                         
        self.kafkaProducer()

def dealProto():
    importer_result = importer_pb2.ImporterResult()
    fd = open(fileName,'r')
    data = fd.read()
    fd.close()
    importer_result.ParseFromString(data)
    importer_result.SensorFilter.QualityThreshold = 0.3
    importer_result.SensorFilter.IsRemoveDuplication = False
    #print importer_result.RecResult.Objects
    importer_result.RecResult.Meta.SensorId = sensorId
    importer_result.RecResult.Image.URL = "http://192.168.2.16:6001/face/image.jpg"
    importer_result.RecResult.Image.Width = 529
    importer_result.RecResult.Image.Height = 503
    importer_result.RecResult.Objects[0].QualityOK = True
    importer_result.RecResult.Objects[0].URL = "http://192.168.2.16:6001/face/p.jpg"
    importer_result.RecResult.Objects[1].QualityOK = True
    importer_result.RecResult.Objects[1].URL = "http://192.168.2.16:6001/face/f.jpg"
    importer_result.RecResult.Objects[1].X = 210
    importer_result.RecResult.Objects[1].Y = 15
    importer_result.RecResult.Objects[1].RelativeWidth = 302
    importer_result.RecResult.Objects[1].RelativeHeight = 315
    importer_result.RecResult.Objects[1].AbsoluteWidth = 302
    importer_result.RecResult.Objects[1].AbsoluteHeight = 315
    
    return importer_result
    
def main():
    obj = dealProto()                                                                                                                                 
    query_list = []                                                                                                                        
    for i in range(threadNum):                                                                                                            
        t = IsdTest(obj)                                                                                                                      
        query_list.append(t)                                                                                                               
                                                                                                                                           
    for i in range(threadNum):                                                                                                            
        query_list[i].start()                                                                                                              
                                                                                                                                           
    #for i in range(threadNum):                                                                                                            
        #query_list[i].join()

    while True:
        time.sleep(36000)
    sys.exit(0)

if __name__ == '__main__':
    main()
