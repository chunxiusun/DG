#/usr/bin/python
#coding:UTF-8

import requests,unittest,pexpect,re,json,random,time

IP_ADDRESS = '192.168.5.153'
PORT = '8004'
SENSORID = 'a1f20f44503532313300000400fa0109'
USERNAME = 'ubuntu'
PASSWORD = 'ubuntu'
HEADERS = {'Authorization':'Basic YWRtaW46YWRtaW4='}
SERVICE = 'vulcand'
RESTART_SERVICE = 'adu'
ETCD_PATH = 'http://127.0.0.1:2379/v2/keys/config/'
SERVER_IP = '192.168.2.26'
TAG = ''

class TestOptimusApi(unittest.TestCase):
    @classmethod
    def setUpClass(self):
	global s
	s = pexpect.spawn('ssh %s@%s' % (USERNAME, IP_ADDRESS), timeout=60)
	index = s.expect(['.*/no\)\?','.*ssword:', pexpect.EOF, pexpect.TIMEOUT])
        if index == 0 or index == 1:
           if index == 0 :
              s.sendline('yes')
              s.expect('.*ssword:')
           s.sendline(PASSWORD)
           s.expect('\$')
	else:
           print "ssh login failed, due to TIMEOUT or EOF"

    @classmethod
    def tearDonwClass(self):
	pass
	s.close()

    #1 获取optimus版本信息的API，从`VERSION`文件读取，异常返回文件不存在
    def get_version(self):
	url = 'http://%s:%s/api/get/version'%(IP_ADDRESS,PORT)
        r = requests.get(url,headers=HEADERS)
        self.assertEqual(r.status_code,200)
	
    #2 添加获取服务器系统版本的接口，依赖文件'/data/version/Release'
    def get_image(self):
	url = 'http://%s:%s/api/get/image'%(IP_ADDRESS,PORT)
        r = requests.get(url,headers=HEADERS)
        self.assertEqual(r.status_code,200)
	s.sendline('cat /data/version/Release')                                                                                                              
        s.expect("\$")                                                                                                                     
        data = s.before.split('\r\n')[1]
	self.assertEqual(r.content.strip(),data)

    #3 获取该设备关联的服务器地址信息，服务器地址信息存储在etcd内，键值为`config/optimus/server`
    def get_server(self):
	url = 'http://%s:%s/api/get/server'%(IP_ADDRESS,PORT)
        r = requests.get(url,headers=HEADERS)
        self.assertEqual(r.status_code,200)
	#判断关联的服务器是否为空
	value = ''
	if r.content == '':
	    s.sendline('curl -L %soptimus/'% ETCD_PATH)                                                                                  
            s.expect("\$")                                                                                                                     
            data = s.before
	    if 'server' not in data:
		value = ''
	else:
	    s.sendline('curl -L %soptimus/server'% ETCD_PATH)
            s.expect("\$")
	    data = s.before
	    pattern = re.compile('((?<=value":").*?(?="))',re.S)
	    value = re.findall(pattern,data)[0]
	self.assertEqual(r.content.strip(),value)

    #4 设置该设备关联的服务器地址信息，服务器地址设置完毕会切换与服务器的通道
    def set_server(self):
	url = 'http://%s:%s/api/set/server?addr=%s'%(IP_ADDRESS,PORT,SERVER_IP)                                                                              
        r = requests.post(url,headers=HEADERS)                                                                                              
	self.assertEqual(r.status_code,201)
	value = ''
	#判断关联的服务器是否设置为空
	if SERVER_IP == '':
	    s.sendline('curl -L %soptimus/'% ETCD_PATH)                                                                                    
            s.expect("\$")                                                                                                                     
            data = s.before                                                                                                                
            if 'server' not in data:                                                                                                       
                value = ''
	else:
	    s.sendline('curl -L %soptimus/server'% ETCD_PATH)                                                                                  
            s.expect("\$")                                                                                                                     
            data = s.before
            pattern = re.compile('((?<=value":").*?(?="))',re.S)                                                                                    
            value = re.findall(pattern,data)[0]
	self.assertEqual(SERVER_IP,value)

    #5 获取该设备的描述信息，描述信息存储在etcd内，键值为`config/optimus/tag`，如：`北京.海淀.青龙桥.格灵深瞳`
    def get_tag(self):
	url = 'http://%s:%s/api/get/tag'%(IP_ADDRESS,PORT)                                                                              
        r = requests.get(url,headers=HEADERS)                                                                                              
        self.assertEqual(r.status_code,200)
	#判断描述信息是否为空                                                                                                          
        value = ''                                                                                                                         
        if r.content == '':                                                                                                                
            s.sendline('curl -L %soptimus/'% ETCD_PATH)                                                                                    
            s.expect("\$")                                                                                                                     
            data = s.before                                                                                                                
            if 'tag' not in data:                                                                                                       
                value = ''                                                                                                                 
        else:                                                                                                                              
            s.sendline('curl -L %soptimus/tag'% ETCD_PATH)                                                                              
            s.expect("\$")                                                                                                                 
            data = s.before
	    p = re.compile(r'\\')
	    data1 = re.sub(p,'',data) #描述为中文
            pattern = re.compile('((?<=value":").*?(?=",))',re.S)                                                                           
            value = re.findall(pattern,data)[0]                                                                                            
        self.assertEqual(r.content.strip(),value)

    #6 设置该设备的描述信息
    def set_tag(self):
	str = 'abcdefghigkslmnBCDE0123456789.*?@'
        word = random.sample(str,8)
        str1 = ""
        for i in word:
            str1 += i
	TAG = str1
	#print TAG
	url = 'http://%s:%s/api/set/tag?tag=%s'%(IP_ADDRESS,PORT,TAG)
        r = requests.post(url,headers=HEADERS)
        self.assertEqual(r.status_code,201)
        value = ''
        #判断设备描述是否设为空
        if TAG == '':
            s.sendline('curl -L %soptimus/'% ETCD_PATH)
            s.expect("\$")
            data = s.before
            if 'tag' not in data:
                value = ''
        else:
            s.sendline('curl -L %soptimus/tag'% ETCD_PATH)
            s.expect("\$")
            data = s.before
	    p = re.compile(r'\\')
            data1 = re.sub(p,'',data) #描述为中文
            pattern = re.compile('((?<=value":").*?(?=",))',re.S)
            value = re.findall(pattern,data1)[0]
        self.assertEqual(TAG,value)

    #7 获取该设备的网络配置信息
    def get_network(self):
	url = 'http://%s:%s/api/get/network'%(IP_ADDRESS,PORT)                                                                                 
        r = requests.get(url,headers=HEADERS)                                                                                              
        self.assertEqual(r.status_code,200)
	r_content = eval(r.content)
	s.sendline('cat /etc/network/interfaces')                                                                                 
        s.expect("\$")                                                                                                                 
        data = s.before
	pattern = re.compile(r'(?<=static\r\n\t).*?(?=\r\n\r\nubuntu)',re.S)
	data1 = re.findall(pattern,data)[0].split('\r\n\t')
	data_dict = {}
	for item in data1:
	    if 'address' in item:
		data_dict['address'] = item.split()[1]
	    if 'netmask' in item:
		data_dict['netmask'] = item.split()[1]
	    if 'gateway' in item:
		data_dict['gateway'] = item.split()[1]
	    if 'dns-nameservers' in item:
		data_dict['maindns'] = item.split()[1]
		data_dict['subdns'] = item.split()[2] 
	self.assertEqual(r_content,data_dict)
   
    #9、10 获取和设置调整时间的方式_网管服务器校时
    def set_get_datesource0(self):
	set_url = 'http://%s:%s/api/set/datesource'%(IP_ADDRESS,PORT)
        get_url = 'http://%s:%s/api/get/datesource'%(IP_ADDRESS,PORT)
	svr = '192.168.4.41'
	pawd = 'ubuntu'                                                                               
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
        s1 = pexpect.spawn('ssh ubuntu@%s' % (svr, ), timeout=60)
        s1.sendline(pawd)
        s1.expect("\$")
        s1.sendline('date')                                                                                                                
        s1.expect("\$")                          
	svrdate1 = s1.before.split('\r\n')[1]                                                                                              
        svrdate = svrdate1[:16]+svrdate1[20:]                                                                                               
        s1.close()                                                                                                                         
        self.assertEqual(re_date,svrdate)#不对比秒

    #9、10 获取和设置调整时间的方式_ntp服务校时
    def set_get_datesource1(self):
        set_url = 'http://%s:%s/api/set/datesource'%(IP_ADDRESS,PORT)
        get_url = 'http://%s:%s/api/get/datesource'%(IP_ADDRESS,PORT)
	ntp = '192.168.4.41'
	pawd = 'ubuntu'                                                                                                               
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
        s1 = pexpect.spawn('ssh ubuntu@%s' % (ntp,), timeout=60)
	s1.sendline(pawd)
        s1.expect("\$")
	s1.sendline('date')                                                                                                                
        s1.expect("\$")                                                                                                                         
        ntpdate1 = s1.before.split('\r\n')[1]                                                                                              
        ntpdate = ntpdate1[:16]+ntpdate1[20:]                                                                                              
        s1.close()                                                                                                                         
        self.assertEqual(re_date,ntpdate)#不对比秒

    #9、10 获取和设置调整时间的方式_手动校时
    def set_get_datesource2(self):
	set_url = 'http://%s:%s/api/set/datesource'%(IP_ADDRESS,PORT)
	get_url = 'http://%s:%s/api/get/datesource'%(IP_ADDRESS,PORT)
	setdate = 'wed May 18 18:18:22 CST 2016'
        dict_source = {'Mode':2,
                       'Server':'',
                       'Ntp':'',
                       'Date':setdate
                      }
        datesource = json.dumps(dict_source)
        r1 = requests.post(set_url,headers=HEADERS,data=datesource)
        self.assertEqual(r1.status_code,204) #r1.status_code为200或204不固定？？
        s.sendline('date')
        s.expect("\$")
        date = s.before.split('\r\n')[1]
        self.assertEqual(setdate,date)
        r2 = requests.get(get_url,headers=HEADERS)
        self.assertEqual(r2.status_code,200)
        s_content = eval(r2.content)
        self.assertEqual(s_content['Mode'],2)
        self.assertEqual(s_content['Date'],setdate)
                                                                                 
        r = requests.get(url,headers=HEADERS)                                                                                              
        self.assertEqual(r.status_code,200)
	print r.content

    #15 获取该服务器下注册绑定的sensor列表
    def get_sensors(self):
	code = 0 #存放状态码
        request_sensor = {} #request请求的sensor信息
        etcd_sensor = {} #etcd中sensor信息

	url = 'http://%s:%s/api/get/sensors'%(IP_ADDRESS,PORT)
        r = requests.get(url,headers=HEADERS)

	s.sendline('curl -L %ssensors'% ETCD_PATH)                                                            
        s.expect("\$")                                                                                                                 
        data = s.before

	if r.content == '':
	    code = 204
	    request_sensor['sensor'] = r.content
	    p = re.compile(r'(?<=/config/sensors")''')
	    etcd_sensor['sensor'] = re.findall(p,data)[0]
	    #print request_sensor
	    #print etcd_sensor
	else:
	    code = 200
	    r_content = eval(r.text)
	    for i in r_content:                                                                                                            
                #print type(i),i                                                                                                            
                del i['status']                                                                                                            
                del i['lsthbtime']                                                                                                         
                i1 = json.dumps(i)                                                                                                         
                request_sensor = json.loads(i1)
	        #print request_sensor

	    pattern = re.compile(r'\\')
	    newdata = re.sub(pattern,'',data)
	    #print newdata
	    data1 = newdata.split('[')[1].split(']')[0]
	    #print data1
	    pattern1 = re.compile(r'{"key.*?"value":"(.*?)","modifiedIndex.*?}',re.S)
	    data2 = re.findall(pattern1,data1)
	    #print data2[0],data2[1]
	    for item in data2:
	        #print item
	        sensor_info = json.loads(item)
	        del sensor_info['status']
		etcd_sensor = sensor_info
	    self.assertEqual(r.status_code,code)
	    self.assertEqual(sorted(request_sensor),sorted(etcd_sensor))

    ##16 通过设备ID从设备列表中删除设备的接口，设备在线时直接删除，设备离线时在设备再次上线后删除
    def delete_sensor(self):
	k = 0
	code = 0
	#查看设备状态
	url = 'http://%s:%s/api/get/sensors'%(IP_ADDRESS,PORT)
        r = requests.get(url,headers=HEADERS)
	#查看要删除的sensor是否在列表中
	if SENSORID not in r.content:
	    url1 = 'http://%s:%s/api/del/sensor?sensorid=%s'%(IP_ADDRESS,PORT,SENSORID)                                                         
            r1 = requests.delete(url1,headers=HEADERS)
	    k = 1
	    code = 500
	else:
	    r_content = eval(r.text)
	    #print r_content
	    for i in r_content:
		if i['sensorid'] == SENSORID:
	            if i['status'] == 0 or i['status'] == 1:
		        url1 = 'http://%s:%s/api/del/sensor?sensorid=%s'%(IP_ADDRESS,PORT,SENSORID)                                                         
		        r1 = requests.delete(url1,headers=HEADERS)
			code = 204
		        s.sendline('curl -L %ssensors'% ETCD_PATH)
                        s.expect("\$")                                                                                                                     
        	        data = s.before
		        if i['sensorid'] in data:
		            k = 0 #删除失败
		        else:
		            k = 1 #删除成功
	            elif i['status'] == -1:
		        url1 = 'http://%s:%s/api/del/sensor?sensorid=%s'%(IP_ADDRESS,PORT,i['sensorid'])                                               
                        r1 = requests.delete(url1,headers=HEADERS)
                        code = 204
                        s.sendline('curl -L %ssensors'% ETCD_PATH)
                        s.expect("\$")
                        data = s.before
                        if i['sensorid'] in data:
                            k = 0 #删除失败
                        else:
                            k = 1 #删除成功
        self.assertEqual(r1.status_code,code)
	self.assertEqual(k,1)

    ##17 获取该服务器下注册级联的server列表
    def get_servers(self):
	url = 'http://%s:%s/api/get/servers'%(IP_ADDRESS,PORT)
        r = requests.get(url,headers=HEADERS)
        self.assertEqual(r.status_code,204)

    #18 获取服务列表，即docker container的列表
    def get_processlist(self):
	url = 'http://%s:%s/api/get/processlist'%(IP_ADDRESS,PORT)
        r = requests.get(url,headers=HEADERS)
        self.assertEqual(r.status_code,200)
	r_content = eval(r.content)                                                                                               
        s.sendline('sudo docker ps -a')
        s.expect(':')
        s.sendline(PASSWORD)
        s.expect("\$")
        status = s.before.split('\r\n')
	#print r_content
	for item in r_content:
	    #print item['Name']
	    for i in status:
		if item['Name'] in i:
		    serverid = i.split()[0]
		    r_id = item['id'][:12]
	self.assertEqual(r_id,serverid)

    #19 通过服务名称获取服务的ID
    def get_idfromname(self):
	url = 'http://%s:%s/api/get/idfromname?name=%s'%(IP_ADDRESS,PORT,SERVICE)
        r = requests.get(url,headers=HEADERS)
        self.assertEqual(r.status_code,200)                                                                                               
        s.sendline('sudo docker ps -a')
        #s.expect(':')
        #s.sendline(PASSWORD)
        s.expect("\$")
        status = s.before.split('\r\n')
	for item in status:
	    if SERVICE in item:
	   	serverid = item.split()[0]
	self.assertEqual(r.content[:12],serverid)
    
    #21 关闭指定ID或name的服务                                                                                                             
    def get_stopprocess(self):                                                                                                             
        url = 'http://%s:%s/api/get/stopprocess?name=%s'%(IP_ADDRESS,PORT,SERVICE)                                                        
        r = requests.get(url,headers=HEADERS)                                                                                              
        #self.assertEqual(r.status_code,204)                                                                                               
        s.sendline('sudo docker ps -a')                                                                                            
        #s.expect(':')                                                                                                                      
        #s.sendline(PASSWORD)                                                                                                               
        s.expect("\$")                                                                                                                     
        status = s.before.split('\r\n')
	#print status
        k = 0
        for item in status:                                                                                                                
            if SERVICE in item:
		if 'Exited' in item:
		    k = 1 #关闭服务成功
		else:
		    k = 0 #关闭服务失败
	self.assertEqual(r.status_code,204)
        self.assertEqual(k,1)

    #20 启动指定ID或name的服务
    def get_startprocess(self):
	url = 'http://%s:%s/api/get/startprocess?name=%s'%(IP_ADDRESS,PORT,SERVICE)
        r = requests.get(url,headers=HEADERS)
        #self.assertEqual(r.status_code,204)
        s.sendline('sudo docker ps -a')
        #s.expect(':')
        #s.sendline(PASSWORD)
        s.expect("\$")
        status = s.before.split('\r\n')
        #print status
	m = 0
	for item in status:
	    if SERVICE in item:
		time = item.split()
		ln = len(time)
		if 'Up' in item and time[ln-2]=='second':   
                    m = 1 #启动服务成功                                                                                                    
                else:                                                                                                                      
                    m = 0 #启动服务失败
        self.assertEqual(r.status_code,204)
	self.assertEqual(m,1)

    #22 重启指定ID或name的服务
    def get_restartprocess(self):                                                                                                            
        url = 'http://%s:%s/api/get/restartprocess?name=%s'%(IP_ADDRESS,PORT,RESTART_SERVICE)                                                        
        r = requests.get(url,headers=HEADERS)                                                                                              
        #self.assertEqual(r.status_code,204)                                                                       
        s.sendline('sudo docker ps -a')
        s.expect("\$")
        status = s.before.split('\r\n')
	n = 0                                                                                                    
        #print status
        for item in status:                                                                                                                
            if RESTART_SERVICE in item:
		time = item.split()
                ln = len(time)
		if 'Up' in item and time[ln-2]=='second':
                    n = 1 #重启服务成功                                                                                                    
                else:                                                                                                                      
                    n = 0 #重启服务失败
        self.assertEqual(r.status_code,204)
	self.assertEqual(n,1)                                                                                                            

    #23 查看指定ID或name服务的详细信息
    def get_processinfo(self):
        url = 'http://%s:%s/api/get/processinfo?name=%s'%(IP_ADDRESS,PORT,SERVICE)                                                        
        r = requests.get(url,headers=HEADERS)                                                                                              
        self.assertEqual(r.status_code,200)
	
    #24 查看指定ID或name服务的日志信息
    def get_processlog(self):
	url = 'http://%s:%s/api/get/processlog?name=%s'%(IP_ADDRESS,PORT,SERVICE)   
        r = requests.get(url,headers=HEADERS)
        self.assertEqual(r.status_code,200)

