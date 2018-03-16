#!/usr/bin/env python
# -*- coding: utf-8 -*-

from concurrent import futures
import time
import grpc
import witness_pb2
import common_pb2
import requests
import json
import os
import sys

reload(sys)
sys.setdefaultencoding( "utf-8" )

TIME = 15 
IMAGE_WIDTH = 1920
IMAGE_HEIGHT = 1080
THRESHOLD = 0.1
TOPN = 10
IP = "192.168.2.162"
PORT = "8086"
#URL = "http://192.168.2.162:8086/api/source"

class WitnessService(witness_pb2.WitnessServiceServicer):
    def RenderInfo(self, request, context):
        print "*****************************************"
	#request_info = []
        with open("./test_result/tmp.txt" , "a") as f:
          for item in request.item:
             one = []
             roi = []
             x = item.RelativeRoi.PosX*IMAGE_WIDTH*1.0/100
             y = item.RelativeRoi.PosY*IMAGE_HEIGHT*1.0/100
             width = item.RelativeRoi.Width*IMAGE_WIDTH*1.0/100
             height = item.RelativeRoi.Height*IMAGE_HEIGHT*1.0/100
             print item.FrameId
             print item.RelativeRoi.PosX, item.RelativeRoi.PosY,item.RelativeRoi.Width,item.RelativeRoi.Height
             print x,y,width,height
             one.append(str(item.FrameId)+",")
             one.append(str(item.Id)+",")
             one.append(str(x)+",")
             one.append(str(y)+",")
             one.append(str(width)+",") 
             one.append(str(height)+",")
           
             for citem in item.Candidates:
                  print citem.Id
                  print citem.Name
                  one.append(str(citem.Id)+",")
                  one.append(citem.Name+",")
                  one.append(str(citem.Score)+",")
             #print one 
           
             f.writelines(one)
             f.writelines("\n")

        return witness_pb2.RenderInfoResponse()
 
def serve(vname):
  server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
  witness_pb2.add_WitnessServiceServicer_to_server(WitnessService(), server)
  server.add_insecure_port('[::]:50051')
  server.start()
  #try:
  exsize = 0
  while True:
      time.sleep(TIME)
      prs = os.popen("du -b ./test_result/tmp.txt").read()
      size = prs.split("\t")[0]
      print size
      if str(exsize) == str(size):
         print "video is over."
         os.system("cp ./test_result/tmp.txt ./test_result/%s.txt" % vname )
         break
      exsize = size
  server.stop(0)

def postreq(vname):
   #req = '{ "SorceURI": "%s.mp4","Id": "", "Protocol":"local","SourceName": "newtest011748","Speed":1, "StartTime":"","Opened":true,"IsDeleted":false,"UserConfigMap":{ "DataOutput/WindowsClient/ClientAddr":"192.168.2.16:50051","noroll":true}, "DetectFeatures": [{ "DetectionType": 201,"FeatureTypes": [1011 ],"HotSpots": [], "Outputs": [] }]}' % vname
   req = { "SourceURI": "%s.mp4"%(vname),
           "Id":"",
           "Protocol":"local",
           "SourceName": "scriptest",
           "Speed":1,
           "StartTime":"", 
           "Opened":True, 
           "IsDeleted":False,  
           "UserConfigMap":{ "DataOutput/WindowsClient/ClientAddr":"192.168.2.16:50051", "Enable":True, "noroll":True }, 
           "DetectFeatures": [ {"DetectionType": 201,  "FeatureTypes": [ 1011 ], "HotSpots": [], "Outputs": [] }  ]
         }
   headers = {"Content-Type":"application/json"}
   url = "http://%s:%s/api/source" % (IP, PORT)
   req = json.dumps(req)
   print req
   resp = requests.post(url, data = req, headers=headers)
   if resp.status_code != 201:
      print "post req error!"
   sourceId = resp.content.strip(":%!s(MISSING)")
   print sourceId
   return sourceId 
   
def deleteSource(sid):
   url = "http://%s:%s/api/source/%s" % (IP, PORT, sid)
   resp = requests.delete(url)
   print resp.content
   


def run():
   #video_list = ["day_1_1","day_1_2","day_1_3","day_1_4","day_2_1","day_2_2","day_2_3","day_2_4","day_3_1","day_3_2","day_3_3","day_3_4","day_4_1","day_4_2","day_4_3","day_4_4","night_1_1","night_1_2","night_1_3","night_1_4","night_2_1","night_2_2","night_2_3","night_2_4","night_3_1","night_3_2","night_3_3","night_3_4","night_4_1","night_4_2","night_4_3","night_4_4"]
   #video_list = ["day_1_1","day_1_2","day_1_3","day_1_4"]
   #video_list = ["day_out"]
   video_list = ["day_out"]
   for item in video_list:
     if os.path.exists("./test_result/tmp.txt"):
        print "delete tmp.txt"
        os.system("rm ./test_result/tmp.txt")
     print "~~~~~~~~~~~~start %s~~~~~~~~~" % item
     sourceId = postreq(item)
     time.sleep(5)
     serve(item)
     deleteSource(sourceId)
   

if __name__ == '__main__':
   #serve()
   #postreq("day_1_1")
   run()
