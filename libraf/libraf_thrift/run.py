#!/usr/bin/python
# -*- coding:utf-8 -*-

# author : chunxiusun

import os
import time

n = 1

while True:
    try:
        os.system('python testcase_func.py')
	#os.popen('python testcase_func.py')
	#execfile(testcase_func.py)
	#import testcase_func.py
    except:
	print 'testcase_func.py error...' 
    '''if n%10 == 0:
        try:
            os.system('python testcase_abnormal.py')
        except:
	    print 'testcase_testcase_abnormal.py error...'
        try:
            os.system('python testcase_interactive.py')
        except:
	    print 'testcase_interactive.py error' '''
    print n
    n = n+1
    #time.sleep(5)
    #break
