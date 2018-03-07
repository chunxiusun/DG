#!/usr/bin/env python
#-*- coding:utf-8 -*-

import time,json,requests,xlrd
import psycopg2
import uuid

FLAG = 0 #0 means libraf, 1 means ftp, 2 means vsd

#database
db = "deepface_v4"
user = "root"
password = "?7iHUrXrUzVW"
host = "10.19.104.210"
port = "5432"


IP = "10.19.183.165"
PORT = "9876"


repoID = "bd6959e3-7735-411c-9cb0-b9ec86b58d66"
sensorFile = "龙岩泉州厦门设备安装点清单.xlsx"
startNum = 61

def select_postgres(sensor_id,sensor_name,rule_id):
    sql_list = []
    conn = psycopg2.connect(database=db, user=user, password=password, host=host, port=port)
    cur = conn.cursor()
    addsensor_time = int(time.time()*1000)
    print addsensor_time
    if FLAG == 0:
        sensor_type = 1
    cur.execute("INSERT INTO sensors(ts,latitude,type,renderedurl,comment,alg_type,status,sensor_id,ip,live_active,process_warned_reid,window_size,sensor_name,sn_id,user_id,longitude,eur_threshold,cos_threshold,process_captured_reid,repo_id,port,url,rtmpurl,data_active,olympus_id) VALUES(%s,-200,1,'rtsp://10.19.126.219/live/dg-6123e4e4-6670-4cb9-9ed4-985ce27b7b2a','','EUR',2,%s,'192.168.11.11',false,1,20,%s,%s,'',-200,5.5,0.8999999761581421,1,'5300','9876','rtsp://192.168.11.11:9876/live/main','',false,'') ON CONFLICT (sensor_id) DO UPDATE SET ts=EXCLUDED.ts,repo_id=EXCLUDED.repo_id,sensor_name=EXCLUDED.sensor_name,sn_id=EXCLUDED.sn_id,user_id=EXCLUDED.user_id,longitude=EXCLUDED.longitude,latitude=EXCLUDED.latitude,type=EXCLUDED.type,ip=EXCLUDED.ip,port=EXCLUDED.port,url=EXCLUDED.url,renderedurl=EXCLUDED.renderedurl,rtmpurl=EXCLUDED.rtmpurl,live_active=EXCLUDED.live_active,data_active=EXCLUDED.data_active,comment=EXCLUDED.comment,alg_type=EXCLUDED.alg_type,eur_threshold=EXCLUDED.eur_threshold,cos_threshold=EXCLUDED.cos_threshold,process_captured_reid=EXCLUDED.process_captured_reid,process_warned_reid=EXCLUDED.process_warned_reid,window_size=EXCLUDED.window_size,olympus_id=EXCLUDED.olympus_id,status=EXCLUDED.status",(addsensor_time,sensor_id,sensor_name,sensor_id))
    conn.commit()
    time.sleep(5)
    sql = "select * from sensors where sensor_name='%s'"%sensor_name
    cur.execute(sql)
    sensor_rows = cur.fetchall()
    for i in sensor_rows:
        print i
    addrule_time = int(time.time()*1000)
    rule = "sensor_ids=%s;sensor_names=%s;repos={%s:0.8}"%(sensor_id,sensor_name,repoID)
    cur.execute("INSERT INTO face_rule_sensors(sensor_id,user_ids,switcher,rule_id,start_date,start_time,end_time,comment,rois,rule,ts,is_long,end_date,repo_id,status) VALUES (%s,'',1,%s,0,0,0,'','[]',%s,%s,true,0,%s,2)",(sensor_id,rule_id,rule,addrule_time,repoID))
    conn.commit()
    time.sleep(5)
    cur.execute("select * from face_rule_sensors where sensor_id='%s'"%(sensor_id))
    rule_rows = cur.fetchall()
    for i in rule_rows:
        print i
    cur.close()
    conn.close()


if __name__ == '__main__':
    data = xlrd.open_workbook(sensorFile)
    table = data.sheets()[2]
    nrows = table.nrows
    fsid = open("sensor_id.txt",'w')
    for i in range(startNum,nrows):
        print i
        nemo_id = str(table.row(i)[0].value.split('--')[0])
        store_num = str(table.row(i)[0].value.split('--')[1])
        store_name = table.row(i)[1].value.encode("utf8","ignore")
        print nemo_id,store_num,store_name
        sensor_name = nemo_id+store_name
        sensor_id = str(uuid.uuid4())
        rule_id = str(uuid.uuid4())
        #sensor_name = "sunsunsun"
        print sensor_name,sensor_id,rule_id
        select_postgres(sensor_id,sensor_name,rule_id)
        fsid.write("%s %s\n"%(nemo_id,sensor_id))
        break
    fsid.close()
