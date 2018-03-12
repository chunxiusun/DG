#/usr/bin/python
#coding:utf -8

import requests,unittest,pxssh,random,json,re

IP_ADDRESS = '192.168.4.215'
USERNAME = 'ubuntu'
PASSWORD = 'ubuntu'
HEADERS = {'Authorization':'Basic YWRtaW46YWRtaW4='}
BUMBLE_PATH = '/data/workspace/package-160510-1462864418/bumble-0.10.6/'
CONFID_PATH = '/data/configs/'
SVR = '192.168.2.26'

class TestBumbleApi(unittest.TestCase):

    def setUp(self):
	global s
        s = pxssh.pxssh()
	s.login (IP_ADDRESS, USERNAME, PASSWORD, original_prompt='[$#>]')

	s.sendline('sudo cp %sbumble.ini %sbumble.ini.bak' % (CONFID_PATH, CONFID_PATH))
	#s.expect(':')
        s.sendline(PASSWORD)
        s.prompt()

    def tearDown(self):
	s.sendline('sudo cp %sbumble.ini.bak %sbumble.ini' % (CONFID_PATH, CONFID_PATH))
	#s.expect(':')
        s.sendline(PASSWORD)
        s.prompt()
	s.close()

    #1.获取bumble版本号
    def	test_get_bumble_version(self):
	url = 'http://' + IP_ADDRESS + ':8008/api/get/version'
	r = requests.get(url,headers=HEADERS)
	self.assertEqual(r.status_code,200)
	s.sendline('cat %sVERSION' % BUMBLE_PATH)
	s.prompt()
	version = s.before.split('\r\n')[1]
	self.assertEqual(r.content.strip(),version)

    #2.获取系统镜像版本号
    def test_get_image_version(self):
	url = 'http://' + IP_ADDRESS + ':8008/api/get/image'
	r = requests.get(url,headers=HEADERS)
        self.assertEqual(r.status_code,200)
	s.sendline ('cat Release')
        s.prompt()
        s_content = s.before.split('\r\n')
	for item in s_content:
	    i = item.split(':')
	    if i[0] == 'Release Version':
		version = i[1].strip()
        self.assertEqual(r.content,version)

    #3.获取产品厂商
    def test_get_manufacture(self):
	url = 'http://' + IP_ADDRESS + ':8008/api/get/manufacture'
	r = requests.get(url,headers=HEADERS)
        self.assertEqual(r.status_code,200)
	s.sendline ('cat Release')
        s.prompt()
        s_content = s.before.split('\r\n')
        for item in s_content:
            i = item.split(':')
            if i[0] == 'Manufacture':
                manufacture = i[1].strip()
        self.assertEqual(r.content,manufacture)

    #4.获取产品型号
    def test_get_model(self):
	url = 'http://' + IP_ADDRESS + ':8008/api/get/model'
        r = requests.get(url,headers=HEADERS)
        self.assertEqual(r.status_code,200)
	s.sendline ('cat Release')
        s.prompt()
        s_content = s.before.split('\r\n')
        for item in s_content:
            i = item.split(':')
            if i[0] == 'Model':
                model = i[1].strip()
        self.assertEqual(r.content,model)

    #5.获取设备序列号
    def test_get_sensorsn(self):
	url = 'http://' + IP_ADDRESS + ':8008/api/get/sensorsn'
        r = requests.get(url,headers=HEADERS)
        self.assertEqual(r.status_code,200)
	s.sendline('sudo /usr/bin/unosafe sn')                                                                                                         
        #s.expect(':')
	s.sendline(PASSWORD)
	s.prompt()                                                                                                               
        sensorsn = s.before.split('\r\n')[1].strip()
        self.assertEqual(r.content,sensorsn)

    #6.获取设备唯一ID
    def test_get_sensorid(self):
	url = 'http://' + IP_ADDRESS + ':8008/api/get/sensorid'
        r = requests.get(url,headers=HEADERS)
        self.assertEqual(r.status_code,200)
	s.sendline('sudo /usr/bin/unosafe id') 
        #s.expect(':')
        #s.sendline(PASSWORD)
        s.prompt()
	s_content = s.before.split('\r\n')                                                                                                               
        sensorid = s_content[1].strip()
        self.assertEqual(r.content,sensorid)

    #7.获取设备名称
    def test_get_hostname(self):
	url = 'http://' + IP_ADDRESS + ':8008/api/get/hostname'
        r = requests.get(url,headers=HEADERS)
        self.assertEqual(r.status_code,200)
	s.sendline('hostname')
        s.prompt()
        hostname = s.before.split('\r\n')[1]
        self.assertEqual(r.content.strip(),hostname)

    #8.获取设备时间
    def test_get_date(self):
	url = 'http://' + IP_ADDRESS + ':8008/api/get/date'
        r = requests.get(url,headers=HEADERS)
        self.assertEqual(r.status_code,200)
	r_content = r.content[:16]+r.content[20:]
	s.sendline('date')
        s.prompt()
        date = s.before.split('\r\n')[1]
	newdate = date[:16]+date[20:]
        self.assertEqual(r_content.strip(),newdate)

    #9.获取设备已经运行的时间
    def test_get_uptime(self):
	url = 'http://' + IP_ADDRESS + ':8008/api/get/uptime'                                                                                
        r = requests.get(url,headers=HEADERS)                                                                                              
        self.assertEqual(r.status_code,200)
	s.sendline('uptime')                                                                                                                 
        s.prompt()                                                                                                                         
        uptime = s.before.split('\r\n')[1].split(',')[0].strip()
        self.assertEqual(r.content.strip(),uptime)

    ##10.获取系统的运行状态
    def test_get_status(self):
	url = 'http://' + IP_ADDRESS + ':8008/api/get/status'
        r = requests.get(url,headers=HEADERS)
        self.assertEqual(r.status_code,200)
        status = '{"cpu":0,"disk":0,"mem":0,"process":0,"usb":0}'
        self.assertEqual(r.content,status)

    #11.获取设备描述
    def test_get_tag(self):
	url = 'http://' + IP_ADDRESS + ':8008/api/get/tag'                                                                                
        r = requests.get(url,headers=HEADERS)                                                                                              
        self.assertEqual(r.status_code,200)
	s.sendline ('cat %sbumble.ini' % CONFID_PATH)
        s.prompt()                                                                                                                         
        s_content = s.before.split('\r\n')                                                                                                 
        for item in s_content:
	    #i = item.split('=')
            #if i[0].strip() == 'devicetag':
	    i = item.split(' = ')
	    if i[0] == 'devicetag':
	        tag = i[1].strip()
		print tag
		print r.content
	self.assertEqual(r.content,tag)

    #12.设置设备描述
    def test_set_tag(self):
	str = 'abcdefghBCDE0123456789.*?@'
	word = random.sample(str,5)
	str1 = ""
	for i in word:
    	    str1 += i
	#print str1
	url = 'http://' + IP_ADDRESS + ':8008/api/set/tag'
        r = requests.post(url,headers=HEADERS,data=str1) 
        self.assertEqual(r.status_code,204)
        
	s.sendline ('cat %sbumble.ini' % CONFID_PATH)
        s.prompt()
        s_content = s.before.split('\r\n')
        for item in s_content:
            #i = item.split('=')
            #if i[0].strip() == 'devicetag':
            i = item.split(' = ')
            if i[0] == 'devicetag':
                tag = i[1].strip()
		print tag
		print str1
        self.assertEqual(str1,tag)           

    #13.1 设置和获取调整时间的方式_手动校时（每次设置都自动重启？？）
    def test_set_get_datesource1(self):
	set_url = 'http://' + IP_ADDRESS + ':8008/api/set/datesource'
	get_url = 'http://' + IP_ADDRESS + ':8008/api/get/datesource'
	setdate = 'wed May 18 18:18:22 CST 2016'
	dict_source = {'Mode':2,
                       'Server':'',
                       'Ntp':'',
                       'Date':setdate
                      }
	datesource = json.dumps(dict_source)
	r1 = requests.post(set_url,headers=HEADERS,data=datesource)
	self.assertEqual(r1.status_code,200) #r1.status_code为200或204不固定？？
	s.sendline('date')
        s.prompt()
        date = s.before.split('\r\n')[1]
        self.assertEqual(setdate,date)
        r2 = requests.get(get_url,headers=HEADERS)
        self.assertEqual(r2.status_code,200)
	s_content = eval(r2.content)                                                                                                 
        self.assertEqual(s_content['Mode'],2)
	self.assertEqual(s_content['Date'],setdate)

    #13.2 设置和获取调整时间的方式_ntp校时
    def test_set_get_datesource2(self):
        set_url = 'http://' + IP_ADDRESS + ':8008/api/set/datesource'
        get_url = 'http://' + IP_ADDRESS + ':8008/api/get/datesource'
	ntp = '192.168.4.41'
	dict_source = {'Mode':1,
                       'Server':'',
                       'Ntp':ntp,
                       'Date':''
                      }
	datesource = json.dumps(dict_source)
        r1 = requests.post(set_url,headers=HEADERS,data=datesource)
        self.assertEqual(r1.status_code,204) #r1.status_code为200或204不固定？？
	r2 = requests.get(get_url,headers=HEADERS)                                                                                         
        self.assertEqual(r2.status_code,200)                                                                                               
        s_content = eval(r2.content)                                                                                                       
        self.assertEqual(s_content['Mode'],1)
	self.assertEqual(s_content['Ntp'],ntp)
	re_date = s_content['Date'][:16]+s_content['Date'][20:]
	#s.sendline('date')
        #s.prompt()                                                                                                                         
        #date = s.before.split('\r\n')[1]                                                                                                   
	s1 = pxssh.pxssh()
        s1.login (ntp, 'ubuntu', 'ubuntu', original_prompt='[$#>]')
	s1.sendline('date')
        s1.prompt()                                                                                                                         
        ntpdate1 = s1.before.split('\r\n')[1]
	ntpdate = ntpdate1[:16]+ntpdate1[20:]
	s1.close()                                                                                                   
        self.assertEqual(re_date,ntpdate)#不对比秒

    #13.3 设置和获取调整时间的方式_网管服务器校时
    def test_set_get_datesource3(self):
        set_url = 'http://' + IP_ADDRESS + ':8008/api/set/datesource'
        get_url = 'http://' + IP_ADDRESS + ':8008/api/get/datesource'
        svr = '192.168.2.26'#26上没有ntp服务，无法对时
        dict_source = {'Mode':0,
                       'Server':svr,
                       'Ntp':'',
                       'Date':''
                      }
        datesource = json.dumps(dict_source)
        r1 = requests.post(set_url,headers=HEADERS,data=datesource)
        self.assertEqual(r1.status_code,204) #r1.status_code为200或204不固定？？
        r2 = requests.get(get_url,headers=HEADERS)
        self.assertEqual(r2.status_code,200)
        s_content = eval(r2.content)
        self.assertEqual(s_content['Mode'],0)
	self.assertEqual(s_content['Server'],svr)
	re_date = s_content['Date'][:16]+s_content['Date'][20:]
        #s.sendline('date')
        #s.prompt()                                                                                                                         
        #date = s.before.split('\r\n')[1]                                                                                                   
        s1 = pxssh.pxssh()
        s1.login (svr, 'deepglint', 'dg2015', original_prompt='[$#>]')
        s1.sendline('date')                                                                                                                
        s1.prompt()                                                                                                                         
        svrdate1 = s1.before.split('\r\n')[1]
	svrdate = svrdate1[:16]+svrdate1[20:]                                                                                               
        s1.close()                                                                                                                         
        self.assertEqual(re_date,svrdate)#不对比秒
    
    #14.获取服务器地址
    def test_get_serveraddr(self):
	url = 'http://' + IP_ADDRESS + ':8008/api/get/serveraddr'
        r = requests.get(url,headers=HEADERS)
        self.assertEqual(r.status_code,200)
	s.sendline ('cat %sbumble.ini' % CONFID_PATH)                                                                                      
        s.prompt()                                                                                                                         
        s_content = s.before.split('\r\n')                                                                                                 
        for item in s_content:                                                                                                             
            i = item.split(' = ')                                                                                                          
            if i[0] == 'serveraddr':                                                                                                        
                serveraddr = i[1].strip()
        self.assertEqual(r.content,serveraddr)

    #15.设置服务器地址
    def test_set_serveraddr(self):
	#svr = '192.168.2.31'
	url = 'http://' + IP_ADDRESS + ':8008/api/set/serveraddr?addr='+SVR
        #values = '192.168.2.31'
        #r = requests.post(url,headers=HEADERS,addr=values)
	r = requests.post(url,headers=HEADERS)
        self.assertEqual(r.status_code,204)

	s.sendline ('cat %sbumble.ini' % CONFID_PATH)
        s.prompt()
        s_content = s.before.split('\r\n')
        for item in s_content:
            i = item.split(' = ')
            if i[0] == 'serveraddr':
                serveraddr = i[1].strip()
        self.assertEqual(SVR,serveraddr) 

    #16.获取设备的网络配置
    def test_get_network(self):
	url = 'http://' + IP_ADDRESS + ':8008/api/get/network'
        r = requests.get(url,headers=HEADERS)
        self.assertEqual(r.status_code,200)
	r_content = eval(r.content)
	s.sendline ('cat /etc/network/interfaces')
	s.prompt()
        s_content = s.before.split('\r\n')
	for item in s_content:
	    if 'address' in item:
		address = item.split(' ')[1]
	    elif 'netmask' in item:
                netmask = item.split(' ')[1]
            elif 'gateway' in item:
                gateway = item.split(' ')[1]
            elif 'dns-nameservers' in item:
                maindns = item.split(' ')[1]
                subdns = item.split(' ')[2]
	self.assertEqual(r_content['address'],address)
	self.assertEqual(r_content['netmask'],netmask)
	self.assertEqual(r_content['gateway'],gateway)
	self.assertEqual(r_content['maindns'],maindns)
	self.assertEqual(r_content['subdns'],subdns)

    #17.设置设备的网络配置
    def test_set_network(self):
	url = 'http://' + IP_ADDRESS + ':8008/api/set/network'
        dict_network = {"address":"192.168.4.50",
                        "netmask":"255.255.255.0",
                        "gateway":"192.168.4.254",
                        "maindns":"202.106.0.10",
                        "subdns":"202.106.46.252"
                       }
        s.sendline('sudo cp /etc/network/interfaces  /etc/network/interfaces.bak')
	#s.expect(':')
        s.sendline(PASSWORD)
        s.prompt()
        source = json.dumps(dict_network)
	r = requests.post(url,headers=HEADERS,data=source) #只修改了ip
        self.assertEqual(r.status_code,200)
	s.sendline('cat /etc/network/interfaces')
	s.prompt()                                                                                                                         
        s_content = s.before.split('\r\n')
	for item in s_content:                                                                                                             
            if 'address' in item:                                                                                                          
                address = item.split(' ')[1]                                                                                               
            elif 'netmask' in item:                                                                                                        
                netmask = item.split(' ')[1]                                                                                               
            elif 'gateway' in item:                                                                                                        
                gateway = item.split(' ')[1]                                                                                               
            elif 'dns-nameservers' in item:                                                                                                
                maindns = item.split(' ')[1].split(',')[0]                                                                                 
                #subdns = item.split(' ')[1].split(',')[1] #列表索引超出范围
		subdns = item.split(' ')[2]
	s.sendline('sudo cp /etc/network/interfaces.bak  /etc/network/interfaces')
        #s.expect(':')
        s.sendline(PASSWORD)
	s.prompt()
	self.assertEqual(dict_network['address'],address)                                                                                     
        self.assertEqual(dict_network['netmask'],netmask)                                                                                     
        self.assertEqual(dict_network['gateway'],gateway)                                                                                     
        self.assertEqual(dict_network['maindns'],maindns)                                                                                     
        self.assertEqual(dict_network['subdns'],subdns)  

    #18.获取ntp服务器地址
    def test_get_ntp(self):
	url = 'http://' + IP_ADDRESS + ':8008/api/get/ntpaddr'
        r = requests.get(url,headers=HEADERS)
        self.assertEqual(r.status_code,200)
	s.sendline ('cat %sbumble.ini' % CONFID_PATH)
        s.prompt()
        s_content = s.before.split('\r\n')
        for item in s_content:
            i = item.split(' = ')
            if i[0] == 'ntpaddr':
                ntpaddr = i[1].strip()
        self.assertEqual(r.content,ntpaddr)

    #19.获取NVR服务器信息
    def test_get_nvrconfig(self):
	url = 'http://' + IP_ADDRESS + ':8008/api/get/nvrconfig'
        r = requests.get(url,headers=HEADERS)
        self.assertEqual(r.status_code,200)
	r_content = eval(r.content)
	s.sendline ('cat %sbumble.ini' % CONFID_PATH)                                                                                      
        s.prompt()                                                                                                                         
        s_content = s.before.split('\r\n')
	for item in s_content:
	    i = item.split(' = ')                                                                                                          
            if i[0] == 'address':                                                                                                          
                address = i[1].strip()
	    elif i[0] == 'port':
		if ':'in i[1]:#过滤掉第一个port
                    return
		port = eval(i[1].strip()) #有两个port
	    elif i[0] == 'username':
		username = i[1].strip()
	    elif i[0] == 'password':
		password = i[1].strip()
	    elif i[0] == 'channel':
		channel = i[1].strip()
	    elif i[0] == 'model':
		model = i[1].strip()
        self.assertEqual(r_content['address'],address)
	self.assertEqual(r_content['port'],port)
	self.assertEqual(r_content['username'],username)
	self.assertEqual(r_content['password'],password)
	self.assertEqual(r_content['channel'],channel)
	self.assertEqual(r_content['model'],model)

    #20.设置NVR服务器信息
    def test_set_nvrconfig(self):
	url = 'http://' + IP_ADDRESS + ':8008/api/set/nvrconfig'
        dict_source = {"address":"192.168.11.116",
                  "port":8000,
                  "username":"admin",
                  "password":"admin123",
                  "channel":6,
                  "model":"海康威视"
                 }
	datesource = json.dumps(dict_source)
        r = requests.post(url,headers=HEADERS,data=datesource)
        self.assertEqual(r.status_code,204) 
	
	s.sendline ('cat %sbumble.ini' % CONFID_PATH)
        s.prompt()
        s_content = s.before.split('\r\n')
        for item in s_content:
            i = item.split(' = ')
            if i[0] == 'address':
                address = i[1].strip()
            elif i[0] == 'port':                                                                                                           
                if ':'in i[1]:#过滤掉第一个port                                                                                            
                    return                                                                                                                 
                port = eval(i[1].strip()) #有两个port                                                                                      
            elif i[0] == 'username':                                                                                                       
                username = i[1].strip()                                                                                                    
            elif i[0] == 'password':                                                                                                       
                password = i[1].strip()                                                                                                    
            elif i[0] == 'channel':                                                                                                        
                channel = i[1].strip()                                                                                                     
            elif i[0] == 'model':                                                                                                          
                model = i[1].strip()                                                                                                       
        self.assertEqual(dict_source['address'],address)                                                                                     
        self.assertEqual(dict_source['port'],port)                                                                                           
        self.assertEqual(dict_source['username'],username)                                                                                   
        self.assertEqual(dict_source['password'],password)                                                                                   
        self.assertEqual(dict_source['channel'],channel)                                                                                     
        self.assertEqual(dict_source['model'],model)

    #21.登录
    def test_set_login(self):
	url = 'http://' + IP_ADDRESS + ':8008/api/set/login'
        values = 'admin:admin'
        r = requests.post(url,data=values)
        self.assertEqual(r.status_code,200)
	self.assertEqual(r.content,'true')

	value1 = 'admin:admin1'                                                                                                             
        r = requests.post(url,data=value1)                                                                                                 
        self.assertEqual(r.status_code,400)                                                                                                
        self.assertEqual(r.content,'auth fail') 
    #22.设置新的密码(该接口不需要basic auth 验证)
    def test_set_changepwd(self):
	url = 'http://' + IP_ADDRESS + ':8008/api/set/changepwd'
        values = 'admin:admin:admin123'
        r = requests.post(url,headers=HEADERS,data=values)
        self.assertEqual(r.status_code,200)
	self.assertEqual(r.content,'SUCCESS')

    #23.重置用户名和密码为admin:admin
    def test_resetpwd(self):
	url = 'http://' + IP_ADDRESS + ':8008/api/set/resetpwd'
        headers = {'Authorization':'Basic YWRtaW46YWRtaW4xMjM='}
        r = requests.post(url,headers=headers)
        self.assertEqual(r.status_code,200) 
        self.assertEqual(r.content,'SUCCESS')

    #24.获取进程列表                                                                                                                      
    def test_get_processlist(self):
        url = 'http://' + IP_ADDRESS + ':8008/api/get/processlist'
        r = requests.get(url,headers=HEADERS)
        self.assertEqual(r.status_code,200)
        re_content = eval(r.content)
        re_list = []
        for item in re_content:
            re_list.append(item['Name'])
        s.sendline('sudo supervisorctl status')
        #s.expect(':')
        #s.sendline(PASSWORD)
        s.prompt()
        s_content = s.before.strip().split('\r\n')[1:]
        s_list = []
        for item in s_content:
	    i = item.split()
            s_list.append(item.split()[0])
        self.assertEqual(sorted(re_list),sorted(s_list))
    
