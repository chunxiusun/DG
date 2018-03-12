#!/usr/bin/python
#coding:utf-8

import os,requests,hashlib,time,json,commands,re

PACKAGE = 'package-0623'
HOME_DIR = '/home/ubuntu/sun/'
SERVER_IP = '192.168.4.41'
VERSION = 'V2.13.160623R'

def MyPackage():
    global FILE_PATH
    os.chdir(HOME_DIR)
    os.system('pwd')
    if (os.path.exists('%s.tar.gz' % PACKAGE) == False):
        os.system('tar -zcvf %s.tar.gz *' % PACKAGE)
    FILE_PATH = HOME_DIR + PACKAGE + ".tar.gz"

def MyMD5():
    if not os.path.isfile(FILE_PATH):
	return 0
    myhash = hashlib.md5()
    f = open(FILE_PATH,'r')
    f_content = f.read()
    f.close()
    myhash.update(f_content)
    md5 = myhash.hexdigest()
    print 'md5:%s' % md5
    return md5

def MyUpgrade():
    url = 'http://'+SERVER_IP+':8008/api/upgrade'
    files = {'file': open(FILE_PATH, 'rb')}
    data = {}
    if MyMD5() == 0:
        print "the function failed!"
        return 0
    data['md5'] = MyMD5()
    r = requests.post(url, files=files, data = data)
    print r.status_code
    print r.content
    while True:
        time.sleep(60)
        c = commands.getoutput('curl –L http://127.0.0.1:2379/v2/keys/config/global/cur_version')
        p = re.compile('.*?"value":"(.*?)",".*?')
        cur_version = re.findall(p,c)
	if cur_version == VERSION:
	    print 'Uploaded successfully.'
	    break

if __name__ == '__main__':
    MyPackage()
    MyUpgrade()
