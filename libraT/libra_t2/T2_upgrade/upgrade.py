#/usr/bin/python
#coding:utf-8

import os,requests,hashlib

PACKAGE = 'package-1604211'
HOME_DIR = '/home/dell/python/sun/'
FILE_PATH = os.path.join(HOME_DIR, PACKAGE)
#print path
IP = raw_input('Please input your ip address:')

def MyPackage():
    os.chdir(FILE_PATH)
    os.system('pwd')
    if (os.path.exists('%s.tar.gz' % PACKAGE) == False):
        os.system('tar -zcvf %s.tar.gz *' % PACKAGE)
#	filepath = os.path.join(filepath,'package-160330.tar.gz')

def MyMD5():
    file_path = FILE_PATH + "/" + PACKAGE + ".tar.gz"
    if not os.path.isfile(file_path):
        return 0
    myhash = hashlib.md5()
    f = open(file_path,'r')
    f_content = f.read()
    f.close()
    myhash.update(f_content)
    md5 = myhash.hexdigest()
    return md5
#    print md5
#md5 = os.popen('md5sum package-160330.tar.gz').readlines()[0].split(' ')[0]

def MyPost():
    file_path = FILE_PATH + "/" + PACKAGE + ".tar.gz"
    url = 'http://'+IP+':8006/api/upgrade'
#    print url
    files = {'file': open(file_path, 'rb')}
    data = {}
    if MyMD5() == 0:
        print "the function failed!"
        return 0
    data['md5'] = MyMD5()
    data['force'] = 'false'
#    print data
    r = requests.post(url, files=files, data = data)
    print r.status_code
    print r.content


if __name__ == '__main__':
    MyPackage()
    MyPost()

