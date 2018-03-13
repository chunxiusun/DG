#!/usr/bin/env python
# -*- coding: utf8 -*-
#author:chunxiusun

import datetime
import base64
import numpy
import logging
import logging.handlers
import os
import signal
import sys
import multiprocessing
import time
from grpc.beta import implementations
from google.protobuf.text_format import Merge
sys.path.append(os.getcwd()+'/src/python')
import witness_pb2
import common_pb2


reload(sys)
sys.setdefaultencoding("utf-8")

## global configure infomation
conf = dict(
        matrix_align = "127.0.0.1:9814",
        matrix_rec = "127.0.0.1:9804", #可以为空，为空表示不调rec
        thread_num = int(sys.argv[1]),                 # thread num
        mode = 0,                       # 0 means single, 1 means batch
        batch_num = 8,                 # batch num
        svr_type = 2,                   # 1:car 2:face 3:all 0:default(face)
        functions = [200,201,202,203,204,205],
        binData = 0,
	    img_url_file = 'img.list',
        timeout = 5,                   # timeout
        requestID = 0,                  # request Id
        interval = 3,                   # stat interval
        onePass = 0,                    # 1 means run one time
        duration = 0                   # how long to run, now default: never stop
)


## init log
logger = logging.getLogger("MyLogger")
os.system("mkdir -p ./log")
log_name = "./log/matrix_grpc.log." + str(conf["requestID"])
logging.basicConfig(level=logging.DEBUG,
           format='[%(asctime)s %(name)s %(levelname)s] %(message)s',
           #format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
           datefmt='%Y-%m-%d %H:%M:%S',
           filename=log_name,
           filemode='w')
handler = logging.handlers.RotatingFileHandler(log_name,
            maxBytes = 20971520, backupCount = 20)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)
logger.info(
        "[[time.time:%s]]" % str(int(time.time())))
logger.info(
        "[[loadtest start at %s]]" % str(datetime.datetime.now()))
logger.info("Timeout Threshold: %dms", conf["timeout"])
logger.info("thread_num: %d", conf["thread_num"])


