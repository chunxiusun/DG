#!/bin/bash

for i in {0..49}
do
    s=$[$i*20000+1]
    e=$[$s+19999]
    echo $s,$e
    #echo $i
    sed -n "$s,${e}p" feature_384.txt > feature_384_20000_$i.txt 
done
