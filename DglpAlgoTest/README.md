1. suite

dglp测试文件所在目录

其中，
LPDRTest_new.cc是针对新算法的

LPDRTest_old.cc是针对老算法的


编译运行方式:

a. 移动

将测试文件放到dgLP/test目录下

b. 编译

cd dgLP/build

conan install -f ../conanfile.txt --build

cmake ..

make

c. 运行

cd dgLP

mkdir testResult

cd testResult

../build/bin/dgLP_test ../data/newEnergyVehicle.list


d.结果（部分）


38560_1518056942000_part.jpg 粤B047150 粤B047150

38552_1518056935000_part.jpg 粤B02185D 粤B02185D

 
2. utils

dglpCarScoreCheckLabel_new.py

功能：

根据dglp测试结果生成错误率，准确率指标。

运行：

python dglpCarScoreCheckLabel_new.py

结果：

errRate: 0.153846153846

acccurate: 0.846153846154

3. data

存放一些demo数据