## query thread
class QueryThread():
    def __init__(self,mutex,fileList):
        self.header = {"Content-type": "application/json"}
        self.functions = conf['functions']
        self.svr_type = conf['svr_type']
        self.stopped = False
        #self.name = threadname
        self.index = '0'
        self.cnt = 0
        self.mutex = mutex
        self.fileList = fileList


    def STOP(self):
        self.stopped = True

    def Error(self, error_file, query):
        errormutex.acquire()
        with open(error_file, "a") as f:
            if type(query) is str: 
                stat['errorImageCount'] += 1
                f.write(query + '\n')
            else:
                for t in query: 
                    stat['errorImageCount'] += 1
                    f.write(t + '\n')
        errormutex.release()


    def grpc_run(self,stat,alignGrpcError,recGrpcError):
        channel = implementations.insecure_channel(conf["matrix_align"].split(":")[0], eval(conf["matrix_align"].split(":")[1]))
        stub = witness_pb2.beta_create_WitnessService_stub(channel)

        if conf["matrix_rec"] != "":
            conn = implementations.insecure_channel(conf["matrix_rec"].split(":")[0], eval(conf["matrix_rec"].split(":")[1]))
            client = witness_pb2.beta_create_WitnessService_stub(conn)

        if conf["mode"] == 0:
            while True:
                WitnessRequest = witness_pb2.WitnessRequest()
                WitnessRequest.Context.SessionId = "grpc_test_123"
                for function in conf["functions"]:
                    WitnessRequest.Context.Functions.append(function)
                WitnessRequest.Context.Type = conf["svr_type"]
                if not self.fileList.empty():
                    with self.mutex:
                        message = self.fileList.get()
                else:
                    continue
                if conf["binData"] == 1:
                    fd = open(message,'r')
                    message_encode = base64.b64encode(fd.read())
                    fd.close()
                    WitnessRequest.Image.Data.BinData = message_encode
                else:
                    WitnessRequest.Image.Data.URI = message
                begin_align = time.time()
                try:
                    WitnessResponseAlign = stub.Recognize(WitnessRequest,conf['timeout'])
                except Exception as x:
                    #print "ERROR Exception"
                    #print x
                    with self.mutex:
                        logger.error("align:ERROR Exception")
                        logger.error("align:%s"%x)
                    details = x.details
                    for code in ("10006","10007_read","10007_decode","10009","Deadline Exceeded"):
                     #   print "align code:%s" % WitnessRequest.Image.Data.URI
                        with self.mutex:
                            logger.error("align:%s %s"%(code,WitnessRequest.Image.Data.URI))
                        if code == "10007_read":
                            if "10007" in details and "read image failed" in details:
                                alignGrpcError[code] += 1
                        elif code == "10007_decode":
                            if "10007" in details and "decode image failed" in details:
                                alignGrpcError[code] += 1
                        else:
                            if code in details:
                                with self.mutex:
                                    alignGrpcError[code] += 1
                    continue                        
                end_align = time.time()
                with self.mutex:
                    stat["alignRequestCount"] += 1
                elapse_align = (end_align - begin_align) * 1000
                alignCode = int(WitnessResponseAlign.Context.Status)

                if int(alignCode) != 200:
                    with self.mutex:
                        stat["alignErrorCount"] += 1
                    continue

                with self.mutex:
                    stat["alignRequestTime"] += elapse_align

                with self.mutex:
                    stat["alignMaxTime"] = max(elapse_align, stat["alignMaxTime"])
                    stat["alignMinTime"] = min(elapse_align, stat["alignMinTime"])

                faces = WitnessResponseAlign.Result.Faces

                align_face_num = len(faces)
                with self.mutex:
                    stat["alignFaceCount"] += align_face_num

                if len(faces) == 0:
                    print faces
                    continue
                if conf["matrix_rec"] == "":
                    continue
                align_result = faces[0].AlignResult
                user_object = WitnessRequest.Image.UserObject.add()
                user_object.Type = 1
                for landmark in align_result.LandMarks:
                    LandMark = user_object.AlignResult.LandMarks.add()
                    LandMark.X = landmark.X
                    LandMark.Y = landmark.Y
                for landmarkscore in align_result.LandMarkScores:
                    LandMarkScore = user_object.AlignResult.LandMarkScores.append(landmarkscore)
                user_object.AlignResult.Box.X = align_result.Box.X
                user_object.AlignResult.Box.Y = align_result.Box.Y
                user_object.AlignResult.Box.Width =  align_result.Box.Width
                user_object.AlignResult.Box.Height = align_result.Box.Height
                for score in align_result.Scores:
                    value = align_result.Scores[score]
                    Score = user_object.AlignResult.Scores[score] = value

                begin_rec = time.time()
                try:
                    WitnessResponseRec = client.Recognize(WitnessRequest,conf['timeout'])
                except Exception as x:
                    #print "ERROR Exception"
                    #print x
                    with self.mutex:
                        logger.error("rec:ERROR Exception")
                        logger.error("rec:%s"%x)
                    details = x.details
                    for code in ("10006","10007_read","10007_decode","10009","Deadline Exceeded"):
                     #   print "rec code:%s" % WitnessRequest.Image.Data.URI
                        with self.mutex:
                            logger.error("rec:%s %s"%(code,WitnessRequest.Image.Data.URI))
                        if code == "10007_read":
                            if "10007" in details and "read image failed" in details:
                                recGrpcError[code] += 1
                        elif code == "10007_decode":
                            if "10007" in details and "decode image failed" in details:
                                recGrpcError[code] += 1
                        else:
                            if code in details:
                                with self.mutex:
                                    recGrpcError[code] += 1
                    continue
                end_rec = time.time()
                with self.mutex:
                    stat["recRequestCount"] += 1
                elapse_rec = (end_rec - begin_rec) * 1000
                recCode = int(WitnessResponseRec.Context.Status)

                if int(recCode) != 200:
                    with self.mutex:
                        stat["recErrorCount"] += 1
                    continue

                with self.mutex:
                    stat["recRequestTime"] += elapse_rec                                                                                   

                with self.mutex:
                    stat["recMaxTime"] = max(elapse_rec, stat["recMaxTime"])
                    stat["recMinTime"] = min(elapse_rec, stat["recMinTime"])
                #feature = WitnessResponseRec.Result.Faces[0].Features
                #print feature
                #fea = base64.decodestring(feature)
                #array = numpy.frombuffer(fea,dtype=numpy.float32)
                #print "feature size : %s" % str(array.size)
                #sumsquare = 0
                #for num in array:
                #    sumsquare += num * num
                #print "sumsquare: "+str(sumsquare)
                #print WitnessResponseRec
        elif conf["mode"] == 1:
            while True:
                WitnessBatchRequest = witness_pb2.WitnessBatchRequest()
                WitnessBatchRequest.Context.SessionId = "grpc_test_123"
                for function in conf["functions"]:
                    WitnessBatchRequest.Context.Functions.append(function)
                WitnessBatchRequest.Context.Type = conf["svr_type"]
                for batch in range(0,conf["batch_num"]):
                    images = WitnessBatchRequest.Images.add()
                    mutex.acquire()
                    message = fileList.get()
                    mutex.release()
                    images.Data.URI = message
                begin_align = time.time()
                try:
                    WitnessBatchResponseAlign = stub.BatchRecognize(WitnessBatchRequest,conf['timeout']*1.0/10000)
                except Exception as x:
                    print "ERROR Exception"
                    print x
                end_align = time.time()
                stat["alignRequestCount"] += 1
                elapse_align = (end_align - begin_align) * 1000
                alignCode = int(WitnessBatchResponseAlign.Context.Status)
                stat["alignCodeDist"][alignCode] += 1

                if int(alignCode) != 200:
                    stat["alignErrorCount"] += 1
                    continue

                stat["alignRequestTime"] += elapse_align

                for (i, bound) in enumerate(alignTimeBound) :
                    if elapse_align < bound :
                        stat["alignTimeDist"][i] += 1
                        break
                if elapse_align > alignTimeBound[-1]:
                    stat["alignTimeDist"][-1] += 1

                stat["alignMaxTime"] = max(elapse_align, stat["alignMaxTime"])
                stat["alignMinTime"] = min(elapse_align, stat["alignMinTime"])

                for result in WitnessBatchResponseAlign.Results:
                    faces = result.Faces
                    if len(faces) == 0:
                        print faces
                
        #channel.close()
        #conn.close()

    def run(self,stat,alignGrpcError,recGrpcError):
        try:
            self.grpc_run(stat,alignGrpcError,recGrpcError)
        except Exception as e:
            print e
        #import traceback
        #while True:
            #try:
             #   self.grpc_run(stat,alignGrpcError,recGrpcError)
            #except Exception as e:
                #traceback.print_tb()
                #traceback.print_exc(file=sys.stdout)
                #print "ERROR run Exception"
                #print e
		#pass

