#!/usr/bin/env python
#-*- coding:utf-8 -*-

import requests,json,datetime,time,os,sys
import signal
import logging
import logging.handlers
import threading
import pdb
from bs4 import BeautifulSoup

IP = "192.168.2.222"
PORT = "8900"
TYPE = "vsd"
mock_config = "vsd.json"

frontPort = 1111
threadNum = 3
CountInterval = 5
PPORT = "38647"

stat = dict(
     countNum = 0,
     countNumAll = 0,
     
     httpCodeCI = {},
     httpCodeCIAll = {},
     requestCountCI = 0,
     requestCountCIAll = 0,
     requestTimeCI = 0.0,
     requestTimeCIAll = 0.0,

     httpCodeCG = {},
     httpCodeCGAll = {},
     requestCountCG = 0,
     requestCountCGAll = 0,
     requestTimeCG = 0.0,
     requestTimeCGAll = 0.0,

     httpCodeGAI = {},
     httpCodeGAIAll = {},
     requestCountGAI = 0,
     requestCountGAIAll = 0,
     requestTimeGAI = 0.0,
     requestTimeGAIAll = 0.0,

     httpCodeDI = {},
     httpCodeDIAll = {},
     requestCountDI = 0,
     requestCountDIAll = 0,
     requestTimeDI = 0.0,
     requestTimeDIAll = 0.0,

     httpCodeDG = {},
     httpCodeDGAll = {},
     requestCountDG = 0,
     requestCountDGAll = 0,
     requestTimeDG = 0,
     requestTimeDGAll = 0,

     goroutineNum = 0,
     heapNum = 0,
     threadcreateNum = 0 
)


## init log
logger = logging.getLogger("MyLogger")
os.system("mkdir -p ./log")
log_name = "./log/olympus_test.log"
formatter = logging.Formatter(
    '%(asctime)s %(filename)s %(funcName)s [line:%(lineno)d] %(levelname)s: %(message)s')
handler = logging.handlers.RotatingFileHandler(log_name,
            maxBytes = 20971520, backupCount = 5)
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)
logger.info("[[time.time:%s]]" % str(int(time.time())))
logger.info("[[loadtest start at %s]]" % str(datetime.datetime.now()))
#logger.info("Timeout Threshold: %dms", conf["timeout"])
logger.info("threadNum: %d", threadNum)


