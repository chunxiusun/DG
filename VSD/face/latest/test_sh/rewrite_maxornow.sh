#!/bin/bash
for i in true false;  
do
rm result.txt   
echo $i;
./nogus_config_json.linux -src=config.json -dst=config_maxornow$i.json -logtostderr=1 <<EOF
{
    "Sys/ClassifyMaxOrNew/write": $i,
    "DataOutput/FileOutput/FileName/write":"result.txt"
}
EOF
./run.sh config_maxornow$i.json

cd /home/dell/vsd_test/
echo config_maxornow$i.json >> t_maxornow.txt
./analyze_lost.py >> t_maxornow.txt
cd - 

done  
