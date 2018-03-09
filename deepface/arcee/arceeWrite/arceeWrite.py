#!/usr/bin/env python
#-*- coding:utf-8 -*-

import requests,json
import base64
import datetime,time,threading
import signal

IP = "192.168.2.19"
PORT = "8501"

IMAGE = "image.jpg"

threadNum = 100
Interval = 5

stat = dict(
     countNum = 0,
     countNumAll = 0,
     countTimeAll = 0,
    
     httpCode = {}, 
     httpCodeAll = {}, 
     requestCount = 0,
     requestCountAll = 0,
     requestTime = 0.0,
     requestTimeAll = 0.0
)

class ArceeTest(threading.Thread):
    def __init__(self,k):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.k = k

    def get_fids(self):
        url = "http://%s:%s/api/fids"%(IP,PORT)
        image = open(IMAGE,'r').read()
        bs = base64.b64encode(image)
        n = 1
        while True:
            key = "%s_%d"%(self.k,n)
            data = {key:bs}
            begin = int(time.time()*1000)
            r = requests.post(url,data=json.dumps(data))
            end = int(time.time()*1000)
            stat["countNum"] += 1
            r_time = end - begin
            r_code = r.status_code
            if r_code not in stat["httpCode"]:                                                                                               
                stat["httpCode"][r_code] = 0                                                                                                 
            stat["httpCode"][r_code] += 1                                                                                                    
            if r_code != 200:
                print "http_code:%s" % r_code                                                                                          
                return
            stat["requestTime"] += r_time                                                                                                    
            stat["requestCount"] += 1
            n += 1
         
    def run(self):
        self.get_fids()

class StatThread(threading.Thread):                                                                                                        
    def __init__(self):                                                                                                                    
        threading.Thread.__init__(self)                                                                                                    
        self.setDaemon(True)

    def DealStat(self):                                                                                                                    
        # save stats                                                                                                                       
        self.countNum = stat["countNum"]                                                                                                   
        self.httpCode = stat["httpCode"]                                                                                               
        self.requestCount = stat["requestCount"]                                                                                       
        self.requestTime = stat["requestTime"]

        # reset stats                                                                                                                      
        stat["countNum"] = 0                                                                                                               
        stat["httpCode"] = {}                                                                                                            
        stat["requestCount"] = 0                                                                                                         
        stat["requestTime"] = 0.0

        #count all                                                                                                                         
        stat["countNumAll"] += self.countNum
        stat["countTimeAll"] += Interval                                                                                               
        stat["httpCodeAll"] = self.dealDict(self.httpCode,stat["httpCodeAll"])                                                       
        stat["requestCountAll"] += self.requestCount                                                                                   
        stat["requestTimeAll"] += self.requestTime

    def dealDict(self,dict1,dict2):                                                                                                        
        for key in dict1:                                                                                                                  
            if key not in dict2:                                                                                                           
                dict2[key] = 0                                                                                                             
            dict2[key] += dict1[key]                                                                                                       
        return dict2

    def StatInfo(self,countNum,httpCode,requestCount,requestTime,countTime):                                                                               
        avg_requestTime = requestTime*1.0 / requestCount                                                                             
                                                                                                                                           
        statInfo = "### Count Num:%d\n"\
                   "### Requests Count:%d, avg_time:%0.2fms\n"\
                   "### Count Interval:%d\n"\
                   "### Count Time:%d\n"\
                   "httpCode:  \n"%(countNum,                                  
                   requestCount,avg_requestTime,Interval,countTime)                     
                                                                                                                                           
        httpcode_list = []                                                                                                                 
        for codedict in [httpCode]:                                                         
            for key in codedict:                                                                                                           
                if key not in httpcode_list:                                                                                               
                    httpcode_list.append(key)                                                                                              
                                                                                                                                           
        for k in sorted(httpcode_list):                                                                                                    
            s1 = self.dealCodeDict(k,httpCode)                                                                                           
            statInfo += "%-15s\n"%(s1)                                                                 
                                                                                                                                           
        return statInfo

    def dealCodeDict(self,key,dict0):                                                                                                      
        if key not in dict0:                                                                                                               
            s = ""                                                                                                                         
        else:                                                                                                                              
            s = "%s : %s"%(str(key),str(dict0[key]))                                                                                       
        return s

    def run(self):                                                                                                                         
        while True:
            time.sleep(Interval)                                                                                                                        
            self.DealStat()                                                                                                            
            statInfo = "#" * 26 + str(datetime.datetime.now()) + "#" * 26 + "\n"                                                       
            statInfo += self.StatInfo(self.countNum,self.httpCode,self.requestCount,self.requestTime,Interval)                            
            statInfo += "=-" * 13 + str(datetime.datetime.now()) + "=-" * 13 + "\n"                                                    
            statInfo += self.StatInfo(stat["countNumAll"],stat["httpCodeAll"],stat["requestCountAll"],                             
                                     stat["requestTimeAll"],stat["countTimeAll"])                             
            print statInfo                                                                                                             

def LoadTest():                                                                                                                            
    testThreads = []                                                                                                                       
    for i in range(threadNum):                                                                                                             
        thrd = ArceeTest(str(i))                                                                                                      
        testThreads.append(thrd)                                                                                                           
        thrd.start()                                                                                                                       
                                                                                                                                           
    statThread = StatThread()                                                                                                              
    statThread.start()                                                                                                                     
                                                                                                                                           
                                                                                                                                           
    while True :                                                                                                                           
        time.sleep(36000)                                                                                                                  
                                                                                                                                           
    sys.exit(0)                                                                                                                            
                                                                                                                                           
                                                                                                                                           
if __name__ == '__main__':                                                                                                                 
    LoadTest() 

