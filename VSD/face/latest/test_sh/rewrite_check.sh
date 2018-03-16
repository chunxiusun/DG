#!/bin/bash
for((i=1;i<=5;i++));  
do
#let "i=$j*2"
rm result.txt   
echo $i;
./nogus_config_json.linux -src=config.json -dst=config_check$i.json -logtostderr=1 <<EOF
{
    "Sys/CheckTrackInterval/write": $i,
    "DataOutput/FileOutput/FileName/write":"result.txt"
}
EOF
./run.sh config_check$i.json

cd /home/dell/vsd_test/
echo config_check$i.json >> t_check.txt
./analyze_lost.py >> t_check.txt
cd - 
done  
