#!/usr/bin/env python
#-*- coding:utf-8 -*-

import requests,json
import base64
import datetime,time,threading

IP = "192.168.2.19"
PORT = "8501"

#FID = "0.txt"
FID = "214,cce4452506959f"

threadNum = 100

class ArceeTest(threading.Thread):
    def __init__(self):#,fid_list):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        #self.fid_list = fid_list

    def get_file_by_id(self):
        url = "http://%s:%s/api/file/%s"%(IP,PORT,FID)
        r = requests.get(url)
        print datetime.datetime.now()
        '''for fid in self.fid_list:
            url = "http://%s:%s/api/file/%s"%(IP,PORT,fid)
            #begin = int(time.time()*1000)
            r = requests.get(url)
            print datetime.datetime.now()
            time.sleep(1)
            break
            #end = int(time.time()*1000)
            #print r.content'''
         
    def run(self):
        while True:                                                                                                                         
            self.get_file_by_id()

def deal_fid():
    fid_list = []
    fd = open(FID,'r')
    for line in fd.readlines():
        fid = line.strip().split('/')[-1]
        #print fid
        fid_list.append(fid)
    return fid_list                                                                                                          

def main():
    #fid_list = deal_fid()                                                                                                                                 
    query_list = []                                                                                                                        
    for i in range(threadNum):                                                                                                            
        #t = ArceeTest(fid_list)
        t = ArceeTest()                                                                                                                      
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
