#!/bin/bash



for((i=1;i<=5;i++));
do
    j=$[i*10]
    echo $j
    nohup python -u matrixFaceGrpc.py $j > nohup_$j.out &
    sleep 2
    pid=`ps -ef|grep "matrixFaceGrpc.py"|grep -v grep |awk  '{print $2}'`
    echo $pid
    kill -9 $pid
done
