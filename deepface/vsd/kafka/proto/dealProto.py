#!/usr/bin/env python
#-*- coding:utf-8 -*-

import sys
import vsd_pb2

result = vsd_pb2.RecResult()
fd = open("haiguan_86.txt",'r')
data = fd.read()
result.ParseFromString(data)
print result.Meta.Timestamp


