#!/bin/sh

# startTime, endTime from the input
startTime=$1
endTime=$2

if [ "$startTime" =  "" ];then
    echo "startTime is null, eg. 11:53:05"
    exit 0
elif [ "$endTime" = "" ]; then
    echo "endTime is null, eg. 11:53:06"
    exit 1
fi

# get the number of add feature
numOfFeatures=`awk -v var=$startTime -v var1=$endTime '$2 >= var && $2 <= var1' /data/zhouping/ranker2/logs/ranker2.out|grep "Add feature succeed"|wc -l`
echo "num of features:" $numOfFeatures

# get the minus between end and start time
sTime=`date +%s -d "$startTime"`
eTime=`date +%s -d "$endTime"`
minusTime=$[$eTime-$sTime]
echo "minusTime:" $minusTime

# get the qps 
numOfQps=$[$numOfFeatures/$minusTime]
echo "num of qps:" $numOfQps
