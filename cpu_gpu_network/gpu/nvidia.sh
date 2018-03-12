#! /bin/bash

function test()
{
    while true
    do
        echo "stat..."
        nvidia-smi > tmp.txt
        sed -n '9p' tmp.txt >> nvidia1.log
        sed -n '12p' tmp.txt >> nvidia2.log
        sleep 1
    done
}

rm nvidia1.log
rm nvidia2.log
test
