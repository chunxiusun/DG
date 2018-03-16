#!/usr/bin/env python
#-*- coding:utf-8 -*-

import sys,os,json,signal
import time,datetime
import hashlib
import logging
import logging.handlers

logger = logging.getLogger("MyLogger")
os.system("mkdir -p /home/dell/python/sun/olympus_test/mock/log")
log_name = "/home/dell/python/sun/olympus_test/mock/log/mock.log"
formatter = logging.Formatter(
    '%(asctime)s %(filename)s %(funcName)s [line:%(lineno)d] %(levelname)s: %(message)s')
handler = logging.handlers.RotatingFileHandler(log_name,
            maxBytes = 20971520, backupCount = 5)
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

try:
    config_file = os.path.join("./","%s"%(sys.argv[1]))
    fd = open(config_file,'r')
    data = fd.read()
    config = json.loads(data)
    #print config
    haha = config["haha"]
except:
    sys.exit(1)

def mock():
    start_time = str(datetime.datetime.now())
    m = hashlib.md5()   
    m.update(start_time)   
    time_md5 = m.hexdigest()
    sys.stdout.write("time:%s, hash:%s, start"%(start_time,time_md5))
    logger.info("time:%s, hash:%s, start"%(start_time,time_md5))
    while True:
        pass

def onsignal_term(a,b):
    stop_time = str(datetime.datetime.now())
    m = hashlib.md5()
    m.update(stop_time)
    time_md5 = m.hexdigest()
    sys.stdout.write("time:%s, hash:%s, stop"%(stop_time,time_md5))
    logger.info("time:%s, hash:%s, stop"%(stop_time,time_md5))
    sys.exit(0)

signal.signal(signal.SIGTERM,onsignal_term)

if __name__ == '__main__':
    mock()
