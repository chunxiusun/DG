#!/bin/sh

int=1
n=0
while [ $int -lt 5 ]
do
    log_date=$(date +%Y-%m-%d)
    log_time=$(date +%H:%M:%S) 
    log_data="== [$log_date $log_time] Operation Log:$n =="
    log_type="operation" #operation（操作日志）/ service（服务日志）/ alarm（报警日志）
    log_user="sun"
    log_code="200"
    log="[type:$log_type,user:$log_user,code:$log_code] $log_data"
    event_log="<!--XSUPERVISOR:BEGIN--> $log<!--XSUPERVISOR:END-->"
    echo $event_log

    log_data_1="== [$log_date $log_time] Service Log:$n =="
    log_type_1="service" #operation（操作日志）/ service（服务日志）/ alarm（报警日志）
    log_user_1="admin"
    log_code_1="200"
    log_1="[type:$log_type_1,user:$log_user_1,code:$log_code_1] $log_data_1"
    event_log_1="<!--XSUPERVISOR:BEGIN--> $log_1<!--XSUPERVISOR:END-->"
    echo $event_log_1

    err_data="== [$log_date $log_time] Alarm Error:$n =="
    err_type="alarm"
    err_user="sun_sun"
    err_code="400"
    err="[type:$err_type,user:$err_user,code:$err_code] $err_data"
    event_err="<!--XSUPERVISOR:BEGIN--> $err<!--XSUPERVISOR:END-->"
    echo $event_err
    let "n=$n+1"
    sleep 5
done
