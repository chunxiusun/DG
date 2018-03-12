#/usr/bin/python
#coding:UTF-8

import requests,unittest,pexpect,re,json,random
from config import *

class TestOptimusApi(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        global p
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

    @classmethod
    def tearDonwClass(self):
        p.close()

    #1 获取optimus版本信息的API，从`VERSION`文件读取，异常返回文件不存在
    def case1_get_optimus_version(self):
	url = 'http://%s:%s/api/get/version'%(IP_ADDRESS,PORT)
        r = requests.get(url,headers=HEADERS)
        self.assertEqual(r.status_code,200)
	p.sendline('sudo docker images')
        p.expect(':')
        p.sendline(PASSWORD)
        p.expect('\$')
        optimus_v = p.before.strip()                                                                                                         
        ov = re.compile('192.168.5.46:5000/.*?optimus(.*?)_T2')                                                                              
        ov1 = re.findall(ov,optimus_v)[0].strip()                                                                                                       
        self.assertEqual(r.content.strip(),ov1)

    #2 添加获取服务器系统版本的接口，依赖文件'/data/version/Release'
    def case2_get_image_version(self):
	url = 'http://%s:%s/api/get/image'%(IP_ADDRESS,PORT)
        r = requests.get(url,headers=HEADERS)
        self.assertEqual(r.status_code,200)
	p.sendline('cat %s' % IMAGE_PATH)                                                                                           
        p.expect('\$')                                                                                                                     
        image_v = p.before.split("\n")[1].strip()                                                                                          
        self.assertEqual(r.content.strip(),image_v)

    #3 获取该设备关联的服务器地址信息，服务器地址信息存储在etcd内，键值为`config/optimus/server`
    def case3_get_server(self): 
	url = 'http://%s:%s/api/get/server'%(IP_ADDRESS,PORT)                                                                              
        r = requests.get(url,headers=HEADERS)                                                                                              
        self.assertEqual(r.status_code,200)
        p.sendline('curl -L %soptimus/server'% ETCD_PATH)                                                                              
        p.expect("\$")
	addrserver = p.before.strip()                                                                                                      
        st=re.compile('"value":".*?(.*?)","modifiedIndex"',re.S)                                                                                
        st1=re.findall(st,addrserver)[0].strip()
        #print st1
	self.assertEqual(r.content.strip(),st1)

    #4 设置该设备关联的服务器地址信息，服务器地址设置完毕会切换与服务器的通道
    def case4_set_server(self):
	url = 'http://%s:%s/api/set/server?addr=%s'%(IP_ADDRESS,PORT,SERVER_IP)                                                                             
        r = requests.post(url,headers=HEADERS)                                                                                              
        self.assertEqual(r.status_code,201)                                                                                                
        p.sendline('curl -L %soptimus/server'% ETCD_PATH)                                                                                  
        p.expect("\$")
	data = p.before                                                                                                                
        pattern = re.compile('((?<=value":").*?(?="))',re.S)                                                                                          
        value = re.findall(pattern,data)[0]
	#print value                                                                                            
        self.assertEqual(SERVER_IP,value)
	    
    #5 获取该设备的描述信息，描述信息存储在etcd内，键值为`config/optimus/tag`，如：`北京.海淀.青龙桥.格灵深瞳`
    def case5_get_tag(self):
	url = 'http://%s:%s/api/get/tag'%(IP_ADDRESS,PORT)                                                                                 
        r = requests.get(url,headers=HEADERS)                                                                                              
        self.assertEqual(r.status_code,200)
	p.sendline('curl -L %soptimus/tag'% ETCD_PATH)                                                                                                    
        p.expect('\$')                                                                                                                      
        tag = p.before.strip()                                                                                                             
        st=re.compile('((?<=value":").*?(?=",))',re.S)                                                                                
        st1=re.findall(st,tag)[0].strip()
        self.assertEqual(r.content.strip(),st1)

    #6 设置该设备的描述信息
    def case6_set_tag(self):
	str = 'abcdefghigkslmnBCDE0123456789.*?@'                                                                                          
        word = random.sample(str,8)                                                                                                        
        strtag = ""                                                                                                                        
        for i in word: 
            strtag += i
	TAG = strtag
	url = 'http://%s:%s/api/set/tag?tag=%s'%(IP_ADDRESS,PORT,TAG)                                                                      
        r = requests.post(url,headers=HEADERS)                                                                                             
        self.assertEqual(r.status_code,201)
	p.sendline('curl -L %soptimus/tag'% ETCD_PATH)                                                                                 
        p.expect("\$")
	tag = p.before.strip()                                                                                                             
        st=re.compile('"value":".*?(.*?)","modifiedIndex"')                                                                                
        st1=re.findall(st,tag)[0].strip()                                                                                                   
        self.assertEqual(TAG,st1)

    #7 获取该设备的网络配置信息
    def case7_get_network(self):
	url = 'http://%s:%s/api/get/network'%(IP_ADDRESS,PORT)                                                                                 
        r = requests.get(url,headers=HEADERS)                                                                                              
        self.assertEqual(r.status_code,200)
	r_content = eval(r.content)
	interfaces = {}
	p.sendline('cat /etc/network/interfaces')                                                                                          
        p.expect('\$')                                                                                                                     
        s = p.before.split('\r\n')                                                                                                           
        #print s                                                                                                                           
        for item in s:                                                                                                                     
           if 'address' in item:
              interfaces["address"] = item.split(' ')[1]                                                                  
           elif 'netmask' in item:                                                                                                         
              interfaces["netmask"] = item.split(' ')[1]                                                                  
           elif 'gateway' in item:                                                                                                         
              interfaces["gateway"] = item.split(' ')[1]                                                                  
           elif 'dns-nameservers' in item:                                                                                                 
              interfaces["maindns"] = item.split(' ')[1]                                                                  
              interfaces["subdns"] = item.split(' ')[2]
	self.assertEqual(r_content, interfaces)	

    #9、10 获取和设置调整时间的方式
    def case8_get_set_datesource(self):
	set_url = 'http://%s:%s/api/set/datesource'%(IP_ADDRESS,PORT)                                                                      
        get_url = 'http://%s:%s/api/get/datesource'%(IP_ADDRESS,PORT)
	source = dict(Mode = 0,
                      Server = "",
                      NTP = "",
                      Date = "",
                      Timezone = ""
                     )
        #从服务器同步时间
        source["Mode"] = 0
        source["Server"] = svr
        jsource = json.dumps(source)
        p_req1 = requests.post(set_url,data = jsource, headers = headers)
        self.assertEqual(p_req1.status_code,204)
        g_req1 = requests.get(get_url,headers = headers)
        self.assertEqual(g_req1.status_code,200)
        getsource1 = eval(g_req1.content)
        self.assertEqual(getsource1["Mode"],0)
        self.assertEqual(getsource1["Server"],svr)

        #从NTP时间服务器同步时间  
        source["Mode"] = 1
        source["NTP"] = ntp                                                                                                                
        jsource = json.dumps(source)                                                                                                       
        p_req2 = requests.post(set_url,data = jsource, headres = headers)                                                                  
        self.assertEqual(p_req2.status_code,204)                                                                                           
        g_req2 = requests.get(get_url,headers = headers)                                                                                   
        self.assertEqual(g_req2.status_code,200)                                                                                           
        getsource2 = eval(g_req2.content)                                                                                                  
        self.assertEqual(getsource2["Mode"],1)                                                                                             
        self.assertEqual(getsource2["NTP"],ntp)                                                                                            
                                                                                                                                           
        #手动同步时间                                                                                                                  
        source["Mode"] = 2                                                                                                                 
        source["Date"] = setdate                                                                                                           
        jsource = json.dumps(source)                                                                                                       
        #print source                                                                                                                      
        p_req3 = requests.post(set_url, data = jsource, headers = headers) #post request                                                   
        self.assertEqual(p_req3.status_code, 204)                                                                                          
        p.sendline('date')                                                                                                                 
        p.expect('\$')                                                                                                                     
        date = p.before.split('\n')[1].strip()                                                                                             
        print date                                                                                                                         
        date = date[:15] + date[19:]                                                                                                       
        setdate = setdate[:15] + setdate[19:]                                                                                              
        self.assertEqual(setdate, date)                                                                                                    
        g_req3 = requests.get(get_url, headers = headers) #get request                                                                     
        self.assertEqual(g_req3.status_code, 200)                                                                                          
        getsource = eval(g_req3.content)
	self.assertEqual(getsource["Mode"], 2)                                                                                             
        getdate = getsource["Date"][:15] + getsource["Date"][19:]                                                                          
        self.assertEqual(getdate, setdate)                                                                                                 
                                                                                                                                           
        #调整设备时区                                                                                                                   
        source["Mode"] = 3                                                                                                                 
        source["Timezone"] = timezone                                                                                                      
        jsource = json.dumps(source)                                                                                                        
        p_req4 = requests.post(set_url,data = jsource, headers=headers)                                                                    
        self.assertEqual(p_req4.status_code,204)                                                                                           
        g_req4 = requests.get(get_url, data = jsource, headers=headers)                                                                    
        self.assertEqual(g_req4.status_code,200)                                                                                           
        getsource4 = eval(g_req4.content)                                                                                                  
        self.assertEqual(getsource4["Mode"],3)                                                                                             
        self.assertEqual(getsource4["Timezone"],timezone)

    #15 获取该服务器下注册绑定的sensor列表
    def case15_get_sensorlist(self):
	code = 0 #存放状态码
        request_sensor = {} #request请求的sensor信息
        etcd_sensor = {} #etcd中sensor信息
	url = 'http://%s:%s/api/get/sensors'%(IP_ADDRESS,PORT)                                                                             
        r = requests.get(url,headers=HEADERS)
	
	p.sendline('curl -L %ssensors'% ETCD_PATH)                                                                                         
        p.expect("\$")
	data = p.before
	if r.content == '':
            code = 204
            request_sensor['sensor'] = r.content
            s = re.compile(r'(?<=/config/sensors")''')
            etcd_sensor['sensor'] = re.findall(s,data)[0]
        else:
            code = 200
            r_content = eval(r.text)
            for i in r_content:
                del i['status'] #不比对
                del i['lsthbtime'] #不比对
                i1 = json.dumps(i)
		request_sensor = json.loads(i1)
            pattern = re.compile(r'\\')
            newdata = re.sub(pattern,'',data)
            pattern1 = re.compile('.*?"value":"(.*?)","modifiedIndex.*?}',re.S)
            data2 = re.findall(pattern1,newdata)
            for item in data2:
                sensor_info = json.loads(item)
                del sensor_info['status']
                etcd_sensor = sensor_info
            self.assertEqual(r.status_code,code)
            self.assertEqual(sorted(request_sensor),sorted(etcd_sensor))

    ##16 通过设备ID从设备列表中删除设备的接口，设备在线时直接删除，设备离线时在设备再次上线后删除
    def case16_delete_sensor(self):
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
                        p.sendline('curl -L %ssensors'% ETCD_PATH)                                                                         
                        p.expect("\$")                                                                                                                     
                        data = p.before                                                                                                    
                        if i['sensorid'] in data:                                                                                          
                            k = 0 #删除失败                                                                                                
                        else:                                                                                                              
                            k = 1 #删除成功                                                                                                
                    elif i['status'] == -1: #离线时也是直接删除                                                           
                        url1 = 'http://%s:%s/api/del/sensor?sensorid=%s'%(IP_ADDRESS,PORT,i['sensorid'])                                                 
                        r1 = requests.delete(url1,headers=HEADERS)                                                                         
                        code = 204                                                                                                         
                        p.sendline('curl -L %ssensors'% ETCD_PATH)                                                                         
                        p.expect("\$")                                                                                                     
                        data = p.before                                                                                                    
                        if i['sensorid'] in data:                                                                                          
                            k = 0 #删除失败                                                                                                
                        else:                                                                                                              
                            k = 1 #删除成功                                                                                                
        self.assertEqual(r1.status_code,code)                                                                                              
        self.assertEqual(k,1)    

     ##17 获取该服务器下注册级联的server列表
    def case17_get_servers(self):
	url = 'http://%s:%s/api/get/servers'%(IP_ADDRESS,PORT)                                                                             
        r = requests.get(url,headers=HEADERS)                                                                                              
        self.assertEqual(r.status_code,204)

    #18 获取服务列表，即docker container的列表
    def case18_get_processlist(self):
	url = 'http://%s:%s/api/get/processlist'%(IP_ADDRESS,PORT)                                                                         
        r = requests.get(url,headers=HEADERS)                                                                                              
        self.assertEqual(r.status_code,200)                                                                                                
        r_content = eval(r.content)                                                                                                        
        p.sendline('sudo docker ps -a')                                                                                                    
        #p.expect(':')                                                                                                                      
        #p.sendline(PASSWORD)                                                                                                               
        p.expect("\$")                                                                                                                     
        status = p.before.split('\r\n')[2:-1]
	serverid = []
	r_id = []                                                                                                    
        for item in r_content:
	    r_id.append(item['id'][:12])                                                                                                             
        for i in status:
	    serverid.append(i.split()[0])
	self.assertEqual(sorted(r_id),sorted(serverid))

    #19 通过服务名称获取服务的ID
    def case19_get_idfromname(self):
	url = 'http://%s:%s/api/get/idfromname?name=%s'%(IP_ADDRESS,PORT,SERVICE)                                                          
        r = requests.get(url,headers=HEADERS)                                                                                              
        self.assertEqual(r.status_code,200)                                                                                                
        p.sendline('sudo docker ps -a')                                                                                                    
        p.expect("\$")
        status = p.before.split('\r\n')                                                                                                    
        for item in status:                                                                                                                
            if SERVICE in item:                                                                                                            
                serverid = item.split()[0]                                                                                                 
        self.assertEqual(r.content[:12],serverid)

    #21 关闭指定ID或name的服务
    def case21_get_stopprocess(self):
	k = 1
	code = 0
	url = 'http://%s:%s/api/get/stopprocess?name=%s'%(IP_ADDRESS,PORT,SERVICE)
	p.sendline('sudo docker ps -a')
        p.expect("\$")
        status = p.before.split('\r\n')
        for item in status:
            if SERVICE in item:
                if 'Exited' in item: #查看服务状态
		    r = requests.get(url,headers=HEADERS)
		    code = 500
		else:
        	    r = requests.get(url,headers=HEADERS)
		    code = 204                                                                                              
        	    p.sendline('sudo docker ps -a')                                                                                                    
        	    p.expect("\$")                                                                                                                     
        	    status = p.before.split('\r\n')                                                                                                    
        	    for item in status:                                                                                                                
            		if SERVICE in item:                                                                                                            
                	    if 'Exited' in item:                                                                                                       
                    		k = 1 #关闭服务成功                                                                                                    
                	    else:                                                                                                                      
                    		k = 0 #关闭服务失败                                                                                                    
        self.assertEqual(r.status_code,code)
	self.assertEqual(k,1)

    #20 启动指定ID或name的服务                                                                                                             
    def case20_get_startprocess(self):
	k = 1 
	code = 0                                                                                           
        url = 'http://%s:%s/api/get/startprocess?name=%s'%(IP_ADDRESS,PORT,SERVICE)                                                        
        p.sendline('sudo docker ps -a')
        p.expect("\$")
        status = p.before.split('\r\n')
        for item in status:
            if SERVICE in item:
                if 'Exited' in item: #查看服务状态
                    r = requests.get(url,headers=HEADERS)
		    code = 204
		    p.sendline('sudo docker ps -a')
        	    p.expect("\$")
        	    status = p.before.split('\r\n')
        	    for item in status:
            		if SERVICE in item:
                	    time = item.split()
                	    if 'Up' in item and time[-2]=='second':
                    		k = 1 #启动服务成功                                                                                                    
                	    else:
                    		k = 0 #启动服务失败
		else:
		    r = requests.get(url,headers=HEADERS)
                    code = 200 
        self.assertEqual(r.status_code,code)                                                                                               
        self.assertEqual(k,1)

    #22 重启指定ID或name的服务                                                                                                             
    def case22_get_restartprocess(self):
        url = 'http://%s:%s/api/get/restartprocess?name=%s'%(IP_ADDRESS,PORT,RESTART_SERVICE)                                                            
        r = requests.get(url,headers=HEADERS)                                                                                              
        self.assertEqual(r.status_code,204)                                                                                               
        p.sendline('sudo docker ps -a')                                                                                                    
        p.expect("\$")                                                                                                                     
        status = p.before.split('\r\n')                                                                                                    
        n = 0                                                                                                                              
        for item in status:                                                                                                                
            if RESTART_SERVICE in item:                                                                                                    
                time = item.split()                                                                                                        
                if 'Up' in item and time[-2]=='second':                                                                                  
                    n = 1 #重启服务成功                                                                                                    
                else:                                                                                                                      
                    n = 0 #重启服务失败                                                                                                    
        self.assertEqual(n,1)                                                                                                              
                                                                                                                                           
    #23 查看指定ID或name服务的详细信息                                                                                                     
    def case23_get_processinfo(self):                                                                                                             
        url = 'http://%s:%s/api/get/processinfo?name=%s'%(IP_ADDRESS,PORT,SERVICE)                                                         
        r = requests.get(url,headers=HEADERS)                                                                                              
        self.assertEqual(r.status_code,200)                                                                                                
                                                                                                                                           
    #24 查看指定ID或name服务的日志信息                                                                                                     
    def case24_get_processlog(self):                                                                                                              
        url = 'http://%s:%s/api/get/processlog?name=%s'%(IP_ADDRESS,PORT,SERVICE)                                                          
        r = requests.get(url,headers=HEADERS)                                                                                              
        self.assertEqual(r.status_code,200)

if __name__ == '__main__':
    suite = unittest.TestSuite()

    suite.addTest(TestOptimusApi("case1_get_optimus_version"))
    suite.addTest(TestOptimusApi("case2_get_image_version"))
    suite.addTest(TestOptimusApi("case3_get_server"))
    suite.addTest(TestOptimusApi("case4_set_server"))
    suite.addTest(TestOptimusApi("case5_get_tag"))
    suite.addTest(TestOptimusApi("case6_set_tag"))
    suite.addTest(TestOptimusApi("case7_get_network"))
    #suite.addTest(TestOptimusApi("case8_get_set_datesource"))
    suite.addTest(TestOptimusApi("case15_get_sensorlist"))
    suite.addTest(TestOptimusApi("case16_delete_sensor"))
    suite.addTest(TestOptimusApi("case17_get_servers"))
    suite.addTest(TestOptimusApi("case18_get_processlist"))
    suite.addTest(TestOptimusApi("case19_get_idfromname"))
    suite.addTest(TestOptimusApi("case21_get_stopprocess"))
    suite.addTest(TestOptimusApi("case20_get_startprocess"))
    suite.addTest(TestOptimusApi("case22_get_restartprocess"))
    suite.addTest(TestOptimusApi("case23_get_processinfo"))
    suite.addTest(TestOptimusApi("case24_get_processlog"))

#执行测试                                                                                                                              
    runner = unittest.TextTestRunner()
    runner.run(suite)
