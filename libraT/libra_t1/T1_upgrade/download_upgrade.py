#!/usr/bin/python
#coding:utf-8

import requests,json,commands,re,time

VERSION = 'V2.13.160623R'
SENSOR_IP = '192.168.4.226' 
SENSORID = 'a1f20f44503532313300000400c4011d' 
SERVER_IP = '192.168.4.41' 

def SensorDownload():
    global p                                                                                                                      
    c = commands.getoutput('curl –L http://127.0.0.1:4001/v2/keys/config/global/download')
    p = re.compile('.*?"value":"(.*?)",".*?')
    dwl = re.findall(p,c)
    if dwl != 'TOBE':
        print 'download status:'+dwl
    else:
	url = 'http://'+SENSOR_IP+':4151/pub?topic=cmd_topic'
        data = {"SessionId":"123456","Cmd":"download_package","Params":{}}
        value = json.dumps(data)                        
        r = requests.post(url, data = value)                                                                                                   
        print r.status_code,r.content
        while True:
	    time.sleep(3)
	    cd = commands.getoutput('curl –L http://127.0.0.1:4001/v2/keys/config/global/download')
            #pd = re.compile('.*?"value":"(.*?)",".*?')
            download = re.findall(p,cd)
	    cv = commands.getoutput('curl –L http://127.0.0.1:4001/v2/keys/config/global/dwn_version')
            #pv = re.compile('.*?"value":"(.*?)",".*?')
            dwn_version = re.findall(p,cv)
            if download == 'DONE' and dwn_version == VERSION:
	        print 'The download is complete.'
	        break
	                                                                                            
#升级之后设备重启
def SensorUpgrade():
    c = commands.getoutput('curl –L http://127.0.0.1:4001/v2/keys/config/global/upgrade')
    upgrade = re.findall(p,c)
    if upgrade != 'TOBE':
	print 'upgrade status:'+upgrade
    else:
	url = 'http://'+SENSOR_IP+':4151/pub?topic=cmd_topic'                                                                                  
        data = {"SessionId":"123456","Cmd":"switch_package","Params":{}}                                                                       
        value = json.dumps(data)                                                                                                               
        r = requests.post(url, data = value)                                                                                                   
        print r.status_code,r.content
        print 'TK1 is upgrading and will restart...'


def ServerDownload():
    c = commands.getoutput('curl –L http://127.0.0.1:4001/v2/keys/config/global/download')
    dwl = re.findall(p,c)
    if dwl != 'TOBE':
        print 'download status:'+dwl
    else:                                  
        url = 'http://'+SERVER_IP+':4151/pub?topic=bumble_cmd_to_'+SENSORID                                                                    
        data = {"SessionId":"123456","UserId":"deepglint","SensorId":SENSORID,"Cmd":"download_package","Params":{}}                            
        value = json.dumps(data)
        r = requests.post(url, data = value)                                                                                                    
        print r.status_code,r.content                                                                                                                    
        while True:
            time.sleep(3)
            cd = commands.getoutput('curl –L http://127.0.0.1:4001/v2/keys/config/global/download')
            #pd = re.compile('.*?"value":"(.*?)",".*?')
            download = re.findall(p,cd)
            cv = commands.getoutput('curl –L http://127.0.0.1:4001/v2/keys/config/global/dwn_version')
            #pv = re.compile('.*?"value":"(.*?)",".*?')
            dwn_version = re.findall(p,cv)
            if download == 'DONE' and dwn_version == VERSION:
                print 'The download is complete.'
                break

#升级之后设备重启
def ServerUpgrade():
    c = commands.getoutput('curl –L http://127.0.0.1:4001/v2/keys/config/global/upgrade')
    upgrade = re.findall(p,c)
    if upgrade != 'TOBE':
        print 'upgrade status:'+upgrade
    else:                                                                                                                       
        url = 'http://'+SERVER_IP+':4151/pub?topic=bumble_cmd_to_'+SENSORID                                                                    
        data = {"SessionId":"123456","UserId":"deepglint","SensorId":SENSORID,"Cmd":"switch_package","Params":{}}                              
        value = json.dumps(data)
        r = requests.post(url, data = value)                                                                                                    
        print r.status_code,r.content
        print 'TK1 is upgrading and will restart...'

if __name__ == '__main__':                                                                                                                 
    #sensor
    SensorDownload()
    SensorUpgrade()
    
    #server
    ServerDownload()                                                                                                                      
    ServerUpgrade()                                                                                                                       
