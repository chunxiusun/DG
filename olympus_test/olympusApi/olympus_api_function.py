#!/usr/bin/env python
#-*- coding:utf-8 -*-

# author:chunxiusun

import requests,unittest,pexpect,re,json,random,time,os

IP = "192.168.2.16"
PORT = "8900"

instance_type = "vsd"
instance_config = "vsd_config.json"
matrix_port = 6700
matrix_threads = [1]

#instance_type = "importer"
#instance_config = "importer_config.txt"

instance_id = ""

class TestOlympusApi(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        pass
    
    @classmethod
    def tearDownClass(self):
        pass

    def test01_creat_instance(self):
        global instance_id
        url = "http://%s:%s/olympus/v1/instance?type=%s"%(IP,PORT,instance_type)#&pause_on_created=true"%(IP,PORT,TYPE)
        if instance_type == "matrix":
            os.system('''sed -i 's/"Port": .*,/"Port": %d,/' %s'''%(matrix_port,instance_config))
            os.system('''sed -i 's/"Threads": .*/"Threads": %s/' %s'''%(matrix_threads,instance_config))
        config = open(instance_config,'r').read()
        pre = [{"pre_fetch_cmd": "echo hello framework!!"}]
        data = {}
        data["config_json"] = {}#config
        data["pre_executor"] = json.dumps(pre)
        r = requests.post(url,data=data)
        print r.status_code
        print r.content
        resp = json.loads(r.content)
        code = resp["Code"]
        instance_id = resp["Data"]["instance_id"]
        self.assertEqual(r.status_code,200)
        self.assertEqual(code,0)

        #get instance
        url = "http://%s:%s/olympus/v1/instance?iid=%s"%(IP,PORT,instance_id)
	r1 = requests.get(url)
        self.assertEqual(r1.status_code,200)
	resp1 = json.loads(r1.content)
        code1 = resp1["Code"]
        self.assertEqual(code1,0)
        state = resp1["Data"]["State"]
        self.assertEqual(state,"init")

        time.sleep(5)
         
    def test02_start_instance(self):
        #instance_id = "2fea3983943b01859ac96db2e78c35b7"
        url = "http://%s:%s/olympus/v1/instance/start?iid=%s"%(IP,PORT,instance_id)
        r = requests.post(url)
        print r.status_code
        print r.content
        resp = json.loads(r.content)
        code = resp["Code"]
        self.assertEqual(r.status_code,200)
        self.assertEqual(code,0)

        #get instance
        state = ""
        while state!= "RUNNING":
            url = "http://%s:%s/olympus/v1/instance?iid=%s"%(IP,PORT,instance_id)
            r1 = requests.get(url)
            self.assertEqual(r1.status_code,200)
            resp1 = json.loads(r1.content)
            code1 = resp1["Code"]
            self.assertEqual(code1,0)
            state = resp1["Data"]["State"]
        self.assertEqual(state,"RUNNING")

        time.sleep(5)

    def test03_restart_instance(self):
        #instance_id = "2fea3983943b01859ac96db2e78c35b7"
        url = "http://%s:%s/olympus/v1/instance/restart?iid=%s"%(IP,PORT,instance_id)
        r = requests.post(url)
        print r.status_code
        print r.content
        resp = json.loads(r.content)
        code = resp["Code"]
        self.assertEqual(r.status_code,200)
        self.assertEqual(code,0)

        #get instance
        url = "http://%s:%s/olympus/v1/instance?iid=%s"%(IP,PORT,instance_id)
        r1 = requests.get(url)
        self.assertEqual(r1.status_code,200)
        resp1 = json.loads(r1.content)
        code1 = resp1["Code"]
        self.assertEqual(code1,0)
        state = resp1["Data"]["State"]
        self.assertEqual(state,"RUNNING")

        time.sleep(5)

    def test04_stop_instance(self):
        #instance_id = "2fea3983943b01859ac96db2e78c35b7"
        url = "http://%s:%s/olympus/v1/instance/stop?iid=%s"%(IP,PORT,instance_id)
        r = requests.post(url)
        print r.status_code
        print r.content
        resp = json.loads(r.content)
        code = resp["Code"]
        self.assertEqual(r.status_code,200)
        self.assertEqual(code,0)

        #get instance
        state = ""
        while state != "STOPPED":
            url = "http://%s:%s/olympus/v1/instance?iid=%s"%(IP,PORT,instance_id)
            r1 = requests.get(url)
            self.assertEqual(r1.status_code,200)
            resp1 = json.loads(r1.content)
            code1 = resp1["Code"]
            self.assertEqual(code1,0)
            state = resp1["Data"]["State"]                                                                                                     
        self.assertEqual(state,"STOPPED")

        time.sleep(5)

    def test05_delete_instance(self):
        #instance_id = "ba1501e52edb5d390e46ad698450041b"
        url = "http://%s:%s/olympus/v1/instance/delete?iid=%s"%(IP,PORT,instance_id)
        r = requests.post(url)
        print r.status_code
        print r.content
        resp = json.loads(r.content)
        code = resp["Code"]
        self.assertEqual(r.status_code,200)
        self.assertEqual(code,0)

        #get instance
        resp_code = 0
        while resp_code != 400:
            url = "http://%s:%s/olympus/v1/instance?iid=%s"%(IP,PORT,instance_id)
            r1 = requests.get(url)
            resp_code = r1.status_code
            print resp_code
        self.assertEqual(r1.status_code,400)
        resp1 = json.loads(r1.content)
        code1 = resp1["Code"]
        self.assertEqual(code1,4)


if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(TestOlympusApi("test01_creat_instance"))
    #suite.addTest(TestOlympusApi("test02_start_instance"))
    #suite.addTest(TestOlympusApi("test03_restart_instance"))
    #suite.addTest(TestOlympusApi("test04_stop_instance"))
    #suite.addTest(TestOlympusApi("test05_delete_instance"))

    runner = unittest.TextTestRunner()
    runner.run(suite)
