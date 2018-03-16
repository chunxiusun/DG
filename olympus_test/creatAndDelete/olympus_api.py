#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:chunxiusun

import requests,unittest,pexpect,re,json,random,time,os

IP = "192.168.2.16"
PORT = "8900"
TYPE = "mock"
mock_config = "mock_1.json"

front_port = 1111

def creat_instance():
    print "##creat instance##"
    url = "http://%s:%s/olympus/v1/instance?type=%s"%(IP,PORT,TYPE)
    config = open(mock_config,'r').read()
    pre = [{"pre_fetch_cmd": "echo hello framework!!"}]
    data = {}
    data["config_json"] = config
    data["pre_executor"] = json.dumps(pre)
    r = requests.post(url,data=data)
    print r.status_code
    print r.content
    print r.elapsed.microseconds
    resp = json.loads(r.content)
    instance_id = resp["Data"]["instance_id"]

    #get instance
    state = ""
    while state!= "RUNNING":
        url = "http://%s:%s/olympus/v1/instance?iid=%s"%(IP,PORT,instance_id)
        r1 = requests.get(url)
        resp1 = json.loads(r1.content)
        code1 = resp1["Code"]
        state = resp1["Data"]["State"]
    return instance_id

def creat_group():
    print "##creat group##"
    url = "http://%s:%s/olympus/v1/group"%(IP,PORT)
    data = {}
    data["frontend"] = front_port
    r = requests.post(url,data=data)
    print r.status_code
    print r.content
    print r.elapsed.microseconds
    resp = json.loads(r.content)
    code = resp["Code"]
    if code == 0:
        group_id = resp["Data"]["group_id"]
    else:
        group_id = ""
    return group_id

def group_add_instance(gid,iid):
    print "##group add instance##"
    url = "http://%s:%s/olympus/v1/group/add/instance?gid=%s"%(IP,PORT,gid)
    data = {}
    data["iid"] = iid
    data["backend"] = "%s:%s"%(IP,front_port)
    r = requests.post(url,data=data)
    print r.status_code
    print r.content
    print r.elapsed.microseconds

def delete_instance(iid):
    print "##delete instance##"
    url = "http://%s:%s/olympus/v1/instance/delete?iid=%s"%(IP,PORT,iid)                                                              
    r = requests.post(url)                                                                                                           
    print r.status_code                                                                                                               
    print r.content
    print r.elapsed.microseconds
    
    resp_code = 0 
    while resp_code != 400:
        url = "http://%s:%s/olympus/v1/instance?iid=%s"%(IP,PORT,iid)
        r1 = requests.get(url)
        resp_code = r1.status_code

def delete_group(gid):
    print "##delete group##"
    url = "http://%s:%s/olympus/v1/group/delete?gid=%s"%(IP,PORT,gid)                                                                 
    r = requests.post(url)                                                                                                           
    print r.status_code                                                                                                               
    print r.content
    print r.elapsed.microseconds

    resp_code = 0 
    while resp_code != 500:
        url = "http://%s:%s/olympus/v1/group?gid=%s"%(IP,PORT,gid)
        r1 = requests.get(url)
        print r1.status_code
        resp_code = r1.status_code

def run():
    instance_id = creat_instance()
    #group_id = creat_group()
    #group_add_instance(group_id,instance_id)
    #delete_instance(instance_id)
    #delete_group(group_id)

if __name__ == '__main__':
    run()
