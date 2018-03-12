#!/usr/bin/python
# -*- coding:utf-8 -*-
# author : chunxiusun

import time
import datetime
import pexpect

IP_ADDRESS = '192.168.5.168'
USERNAME = 'ubuntu'
PASSWORD = 'ubuntu'
PID = 0
count = -1

def get_process(name):
    global PID,count
    try:
        p = pexpect.spawn('ssh %s@%s' % (USERNAME, IP_ADDRESS), timeout=60)
        index = p.expect(['.*/no\)\?','.*ssword:', pexpect.EOF, pexpect.TIMEOUT])
        if index == 0 or index == 1:
            if index == 0 :
                p.sendline('yes')
                p.expect('.*ssword:')
        p.sendline(PASSWORD)
        p.expect('\$')
    except:
        print '[%s]ssh %s@%s failed' % (datetime.datetime.now(),USERNAME, IP_ADDRESS)
	return

    try:
        p.sendline('sudo supervisorctl status')
	#p.expect('.*ubuntu:')
        #p.sendline(PASSWORD)
        p.expect('\$')
    except:
	print 'timeout'
	return
    r = p.before
    #print r
    l = r.split('\n')
    for line in l:
	if name in line:
	    #print line
	    s = line.split()
	    if s[1] == 'RUNNING':
		pid = s[3].split(',')[0]
		if PID != pid:
		    print line
		    print '%s pid:%s'%(name,pid)
		    PID = pid
		    count = count + 1
		    print '[%s]the number of %s hang up:%d'%(datetime.datetime.now(),name,count)
	    elif s[1] == 'STOPPED':
		print line
		print '[%s]process[%s] is stopped' % (datetime.datetime.now(),name)
	    else:
		print line
		print '[%s]process[%s] has some errors' % (datetime.datetime.now(),name)
    p.close()


if __name__ == '__main__':
    while True:
        get_process('libraf')
