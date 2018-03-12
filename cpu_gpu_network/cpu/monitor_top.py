#!/usr/bin/env python
# -*- coding: utf8 -*-

# author: mikahou

import commands, os

def get_pid(keyWord, timeLen) :
    pid_cmd = "ps -ef|grep \"%s\"|grep -v grep |awk  '{print $2}'" %(keyWord)
    print pid_cmd
    pids_return = commands.getstatusoutput(pid_cmd)
    print pids_return
    print pids_return[1]
    if pids_return[0] != 0:
        print "get pid error,exit...."
        return
    pids = pids_return[1].split("\n")
    print len(pids)
    for pid in pids:
        keyWord_temp = keyWord.replace(" ","_")
        top_cmd = "top -p %s -b -d 1 -n %d >> ./log/%s.log.%s&" \
                  %(pid, timeLen, keyWord_temp, pid)
        #top_cmd = "top -p %s -b -d 1 -n %d|grep %s >> %s.log.%s" \
        #          %(pid, timeLen, pid, keyWord_temp, pid)
        print top_cmd
        os.system(top_cmd)


get_pid("matrix_apps",600)
get_pid("mxadaptor",600)
