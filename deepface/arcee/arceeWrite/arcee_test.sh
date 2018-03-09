#!/bin/bash

#for((i=6;i>0;i--))
#do
    #echo "/home/dell/data/logs/arcee.log.$i"
    #cat "/home/dell/data/logs/arcee.log.$i"|grep POST >> post_request
    #cat "/home/dell/data/logs/arcee.log.$i"|grep Batch|grep started >> post_started
    #cat "/home/dell/data/logs/arcee.log.$i"|grep Batch|grep duration >> post_done
#done

echo "/home/dell/data/logs/arcee.log"

cat /home/dell/data/logs/arcee.log|grep POST >> post_request
cat /home/dell/data/logs/arcee.log|grep Batch|grep started >> post_started
cat /home/dell/data/logs/arcee.log|grep Batch|grep duration >> post_done

echo "deal post_request"
cat post_request|awk '{print $4}'> h
sort -n h -o h
cat h |uniq -c >> post_request.txt

echo "deal post_started"
cat post_started|awk '{print $2}'|awk -F'.' '{print $1}'> h
sort -n h -o h
cat h |uniq -c >> post_started.txt

echo "deal post_done"
cat post_done|awk '{print $2}'|awk -F'.' '{print $1}'> h
sort -n h -o h
cat h |uniq -c >> post_done.txt
