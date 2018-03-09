#! /usr/bin/env python
# -*- coding: utf-8 -*-
import time,json,threading
import uuid
import grpc
import db_pb2
import db_pb2_grpc

_HOST = '192.168.2.162'
_PORT = '8041'

threadNum = 100
sendNumPerSencond = 1

class dbserverTest(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.timeCount = 0 
        self.sendCount = 1 
        self.sendAll = 1

    def grpcClient(self):
        conn = grpc.insecure_channel(_HOST + ':' + _PORT)
        client = db_pb2_grpc.DatabaseServiceStub(channel=conn)
        s = str(uuid.uuid4()).split("-")[-1]
        count = 0
        self.timeCount = int(time.time()*1000)
        while True:
            face_reid = "%s_%d"%(s,count)
            batchMetaInsert = self.BatchMetaInsert(face_reid)
            body = json.dumps(batchMetaInsert)
            #print body
            request = db_pb2.MetaExecuteRequest()
            request.Tag = 'faces'
            request.MetaOpts = 16
            request.MetaBody = body
            response = client.ExecuteMeta(request)
            print response
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

    def BatchMetaInsert(self,face_reid):
        batchMetaInsert = {}
        batchMetaInsert["Table"] = "faces"
        MultiFields = []
        lst = []
        Field = {}
        Field["ts"] = int(time.time()*1000)
        Field["sensor_id"] = "8a4ac6f4-6121-4670-80f3-a920644cb3bc"
        Field["face_id"] = str(uuid.uuid4()).split("-")[-1]
        Field["face_reid"] = face_reid
        print Field["face_id"]
        print Field["face_reid"]
        Field["feature"] = ""
        Field["confidence"] = 0.85
        Field["gender_id"] = 0
        Field["gender_confidence"] = 0
        Field["age_id"] = 0
        Field["age_confidence"] = 0
        Field["nation_id"] = 0
        Field["nation_confidence"] = 0
        Field["glass_id"] = 0
        Field["glass_confidence"] = 0
        Field["image_uri"] = "http://192.168.2.16:6001/face/image.jpg"
        Field["thumbnail_image_uri"] = "http://192.168.2.16:6001/face/p.jpg"
        Field["cutboard_image_uri"] = "http://192.168.2.16:6001/face/f.jpg"
        Field["cutboard_x"] = 210
        Field["cutboard_y"] = 15
        Field["cutboard_width"] = 302
        Field["cutboard_height"] = 315
        Field["cutboard_res_width"] = 529
        Field["cutboard_res_height"] = 503
        Field["is_warned"] = 2
        Field["status"] = 1
        for key,value in Field.iteritems():
            dic = {}
            dic["Key"] = key
            dic["Value"] = value
            lst.append(dic)
        MultiFields.append(lst)
        batchMetaInsert["MultiFields"] = MultiFields
        #print batchMetaInsert
        return batchMetaInsert

    def run(self):
        self.grpcClient()

def main():
    query_list = []
    for i in range(threadNum):                                                                                                            
        t = dbserverTest()
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
