#!/usr/bin/env python
#-*- coding:utf-8 -*-

import xlrd,xlwt
import psycopg2

sql = "WITH p AS (SELECT *, ROW_NUMBER() OVER (PARTITION BY event_reid ORDER BY confidence DESC) AS rn FROM (SELECT * FROM face_event_view WHERE (((ts>=1499011200960 AND ts<=1499307428960)) AND sensor_id='ea9a713e-ec78-4896-a1b1-e031b9db95b0' AND repo_id IN ('94e3e127-d094-460d-af68-b55064b675ac','f7165333-22dc-4dc2-ab96-2ebda2b8f82e','0f87d351-41bd-4a45-b157-34d8ebe59cd2','4b3fa376-e3a6-4173-b3e7-75c05979c25f','92aa72d0-465a-49cb-a977-95e53981f1b6','0f480617-48e9-43c2-910d-ee1f97abdf47','b916f9f9-c08e-4407-9ab4-950273f84e3d','bbfa0b9f-1c10-4adc-b7b0-e728417cf5ce','634f9f39-c69f-4169-98d4-26b3bb10f4bd','444e7666-97b9-4cc2-be6b-5b359c3fd8b9','0e89065d-9183-42b2-b395-1444cfabb741','a6fbdee2-0cc9-4704-9116-f94fc3a77b11','3b92032c-b978-484e-9743-6ef193bd9375','c1514e41-202a-437b-960c-1ef22b0211f8') AND id_type='1' AND status!=4)) AS t) SELECT * FROM p WHERE rn<=1  ORDER BY ts DESC LIMIT 300 OFFSET 100"
#database
db = "deepface_v3"
user = "postgres"
password = "123456"
host = "192.168.2.164"
port = "5432"

xlsname = "haha.xls"


def select_postgres(worksheet,dateFormat):
    sql_list = []
    conn = psycopg2.connect(database=db, user=user, password=password, host=host, port=port)
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    row_num = 1
    for i in rows:
        print i[0]
        worksheet.write(row_num,0,i[13])
        worksheet.write(row_num,1,i[9])
        worksheet.write(row_num,2,i[18])
        worksheet.write(row_num,3,i[25])
        worksheet.write(row_num,4,i[27])
        worksheet.write(row_num,5,i[29])
        worksheet.write(row_num,6,i[16])
        worksheet.write(row_num,7,i[0],dateFormat)
        row_num += 1
    cur.close()
    conn.close()


if __name__ == '__main__':
    dateFormat = xlwt.XFStyle()
    dateFormat.num_format_str = 'yyyy-mm-dd hh:mm:ss'
    workbook = xlwt.Workbook(encoding = 'utf-8')
    worksheet = workbook.add_sheet("Sheet1")
    row0 = [u"通行摄像机",u"相似度",u"抓拍图片",u"比中图片",u"姓名",u"身份证号",u"抓拍背景图片",u"通行时间"]
    for i in range(0,len(row0)):
        worksheet.write(0,i,row0[i])
    select_postgres(worksheet,dateFormat)
    workbook.save(xlsname)
