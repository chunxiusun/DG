#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os,xlrd

sensorFile = "ID.xlsx"
sensorIdFile = "sensor_id.txt"
userFile = "/etc/vsftpd_user.txt"
userDir = "/home/dell/data/ftp/"
passWord = "CP#mnuP&Al"

def addUser():
   # sensor_list = sensorFilter()
   # os.system("rm /etc/vsftpd_user.txt.bak")
   # os.system("rm -r /etc/vsftpd_user_conf.bak/")
   # os.system("cp /etc/vsftpd_user.txt /etc/vsftpd_user.txt.bak")
   # os.system("cp -r /etc/vsftpd_user_conf/ /etc/vsftpd_user_conf.bak/")
    fd = open(userFile,'aw+')
    fs = open(sensorIdFile,'r')
    for line in fs.readlines():
	#user_name = "test"
    	user_name = line.strip().split()[0]
        #print type(user_name)
   # data = xlrd.open_workbook(sensorFile)
   # table = data.sheets()[0]
   # nrows = table.nrows
   # for i in range(nrows):
   #     sensor_name = str(int(table.row(i)[0].value))
   #     print sensor_name
   #     if sensor_name in sensor_list:
   #         print item
   #         continue
        fd.write("%s\n"%user_name)
        fd.write("%s\n"%passWord)
        user_dir_file = "/etc/vsftpd_user_conf/%s"%(user_name)
        print user_dir_file
        fu = open(user_dir_file,'w')
        fu.write("local_root=%s%s"%(userDir,user_name))
        fu.close()
        os.system("mkdir -p %s%s"%(userDir,user_name))
        os.system("chown ftp %s%s"%(userDir,user_name))
        #break
    fs.close()
    fd.close()
    os.system("db_load -T -t hash -f /etc/vsftpd_user.txt /etc/vsftpd_login.db")
    os.system("chmod 600 /etc/vsftpd_login.db")
    os.system("service vsftpd restart")

def sensorFilter():
    data = xlrd.open_workbook("Nemo设备信息.xlsx")
    table = data.sheets()[0]
    nrows = table.nrows
    sensor_list = []
    for i in range(1,nrows):
        if table.row(i)[0].value != "":
            sensor_info = str(int(table.row(i)[0].value))
            sensor_list.append(sensor_info)
    print sensor_list
    return sensor_list
        

def startImporter():
    fd = open(sensorIdFile,'r')
    for line in fd.readlines():
        print line
        sensor_name = line.strip().split()[0]
        sensor_id = line.strip().split()[1]
        print sensor_name,sensor_id
        supervisor_conf = "/etc/supervisor/conf.d/importer_ftp_%s.conf"%sensor_name
        os.system("cp importer_ftp_1414638305.conf %s"%supervisor_conf)
        os.system("sed -i 's/1414638305/%s/g' %s"%(sensor_name,supervisor_conf))

        importer_conf = "/home/dell/face/importer/latest/configs/ftpconfig_%s.txt"%sensor_name
        os.system("cp ftpconfig_1414638305.txt %s"%importer_conf)
        os.system("sed -i 's/1414638305/%s/g' %s"%(sensor_name,importer_conf))
        os.system('''sed -i 's/"SensorID": .*/"SensorID": "%s",/g' %s'''%(sensor_id,importer_conf))
        #break
    fd.close()
    os.system("supervisorctl update")


if __name__ == '__main__':
    addUser()
    #startImporter()
