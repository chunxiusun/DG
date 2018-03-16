#!/usr/bin/env python
#-*- coding:utf-8 -*-

import requests,re,json,random,time,os

PORT = "8900"
TYPE = "matrix"

# matrix_align
#IP = "192.168.2.18"
#grpc_port = 9814
#restful_port = 9815
#matrix_config = "config_face_align.json"
#min_port = 19820
#max_port = 19841
#matrix_threads = [1,1,1,1]

# matrix_rec
#IP = "192.168.2.19"
#grpc_port = 9804
#restful_port = 9805
#matrix_config = "config_face_rec.json"
#min_port = 19720
#max_port = 19725
#matrix_threads = [1,1,1,1]

# matrix_ssd
#IP = "192.168.2.162"
#grpc_port = 9800
#restful_port = 9801
#matrix_config = "config_face_ssd.json"
#min_port = 19620
#max_port = 19625
#matrix_threads = [1,1,1,1]

# rank_black
#IP = "192.168.2.162"
#grpc_port = 9808
#restful_port = 9809
#matrix_config = "config_face_rank_black.json"
#min_port = 19520
#max_port = 19521
#matrix_threads = [1,1,1,1]

## rank_runtime
IP = "192.168.2.21"
grpc_port = 9812
restful_port = 9813
matrix_config = "config_face_rank_runtime.json"
min_port = 19420
max_port = 19421
matrix_threads = [1,1]

def creat_instance(matrix_port):
    url = "http://%s:%s/olympus/v1/instance?type=%s"%(IP,PORT,TYPE)
    os.system('''sed -i 's/"Port": .*,/"Port": %d,/' %s'''%(matrix_port, matrix_config))
    os.system('''sed -i 's/"Threads": .*/"Threads": %s/' %s'''%(matrix_threads, matrix_config))
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
    

def run():
    ggid = creat_group(grpc_port)
    rgid = creat_group(restful_port)
    instance_id_dict = {}
    for matrix_port in range(min_port, max_port, 2):
	print matrix_port
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
    run()
    #creat_instance(1111)
