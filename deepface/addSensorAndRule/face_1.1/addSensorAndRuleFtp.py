#!/usr/bin/env python
#-*- coding:utf-8 -*-

import time,json,requests,uuid

IP = "192.168.2.222"
PORT = "9876"

ftpServer = "192.168.2.164"
ftpUserName = "sun"
ftpUserPassword = "admin123"
ftpDir = "/home/ftp/"

startNum = 1
endNum = 1
sensorName = u"抓拍机"
sensorId = ""

sensorID = "5d9b4add-48c4-436c-a7b0-2a0dea34d2a1"
repoID = "437f7783-243f-44e1-87cd-bf06dffd75f9"

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

def add_sensor(ftp_dir,sensor_id,sensor_name,config):
    print "add sensor"
    url = "http://%s:%s/api/device/sensor"%(IP,PORT)
    config["InputSlice"][0]["ConfigInfo"]["Address"] = "%s:21"%ftpServer
    config["InputSlice"][0]["ConfigInfo"]["UserName"] = ftpUserName
    config["InputSlice"][0]["ConfigInfo"]["Password"] = ftpUserPassword
    config["InputSlice"][0]["ConfigInfo"]["RootDir"] = ftp_dir
    config["InputSlice"][0]["ConfigInfo"]["SensorInfo"]["SensorID"] = sensor_id
    post_data = {
                "Timestamp": int(time.time()*1000),
                "RepoId": "5300",
                "RepoName": "默认部门",
                "SensorId": sensor_id,
                "SensorName": sensor_name,
                "SerialId":sensor_id,
                "Type": 2,
                "Status": 1,
                "LiveActive": False,
                "DataActive": False,
                "Longitude": -200,
                "Latitude": -200,
                "Ip": "",
                "Port": "",
                "Url": "",
                "RenderedUrl": "rtsp://%s/live/dg-%s"%(IP,sensor_id),
                "RtmpUrl": "",
                "Comment": "",
                "ConfigJson": json.dumps(config),
                "OlympusId": ""
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
    fsid = open("sensor_id.txt",'wa')
    for i in range(startNum,endNum+1):
        ftp_dir = "%s_%s"%(ftpDir,str(i))
        sensor_name = "%s%d"%(sensorName,i)
        sensor_id = str(uuid.uuid4())
        #sensor_id = sensorId
        print sensor_id
        code1 = 0
        while code1 != 200:
            code1 = add_sensor(ftp_dir,sensor_id,sensor_name,config)
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
        fsid.write("%s\n"%sensor_id)
    fsid.close()
