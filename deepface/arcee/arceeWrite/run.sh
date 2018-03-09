#!/bin/bash

echo "arceeApi.py"
nohup ./arceeApi.py > sun &

for((i=1;i<10;i++))
do
    echo "arceeApi_$i.py"
    nohup ./arceeApi_$i.py > sun$i &
done
