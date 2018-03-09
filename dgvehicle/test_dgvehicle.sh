#!/bin/bash

#cd /data/zhangshuye/dgvehicle/build/bin
cd /mnt/sde1/liuhao/workspace/14_cycle_attribute/dgvehicle_becompared/build/bin
for ((i=1;i<13;i++))
do
    ./test_detector2  /data/sun/images_all/$i.list /data/sun/12testresult_2/$i.txt 8
done

#./test_detector2  /data/sun/images_all/6.list /data/sun/12testresult_2/6.txt 8