if __name__ == '__main__':
    #unittest.main()
    #构造测试集
    suite = unittest.TestSuite()
    suite.addTest(TestBumbleApi("test_get_bumble_version"))
    suite.addTest(TestBumbleApi("test_get_image_version"))
    suite.addTest(TestBumbleApi("test_get_manufacture"))
    suite.addTest(TestBumbleApi("test_get_model"))
    suite.addTest(TestBumbleApi("test_get_sensorsn"))
    suite.addTest(TestBumbleApi("test_get_sensorid"))
    suite.addTest(TestBumbleApi("test_get_hostname"))
    suite.addTest(TestBumbleApi("test_get_date"))
    suite.addTest(TestBumbleApi("test_get_uptime"))
    suite.addTest(TestBumbleApi("test_get_status"))
    #suite.addTest(TestBumbleApi("test_get_tag"))
    suite.addTest(TestBumbleApi("test_set_tag"))
    #suite.addTest(TestBumbleApi("test_set_get_datesource1"))
    suite.addTest(TestBumbleApi("test_set_get_datesource2"))
    suite.addTest(TestBumbleApi("test_set_get_datesource3"))
    suite.addTest(TestBumbleApi("test_set_serveraddr"))
    suite.addTest(TestBumbleApi("test_get_serveraddr"))
    #suite.addTest(TestBumbleApi("test_set_network"))
    suite.addTest(TestBumbleApi("test_get_network"))
    suite.addTest(TestBumbleApi("test_get_ntp"))
    suite.addTest(TestBumbleApi("test_get_nvrconfig"))
    #suite.addTest(TestBumbleApi("test_set_nvrconfig"))
    suite.addTest(TestBumbleApi("test_set_login"))
    suite.addTest(TestBumbleApi("test_set_changepwd"))
    suite.addTest(TestBumbleApi("test_resetpwd"))
    suite.addTest(TestBumbleApi("test_get_processlist"))

    #执行测试
    runner = unittest.TextTestRunner()
    runner.run(suite)
