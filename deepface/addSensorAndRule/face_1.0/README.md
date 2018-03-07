批量接入设备适配face1.0对应thor的接口

1、addSensorAndRuleVsd.py

功能：接入普通相机或本地视频（后台启VSD任务）

参数：

   接入VSD路数 = endNum - startNum + 1

   接入相机名称 = “%s%d”%(sensorName,i for i in range(startNum,endNum+1))

   获取已经接入的某路设备（sensorID）的配置文件为模板

   repoID是要布控的比对库id

   videoFile是视频流列表文件（.txt）


2、addSensorAndRuleLibraf.py

功能：接入人眼相机（后台启zmq方式的importer服务）

参数含义基本与addSensorAndRuleVsd.py一致


3、addSensorAndRuleSql.py

功能：接入人眼相机、视频、图片流（Libraf、ftp、vsd）

参数含义基本与addSensorAndRuleVsd.py一致

4、addFtpUserAndStartImporter.py

功能：创建ftp用户及目录、启动importer服务



