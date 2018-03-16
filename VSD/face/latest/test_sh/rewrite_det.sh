#!/bin/bash
for((i=1;i<=5;i++));  
do
rm result.txt   
echo $i;
./nogus_config_json.linux -src=config.json -dst=config_$i.json -logtostderr=1 <<EOF
{
    "Sys/DetectionInterval/write": $i,
    "DataOutput/FileOutput/FileName/write":"result.txt"
}
EOF
./run.sh config_$i.json

cd /home/dell/vsd_test/
echo config_$i.json >> t.txt
./analyze_lost.py >> t.txt
cd - 

done  