def query_run(mutex,fileList,stat,alignGrpcError,recGrpcError):
    q = QueryThread(mutex,fileList)
    q.run(stat,alignGrpcError,recGrpcError)

class StatThread() :
    def __init__(self) :
        self.cycleCount = 0
        self.logger = logging.getLogger("StatLogger")
        log_name = "./log/stat_grpc.log." + str(conf["requestID"])
        print "log_name:%s" %(log_name)
        handler = logging.handlers.RotatingFileHandler(log_name,
                maxBytes = 20971520, backupCount = 5)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.DEBUG)
        self.logger.info(
                "[[time.time:%s]]" % str(int(time.time())))
        self.logger.info(
                "[[loadtest start at %s]]" % str(datetime.datetime.now()))
        self.logger.info("Timeout Threshold: %dms", conf["timeout"])
        self.logger.info("thread_num: %d", conf["thread_num"])


    def run(self,mutex,stat,alignGrpcError,recGrpcError):
        while True:
            time.sleep(conf["interval"])
            self.cycleCount += 1
            with mutex:
                alignRequestCount = stat["alignRequestCount"]
                alignErrorCount = stat["alignErrorCount"]
                recRequestCount = stat["recRequestCount"]
                recErrorCount = stat["recErrorCount"]
                alignRequestTime = stat["alignRequestTime"]
                alignMaxReqestTime = stat["alignMaxTime"]
                alignMinRequestTime = stat["alignMinTime"]
                recMaxReqestTime = stat["recMaxTime"]
                recMinRequestTime = stat["recMinTime"]
                recRequestTime = stat["recRequestTime"]
                alignFaceCount = stat["alignFaceCount"]
            avgAlignRequestCount = alignRequestCount*1.0/(self.cycleCount * conf["interval"])
            avgAlignEffectiveCount = (alignRequestCount-alignErrorCount)*1.0/(self.cycleCount * conf["interval"])
            avgRecRequestCount = recRequestCount*1.0/(self.cycleCount * conf["interval"])
            avgRecEffectiveCount = (recRequestCount-recErrorCount)*1.0/(self.cycleCount * conf["interval"])
            if alignRequestCount != 0:
                avgAlignRequestTime = alignRequestTime*1.0/alignRequestCount
            else:
                avgAlignRequestTime = 0.0
            if recRequestCount != 0:
                avgRecRequestTime = recRequestTime*1.0/recRequestCount
            else:
                avgRecRequestTime = 0.0
            face_per_p = alignFaceCount*1.0/(alignRequestCount-alignErrorCount)
            align_throughput = avgAlignEffectiveCount * 86400
            rec_throughput = avgRecEffectiveCount * 86400
            statInfo = "\n"\
                       "########################## %s ###########################\n"\
                       "### Align Search time:%d, AlignErrorCount:%d\n"\
                       "### Rec Search time:%d, RecErrorCount:%d\n"\
                       "### avgAlignQPS/avgAlignEffectiveQPS:%0.2f/%0.2f/s\n"\
                       "### avgRecQPS/avgRecEffectiveQPS:%0.2f/%0.2f/s\n"\
                       "### avgAlignRequestTime:%.2fms\n"\
                       "### avgRecRequestTime:%.2fms\n"\
                       "### alignMaxReqestTime/alignMinRequestTime:%.2fms/%.2fms\n"\
                       "### recMaxReqestTime/recMinRequestTime:%.2fms/%.2fms\n"\
                       "### Align Throughput per Day:%d\n"\
                       "### Rec Throughput per Day:%d\n"\
                       "### faceCount:%d\n"\
                       "### face per photo:%.2f\n"\
                       "### elapse:%d\n"\
                       "align:%s\n"\
                       "rec:%s\n"%(str(datetime.datetime.now()),
                            alignRequestCount,alignErrorCount,
                            recRequestCount,recErrorCount,
                            avgAlignRequestCount,avgAlignEffectiveCount,
                            avgRecRequestCount,avgRecEffectiveCount,
                            avgAlignRequestTime,avgRecRequestTime,
                            alignMaxReqestTime,alignMinRequestTime,
                            recMaxReqestTime,recMinRequestTime,
                            align_throughput,rec_throughput,
                            alignFaceCount,face_per_p,self.cycleCount * conf["interval"],
                            str(alignGrpcError),str(recGrpcError))
            print statInfo
            self.logger.info(statInfo)
     
        os.kill(os.getpid(), signal.SIGKILL)

