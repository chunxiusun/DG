#!/usr/bin/env python
# -*- coding:utf-8 -*-

import pycurl
import StringIO
import time

imageFile = "./http.txt_back"

def curlImage():
    with open(imageFile,'r') as fd:
        for line in fd.readlines():
            img_url = line.strip()
            print img_url
            b = StringIO.StringIO() 
            start = time.time()*1000
            c = pycurl.Curl()
            c.setopt(c.URL, img_url)
            c.setopt(pycurl.TIMEOUT,30)
            c.setopt(pycurl.WRITEFUNCTION, b.write)
            c.setopt(pycurl.FOLLOWLOCATION, 1) 
            c.perform()
            end = time.time()*1000
            image = b.getvalue()
            print len(image)
            print "time:%s"%str((end-start))
            #print c.getinfo(pycurl.HTTP_CODE)
            c.close()
            b.close()

if __name__ == '__main__':
    curlImage()
