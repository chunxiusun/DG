#/usr/bin/python
#coding:utf-8

import requests,json

IP_ADDRESS = '192.168.4.226'
SENSORID = 'a1f20f44503532313300000400c4011d'
HEADERS = {'Authorization':'Basic YWRtaW46YWRtaW4='}

def make_events():
    url = 'http://'+IP_ADDRESS+':4151/pub?topic=events'
    dict_source = {"AlarmLevel": 1,
                   "CutboardBox": None,
                   "CutboardTimeOffset": None,
                   "EventType": 220,
                   "EventTypeProbability": 1,
                   "FrameRate": 15,
                   "HotspotId": "undefined",
                   "Id": "6716e2a36c38520001019ab7",
                   "PeopleId": "beb31629c42a40ce99539be8da1600e6",
                   "PlanetId": "undefined",
                   "SceneId": "undefined",
                   "SensorId": "a1f20f44503532313300000400c4011d",
                   "SliceLength": 8000,
                   "StartTime": "2016-05-20T10:00:02.343CST",
                   "TimeLength": 8000,
                   "UserId": ""
                  }
    source = json.dumps(dict_source)
    r = requests.post(url,headers=HEADERS,data=source)
    print r.status_code

def get_tss_detail_paging():
    url = 'http://'+IP_ADDRESS+':1357/api/tssdetailpaging'
    dict_source = {"SensorId":"a1f20f44503532313300000400c4011d",
                   "TimeStamp":"2016-05-20T10:00:00.000+0800",
                   "EndTimeStamp":"2016-05-20T10:30:00.000+0800",
                   "Amount":10,
                   "EventType":220,
                   "Format":"json",
                   "TimeFormat":"string",
                   "Content":"complete",
                   "Merge":True,
                   "FirstSearch":True
                  }
    source = json.dumps(dict_source)
    r = requests.post(url,headers=HEADERS,data=source)
    print r.content
    print r.status_code
    print '========================================================================'

if __name__ == '__main__':
    make_events()
    get_tss_detail_paging()
