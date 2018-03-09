#!/bin/bash

myvar=1
while [ $myvar -le 10 ]
do
    cat /home/dell/data/logs/isd_0.log|grep Metadata|awk -F '.' '{print $1}'|uniq -c|awk '{sum=sum+$1}END{print sum/NR}' >> metadata.txt
    cat /home/dell/data/logs/isd_0.log|grep assign |awk -F '.' '{print $1}'|uniq -c|awk '{sum=sum+$1}END{print sum/NR}' >> assign.txt
    cat /home/dell/data/logs/isd_0.log|grep TRANSFORM|awk -F '.' '{print $1}'|uniq -c|awk '{sum=sum+$1}END{print sum/NR}' >> transform.txt
    cat /home/dell/data/logs/isd_0.log|grep kafkaoutput|grep finish|awk -F '.' '{print $1}'|uniq -c|awk '{sum=sum+$1}END{print sum/NR}' >> kafkaoutput.txt
    cat /home/dell/data/logs/isd_0.log|grep ZMQ|grep timeout |awk -F '.' '{print $1}'|uniq -c|awk '{sum=sum+$1}END{print sum/NR}' >> zmq_timeout.txt
    sleep 5
done
