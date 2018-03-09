#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os,datetime,time,threading
import vsd_pb2
import uuid
import hashlib
from kafka import KafkaClient
from kafka.producer import SimpleProducer
from kafka.errors import KafkaError

threadNum = 1
sendNumPerSencond = 1
#proto
fileName = "./data/vsd.txt"
#kafka
kafkaServer = "192.168.2.222:9092"
kafkaTopic = "face-topic"
sensorIdFile = "sensor_id.txt"
Feature = "mreQPZqzOb1zMF+98Qy1vMIrOLx6v4K92cAgPZUniby82uI86Cb6PNnCC73cVOe94ulhPMbKRD0CsqG7TMvdPVaqpjsJOiG99IOmPaNGaD1a2E+7MggrPT6kGz3RpEw9UN5CvUhGAr1rqGI9m+NRvNv0z7wW4Vw9zIEyPQ6Bsj0zc8q9HwHgO85f9zxQ/ce9BXZ2vcXoAb2xKru79luoPAuyR72Qh/68uSbdvZrUUzwajCA9aRu2PHRaJz3tPtG9mHHAu+s0mj1k9xu7khYtPYVLMT30I409kLpyvVcMLz2dem69GKzJvay0RD2gPPs8DbwxvSiQCTtZ+zG9JLEkvR7Opb0iYbQ9eYcfPhZF4r2r9T+9XIqUPdF/Oj2eLtc9+1oYPqo/RT1J7n28CGi9vbVzCrzDL4g9jnHzPLKmrTs/iLc638aRPDnfvz21PeK8rLjqPWMpJ73StUA9wmSDvOcgE7ukz3U8vBkyvLNMRb3FJkG9++nkvWLPZD1ck4+9tJzTPdSA27z99Vg87USpvYhtsbxBryS8gRitPTISNT2ljhm9quKaPWGxCT18pRi8FBJ2Oni+W76KWvM9dbHAvCtrcL3yeLA9wstsvPKePD18g5A8AokNvS/KM72CxA29deRdvH8sgjxKgbc9S/EFvnomqD14un09cu6nvX812jxRCCI8Phu/vJwSDL3dCUS9zp+YPeoBgryVuXU9QkScvfWsnLwnRYo9CojIvWU6rDp82A49YTqpPHu12zuwogs8Ax6nvWlRfb1PUkY9cHryPBJvmb0rgtS8bLeuvUrOn7wKyS48LzxWPe78qTv8+s+7GbJBvuHLwryT3wE+J0sVPSkAtTyGh9I9DDhlvRLW9DyNA/a85JGJu/eqoz1JHYS9Wh7QPCn+iLxG3Re90WKJvVIoqj16KzW9AMlKPLcbujtDHba84LYDPCNjnzx1A/Y8XaXTPa/X1D0DaIa7GQzkPPlx87wd//Y8X6c9vry1LrzL5wm942iyvDOhXr1QXJQ9EbusvUOYGLxRcHe9fogjO/Y/H73r/ea7NmgVPSchA7ylBMi9mWutPHZnDj3id6i9aoIDPT1CBr2EmwO8K/wkvW3GIz4Ptnk96/PMvJAc0jzJaJY9zK4mvSC38Lw+A/e7MCZIPewMk72dt4q81WS/vdgSEj4k6iq9v2BuPQpi0zztJ+O9eHhPvRbDkD1ztg4+IJCovCDocL3UL6G7dzW3PY5zkj2cnuO9q0kSvQgbgTlVHZ29bN/BPdPjLD1q4h28cVqePL340j1uK5G94dTsvHu0hz2MeFG8B+u+PZbVlD2L8aS9X+xnvVeGXzxCWaQ9pLQqvfNclr0cyoI9uTsMPQ=="

class Test(threading.Thread):
    def __init__(self,result):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.result = result
        self.timeCount = 0
        self.sendCount = 1
        self.sendAll = 1

    def kafkaProducer(self):
        client = KafkaClient(hosts=[kafkaServer], timeout=30)  
        producer = SimpleProducer(client, async=False)
        count = 0
        s = str(uuid.uuid4())
        #print s
        self.timeCount = int(time.time()*1000)
        while True:
            self.result.Meta.Timestamp = int(time.time())*1000
            self.result.Id = str(uuid.uuid4())
            self.result.Image.Id = "%s_%d"%(s.split("-")[-1],count)
            self.result.ThumbnailImage.Id = "%s_%d"%(s.split("-")[-1],count)
            self.result.Objects[0].Id = str(uuid.uuid1()).split("-")[0]
            self.result.Objects[0].ReId = "%s_%d"%(s.split("-")[0],count)
            self.result.Objects[0].QualityOK = True
            data = self.result.SerializeToString()
            producer.send_messages(kafkaTopic, data)
            print datetime.datetime.now()
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
                else:
                    self.timeCount = int(time.time()*1000)
                    self.sendCount = 0
                    self.sendAll = self.sendAll + 1
            self.sendCount = self.sendCount + 1 
            count += 1
            break
        producer.stop()
        client.close()

    def run(self):                                                                                                                         
        self.kafkaProducer()


def dealProto():
    result = vsd_pb2.RecResult()
    fd = open(fileName,'r')
    data = fd.read()
    fd.close()
    result.ParseFromString(data)
    result.Image.URL = "http://192.168.2.16:6001/deepface/image.jpg"
    result.Image.Width = 529 
    result.Image.Height = 503
    result.ThumbnailImage.URL = "http://192.168.2.16:6001/deepface/p.jpg"
    result.ThumbnailImage.Width = 528 
    result.ThumbnailImage.Height = 502
    result.Objects[0].URL = "http://192.168.2.16:6001/deepface/f.jpg"
    result.Objects[0].X = 210
    result.Objects[0].Y = 15
    result.Objects[0].RelativeWidth = 302                                                                                          
    result.Objects[0].RelativeHeight = 315
    result.Objects[0].AbsoluteWidth = 302
    result.Objects[0].AbsoluteHeight = 315
    result.Objects[0].Feature = Feature
    #print result.Objects
    return result

def main():
    obj = dealProto()                                                                                                                                 
    query_list = []
    fd = open(sensorIdFile,'r')
    for line in fd.readlines():
        #sensor_id = line.strip()
        sensor_id = "97bdbe6a-d20b-4f61-bc14-1262fb082dbb"
        #print sensor_id
        obj.Meta.SensorId = sensor_id                                                                                     
    #for i in range(threadNum):                                                                                                            
        t = Test(obj)                                                                                                                      
        query_list.append(t)
        break                                                                                                               
    #for i in range(len(fd.readlines())):                                                                                                      
    for i in range(threadNum):                                                                                                            
        query_list[i].start()                                                                                                              
    
    fd.close()                                                                                                                                       
    #for i in range(threadNum):                                                                                                            
        #query_list[i].join()

    while True:
        time.sleep(36000)
    sys.exit(0)

if __name__ == '__main__':
    main()