if __name__ == '__main__':
    suite = unittest.TestSuite()
    
    #suite.addTest(TestOptimusApi("get_version"))
    #suite.addTest(TestOptimusApi("get_image"))
    suite.addTest(TestOptimusApi("get_server"))
    suite.addTest(TestOptimusApi("set_server"))
    suite.addTest(TestOptimusApi("get_tag"))
    #suite.addTest(TestOptimusApi("set_tag"))
    suite.addTest(TestOptimusApi("get_network"))
    #suite.addTest(TestOptimusApi("set_get_datesource0"))
    #suite.addTest(TestOptimusApi("set_get_datesource1"))
    #suite.addTest(TestOptimusApi("set_get_datesource2"))
    suite.addTest(TestOptimusApi("get_sensors"))
    #suite.addTest(TestOptimusApi("delete_sensor"))
    #suite.addTest(TestOptimusApi("get_servers"))
    #suite.addTest(TestOptimusApi("get_processlist"))
    #suite.addTest(TestOptimusApi("get_idfromname"))
    #suite.addTest(TestOptimusApi("get_stopprocess"))
    #suite.addTest(TestOptimusApi("get_startprocess"))
    #suite.addTest(TestOptimusApi("get_restartprocess"))
    #suite.addTest(TestOptimusApi("get_processinfo"))
    #suite.addTest(TestOptimusApi("get_processlog"))

    #执行测试                                                                                                                              
    runner = unittest.TextTestRunner()                                                                                                     
    runner.run(suite)	