def stat_run(mutex,stat,alignGrpcError,recGrpcError):
    statThread = StatThread()
    statThread.run(mutex,stat,alignGrpcError,recGrpcError)

def quitTest(signum, frame) :
    print "loadtest quit"
    sys.exit(0)

def read_image(fileList):
    fd = open(conf['img_url_file'],'r')
    for line in fd.readlines():
        temp_path = line.strip()
	while fileList.full():
            time.sleep(1)
	else:
	    fileList.put(temp_path)
    fd.close()

def read_image_while(fileList):
    while True:
        if fileList.empty() == True:
            read_image(fileList)
            if conf["onePass"] == 1:
                break
        time.sleep(1)

#do load test
def LoadTest() :
    manager = multiprocessing.Manager()
    fileList = manager.Queue()
    mutex = manager.Lock()

    stat = manager.dict()
    stat["alignRequestCount"] = 0
    stat["alignErrorCount"] = 0
    stat["alignRequestTime"] = 0.0
    stat["recRequestCount"] = 0
    stat["recErrorCount"] = 0
    stat["recRequestTime"] = 0.0
    stat["alignMaxTime"] = 0.0
    stat["alignMinTime"] = 1000000.0
    stat["recMaxTime"] = 0.0
    stat["recMinTime"] = 1000000.0
    stat["alignFaceCount"] = 0

    alignGrpcError = manager.dict()
    recGrpcError = manager.dict()
    lst = ["ExceptionError","10006","10007_read","10007_decode","10009","Deadline Exceeded"]
    for item in lst:
        alignGrpcError[item] = 0
        recGrpcError[item] = 0

    pool = multiprocessing.Pool(processes = (conf["thread_num"]+3))
    pool.apply_async(stat_run,args=(mutex,stat,alignGrpcError,recGrpcError))
    pool.apply_async(read_image_while,args=(fileList,))
    for i in range(conf["thread_num"]):
        pool.apply_async(query_run,args=(mutex,fileList,stat,alignGrpcError,recGrpcError))
    pool.close()
    pool.join()


    if conf["duration"] != 0 :
        signal.signal(signal.SIGALRM, quitTest)
        signal.alarm(conf["duration"] + 1)


    sys.exit(0)

if __name__ == "__main__":
    LoadTest()
