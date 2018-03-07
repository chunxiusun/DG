#!/usr/bin/env python
#-*- coding:utf-8 -*-

import time,json,requests

IP = "192.168.2.222"
PORT = "9876"

startNum = 1
endNum = 1
sensorName = u"海关本地视频"

sensorID = "6c954f3c-c8f9-4456-95e0-e56ecb549412"
repoID = "c890ac54-e88f-4c2a-b678-77dcb7133fbb"
videoFile = "video_url.txt"

def get_sensorConfig():
    print "get sensorConfig"
    url = "http://%s:%s/api/config/param?sensor_id=%s"%(IP,PORT,sensorID)
    r = requests.get(url)
    #print r.status_code
    data = json.loads(r.content)
    config = json.loads(data["Data"]["Value"])
    print config
    return config

def get_idAndPort():
    print "get id and port"
    url = "http://%s:%s/api/config/sensoridandport"%(IP,PORT)
    r = requests.get(url)
    print r.status_code
    data = json.loads(r.content)
    sensor_id = data["Data"]["SensorId"]
    rtpport = data["Data"]["Port"]
    print sensor_id,rtpport
    return sensor_id,rtpport

def add_sensor(sensor_id,rtpport,sensor_name,video_name,config):
    print "add sensor"
    url = "http://%s:%s/api/device/sensor"%(IP,PORT)
    config["SensorName"] = sensor_id
    config["Source"] = video_name
    config["VideoOutput"]["RTP"]["Port"] = rtpport
    config["VideoOutput"]["RTP"]["BitRate"] = 4096000
    config["VideoOutput"]["ShareMem"]["MemSize"] = 16000000
    config["DataOutput"]["Kafka"]["MaxSizeBytes"] = 4000000
    post_data = {
                "Timestamp": int(time.time()*1000),
                "RepoId": "5300",
                "RepoName": "默认部门",
                "SensorId": sensor_id,
                "SensorName": sensor_name,
                "SerialId": sensor_id,
                "Type": 3,
                "Status": 1,
                "LiveActive": False,
                "DataActive": False,
                "Longitude": -200,
                "Latitude": -200,
                "Ip": "",
                "Port": "",
                "Url": video_name,
                "RenderedUrl": "rtsp://%s:8554/live/%s"%(IP,sensor_id),
                "RtmpUrl": "rtmp://%s/live/%s"%(IP,sensor_id),
                "Comment": "",
                "ConfigJson": json.dumps(config),
                "OlympusId": "",
                "RtpPort": rtpport
            }
    r = requests.post(url,data=json.dumps(post_data))
    print r.status_code
    print r.content
    code = r.status_code
    return code
        

def add_rule(sensor_id,sensor_name):
    print "add rule"
    url = "http://%s:%s/api/bingo/facerule"%(IP,PORT)
    data = {
           "Comment": "",
           "FaceRepos": [
                    {
                     "RepoId": repoID,
                     "Confidence": 0.8
                    }
                        ],
           "Sensors": [
                   {
                   "SensorId": sensor_id,
                   "SensorName": sensor_name,
                   "Rois": []
                   }
                      ],
           "Status": 2,
           "Times": {
                  "_startDate": "1501689600000",
                  "_endDate": "1501689600000",
                  "_startTime": "1501689600000",
                  "_endTime": "1501775999999",
                  "IsLong": True
                    },
           "Timestamp": int(time.time()*1000)
           }
    r = requests.post(url,data=json.dumps(data))
    print r.status_code
    print r.content
    code = r.status_code
    return code

def get_instance_id(sensor_id):
    print "get instance id"
    url = "http://%s:%s/api/device/sensor?sensor_id=%s"%(IP,PORT,sensor_id)
    r = requests.get(url)
    #print r.status_code
    data = json.loads(r.content)
    instance_id = data["Data"]["OlympusId"]
    print instance_id
    return instance_id

def stop_instance(instance_id):
    print "stop instance"
    url = "http://%s:8900/olympus/v1/instance/stop?iid=%s"%(IP,instance_id)
    r = requests.post(url)
    #get instance
    state = ""
    while state != "STOPPED":
        url1 = "http://%s:8900/olympus/v1/instance?iid=%s"%(IP,instance_id)
        r1 = requests.get(url1)
        resp1 = json.loads(r1.content)
        state = resp1["Data"]["State"]
        time.sleep(1)

def delete_instance(instance_id):
    print "delete instance"
    url = "http://%s:8900/olympus/v1/instance/delete?iid=%s"%(IP,instance_id)
    r = requests.post(url)
    print r.status_code
    print r.content
    code = r.status_code
    return code
    #get instance
    #resp_code = 0 
    #while resp_code != 400:
        #url = "http://%s:%s/olympus/v1/instance?iid=%s"%(IP,PORT,instance_id)
        #r1 = requests.get(url)
        #resp_code = r1.status_code
        #print resp_code
        #resp1 = json.loads(r1.content)
        #code1 = resp1["Code"]


if __name__ == '__main__':
    config = get_sensorConfig()
    fd = open(videoFile,'r')
    #fsid = open("sensor_id.txt",'wa')
    #fiid = open("indtance_id.txt",'wa')
    for line in fd.readlines():
        video_name = line.strip()
        for i in range(startNum,endNum+1):
            sensor_name = "%s%d"%(sensorName,i)
            sensor_id,rtpport = get_idAndPort()
            code1 = 0
            while code1 != 200:
                code1 = add_sensor(sensor_id,rtpport,sensor_name,video_name,config)
            time.sleep(10)
            code2 = 0
            while code2 != 200:
                code2 = add_rule(sensor_id,sensor_name)
            time.sleep(10)
            #instance_id = get_instance_id(sensor_id)
            #stop_instance(instance_id)
            #code3 = 0
            #while code3 != 200:
             #   code3 = delete_instance(instance_id)
            #fsid.write("%s\n"%sensor_id)
            #fiid.write("%s\n"%instance_id)
        break
    #fsid.close()
    #fiid.close()
    fd.close()
