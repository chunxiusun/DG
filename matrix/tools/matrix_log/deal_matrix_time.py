#!/usr/bin/python
#-*- coding:utf-8 -*-

fd = open('FaceAlignmentProcessor','r')
t = ''
a = 0
c = 0
for line in fd.readlines():
    atime = eval(line.split()[11])
    ttime = line.split()[1].split('.')[0]
    #print ttime
    #print t
    if t == '':
	t = ttime
	c = 1
	a = atime
	continue
    if ttime == t:
	c = c + 1
	a += atime
    else:
	aligntime = a*1.0/c
	print aligntime
        t = ttime
	c = 1
	a = atime
