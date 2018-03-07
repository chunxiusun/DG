#!/usr/bin/env python
#-*- coding:utf-8 -*-

ftpServer = "192.168.2.222"
ftpUser = "ftp1"
ftpPasswd = "123456"

FLAG = "download" # (upload or download)

from ftplib import FTP

def ftpconnect(host, username, password):
    ftp = FTP()
    #ftp.set_debuglevel(2)
    ftp.connect(host, 21)
    ftp.login(username, password)
    return ftp

def uploadfile(ftp, remotepath, localpath):
    bufsize = 1024
    fp = open(localpath, 'rb')
    ftp.storbinary('STOR ' + remotepath, fp, bufsize)
    ftp.set_debuglevel(0)
    fp.close()

def downloadfile(ftp, remotepath, localpath):
    bufsize = 1024
    fp = open(localpath, 'wb')
    ftp.retrbinary('RETR ' + remotepath, fp.write, bufsize)
    ftp.set_debuglevel(0)
    fp.close()

if __name__ == "__main__":
    ftp = ftpconnect(ftpServer, ftpUser, ftpPasswd)
    if FLAG == "upload":
        uploadfile(ftp, "378314096715775893.jpg", "378314096715775893.jpg")
    elif FLAG == "download":
        downloadfile(ftp, "/378314096715775893.jpg", "2.jpg")
    ftp.quit()
