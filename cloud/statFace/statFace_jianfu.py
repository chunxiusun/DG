#!/usr/bin/env python
#-*- coding:utf-8 -*-

import time
import xlrd
import xlwt
import psycopg2
from optparse import OptionParser


sensorFile = "龙岩泉州厦门设备安装点清单-20171221.xlsx"
startTime = "2018-1-20 00:00:00"
dayNum = 10
saveFile = "faces.xls"
FLAG = 0 # 0 means hour, 1 means minutes

#database
db = "deepface_v5"
user = "root"
password = "o8u&npWbid9Y1"
host = "10.0.1.45"
port = "5432"

rows = 1
dayMax = 0
hourMax = 0
minutesMax = 0

def statFace(host, port, db, user, password, sensorFile, startTime, dayNum, FLAG, saveFile):
    global rows,dayMax,hourMax,minutesMax
    data = xlrd.open_workbook(sensorFile)
    table = data.sheets()[0]
    nrows = table.nrows
    workbook = xlwt.Workbook(encoding = 'ascii')
    worksheet = workbook.add_sheet('sheet0',cell_overwrite_ok=True)
    worksheet.write(0, 0, "sensors")
    worksheet.write(0, 1, "day")
    worksheet.write(0, 2, "all")
    count = 3
    for c in range(3,27):
        if FLAG == 0:
            worksheet.write(0, c, str(c-3))
        elif FLAG == 1:
            for i in range(6):
                worksheet.write(0, count, str(c-3))
                count += 1
    for i in range(1,252):
        sensor_name = table.row(i)[2].value
        sensor_id = table.row(i)[7].value
        sensor_status = table.row(i)[8].value
        if sensor_status == "":
            print sensor_name
            #print sensor_id
            dealSql(sensor_id,sensor_name,worksheet)
    workbook.save(saveFile)
    print dayMax,hourMax,minutesMax

def dealSql(sensor_id,sensor_name,worksheet):
    global rows,dayMax,hourMax,minutesMax
    conn = psycopg2.connect(database=db, user=user, password=password, host=host, port=port)
    cur = conn.cursor()

    D = startTime.split()[0].split("-")[-1]
    for i in range(dayNum):
        s_day = "%s-%s-%s 00:00:00"%(D[0],D[1],str(int(D[-1])+i))
        s_timestamp = timeForm(s_day)
        e_day = "%s-%s-%s 00:00:00"%(D[0],D[1],str(int(D[-1])+i+1))
        e_timestamp = timeForm(e_day)
        sql_face_day = "select count(*) from faces where sensor_id='%s' and ts>=%d and ts<%d" % (sensor_id,s_timestamp,e_timestamp)
        #print sql_face_day
        cur.execute(sql_face_day)
        face_count = cur.fetchall()
        if face_count[0][0] >= dayMax:
            dayMax = face_count[0][0]
            print "dayMax:%d %s"%(dayMax,s_day)
        worksheet.write(rows, 0, sensor_name)
        worksheet.write(rows, 1, s_day.split()[0])
        worksheet.write(rows, 2, face_count[0][0])
        #print face_count[0][0]
        h_d = s_day.split()[0]
        h = int(s_day.split()[1].split(':')[0])
        count_column = 3
        for j in range(24):
            s_hour = "%s %s:00:00"%(h_d,str(h+j))
            e_hour = "%s %s:59:59"%(h_d,str(h+j))
            s_timestamp_hour = timeForm(s_hour)
            e_timestamp_hour = timeForm(e_hour)
            sql_face_hour = "select count(*) from faces where sensor_id='%s' and ts>=%d and ts<%d" % (sensor_id,s_timestamp_hour,e_timestamp_hour)
            cur.execute(sql_face_hour)
            face_count_hour = cur.fetchall()
            if FLAG == 0:
                worksheet.write(rows, j+3, face_count_hour[0][0])
            if face_count_hour[0][0] > hourMax:
                hourMax = face_count_hour[0][0]
                print "hourMax:%d %s %s"%(hourMax,s_hour,e_hour)
            #print face_count_hour[0][0]
            for m in range(6):                                                                                                                    
                s_minutes = "%s %s:%s:00"%(h_d,str(h+j),m*10)                                                                                     
                e_minutes = "%s %s:%s:59"%(h_d,str(h+j),(m+1)*10-1)                                                                               
                s_timestamp_minutes = timeForm(s_minutes)                                                                                         
                e_timestamp_minutes = timeForm(e_minutes)                                                                                         
                sql_face_minutes = "select count(*) from faces where sensor_id='%s' and ts>=%d and ts<%d" % (sensor_id,s_timestamp_minutes,e_timestamp_minutes) 
                cur.execute(sql_face_minutes)                                                                                                     
                face_count_minutes = cur.fetchall()
                if FLAG == 1:                                                                                               
                    worksheet.write(rows, count_column, face_count_minutes[0][0])                                                                     
                    count_column += 1                                                                                                                 
                if face_count_minutes[0][0] > minutesMax:                                                                                         
                    minutesMax = face_count_minutes[0][0]                                                                                         
                    print "minutesMax:%d %s %s"%(minutesMax,s_minutes,e_minutes) 
        rows = rows + 1
    worksheet.write(rows, 0, "")
    rows = rows + 1 
    cur.close()                                                                                                                            
    conn.close()

def timeForm(t):
    timeArray = time.strptime(t, "%Y-%m-%d %H:%M:%S")
    timestamp = (time.mktime(timeArray))*1000 
    return timestamp

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("--host", dest="host", type=str, help="db server ip")
    parser.add_option("--port", dest="port", type=str, help="db server port")
    parser.add_option("--db", dest="db", type=str, help="db name")
    parser.add_option("--user", dest="user", type=str, help="db username")
    parser.add_option("--password", dest="password", type=str, help="db password")
    parser.add_option("--sensorFile", dest="sensorFile", type=str, help="sensor File")
    parser.add_option("--startTime", dest="startTime", type=str, help="start Time, For example,:'2018-1-20 00:00:00' ")
    parser.add_option("--dayNum", dest="dayNum", type=int, help="day Num, Can't across a month",default=1)
    parser.add_option("--flag", dest="FLAG", type=int, help=" (0,1) 0 means hour, 1 means minutes",default=0)
    parser.add_option("--saveFile", dest="saveFile", type=str, help="save File(.xls)")

    (options, args) = parser.parse_args()
    print options

    statFace(options.host, options.port, options.db, options.user, options.password, options.sensorFile, options.startTime, options.dayNum, options.FLAG, options.saveFile)

