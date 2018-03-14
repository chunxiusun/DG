一、testMatrix.py

matrix稳定性测试脚本，适配matrix_1.2.x版本，相比适配0.8.x的增加了非机动车车牌

1、参数介绍：
 
Usage:
 
-h,--help (show help on all flags [tip: all flags can have two dashes])

--ip (matrix ip,defult:127.0.0.1)   #Ip

--port (matrix port,defult:6505)   #port

--mode (0 means single,1 means batch,defult:0)  #single或是batch方式

--batchsize (batchsize,defult:8)   #batch方式下的batchsize

--imagefile (images url list file)   #图片url列表文件

--outputfile (result file,defult:car_result.txt) #结果输出文件

--info  #输出文件中字段含义


2、使用示例：

python testMatrix.py --ip=192.168.2.137  --mode=1 --batchsize=8  --imagefile=02.txt --outputfile=result.txt


3、输出文件: 

每行含义：图片名称；类型（机动车、行人、非机动车）；cutboard；属性信息（以分号分割），为空表示没有此属性



4、属性信息按顺序如下 ：

python matrixRecognize.py --info

机动车:cutboard;主品牌;子品牌;年款;车型;车姿态;车身颜色;车牌号&车牌颜色;年检标数量;摆件数量;挂坠数量;纸巾盒数量;左遮阳板数量;右遮阳板数量;主驾安全带;主驾打电话;副驾安全带;副驾打电话

行人:cutboard;性别;年龄;民族;头部特征;上身颜色;上身纹理;下身颜色;下身类别;包款式

非机动车:cutboard;车辆类型;车辆角度;车身颜色;人员性别;人员民族;人员头部特征;人员上身颜色;人员上身样式;包款式



5、运行脚本时控制台打印内容：

图片url以及检测到的机动车、行人、非机动车的数量


二、drawCutBoard_diff.py/drawCutBoard.py

将MatrixConsistency.py的输出结果中cutboard画到图片上

drawCutBoard_diff.py：两个检测结果的框同时画到图片上

drawCutBoard.py：一个检测结果的框画到图片上
