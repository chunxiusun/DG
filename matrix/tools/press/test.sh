#!/bin/bash
# author : chunxiusun

echo "set dgvehicle.json"
cd /home/dell/data/matrix/matrix_apps/data/dgvehicle/
pwd
sudo cp dgvehicle.json dgvehicle.json.bak
sed -i '/BatchSize/s/"BatchSize":.*/"BatchSize":8/g' dgvehicle.json

echo "set dgLPConfig.json"
cd /home/dell/data/matrix/matrix_apps/data/dgLP/Product/
pwd
sudo cp dgLPConfig.json dgLPConfig.json.bak
sed -i '/BatchSize/s/"BatchSize":.*/"BatchSize":8,/g' dgLPConfig.json

echo "set config.json"
cd /home/dell/data/matrix/matrix_apps
pwd
sudo cp config.json config.json.bak
sed -i '/Port/s/"Port": .*/"Port": 6800,/' config.json

echo "start matrix"
sudo apt-get -y install libopenblas-dev
sudo nohup ./matrix_apps &
sleep 30
matrix_pid=$(ps -ef | grep "matrix_apps" | grep -v grep | awk '{print $2}')
echo $matrix_pid

echo "start car test"
cd /home/dell/data/matrix/test_car/
pwd
nohup ./car_test.py &
test_pid=$(ps -ef | grep "car_test.py" | grep -v grep | awk '{print $2}')
echo $test_pid
sleep 10

echo "start monitor"
cd /home/dell/data/matrix/monitor/
pwd
nohup python monitor.py &
monitor_pid=$(ps -ef | grep "monitor.py" | grep -v grep | awk '{print $2}')
echo $monitor_pid

sleep 60

echo "stat cpu/gpu"
sudo apt-get -y remove libopenblas-base                                                                                                       
sudo python analyze_plot.py

echo "kill matrix/test/monitor"
kill -9 $monitor_pid
kill -9 $test_pid
sudo kill -9 $matrix_pid