class TestOlympus(threading.Thread):
    def __init__(self,front_port):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.instance_id = ""
        self.group_id = ""
        self.front_port = front_port

    def creat_instance(self):
        logger.info("##creat instance##")
        url = "http://%s:%s/olympus/v1/instance?type=%s"%(IP,PORT,TYPE)
        config = open(mock_config,'r').read()
        pre = [{"pre_fetch_cmd": "echo hello framework!!"}]
        data = {}
        data["config_json"] = config
        data["pre_executor"] = json.dumps(pre)
        #pdb.set_trace()
        r = requests.post(url,data=data)
        r_code = r.status_code
        if r_code not in stat["httpCodeCI"]:
            stat["httpCodeCI"][r_code] = 0
        stat["httpCodeCI"][r_code] += 1
        if r_code != 200:
            logger.info("create instance http_code:%s" % r_code)
            return
        r_time = (r.elapsed.microseconds)*1.0/1000
        stat["requestTimeCI"] += r_time
        stat["requestCountCI"] += 1
        logger.info("create instance http_code:%s" % r_code)
        logger.info("create instance resp_content:%s" % r.content)
        logger.info("create instance resp_time:%s" % str(r_time))
        resp = json.loads(r.content)
        self.instance_id = resp["Data"]["instance_id"]
        logger.info("instance id:%s" % self.instance_id)

        #get instance
        state = ""
        while state!= "RUNNING":
            time.sleep(1)
            url = "http://%s:%s/olympus/v1/instance?iid=%s"%(IP,PORT,self.instance_id)
            r1 = requests.get(url)
            resp1 = json.loads(r1.content)
            code1 = resp1["Code"]
            state = resp1["Data"]["State"]

    def creat_group(self):
        logger.info("##creat group##")
        url = "http://%s:%s/olympus/v1/group"%(IP,PORT)
        data = {}
        data["frontend"] = self.front_port
        r = requests.post(url,data=data)
        r_code = r.status_code
        if r_code not in stat["httpCodeCG"]:
            stat["httpCodeCG"][r_code] = 0
        stat["httpCodeCG"][r_code] += 1
        if r_code != 200:
            logger.info("create group http_code:%s" % r_code)
            return
        r_time = (r.elapsed.microseconds)*1.0/1000
        stat["requestTimeCG"] += r_time
        stat["requestCountCG"] += 1
        logger.info("create group http_code:%s" % r_code)
        logger.info("create group resp_content:%s" % r.content)
        logger.info("create group resp_time:%s" % r_time)
        resp = json.loads(r.content)
        code = resp["Code"]
        if code == 0:
            self.group_id = resp["Data"]["group_id"]
        else:
            self.group_id = ""
        logger.info("group id:%s" % self.group_id)

    def group_add_instance(self):
        logger.info("##group add instance##")
        url = "http://%s:%s/olympus/v1/group/add/instance?gid=%s"%(IP,PORT,self.group_id)
        data = {}
        data["iid"] = self.instance_id
        data["backend"] = "%s:%s"%(IP,self.front_port*10)
        r = requests.post(url,data=data)
        r_code = r.status_code
        if r_code not in stat["httpCodeGAI"]:
            stat["httpCodeGAI"][r_code] = 0
        stat["httpCodeGAI"][r_code] += 1
        if r_code != 200:
            logger.info("group add instance http_code:%s" % r_code)
            return
        r_time = (r.elapsed.microseconds)*1.0/1000
        stat["requestTimeGAI"] += r_time
        stat["requestCountGAI"] += 1
        logger.info("group add instance http_code:%s" % r_code)
        logger.info("group add instance resp_content:%s" % r.content)
        logger.info("group add instance resp_time:%s" % r_time)

    def delete_instance(self):
        logger.info("##delete instance##")
        url = "http://%s:%s/olympus/v1/instance/delete?iid=%s"%(IP,PORT,self.instance_id)                                                              
        r = requests.post(url)
        r_code = r.status_code
        if r_code not in stat["httpCodeDI"]:
            stat["httpCodeDI"][r_code] = 0
        stat["httpCodeDI"][r_code] += 1
        if r_code != 200:
            logger.info("delete instance http_code:%s" % r_code)
            return
        r_time = (r.elapsed.microseconds)*1.0/1000
        stat["requestTimeDI"] += r_time
        stat["requestCountDI"] += 1                                                                             
        logger.info("delete instance http_code:%s" % r_code)                                                                               
        logger.info("delete instance resp_content:%s" % r.content)
        logger.info("delete instance resp_time:%s" % r_time)
    
        resp_code = 0 
        while resp_code != 400:
            time.sleep(1)
            url = "http://%s:%s/olympus/v1/instance?iid=%s"%(IP,PORT,self.instance_id)
            r1 = requests.get(url)
            resp_code = r1.status_code

    def delete_group(self):
        logger.info("##delete group##")
        url = "http://%s:%s/olympus/v1/group/delete?gid=%s"%(IP,PORT,self.group_id)                                                                 
        r = requests.post(url)
        r_code = r.status_code
        if r_code not in stat["httpCodeDG"]:
            stat["httpCodeDG"][r_code] = 0
        stat["httpCodeDG"][r_code] += 1
        if r_code != 200:
            logger.info("delete group http_code:%s" % r_code)
            return   
        r_time = (r.elapsed.microseconds)*1.0/1000
        stat["requestTimeDG"] += r_time
        stat["requestCountDG"] += 1                                                              
        logger.info("delete group http_code:%s" % r_code)                                                                                 
        logger.info("delete group resp_content:%s" % r.content)
        logger.info("delete group resp_time:%s" % r_time)

        resp_code = 0 
        while resp_code != 500:
            time.sleep(1)
            url = "http://%s:%s/olympus/v1/group?gid=%s"%(IP,PORT,self.group_id)
            r1 = requests.get(url)
            resp_code = r1.status_code

    def run(self):
        while True:
            self.creat_instance()
            self.creat_group()
            self.group_add_instance()
            self.delete_instance()
            self.delete_group()
            stat["countNum"] += 1

class StatThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.logger = logging.getLogger("StatLogger")
        log_name = "./log/stat.olympus.log"
        formatter = logging.Formatter(
              '%(asctime)s %(filename)s %(funcName)s [line:%(lineno)d] %(levelname)s: %(message)s')
        handler = logging.handlers.RotatingFileHandler(log_name,
               maxBytes = 20971520, backupCount = 5)
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.DEBUG)
        self.logger.info("[[time.time:%s]]" % str(int(time.time())))
        self.logger.info("[[loadtest start at %s]]" % str(datetime.datetime.now()))
        #self.logger.info("Timeout Threshold: %dms", conf["timeout"])
        #self.logger.info("threadNum: %d", conf["threadNum"])


    def DealStat(self):
        # save stats
        self.countNum = stat["countNum"]
        self.httpCodeCI = stat["httpCodeCI"]
        self.requestCountCI = stat["requestCountCI"]
        self.requestTimeCI = stat["requestTimeCI"]
        self.httpCodeCG = stat["httpCodeCG"]
        self.requestCountCG = stat["requestCountCG"]
        self.requestTimeCG = stat["requestTimeCG"]
        self.httpCodeGAI = stat["httpCodeGAI"]
        self.requestCountGAI = stat["requestCountGAI"]
        self.requestTimeGAI = stat["requestTimeGAI"]
        self.httpCodeDI = stat["httpCodeDI"]
        self.requestCountDI = stat["requestCountDI"]
        self.requestTimeDI = stat["requestTimeDI"]
        self.httpCodeDG = stat["httpCodeDG"]
        self.requestCountDG = stat["requestCountDG"]
        self.requestTimeDG = stat["requestTimeDG"]

        # reset stats
        stat["countNum"] = 0
        stat["httpCodeCI"] = {}
        stat["requestCountCI"] = 0
        stat["requestTimeCI"] = 0.0
        stat["httpCodeCG"] = {}
        stat["requestCountCG"] = 0
        stat["requestTimeCG"] = 0.0
        stat["httpCodeGAI"] = {}
        stat["requestCountGAI"] = 0
        stat["requestTimeGAI"] = 0.0
        stat["httpCodeDI"] = {}
        stat["requestCountDI"] = 0
        stat["requestTimeDI"] = 0.0
        stat["httpCodeDG"] = {}
        stat["requestCountDG"] = 0
        stat["requestTimeDG"] = 0.0

        #count all
        stat["countNumAll"] += self.countNum
        stat["httpCodeCIAll"] = self.dealDict(self.httpCodeCI,stat["httpCodeCIAll"])
        stat["requestCountCIAll"] += self.requestCountCI
        stat["requestTimeCIAll"] += self.requestTimeCI
        stat["httpCodeCGAll"] = self.dealDict(self.httpCodeCG,stat["httpCodeCGAll"])
        stat["requestCountCGAll"] += self.requestCountCG
        stat["requestTimeCGAll"] += self.requestTimeCG
        stat["httpCodeGAIAll"] = self.dealDict(self.httpCodeGAI,stat["httpCodeGAIAll"])
        stat["requestCountGAIAll"] += self.requestCountGAI
        stat["requestTimeGAIAll"] + self.requestTimeGAI
        stat["httpCodeDIAll"] = self.dealDict(self.httpCodeDI,stat["httpCodeDIAll"])
        stat["requestCountDIAll"] += self.requestCountDI
        stat["requestTimeDIAll"] += self.requestTimeDI
        stat["httpCodeDGAll"] = self.dealDict(self.httpCodeDG,stat["httpCodeDGAll"])
        stat["requestCountDGAll"] += self.requestCountDG
        stat["requestTimeDGAll"] += self.requestTimeDG

    def dealDict(self,dict1,dict2):
        for key in dict1:
            if key not in dict2:
                dict2[key] = 0
            dict2[key] += dict1[key]
        return dict2

    def StatInfo(self,countNum,httpCodeCI,requestCountCI,requestTimeCI,
               httpCodeCG,requestCountCG,requestTimeCG,httpCodeGAI,
               requestCountGAI,requestTimeGAI,httpCodeDI,requestCountDI,
               requestTimeDI,httpCodeDG,requestCountDG,requestTimeDG):
        
        avg_requestTimeCI = requestTimeCI*1.0 / requestCountCI
        avg_requestTimeCG = requestTimeCG*1.0 / requestCountCG
        avg_requestTimeGAI = requestTimeGAI*1.0 / requestCountGAI
        avg_requestTimeDI = requestTimeDI*1.0 / requestCountDI
        avg_requestTimeDG = requestTimeDG*1.0 / requestCountDG


        statInfo = "### Count Num:%d\n"\
                   "### Create Instance Count:%d, avg_time:%0.2fms\n"\
                   "### Create Group Count:%d, avg_time:%0.2fms\n"\
                   "### Group Add Instance Count:%d, avg_time:%0.2fms\n"\
                   "### Delete Instance Count:%d, avg_time:%0.2fms\n"\
                   "### Delete Group Count:%d, avg_time:%0.2fms\n"\
                   "### Count Interval:%d\n"\
                   "httpCodeCI:   httpCodeCG:   httpCodeGAI:   httpCodeDI:   httpCodeDG:   \n"%(countNum,
                   requestCountCI,avg_requestTimeCI,requestCountCG,avg_requestTimeCG,requestCountGAI,
                   avg_requestTimeGAI,requestCountDI,avg_requestTimeDI,requestCountDG,avg_requestTimeDG,CountInterval)

        httpcode_list = []
        for codedict in [httpCodeCI,httpCodeCG,httpCodeGAI,httpCodeDI,httpCodeDG]:
            for key in codedict:
                if key not in httpcode_list:
                    httpcode_list.append(key)

        for k in sorted(httpcode_list):
            s1 = self.dealCodeDict(k,httpCodeCI)
            s2 = self.dealCodeDict(k,httpCodeCG)
            s3 = self.dealCodeDict(k,httpCodeGAI)
            s4 = self.dealCodeDict(k,httpCodeDI)
            s5 = self.dealCodeDict(k,httpCodeDG)
            statInfo += "%-15s %-12s %-15s %-12s %-15s\n"%(s1,s2,s3,s4,s5)
            
        return statInfo

    def dealCodeDict(self,key,dict0):
        if key not in dict0:
            s = ""
        else:
            s = "%s : %s"%(str(key),str(dict0[key]))
        return s

    def StatPProf(self):
        url = "http://%s:%s/debug/pprof/"%(IP,PPORT)
        r = requests.get(url)
        html = r.content
        #print r.status_code
        #print r.content
        soup = BeautifulSoup(html)
        for i in range(len(soup.table.contents)):
            try:
                name = soup.table.contents[i].contents[1].text.encode("utf-8").strip()
                value = soup.table.contents[i].contents[0].text.encode("utf-8").strip()
                #print name,value
                if name == "goroutine":
                    stat["goroutineNum"] = eval(value)
                if name == "heap":
                    stat["heapNum"] = eval(value)
                if name == "threadcreate":
                    stat["threadcreateNum"] = eval(value)
            except:
                pass
        statPProf = "PProf:\n"\
                    "### goroutine Num:%d,\n"\
                    "### heapNum:%d,\n"\
                    "### threadcreateNum:%d\n"\
                    "\n"%(stat["goroutineNum"],stat["heapNum"],stat["threadcreateNum"])
        return statPProf

    def run(self):
        while True:
            if stat["countNum"] == CountInterval:
                self.DealStat()
                statInfo = "#" * 26 + str(datetime.datetime.now()) + "#" * 26 + "\n"
                statInfo += self.StatInfo(self.countNum,self.httpCodeCI,self.requestCountCI,self.requestTimeCI,
                                     self.httpCodeCG,self.requestCountCG,self.requestTimeCG,self.httpCodeGAI,
                                     self.requestCountGAI,self.requestTimeGAI,self.httpCodeDI,self.requestCountDI,
                                     self.requestTimeDI,self.httpCodeDG,self.requestCountDG,self.requestTimeDG)
                statInfo += "=-" * 13 + str(datetime.datetime.now()) + "=-" * 13 + "\n"
                statInfo += self.StatPProf()
                statInfo += self.StatInfo(stat["countNumAll"],stat["httpCodeCIAll"],stat["requestCountCIAll"],
                                     stat["requestTimeCIAll"],stat["httpCodeCGAll"],stat["requestCountCGAll"],
                                     stat["requestTimeCGAll"],stat["httpCodeGAIAll"],stat["requestCountGAIAll"],
                                     stat["requestTimeGAIAll"],stat["httpCodeDIAll"],stat["requestCountDIAll"],
                                     stat["requestTimeDIAll"],stat["httpCodeDGAll"],stat["requestCountDGAll"],stat["requestTimeDGAll"])
                print statInfo
                self.logger.info(statInfo)
        #os.kill(os.getpid(), signal.SIGKILL)

