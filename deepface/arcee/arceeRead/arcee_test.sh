#!/bin/bash

#for((i=6;i>0;i--))
#do
    #echo "/home/dell/data/logs/arcee.log.$i"
    #cat "/home/dell/data/logs/arcee.log.$i"|grep POST >> post_request
    #cat "/home/dell/data/logs/arcee.log.$i"|grep Batch|grep started >> post_started
    #cat "/home/dell/data/logs/arcee.log.$i"|grep Batch|grep duration >> post_done
#done

echo "/home/dell/data/logs/arcee.log"

#cat /home/dell/data/logs/arcee.log|grep GET >> get_request
cat ./y_w_2/arcee.log|grep GET >> get_request

echo "deal get_request"
cat get_request|awk '{print $4}'> h
sort -n h -o h
cat h |uniq -c >> get_request.txt

