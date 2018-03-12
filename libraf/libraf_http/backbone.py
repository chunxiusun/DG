#!/usr/bin/python
#coding:UTF-8
# author : chunxiusun

import requests,unittest,pexpect,re,json,random,time

IP_ADDRESS = '192.168.5.203'
PORT = '9000'
SENSORID = 'a1f20f44503532313300000400fa0109'
USERNAME = 'ubuntu'
PASSWORD = 'ubuntu'
HEADERS = {'Authorization':'Basic YWRtaW46YWRtaW4='}

class TestBackboneApi(unittest.TestCase):
    @classmethod
    def setUpClass(self):
	pass
        '''global p
        p = pexpect.spawn('ssh %s@%s' % (USERNAME, IP_ADDRESS), timeout=60)
        index = p.expect(['.*/no\)\?','.*ssword:', pexpect.EOF, pexpect.TIMEOUT])
        if index == 0 or index == 1:
           if index == 0 : 
              p.sendline('yes')
              p.expect('.*ssword:')
           p.sendline(PASSWORD)
           p.expect('\$')
        else:
           print "ssh login failed, due to TIMEOUT or EOF"
         '''

    @classmethod
    def tearDonwClass(self):
        pass
        #p.close()

    #图传
    def set_get_imgcaptureproperties(self):
        url1 = 'http://%s:%s/api/setimgcaptureproperties'%(IP_ADDRESS,PORT)
	ip_lst = ["192.168.5.174","192.168.2.13","192.168.1.79","192.168.4.41"]
	body_ip = random.choice(ip_lst)
	print "body_ip:%s" % body_ip
	face_ip = random.choice(ip_lst)
	print "face_ip:%s" % face_ip
	body_port = random.randint(1,9999)
	print "body_port:%s" % body_port
	face_port = random.randint(1,9999)
	print "face_port:%s" % face_port
	dict_source = {"DetTasks":["RpcFace","RpcBody"],
                       "ImgTransList":["RpcFace","RpcBody"],
                       "ImgTransProps":{"RpcBody":{"format":"RPC_JPEG","ip":body_ip,"port":body_port},
                                        "RpcFace":{"format":"RPC_JPEG","ip":face_ip,"port":face_port},
                                        "RpcCar":{"format":"RPC_JPEG","ip":"192.168.5.107","port":9900}
                                       }
                      }
	print dict_source
	datesource = json.dumps(dict_source)
        r1 = requests.post(url1,data=datesource)
	#print r1.status_code

	tamp = int(time.time())
	#print tamp
	url2 = 'http://%s:%s/api/getimgcaptureproperties?_=%s'%(IP_ADDRESS,PORT,tamp)
	r2 = requests.get(url2)
	print r2.status_code
	r_content = eval(r2.text)
	print r_content
	b_ip = r_content["data"]["ImgTransProps"]["RpcBody"]["ip"]
	b_port = r_content["data"]["ImgTransProps"]["RpcBody"]["port"]
	f_ip = r_content["data"]["ImgTransProps"]["RpcFace"]["ip"]
	f_port = r_content["data"]["ImgTransProps"]["RpcFace"]["port"]
	
        self.assertEqual(r1.status_code,200)
	self.assertEqual(r2.status_code,200)
	self.assertEqual(b_ip,body_ip)
	self.assertEqual(b_port,body_port)
	self.assertEqual(f_ip,face_ip)
	self.assertEqual(f_port,face_port)
	



if __name__ == '__main__':
    suite = unittest.TestSuite()

    suite.addTest(TestBackboneApi("set_get_imgcaptureproperties"))

    #执行测试                                                                                                                              
    runner = unittest.TextTestRunner()    
    runner.run(suite)
