#!/bin/bash

myvar=1
while [ $myvar -le 10 ]
do
    cat /home/dell/data/logs/isd_0.log|grep INPUT_KAFKA|awk -F '.' '{print $1}'|uniq -c|awk '{sum=sum+$1}END{print sum/NR}' >> INPUT_KAFKA.txt
    cat /home/dell/data/logs/isd_0.log|grep TRANSFORM|grep output |awk -F '.' '{print $1}'|uniq -c|awk '{sum=sum+$1}END{print sum/NR}' >> TRANSFORM.txt
    cat /home/dell/data/logs/isd_0.log|grep OUTPUT_KAFKA|grep finish|awk -F '.' '{print $1}'|uniq -c|awk '{sum=sum+$1}END{print sum/NR}' >> OUTPUT_KAFKA.txt
    sleep 5
done
