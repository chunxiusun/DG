#!/usr/bin/env python
#-*- coding:utf-8 -*-
#author : chunxiusun

import os,re,time,datetime
import logging
import logging.handlers
import xlrd,xlwt
import psycopg2

sql = "WITH p AS (SELECT *, ROW_NUMBER() OVER (PARTITION BY event_reid ORDER BY confidence DESC) AS rn FROM (SELECT * FROM face_event_view WHERE (((ts>=1497542400448 AND ts<=1497867487451)) AND sensor_id='5e78b172-62f3-4b5f-b6af-099efc5c6b75' AND repo_id='b916f9f9-c08e-4407-9ab4-950273f84e3d' AND id_type='1' AND status!=4)) AS t) SELECT * FROM p WHERE rn<=1  ORDER BY ts DESC LIMIT 300 OFFSET 0;"
#database
db = "deepface_v3"
user = "postgres"
password = "123456"
host = "192.168.2.164"
port = "5432"

recall_total = 120
recall_all = 400
start_score = 65
xlsname = "076.xls"

logger = logging.getLogger("MyLogger")
os.system("mkdir -p ./log")
log_name = "./log/stat_scores.log"
formatter = logging.Formatter(
    '%(asctime)s %(filename)s %(funcName)s [line:%(lineno)d] %(levelname)s: %(message)s')
handler = logging.handlers.RotatingFileHandler(log_name,
            maxBytes = 20971520, backupCount = 5)
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)
logger.info(
        "[[time.time:%s]]" % str(int(time.time())))
logger.info(
        "[[loadtest start at %s]]" % str(datetime.datetime.now()))
#logger.info("Timeout Threshold: %dms", conf["timeout"])
#logger.info("threadNum: %d", conf["threadNum"])

def select_postgres():
    true_list = []
    false_list = []
    conn = psycopg2.connect(database=db, user=user, password=password, host=host, port=port)
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    for i in rows:
        if re.match('[ \u4e00 -\u9fa5]+',i[-9]) == None:
            true_list.append(i[9])
            #print i[-9],i[9]
        else:
            false_list.append(i[9])
    cur.close()
    conn.close()
    return true_list,false_list

def accuracy_rate():
    print "#"*20 + "rates" + "#"*20
    true_list,false_list = select_postgres()
    logger.info("true_list:%s"%str(true_list))
    logger.info("false_list:%s"%str(false_list))
    total_num = len(true_list) + len(false_list)
    logger.info("total_num:%d"%total_num)
    true_count_dict = deal_count(true_list)
    false_count_dict = deal_count(false_list)
    logger.info("true_count_dict:%s"%str(true_count_dict))
    logger.info("false_count_dict:%s"%str(false_count_dict))
    recall_rate_dict = {}
    monitor_rate_dict = {}
    accuracy_rate_dict = {}
    score_dict = {}
    for key in true_count_dict:
	total_count = true_count_dict[key] + false_count_dict[key]
        logger.info(">%d,total_count=%d"%(key,total_count))
	if total_count == 0:
	    accuracy_rate = 0
	else:
	    accuracy_rate = true_count_dict[key]*1.0/total_count
	recall_rate = true_count_dict[key]*1.0/recall_total
	monitor_rate = false_count_dict[key]*1.0/recall_all
	score = (recall_rate*0.7+(1-monitor_rate)*0.3)
	
	recall_rate_dict[key] = "%0.2f%s"%(recall_rate*100,"%")
	monitor_rate_dict[key] = "%0.2f%s"%(monitor_rate*100,"%")
	accuracy_rate_dict[key] = "%0.2f%s"%(accuracy_rate*100,"%")
	score_dict[key] = "%0.2f%s"%(score*100,"%")
	print "score>=%s; recall_rate:%s; accuracy_rate:%s; monitor_rate:%s; score:%s"%(str(key),recall_rate_dict[key],\
              accuracy_rate_dict[key],monitor_rate_dict[key],score_dict[key])
    logger.info("recall_rate_dict:%s"%str(recall_rate_dict))
    logger.info("accuracy_rate_dict:%s"%str(accuracy_rate_dict))
    logger.info("monitor_rate_dict:%s"%str(monitor_rate_dict))
    logger.info("score_dict:%s"%str(score_dict))
    return recall_rate_dict,accuracy_rate_dict,monitor_rate_dict,score_dict
    

def deal_count(file_list):
    count_dict = {}
    for score in file_list:
        for i in range(start_score,101):
            if i not in count_dict:
                count_dict[i] = 0
            if score >= float(i)/100:
                count_dict[i] += 1
    return count_dict


if __name__ == '__main__':
    workbook = xlwt.Workbook(encoding = 'utf-8')
    worksheet = workbook.add_sheet("Sheet1")
    row0 = [u"报警阈值",u"召回率",u"报警正确率",u"布控误报率",u"得分"]
    for i in range(0,len(row0)):
        worksheet.write(0,i,row0[i])

    recall_rate_dict,accuracy_rate_dict,monitor_rate_dict,score_dict = accuracy_rate()
    row_num = 1
    for i in range(start_score,101):
	worksheet.write(row_num,0,i)
	worksheet.write(row_num,1,recall_rate_dict[i])
	worksheet.write(row_num,2,accuracy_rate_dict[i])
	worksheet.write(row_num,3,monitor_rate_dict[i])
	worksheet.write(row_num,4,score_dict[i])
	row_num += 1
    workbook.save(xlsname)