def batch_delete_instance():
    print "##delete instance"
    url = "http://%s:%s/olympus/v1/instance"%(IP,PORT)
    r = requests.get(url)
    #print r.status_code
    #print r.content
    resp = json.loads(r.content)
    datas = resp["Data"]
    for data in datas:
        iid = data["InstanceId"]
        print iid
        url1 = "http://%s:%s/olympus/v1/instance/delete?iid=%s"%(IP,PORT,iid)
        r1 = requests.post(url1)
        print r1.status_code
        print r1.content

def batch_delete_group():
    print "##delete group"
    url = "http://%s:%s/olympus/v1/group"%(IP,PORT)
    r = requests.get(url)
    #print r.status_code
    resp = json.loads(r.content)
    datas = resp["Data"]
    for data in datas:
        gid = data["GroupID"]
        print gid
        url1 = "http://%s:%s/olympus/v1/group/delete?gid=%s"%(IP,PORT,gid)
        r1 = requests.post(url1)
        print r1.status_code
        print r1.content

def onsignal_term(a,b):
    batch_delete_instance()
    batch_delete_group()
    sys.exit(0)

def LoadTest():
    global frontPort
    #init olympus
    print "=======================start init olympus========================="
    batch_delete_instance()
    batch_delete_group()
    print "=======================end init olympus========================="
    print ""
    testThreads = []
    for i in range(threadNum):
        thrd = TestOlympus(frontPort)
        testThreads.append(thrd)
        thrd.start()
        frontPort += 1

    statThread = StatThread()
    statThread.start()

  
    while True :
        time.sleep(36000)

    sys.exit(0)

signal.signal(signal.SIGTERM,onsignal_term)

if __name__ == '__main__':
    LoadTest()
