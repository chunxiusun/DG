#!/usr/bin/env python
#-*- coding:utf-8 -*-


import requests,re,json,random,time,os

IP = "192.168.2.222"
PORT = "8080"
TYPE = "vsd"

grpc_port = 9814
restful_port = 9815
matrix_config = "vsd_config.json"
matrix_port_list = []
matrix_threads = [1,1]
start_port = 9821
end_port = 9826#9840

def creat_instance(matrix_port):
    url = "http://%s:%s/olympus/v1/instance?type=%s"%(IP,PORT,TYPE)
    #os.system('''sed -i 's/"Port": .*,/"Port": %d,/' %s'''%(matrix_port,matrix_config))
    #os.system('''sed -i 's/"Threads": .*/"Threads": %s/' %s'''%(matrix_threads,matrix_config))
    config = open(matrix_config,'r').read()
    pre = [{"pre_fetch_cmd": "echo hello framework!!"}]
    data = {}
    data["config_json"] = config
    data["pre_executor"] = json.dumps(pre)
    r = requests.post(url,data=data)
    print r.status_code
    print r.content
    resp = json.loads(r.content)
    code = resp["Code"]
    if code == 0:
        instance_id = resp["Data"]["instance_id"]
    else:
        instance_id = ""
    restful_port = matrix_port + 1
    return instance_id,matrix_port,restful_port

def creat_group(p):
    url = "http://%s:%s/olympus/v1/group"%(IP,PORT)
    data = {}
    data["frontend"] = p
    r = requests.post(url,data=data)
    print r.status_code
    print r.content
    resp = json.loads(r.content)
    code = resp["Code"]
    if code == 0:
        group_id = resp["Data"]["group_id"]
    else:
        group_id = ""
    return group_id

def group_add_instance(ggid,iid,gip):
    url = "http://%s:%s/olympus/v1/group/add/instance?gid=%s"%(IP,PORT,ggid)
    data = {}
    data["iid"] = iid
    data["backend"] = "%s:%s"%(IP,gip)
    r = requests.post(url,data=data)
    print r.status_code
    print r.content
    
def batch_deal_instance():
    url = "http://%s:%s/olympus/v1/instance"%(IP,PORT)
    r = requests.get(url)
    print r.status_code
    resp = json.loads(r.content)
    datas = resp["Data"]
    for data in datas:
        iid = data["InstanceId"]
        #ty = data["Type"]
        #if ty == "vsd":
         #   print iid
          #  continue
	print iid
        url1 = "http://%s:%s/olympus/v1/instance/delete?iid=%s"%(IP,PORT,iid)
        r1 = requests.post(url1)
        print r1.status_code
        print r1.content

def batch_deal_group():
    url = "http://%s:%s/olympus/v1/group"%(IP,PORT)
    r = requests.get(url)
    print r.status_code
    resp = json.loads(r.content)
    datas = resp["Data"]
    for data in datas:
        gid = data["GroupID"]
        print gid
        url1 = "http://%s:%s/olympus/v1/group/delete?gid=%s"%(IP,PORT,gid)
        r1 = requests.post(url1)
        print r1.status_code
        print r1.content

def run():
    ggid = creat_group(grpc_port)
    rgid = creat_group(restful_port)
    instance_id_dict = {}
    for matrix_port in range(start_port,end_port,2):
        instance_id,m_port,r_port = creat_instance(matrix_port)
        instance_id_dict[instance_id] = []
        instance_id_dict[instance_id].append(m_port)
        instance_id_dict[instance_id].append(r_port)
    print instance_id_dict

    for key,value in instance_id_dict.iteritems():
        gip = value[0]
        rip = value[1]
        group_add_instance(ggid,key,gip)
        group_add_instance(rgid,key,rip)

    


if __name__ == '__main__':
    #batch_deal_instance()
    #batch_deal_group()
    #run()
    creat_instance(1234)
    
