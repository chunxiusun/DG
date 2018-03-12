#!/usr/bin/python
# -*- coding:utf-8 -*-
#author : chunxiusun

import sys
sys.path.append('./gen-py')

import config
from init_parameter import *
from function import LibrafApi
from function_set import FunctionSet
import threading
import time
import unittest
import random
import string
import datetime

from logger import logger

from LibraFService import LibraFService
from LibraFService import ttypes
#from LibraFService.ttypes import *

from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol


class TestInteractive(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        pass

    @classmethod
    def tearDownClass(self):
        pass

    def test01_meanWhile(self):
	logger.info('*****at the same time*****')
	thread_list = []
        func = random.choice(range(1,7))
        #print func
	for item in range(0,11):
	    p = FunctionSet(func)
	    thread_list.append(p)
	for item in thread_list:                                                                                                           
            item.start()

    def test02_two(self):
	logger.info('*****two threads*****')
        thread_list = []
	func = random.sample(range(1,7),2)
	#print func
	for item in func:
	    p = FunctionSet(item)
	    thread_list.append(p)
        for item in thread_list:
            item.start()

    def test03_three(self):
	logger.info('*****three threads*****')
	thread_list = []
	func = random.sample(range(1,7),3)
	#print func
	for item in func:
            p = FunctionSet(item)
            thread_list.append(p)
	for item in thread_list:
            item.start()

    def test04_four(self):
	logger.info('*****four threads*****')
	thread_list = []
        func = random.sample(range(1,7),4)
	#print func
        for item in func:
            p = FunctionSet(item)
            thread_list.append(p)
        for item in thread_list:
            item.start()	

    def test05_five(self):
	logger.info('*****five threads*****')
        thread_list = []
        func = random.sample(range(1,7),5)
	#print func
        for item in func:
            p = FunctionSet(item)
            thread_list.append(p)
        for item in thread_list:
            item.start()

    def test06_six(self):
	logger.info('*****six threads*****')
        thread_list = []
        func = random.sample(range(1,7),6)
	#print func
        for item in func:
            p = FunctionSet(item)
            thread_list.append(p)
        for item in thread_list:
            item.start() 

if __name__ == '__main__':
    suite = unittest.TestSuite()
    
    suite.addTest(TestInteractive("test01_meanWhile"))
    suite.addTest(TestInteractive("test02_two"))
    suite.addTest(TestInteractive("test03_three"))
    suite.addTest(TestInteractive("test04_four"))
    suite.addTest(TestInteractive("test05_five"))
    suite.addTest(TestInteractive("test06_six"))

    runner = unittest.TextTestRunner()
    runner.run(suite)


