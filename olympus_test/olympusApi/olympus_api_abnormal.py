#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:chunxiusun

import requests,unittest,re,json,random,time,datetime,os

IP = "192.168.2.16"
PORT = "8900"

instance_type = "mock"
instance_config = "mock.json"
node_id = ""

front_port = 3333
back_port = 5555

class TestInstanceAbnormal(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        pass
    
    @classmethod
    def tearDownClass(self):
        print "***start clear environment***"
        batch_deal_instance()
        batch_deal_group()
        print "***end clear environment***"

    def test01_create_instance_without_type(self):
        print "test01_create_instance_without_type:%s"%(datetime.datetime.now())
        url = "http://%s:%s/olympus/v1/instance"%(IP,PORT)
        config = open(instance_config,'r').read()
        pre = [{"pre_fetch_cmd": "echo hello framework!!"}]
        data = {}
        data["config_json"] = config
        data["pre_executor"] = json.dumps(pre)
        r = requests.post(url,data=data)
        print r.status_code
        print r.content
        resp = json.loads(r.content)
        code = resp["Code"]
        self.assertEqual(r.status_code,400)
        self.assertEqual(code,1)

    def test02_create_instance_err_type(self):
        print "test02_create_instance_err_type:%s"%(datetime.datetime.now())
        url = "http://%s:%s/olympus/v1/instance?type=haha"%(IP,PORT)
        config = open(instance_config,'r').read()
        pre = [{"pre_fetch_cmd": "echo hello framework!!"}]
        data = {}
        data["config_json"] = config
        data["pre_executor"] = json.dumps(pre)
        r = requests.post(url,data=data)
        print r.status_code
        print r.content
        resp = json.loads(r.content)
        code = resp["Code"]
        self.assertEqual(r.status_code,400)
        self.assertEqual(code,8)

    def test03_create_instance_without_config(self):
        print "test03_create_instance_without_config:%s"%(datetime.datetime.now())
        url = "http://%s:%s/olympus/v1/instance?type=%s"%(IP,PORT,instance_type)
        data = {}
        pre = [{"pre_fetch_cmd": "echo hello framework!!"}]
        data["pre_executor"] = json.dumps(pre)
        r = requests.post(url,data)
        print r.status_code
        print r.content
        resp = json.loads(r.content)
        code = resp["Code"]
        self.assertEqual(r.status_code,200)
        self.assertEqual(code,0)
        iid = resp["Data"]["instance_id"]
        time.sleep(2)
        #get instance
        time.sleep(10)
        gurl = "http://%s:%s/olympus/v1/instance?iid=%s"%(IP,PORT,iid)
        r1 = requests.get(gurl)
        resp1 = json.loads(r1.content)
        config_json = resp1["Data"]["ConfigJSON"]
        state = resp1["Data"]["State"]
        self.assertEqual(config_json,None)
        self.assertEqual(state,"init")

        
    def test04_get_instance_with_inexistence_iid(self):
        print "test04_get_instance_with_inexistence_iid:%s"%(datetime.datetime.now())
        url = "http://%s:%s/olympus/v1/instance?iid=sun"%(IP,PORT)
        r = requests.get(url)
        print r.status_code
        print r.content
        resp = json.loads(r.content)
        code = resp["Code"]
        self.assertEqual(r.status_code,400)
        self.assertEqual(code,4)
        
    def test05_stop_instance_without_iid(self):
        print "test05_stop_instance_without_iid:%s"%(datetime.datetime.now())
        url = "http://%s:%s/olympus/v1/instance/stop?"%(IP,PORT)
        r = requests.post(url)
        print r.status_code
        print r.content
        resp = json.loads(r.content)
        code = resp["Code"]
        self.assertEqual(r.status_code,400)
        self.assertEqual(code,1)

    def test06_stop_instance_with_inexistence_iid(self):
        print "test06_stop_instance_with_inexistence_iid:%s"%(datetime.datetime.now())
        url = "http://%s:%s/olympus/v1/instance/stop?iid=123"%(IP,PORT)
        r = requests.post(url)
        print r.status_code
        print r.content
        resp = json.loads(r.content)
        code = resp["Code"]
        self.assertEqual(r.status_code,500)
        self.assertEqual(code,5)

    def test07_stop_instance_stopped(self):
        print "test07_stop_instance_stopped:%s"%(datetime.datetime.now())
        curl = "http://%s:%s/olympus/v1/instance?type=%s"%(IP,PORT,instance_type)
        iid = create_instance(curl)
        print iid
        stop_instance(iid)
        url = "http://%s:%s/olympus/v1/instance/stop?iid=%s"%(IP,PORT,iid)
        r = requests.post(url)
        print r.status_code
        print r.content
        resp = json.loads(r.content)
        code = resp["Code"]
        self.assertEqual(r.status_code,200)
        self.assertEqual(code,0)
        #get instance
        gurl = "http://%s:%s/olympus/v1/instance?iid=%s"%(IP,PORT,iid)
        gr = requests.get(gurl)
        gresp = json.loads(gr.content)
        instance_state = gresp["Data"]["State"]
        self.assertEqual(instance_state,"STOPPED")
        #delete_instance(iid)

    def test08_stop_instance_other_node_stopped(self):
        print "test08_stop_instance_other_node_stopped:%s"%(datetime.datetime.now())
        curl = "http://%s:%s/olympus/v1/instance?type=%s&nid=%s"%(IP,PORT,instance_type,node_id)
        iid = create_instance(curl)
        print iid
        stop_instance(iid)
        url = "http://%s:%s/olympus/v1/instance/stop?iid=%s"%(IP,PORT,iid)
        r = requests.post(url)
        print r.status_code
        print r.content
        resp = json.loads(r.content)
        code = resp["Code"]
        self.assertEqual(r.status_code,200)
        self.assertEqual(code,0)
        #get instance
        gurl = "http://%s:%s/olympus/v1/instance?iid=%s"%(IP,PORT,iid)
        gr = requests.get(gurl)
        gresp = json.loads(gr.content)
        instance_state = gresp["Data"]["State"]
        self.assertEqual(instance_state,"STOPPED")
        #delete_instance(iid)

    def test09_start_instance_without_iid(self):
        print "test09_start_instance_without_iid:%s"%(datetime.datetime.now())
        url = "http://%s:%s/olympus/v1/instance/start?"%(IP,PORT)
        r = requests.post(url)
        print r.status_code
        print r.content
        resp = json.loads(r.content)
        code = resp["Code"]
        self.assertEqual(r.status_code,400)
        self.assertEqual(code,1)

    def test10_start_instance_with_inexistence_iid(self):
        print "test10_start_instance_with_inexistence_iid:%s"%(datetime.datetime.now())
        url = "http://%s:%s/olympus/v1/instance/start?iid=123"%(IP,PORT)
        r = requests.post(url)
        print r.status_code
        print r.content
        resp = json.loads(r.content)
        code = resp["Code"]
        self.assertEqual(r.status_code,500)
        self.assertEqual(code,5)

    def test11_start_instance_started(self):
        print "test11_start_instance_started:%s"%(datetime.datetime.now())
        curl = "http://%s:%s/olympus/v1/instance?type=%s"%(IP,PORT,instance_type) 
        iid = create_instance(curl)
        print iid
        url = "http://%s:%s/olympus/v1/instance/start?iid=%s"%(IP,PORT,iid)
        r = requests.post(url)
        print r.status_code
        print r.content
        resp = json.loads(r.content)
        code = resp["Code"]
        self.assertEqual(r.status_code,500)
        self.assertEqual(code,5)
        #get instance
        gurl = "http://%s:%s/olympus/v1/instance?iid=%s"%(IP,PORT,iid)
        gr = requests.get(gurl)
        gresp = json.loads(gr.content)
        instance_state = gresp["Data"]["State"]
        self.assertEqual(instance_state,"RUNNING")
        #delete_instance(iid)

    def test12_start_instance_other_node_started(self):
        print "test12_start_instance_other_node_started:%s"%(datetime.datetime.now())
        curl = "http://%s:%s/olympus/v1/instance?type=%s&nid=%s"%(IP,PORT,instance_type,node_id)
        iid = create_instance(curl)
        print iid
        url = "http://%s:%s/olympus/v1/instance/start?iid=%s"%(IP,PORT,iid)
        r = requests.post(url)
        print r.status_code
        print r.content
        resp = json.loads(r.content)
        code = resp["Code"]
        self.assertEqual(r.status_code,200)
        self.assertEqual(code,0)
        #get instance
        gurl = "http://%s:%s/olympus/v1/instance?iid=%s"%(IP,PORT,iid)
        gr = requests.get(gurl)
        gresp = json.loads(gr.content)
        instance_state = gresp["Data"]["State"]
        self.assertEqual(instance_state,"RUNNING")
        #delete_instance(iid)

    def test13_restart_instance_without_iid(self):
        print "test13_restart_instance_without_iid:%s"%(datetime.datetime.now())
        url = "http://%s:%s/olympus/v1/instance/restart"%(IP,PORT)
        r = requests.post(url)
        print r.status_code
        print r.content
        resp = json.loads(r.content)
        code = resp["Code"]
        self.assertEqual(r.status_code,400)
        self.assertEqual(code,1)

    def test14_restart_instance_inexistence_iid(self):
        print "test14_restart_instance_inexistence_iid:%s"%(datetime.datetime.now())
        url = "http://%s:%s/olympus/v1/instance/restart?iid=123"%(IP,PORT)
        r = requests.post(url)
        print r.status_code
        print r.content
        resp = json.loads(r.content)
        code = resp["Code"]
        self.assertEqual(r.status_code,500)
        self.assertEqual(code,5)

    def test15_restart_instance_stopped(self):
        print "test15_restart_instance_stopped:%s"%(datetime.datetime.now())
        curl = "http://%s:%s/olympus/v1/instance?type=%s"%(IP,PORT,instance_type) 
        iid = create_instance(curl)
        print iid
        stop_instance(iid)
        url = "http://%s:%s/olympus/v1/instance/restart?iid=%s"%(IP,PORT,iid)
        r = requests.post(url)
        print r.status_code
        print r.content
        resp = json.loads(r.content)
        code = resp["Code"]
        self.assertEqual(r.status_code,200)
        self.assertEqual(code,0)
        #get instance
        instance_state = ""
        while instance_state != "RUNNING":
            gurl = "http://%s:%s/olympus/v1/instance?iid=%s"%(IP,PORT,iid)
            gr = requests.get(gurl)
            gresp = json.loads(gr.content)
            instance_state = gresp["Data"]["State"]
            time.sleep(1)
        self.assertEqual(instance_state,"RUNNING")
        #delete_instance(iid)

    def test16_restart_instance_other_node_stopped(self):
        print "test16_restart_instance_other_node_stopped:%s"%(datetime.datetime.now()) 
        curl = "http://%s:%s/olympus/v1/instance?type=%s&nid=%s"%(IP,PORT,instance_type,node_id) 
        iid = create_instance(curl)
        print iid
        stop_instance(iid)
        url = "http://%s:%s/olympus/v1/instance/restart?iid=%s"%(IP,PORT,iid)
        r = requests.post(url)
        print r.status_code
        print r.content
        resp = json.loads(r.content)
        code = resp["Code"]
        self.assertEqual(r.status_code,200)
        self.assertEqual(code,0)
        #get instance
        instance_state = ""
        while instance_state != "RUNNING":
            gurl = "http://%s:%s/olympus/v1/instance?iid=%s"%(IP,PORT,iid)
            gr = requests.get(gurl)
            gresp = json.loads(gr.content)
            instance_state = gresp["Data"]["State"]
            time.sleep(1)
        self.assertEqual(instance_state,"RUNNING")
        #delete_instance(iid)

    def test17_delete_instance_without_iid(self):
        print "test17_delete_instance_without_iid:%s"%(datetime.datetime.now())
        url = "http://%s:%s/olympus/v1/instance/delete"%(IP,PORT)
        r = requests.post(url)
        print r.status_code
        print r.content
        resp = json.loads(r.content)
        code = resp["Code"]
        self.assertEqual(r.status_code,400)
        self.assertEqual(code,1)

    def test18_delete_instance_inexistence_iid(self):
        print "test18_delete_instance_inexistence_iid:%s"%(datetime.datetime.now())
        url = "http://%s:%s/olympus/v1/instance/delete?iid=123"%(IP,PORT)
        r = requests.post(url)
        print r.status_code
        print r.content
        resp = json.loads(r.content)
        code = resp["Code"]
        self.assertEqual(r.status_code,500)
        self.assertEqual(code,5)

    def test19_create_group_without_frontend(self):
        print "test19_create_group_without_frontend:%s"%(datetime.datetime.now())
        url = "http://%s:%s/olympus/v1/group"%(IP,PORT)
        r = requests.post(url)
        print r.status_code
        print r.content
        resp = json.loads(r.content)
        code = resp["Code"]
        self.assertEqual(r.status_code,400)
        self.assertEqual(code,1)

    def test20_get_group_inexistence_gid(self):
        print "test20_get_group_inexistence_gid:%s"%(datetime.datetime.now())
        url = "http://%s:%s/olympus/v1/group?gid=123"%(IP,PORT)
        r = requests.post(url)
        print r.status_code
        print r.content
        resp = json.loads(r.content)
        code = resp["Code"]
        self.assertEqual(r.status_code,400)
        self.assertEqual(code,1)

    def test21_group_add_instance_inexistence_iid(self):
        print "test21_group_add_instance_inexistence_iid:%s"%(datetime.datetime.now())
        gid = create_group()
        print gid
        url = "http://%s:%s/olympus/v1/group/add/instance?gid=%s"%(IP,PORT,gid)
        data = {}
        data["iid"] = "123"
        data["backend"] = "%s:%s"%(IP,back_port)
        r = requests.post(url,data=data)
        print r.status_code
        print r.content
        resp = json.loads(r.content)
        code = resp["Code"]
        self.assertEqual(r.status_code,200)
        self.assertEqual(code,0)

    def test22_group_add_instance_inexistence_gid(self):
        print "test22_group_add_instance_inexistence_gid:%s"%(datetime.datetime.now())
        url = "http://%s:%s/olympus/v1/group/add/instance?gid=123456"%(IP,PORT)
        data = {}
        data["iid"] = "123"
        data["backend"] = "%s:%s"%(IP,back_port)
        r = requests.post(url,data=data)
        print r.status_code
        print r.content
        resp = json.loads(r.content)
        code = resp["Code"]
        self.assertEqual(r.status_code,500)
        self.assertEqual(code,11)

    def test23_group_add_instance_repeat_iid(self):
        print "test23_group_add_instance_repeat_iid:%s"%(datetime.datetime.now())
        gid = create_group()
        print gid
        url = "http://%s:%s/olympus/v1/group/add/instance?gid=%s"%(IP,PORT,gid)
        data = {}
        data["iid"] = "123"
        data["backend"] = "%s:%s"%(IP,back_port)
        r1 = requests.post(url,data=data)
        time.sleep(2)
        r = requests.post(url,data=data)
        print r.status_code
        print r.content
        resp = json.loads(r.content)
        code = resp["Code"]
        self.assertEqual(r.status_code,400)
        self.assertEqual(code,11)

    def test24_group_delete_instance_inexistence_gid(self):
        print "test24_group_delete_instance_inexistence_gid:%s"%(datetime.datetime.now())
        url = "http://%s:%s/olympus/v1/group/del/instance?gid=123456"%(IP,PORT)
        data = {}
        data["iid"] = "123"
        data["backend"] = "%s:%s"%(IP,back_port)
        r = requests.post(url,data=data)
        print r.status_code
        print r.content
        resp = json.loads(r.content)
        self.assertEqual(r.status_code,500)
        self.assertEqual(resp["Code"],11)

    def test25_group_delete_instance_inexistence_iid(self):
        print "test25_group_delete_instance_inexistence_iid:%s"%(datetime.datetime.now())
        gid = create_group()
        print gid
        url = "http://%s:%s/olympus/v1/group/del/instance?gid=%s"%(IP,PORT,gid)
        data = {}
        data["iid"] = "123"
        data["backend"] = "%s:%s"%(IP,back_port)
        r = requests.post(url,data=data)
        print r.status_code
        print r.content
        resp = json.loads(r.content)
        self.assertEqual(r.status_code,400)
        self.assertEqual(resp["Code"],11)

    def test26_delete_group_err_gid(self):
        print "test26_delete_group_err_gid:%s"%(datetime.datetime.now())
        url = "http://%s:%s/olympus/v1/group/delete?gid=123456"%(IP,PORT)
        r = requests.post(url)
        print r.status_code
        print r.content
        resp = json.loads(r.content)
        self.assertEqual(r.status_code,200)
        self.assertEqual(resp["Code"],0)

    def test27_delete_group_without_gid(self):
        print "test27_delete_group_without_gid:%s"%(datetime.datetime.now())
        url = "http://%s:%s/olympus/v1/group/delete"%(IP,PORT)
        r = requests.post(url)
        print r.status_code
        print r.content
        resp = json.loads(r.content)
        self.assertEqual(r.status_code,400)
        self.assertEqual(resp["Code"],1)

    def test28_get_info_inexistence_nid(self):
        print "test28_get_info_inexistence_nid:%s"%(datetime.datetime.now())
        url = "http://%s:%s/olympus/v1/info?nid=1"%(IP,PORT)
        r = requests.get(url)
        print r.status_code
        print r.content
        resp = json.loads(r.content)
        self.assertEqual(r.status_code,404)
        self.assertEqual(resp["Code"],4)

    def test29_get_template_without_type(self):
        print "test29_get_template_without_type:%s"%(datetime.datetime.now())
        url = "http://%s:%s/olympus/v1/template?mode=advanced"%(IP,PORT)
        r = requests.get(url)
        print r.status_code
        print r.content
        resp = json.loads(r.content)
        self.assertEqual(r.status_code,400)
        self.assertEqual(resp["Code"],1)

    def test30_get_template_without_mode(self):
        print "test29_get_template_without_mode:%s"%(datetime.datetime.now())
        url = "http://%s:%s/olympus/v1/template?type=%s"%(IP,PORT,instance_type)
        r = requests.get(url)
        print r.status_code
        print r.content
        resp = json.loads(r.content)
        self.assertEqual(r.status_code,400)
        self.assertEqual(resp["Code"],1)

    def test31_get_template_err_type(self):
        print "test31_get_template_err_type:%s"%(datetime.datetime.now())
        url = "http://%s:%s/olympus/v1/template?type=haha&mode=advanced"%(IP,PORT)
        r = requests.get(url)
        print r.status_code
        print r.content
        resp = json.loads(r.content)
        self.assertEqual(r.status_code,400)
        self.assertEqual(resp["Code"],8)

    def test32_get_template_err_mode(self):
        print "test32_get_template_err_mode:%s"%(datetime.datetime.now())
        url = "http://%s:%s/olympus/v1/template?type=%s&mode=hehe"%(IP,PORT,instance_type)
        r = requests.get(url)
        print r.status_code
        print r.content
        resp = json.loads(r.content)
        self.assertEqual(r.status_code,400)
        self.assertEqual(resp["Code"],-1)

    def test33_modify_instance_without_iid(self):
        print "test33_modify_instance_without_iid:%s"%(datetime.datetime.now())
        url = "http://%s:%s/olympus/v1/instance/mod"%(IP,PORT)
        config = open(instance_config,'r').read()
        data = {}
        data["config_json"] = config
        r = requests.post(url,data=data)
        print r.status_code
        print r.content
        resp = json.loads(r.content)
        self.assertEqual(r.status_code,400)
        self.assertEqual(resp["Code"],1)

    def test34_modify_instance_without_config(self):
        print "test34_modify_instance_without_config:%s"%(datetime.datetime.now())
        curl = "http://%s:%s/olympus/v1/instance?type=%s"%(IP,PORT,instance_type)
        iid = create_instance(curl)
        print iid
        url = "http://%s:%s/olympus/v1/instance/mod?iid=%s"%(IP,PORT,iid)
        data = {}
        r = requests.post(url,data=data)
        print r.status_code
        print r.content
        resp = json.loads(r.content)
        self.assertEqual(r.status_code,400)
        self.assertEqual(resp["Code"],1)
        
    def test35_modify_instance_err_iid(self):
        print "test35_modify_instance_err_iid:%s"%(datetime.datetime.now())
        url = "http://%s:%s/olympus/v1/instance/mod?iid=123"%(IP,PORT)
        config = open(instance_config,'r').read()
        data = {}
        data["config_json"] = config
        r = requests.post(url,data=data)
        print r.status_code
        print r.content
        resp = json.loads(r.content)
        self.assertEqual(r.status_code,500)
        self.assertEqual(resp["Code"],5) 

def create_instance(url):
    #url = "http://%s:%s/olympus/v1/instance?type=%s"%(IP,PORT,instance_type)#&pause_on_created=true"%(IP,PORT,TYPE)
    if instance_type == "matrix":
        os.system('''sed -i 's/"Port": .*,/"Port": %d,/' %s'''%(matrix_port,instance_config))
        os.system('''sed -i 's/"Threads": .*/"Threads": %s/' %s'''%(matrix_threads,instance_config))
    config = open(instance_config,'r').read()
    pre = [{"pre_fetch_cmd": "echo hello framework!!"}]
    data = {}
    data["config_json"] = config
    data["pre_executor"] = json.dumps(pre)
    r = requests.post(url,data=data)
    resp = json.loads(r.content)
    instance_id = resp["Data"]["instance_id"]
    #get instance
    state = ""
    while state != "RUNNING":
        url1 = "http://%s:%s/olympus/v1/instance?iid=%s"%(IP,PORT,instance_id)
        r1 = requests.get(url1)
        resp1 = json.loads(r1.content)
        state = resp1["Data"]["State"]
        time.sleep(1)
    return instance_id

def stop_instance(instance_id):
    url = "http://%s:%s/olympus/v1/instance/stop?iid=%s"%(IP,PORT,instance_id)
    r = requests.post(url)
    resp = json.loads(r.content)
    #get instance
    state = ""
    while state != "STOPPED":
        url1 = "http://%s:%s/olympus/v1/instance?iid=%s"%(IP,PORT,instance_id)
        r1 = requests.get(url1)
        resp1 = json.loads(r1.content)
        state = resp1["Data"]["State"]
        time.sleep(1)

def delete_instance(instance_id):
    url = "http://%s:%s/olympus/v1/instance/delete?iid=%s"%(IP,PORT,instance_id)
    r = requests.post(url)
    resp = json.loads(r.content)
    #get instance
    code_state = 0 
    while code_state != 4:
        url1 = "http://%s:%s/olympus/v1/instance?iid=%s"%(IP,PORT,instance_id)
        r1 = requests.get(url1)
        resp1 = json.loads(r1.content)
        code_state = resp1["Code"]
        time.sleep(1)

def create_group():
    url = "http://%s:%s/olympus/v1/group"%(IP,PORT)
    data = {}
    data["frontend"] = front_port
    r = requests.post(url,data=data)
    #print r.status_code
    #print r.content
    resp = json.loads(r.content)
    code = resp["Code"]
    if code == 0:
        group_id = resp["Data"]["group_id"]
    else:
        group_id = ""
    return group_id

def batch_deal_instance():
    print "delete instance"
    url = "http://%s:%s/olympus/v1/instance"%(IP,PORT)
    r = requests.get(url)
    #print r.status_code
    resp = json.loads(r.content)
    datas = resp["Data"]
    for data in datas:
        iid = data["InstanceId"]
        print iid 
        url1 = "http://%s:%s/olympus/v1/instance/delete?iid=%s"%(IP,PORT,iid)
        r1 = requests.post(url1)
        #print r1.status_code
        #print r1.content

def batch_deal_group():
    print "delete group"
    url = "http://%s:%s/olympus/v1/group"%(IP,PORT)
    r = requests.get(url)
    #print r.status_code
    resp = json.loads(r.content)
    datas = resp["Data"]
    for data in datas:
        gid = data["GroupID"]
        print gid 
        url1 = "http://%s:%s/olympus/v1/group/delete?gid=%s"%(IP,PORT,gid)
        r1 = requests.post(url1)
        #print r1.status_code
        #print r1.content

if __name__ == '__main__':
    #batch_deal_instance()
    #batch_deal_group()
    suite = unittest.TestSuite()

    suite.addTest(TestInstanceAbnormal("test01_create_instance_without_type"))
    suite.addTest(TestInstanceAbnormal("test02_create_instance_err_type"))
    suite.addTest(TestInstanceAbnormal("test03_create_instance_without_config"))
    suite.addTest(TestInstanceAbnormal("test04_get_instance_with_inexistence_iid"))
    suite.addTest(TestInstanceAbnormal("test05_stop_instance_without_iid"))
    suite.addTest(TestInstanceAbnormal("test06_stop_instance_with_inexistence_iid"))
    suite.addTest(TestInstanceAbnormal("test07_stop_instance_stopped"))
    #suite.addTest(TestInstanceAbnormal("test08_stop_instance_other_node_stopped"))
    suite.addTest(TestInstanceAbnormal("test09_start_instance_without_iid"))
    suite.addTest(TestInstanceAbnormal("test10_start_instance_with_inexistence_iid"))
    suite.addTest(TestInstanceAbnormal("test11_start_instance_started"))
    #suite.addTest(TestInstanceAbnormal("test12_start_instance_other_node_started"))
    suite.addTest(TestInstanceAbnormal("test13_restart_instance_without_iid"))
    suite.addTest(TestInstanceAbnormal("test14_restart_instance_inexistence_iid"))
    suite.addTest(TestInstanceAbnormal("test15_restart_instance_stopped"))
    #suite.addTest(TestInstanceAbnormal("test16_restart_instance_other_node_stopped"))
    suite.addTest(TestInstanceAbnormal("test17_delete_instance_without_iid"))
    suite.addTest(TestInstanceAbnormal("test18_delete_instance_inexistence_iid"))
    suite.addTest(TestInstanceAbnormal("test19_create_group_without_frontend"))
    suite.addTest(TestInstanceAbnormal("test20_get_group_inexistence_gid"))
    suite.addTest(TestInstanceAbnormal("test21_group_add_instance_inexistence_iid"))
    suite.addTest(TestInstanceAbnormal("test22_group_add_instance_inexistence_gid"))
    suite.addTest(TestInstanceAbnormal("test23_group_add_instance_repeat_iid"))
    suite.addTest(TestInstanceAbnormal("test24_group_delete_instance_inexistence_gid"))
    suite.addTest(TestInstanceAbnormal("test25_group_delete_instance_inexistence_iid"))
    suite.addTest(TestInstanceAbnormal("test26_delete_group_err_gid"))
    suite.addTest(TestInstanceAbnormal("test27_delete_group_without_gid"))
    suite.addTest(TestInstanceAbnormal("test28_get_info_inexistence_nid"))
    suite.addTest(TestInstanceAbnormal("test29_get_template_without_type"))
    suite.addTest(TestInstanceAbnormal("test30_get_template_without_mode"))
    suite.addTest(TestInstanceAbnormal("test31_get_template_err_type"))
    suite.addTest(TestInstanceAbnormal("test32_get_template_err_mode"))
    suite.addTest(TestInstanceAbnormal("test33_modify_instance_without_iid"))
    suite.addTest(TestInstanceAbnormal("test34_modify_instance_without_config"))
    suite.addTest(TestInstanceAbnormal("test35_modify_instance_err_iid"))

    runner = unittest.TextTestRunner()
    runner.run(suite)
