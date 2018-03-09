#!/bin/bash

for ((i=1;i<13;i++))
do
    find ./images/$i -name "*.jpg" -exec readlink -f {} \; > ./images/$i.list
done

