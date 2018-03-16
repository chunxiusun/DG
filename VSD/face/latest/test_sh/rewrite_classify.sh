#!/bin/bash
for((j=0;j<=8;j++));  
do
let "i=$j*6"
if [$j == 0]
then
    i=$j+1
fi
rm result.txt   
echo $i;
./nogus_config_json.linux -src=config.json -dst=config_classify$i.json -logtostderr=1 <<EOF
{
    "Sys/BufferTTLClassifyUpdate/write": $i,
    "DataOutput/FileOutput/FileName/write":"result.txt"
}
EOF
./run.sh config_classify$i.json

cd /home/dell/vsd_test/
echo config_classify$i.json >> t_classify.txt
./analyze_lost.py >> t_classify.txt
cd - 
done  
