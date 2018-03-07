#!/usr/bin/env python
#-*- coding:utf-8 -*-

import time,json,requests,xlrd
import uuid

IP = "10.19.183.165"
PORT = "9876"

sensorID = "2ad10328-af66-43a1-9e81-7eb86d49c7a6"
repoID = "bd6959e3-7735-411c-9cb0-b9ec86b58d66"
sensorFile = "龙岩泉州厦门设备安装点清单.xlsx"

startNum = 61


def get_sensorConfig():
    print "get sensorConfig"
    url = "http://%s:%s/api/config/param?sensor_id=%s"%(IP,PORT,sensorID)
    r = requests.get(url)
    #print r.status_code
    #print r.content
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
    #rtpport = data["Data"]["Port"]
    print sensor_id
    return sensor_id

def add_sensor(sensor_id,sensor_ip,sensor_name,config,comment):
    print "add sensor"
    url = "http://%s:%s/api/device/sensor"%(IP,PORT)
    config["InputSlice"][0]["ConfigInfo"]["SensorInfo"]["SensorID"] = sensor_id
    config["InputSlice"][0]["ConfigInfo"]["RegisterAddress"] = "tcp://%s:9801"%sensor_ip
    config["InputSlice"][0]["ConfigInfo"]["GetMessageAddress"] = "tcp://%s:9800"%sensor_ip
    config["InputSlice"][0]["ConfigInfo"]["ServerPublicKey"] = "111"
    post_data = {
                "Timestamp": int(time.time()*1000),
                "RepoId": "5300",
                "RepoName": "默认部门",
                "SensorId": sensor_id,
                "SensorName": sensor_name,
                "SerialId": sensor_id,
                "Type": 1,
                "Status": 1,
                "LiveActive": False,
                "DataActive": False,
                "Longitude": -200,
                "Latitude": -200,
                "Ip": sensor_ip,
                "Port": "8554",
                "Url": "rtsp://%s:8554/live/main"%sensor_ip,
                "RenderedUrl": "rtsp://%s:8554/live/%s"%(IP,sensor_id),
                "RtmpUrl": "rtmp://%s/live/%s"%(IP,sensor_id),
                "Comment": comment,
                "ConfigJson": json.dumps(config),
                "OlympusId": "",
                "RtpPort": 0
            }
    print post_data
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
    data = xlrd.open_workbook(sensorFile)
    table = data.sheets()[2]
    nrows = table.nrows
    fsid = open("sensor_id.txt",'w')
    for i in range(startNum,nrows):
        print i
        nemo_id = str(table.row(i)[0].value.split('--')[0])
        store_num = str(table.row(i)[0].value.split('--')[1])
        store_name = table.row(i)[1].value.encode("utf8","ignore")
        print nemo_id,store_num,store_name
        sensor_name = nemo_id+store_name
        sensor_ip = "192.168.11.11"
        #sensor_id = str(uuid.uuid4())
        sensor_id = get_idAndPort()
        print sensor_name,sensor_id,sensor_ip
        code1 = 0
        while code1 != 200:
            code1 = add_sensor(sensor_id,sensor_ip,sensor_name,config,store_num)
            time.sleep(2)
        code2 = 0
        while code2 != 200:
            code2 = add_rule(sensor_id,sensor_name)
            time.sleep(2)
        instance_id = get_instance_id(sensor_id)
        #stop_instance(instance_id)
        #code3 = 0
        #while code3 != 200:
        #   code3 = delete_instance(instance_id)
        fsid.write("%s %s %s\n"%(nemo_id,sensor_id,instance_id))
        break
    fsid.close()
