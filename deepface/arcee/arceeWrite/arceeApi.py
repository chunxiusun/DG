#!/usr/bin/env python
#-*- coding:utf-8 -*-

import requests,json
import base64
import datetime,time,threading

IP = "192.168.2.19"
PORT = "8501"

IMAGE = "image.jpg"

threadNum = 1
sendNum = 1024

class ArceeTest(threading.Thread):
    def __init__(self,k):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.k = k
        #self.timeCount = 0
        #self.sendCount = 1
        #self.sendAll = 1

    def get_fids(self):
        url = "http://%s:%s/api/fids"%(IP,PORT)
        image = open(IMAGE,'r').read()
        bs = base64.b64encode(image)
        n = 1
        #fd = open("%s.txt"%self.k,'w')
        while True:
            key = "%s_%d"%(self.k,n)
            data = {key:bs}
            #begin = int(time.time()*1000)
            r = requests.post(url,data=json.dumps(data))
            print datetime.datetime.now()
            #end = int(time.time()*1000)
            #print end - begin
            #print r.status_code
            #print r.content
            resp = json.loads(r.content)
            img_url = resp[key]
            print img_url
            #fd.write("%s\n"%img_url)
            #if n == sendNum:
                #break
            n += 1
            break
        #fd.close()

    def run(self):
        self.get_fids()

def main():                                                                                                                                 
    query_list = []                                                                                                                        
    for i in range(threadNum):                                                                                                            
        t = ArceeTest(str(i))                                                                                                                      
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
