#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os

rootdir = "/home/dell/python/sun/deepdata/images/"
target = "/home/dell/python/sun/deepdata/new_images/"
if not os.path.exists(target):
    os.system("mkdir %s"%target)

for i in range(9,13):
    subdir = "%s/%s"%(rootdir,str(i))
    lst = os.listdir(subdir)
    subtarget = "%s/%s"%(target,str(i))
    if not os.path.exists(subtarget):
        os.system("mkdir %s"%subtarget)
    for i in range(0,len(lst),5):
        print lst[i]
        s_file = "%s/%s"%(subdir,lst[i])
        print s_file
        print subtarget
        os.system("cp %s %s"%(s_file,subtarget))
