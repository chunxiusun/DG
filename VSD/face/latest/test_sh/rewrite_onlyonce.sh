#!/bin/bash
for i in true false;  
do
rm result.txt   
echo $i;
./nogus_config_json.linux -src=config.json -dst=config_onlyonce$i.json -logtostderr=1 <<EOF
{
    "Sys/ClassifyOnlyOnce/write": $i,
    "DataOutput/FileOutput/FileName/write":"result.txt"
}
EOF
./run.sh config_onlyonce$i.json

cd /home/dell/vsd_test/
echo config_onlyonce$i.json >> t_onlyonce.txt
./analyze_lost.py >> t_onlyonce.txt
cd - 

done  
