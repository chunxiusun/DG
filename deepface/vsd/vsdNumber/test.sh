#!/bin/bash

FILENAME=$1
echo $FILENAME

mkdir ../$2

t=`date +%s`
i=1
while read LINE
do
    echo $LINE
    echo $t
    cp sun.json sun_$i.json
    echo sun_$i.json
    sed -i 's/"SensorName":.*/"SensorName": "'$LINE'",/' sun_$i.json
    sed -i 's/"TimeStamp":.*/"TimeStamp":'$t',/' sun_$i.json

    cd ../
    nohup ./run.sh ./sun/sun_$i.json > ./$2/log_$i &
    #./run.sh ./sun/sun_$i.json
    cd -
    let i+=1
    sleep 1
done < $FILENAME

sleep 60
python /home/dell/face/sun/monitor/monitor.py

