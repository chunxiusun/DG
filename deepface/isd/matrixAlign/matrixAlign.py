#!/usr/bin/env python
#-*- coding:utf-8 -*-

import json
import requests
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

MATRIX_ADDRESS = "192.168.2.16"
MATRIX_PORT = "6501"

imgFile = "img.list"

def recImage(img_url):
    url = "http://%s:%s/rec/image"%(MATRIX_ADDRESS,MATRIX_PORT)
    source = {"Context": {"SessionId": "test123",
                          "Functions": [200,201,202,203,204,205],
                          "Type":2
                         },
              "Image": {"Data": {"URI": img_url}
                       }
             }
    jsource = json.dumps(source)
    resp = requests.post(url, data = jsource)
    status_code = resp.status_code
    if status_code != 200:
        rdict = {}
    else:
        rdict = json.loads(resp.content)
    return status_code,rdict

def run():
    fd = open(imgFile,'r')
    lines = fd.readlines()
    fd.close()
    for line in lines:
        img_url = line.strip()
        #print img_url
        status_code,rdict = recImage(img_url)
        if len(rdict) == 0:
            #print "http code: %s"%status_code
            #print ""
            continue
        status = rdict["Context"]["Status"]
        if status != "200":
            #print status
            #print rdict["Context"]["Message"]
            #print ""
            continue
        if "Faces" not in rdict["Result"]:
            #print "not Faces:%s"%img_url
            #print ""
            continue
        faces = rdict["Result"]["Faces"]
        for face in faces:
            scores = face["AlignResult"]["Scores"]
            for score in scores:
                if score["key"] == "local_is_face":
                    LocalIsFaceThreashold = score["value"]
                    #print "LocalIsFaceThreashold: %s"%LocalIsFaceThreashold
                if score["key"] == "global_is_face":
                    GlobalIsFaceThreashold = score["value"]
                    #print "GlobalIsFaceThreashold: %s"%GlobalIsFaceThreashold
                if score["key"] == "global_front_face":
                    GlobalFrontFaceThreashold = score["value"]
                    #print "GlobalFrontFaceThreashold: %s"%GlobalFrontFaceThreashold
            qualities = face["Qualities"]
            for quality in qualities:
                if quality["key"] == "Yaw":
                    YawThreashold = quality["value"]
                    #print "YawThreashold: %s"%YawThreashold
                if quality["key"] == "Blur":
                    BlurThreashold = quality["value"]
                    #print "BlurThreashold: %s"%BlurThreashold
                if quality["key"] == "Pitch":
                    PitchThreashold = quality["value"]
                    #print "PitchThreashold: %s"%PitchThreashold
                    #print ""
            if BlurThreashold >=0.001 and GlobalIsFaceThreashold >= 0.01 and LocalIsFaceThreashold >= 0.01 and GlobalFrontFaceThreashold >= 0.01 and abs(YawThreashold) <=60 and abs(PitchThreashold) <= 60:
                if BlurThreashold >=0.05 and GlobalIsFaceThreashold >= 0.15 and LocalIsFaceThreashold >= 0.15 and GlobalFrontFaceThreashold >= 0.15 and abs(YawThreashold) <= 35 and abs(PitchThreashold) <= 35:
                    print img_url
                    print "LocalIsFaceThreashold: %s"%LocalIsFaceThreashold
                    print "GlobalIsFaceThreashold: %s"%GlobalIsFaceThreashold
                    print "GlobalFrontFaceThreashold: %s"%GlobalFrontFaceThreashold
                    print "YawThreashold: %s"%YawThreashold
                    print "BlurThreashold: %s"%BlurThreashold   
                    print "PitchThreashold: %s"%PitchThreashold

        #break

if __name__ == '__main__':
    run()
