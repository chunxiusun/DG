#!/usr/bin/env python
#-*- coding:utf-8 -*-

# author : chunxiusun

import sys
import time

def testNogus():
    n = 0
    while True:
        log_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) 
        log_data = "== Operation Log:%s =="%str(n)
        log_type = "operation" #operation（操作日志）/ service（服务日志）/ alarm（报警日志）
        log_user = "sun"
        log_code = "200"
        log = "[type:%s,user:%s,code:%s] %s"%(log_type,log_user,log_code,log_data)
	    event_log = "<!--XSUPERVISOR:BEGIN--> %s<!--XSUPERVISOR:END-->"%log
        sys.stdout.write(event_log)
        print "%s InFo:%s"%(log_time,log)

	    log_data_1 = "== Service Log:%s =="%str(n)
        log_type_1 = "service" #operation（操作日志）/ service（服务日志）/ alarm（报警日志）
        log_user_1 = "admin"
        log_code_1 = "200"
        log_1 = "[type:%s,user:%s,code:%s] %s"%(log_type_1,log_user_1,log_code_1,log_data_1)
	    event_log_1 = "<!--XSUPERVISOR:BEGIN--> %s<!--XSUPERVISOR:END-->"%log_1
        sys.stdout.write(event_log_1)
        print "%s InFo:%s"%(log_time,log_1)

        err_data = "== Alarm Error:%s =="%str(n)
        err_type = "alarm"
        err_user = "sun_sun"
        err_code = "400"
        err = "[type:%s,user:%s,code:%s] %s"%(err_type,err_user,err_code,err_data)
        event_err = "<!--XSUPERVISOR:BEGIN--> %s<!--XSUPERVISOR:END-->"%err
        sys.stderr.write(event_err)
        print "%s Error:%s"%(log_time,err)
        n = n + 1
        time.sleep(600)
	    #break

if __name__ == '__main__':
    testNogus()
