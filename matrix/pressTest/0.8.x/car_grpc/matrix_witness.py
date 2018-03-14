#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
import time
import requests
import json
import base64
import threading
import Queue
from optparse import OptionParser
from grpc.beta import implementations
from google.protobuf.text_format import Merge
sys.path.append(os.getcwd()+'/src/python')
import witness_pb2
import common_pb2

queue = Queue.Queue(maxsize = 100000)
lock = threading.Lock()
total = 0

def put_list(filedir):
    while True:
        for filename in os.listdir(filedir):
            tmpfile = os.path.join(filedir,filename) 
            if os.path.isfile(tmpfile):
                with open(tmpfile) as f :
                    for line in f.readlines():
                        queue.put(line.strip('\n'))
    queue.join()
def put_pic(filedir):
    for filename in os.listdir(filedir):
        tmpfile = os.path.join(filedir,filename)
        if os.path.isfile(tmpfile):
            with open(tmpfile,"rb") as fd:
                file_encode = base64.b64encode(fd.read())
                queue.put(file_encode)
    queue.join()
class WitnessThread(threading.Thread):
    def __init__(self,queue,ip,port,function,method,batchsize):
        threading.Thread.__init__(self)
        self.queue = queue
        self.ip = ip
        self.port = int(port)
        self.function = function
        self.method = method
        self.batchsize = int(batchsize)
        self.timeout = 10.0
    def run(self):
        if(self.method == 'grpc'):
            self.start_grpc()
        else:
            self.start_restful()
    def start_restful(self):
        ServiceRestful = "http://%s:%d/rec/image/batch"%(self.ip,self.port) 
        while True:
            source = {"Context":{"SessionId": "restful_test_123","Functions":eval(self.function),"Type":1},"Images":[]}
            for batch in range(0,self.batchsize):
                message = self.queue.get()
                image = {"Data":{"URI":""},"UserObject":[]}
                image["Data"]["URI"]=message.split(' ',2)[0]
        #        userobject = {"Type":1,"Rect":{},"AlignResult":""}
        #        userobject["AlignResult"] = message.split(' ',2)[1]
        #        image["UserObject"].append(userobject)
                source["Images"].append(image)
            post_data = json.dumps(source)
            resp = requests.post(ServiceRestful, data = post_data, timeout=self.timeout)
            print resp.status_code
           # rdict = json.loads(resp.content)
           # print rdict
            lock.acquire()
           # rdict = json.loads(resp.content)
           # for result in rdict["Results"]:
           #     align_file = open('./url_align.log', 'a')
           #     if result.has_key('Faces'):
           #         alignresult = result["Faces"][0]["AlignResult"]
           #     else:
           #         alignresult = ''
           #     align_file.write('%s %s \n'%(result["Image"]["Data"]["URI"],alignresult)) 
           #     align_file.close()
            global total
            total = total + self.batchsize
            log_file = open('./restful.log', 'a')
            log_file.write('%s total send pictures is %d\n'%(time.strftime("%Y-%m-%d %X",time.localtime()),total))
            log_file.close()
            lock.release() 
        #resp_dict = json.loads(resp.content) 
        self.queue.task_done()
    def start_grpc(self):
        channel = implementations.insecure_channel(self.ip, self.port)
        stub = witness_pb2.beta_create_WitnessService_stub(channel)
        print "hello"
        while True:
            req = witness_pb2.WitnessBatchRequest()
            Merge('Context{\nSessionId:"grpc_test_123"\n Type:1 \n Functions:%s \n}\n'%(self.function),req)
            for batch in range(0,self.batchsize):
                message = self.queue.get()
                image = 'Images {\n Data { \n URI:"%s" \n} \n}'%(message)
                Merge(image,req)
            resp = stub.BatchRecognize(req,self.timeout)
            print resp
            lock.acquire()
            global total
            total = total + self.batchsize
            log_file = open('./grpc.log', 'a')
            log_file.write('%s total send pictures is %d, number of vehicle is %d , status: %s\n'%(time.strftime("%Y-%m-%d %X",time.localtime()),total,len(resp.Results[0].Vehicles),resp.Context.Status))
            log_file.close()
            lock.release() 
        self.queue.task_done()
        


if __name__ == "__main__":
    usage = "usage: %prog [options] arg1"
    parser = OptionParser(usage=usage)
    parser.add_option("-I","--ip",action="store",dest="Ip",help="Matrix Ip Address")
    parser.add_option("-P","--port",action="store",dest="Port",help="Matrix Listen Port")
    parser.add_option("-F","--function",action="store",dest="Function",help="Functions [200,201,202,203,204,205]")
    parser.add_option("-D","--dir",action="store",dest="Dir",help="Get Info Dir")
    parser.add_option("-S","--source",action="store",dest="Source",help="Mode: 0-urllistfile,1-picfiles")
    parser.add_option("-M","--method",action="store",dest="Method",help="grpc,restful")
    parser.add_option("-T","--threadnum",action="store",dest="Threadnum",help="threadnum to press test")
    parser.add_option("-B","--batchsize",action="store",dest="BatchSize",help="batchsize to press test")
    (options, args) = parser.parse_args()
    for thn in range(int(options.Threadnum)):
        t = WitnessThread(queue,options.Ip,options.Port,options.Function,options.Method,options.BatchSize)
        t.setDaemon(True)
        t.start()
    if(options.Source == '0'):
        put_list(options.Dir)
    elif(options.Source == '1'):
        put_pic(options.Dir) 
