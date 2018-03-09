#!/usr/bin/env python
#-*- coding:utf-8 -*-
#author : chunxiusun

import xlrd,xlwt

true_file = "076true.xlsx"
false_file = "076falsewarn30.xlsx"
undefined_file = "undefined.xlsx"

start_score = 65
recall_total = 110
recall_all = 405
xlsname = "076.xls"

def recall_rate():
    true_file_list = deal_excel(true_file)
    false_file_list = deal_excel(false_file)

    true_count_dict = deal_count(true_file_list)
    false_count_dict = deal_count(false_file_list)
    print "#"*20 + "recall_rate" + "#"*20
    recall_rate_dict = {}
    for key in true_count_dict:
	recall_rate = true_count_dict[key]*1.0/recall_total
	recall_rate_dict[key] = "%0.2f%s"%(recall_rate*100,"%")
	print "score>=%s; recall rate:%s"%(str(key),recall_rate_dict[key])
    return recall_rate_dict

def accuracy_rate():
    print ""
    print "#"*20 + "accuracy_rate" + "#"*20
    true_file_list = deal_excel(true_file)
    false_file_list = deal_excel(false_file)
    remove_list = []
    for line in false_file_list:
	for row in true_file_list:
	    if line[4] == row[4]:
		remove_list.append(line)
    for i in remove_list:
	try:
	    false_file_list.remove(i)
	except:
	    continue
    
    true_count_dict = deal_count(true_file_list)
    false_count_dict = deal_count(false_file_list)
    recall_rate_dict = {}
    monitor_rate_dict = {}
    accuracy_rate_dict = {}
    score_dict = {}
    for key in true_count_dict:
	total_count = true_count_dict[key] + false_count_dict[key]
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
    return recall_rate_dict,accuracy_rate_dict,monitor_rate_dict,score_dict
    
def err_alarm_rate():
    print ""
    print "#"*20 + "err_alarm_rate" + "#"*20
    true_file_list = deal_excel(true_file)
    false_file_list = deal_excel(false_file)
    undefined_file_list = deal_excel(undefined_file)

    true_count_dict = deal_count(true_file_list)
    false_count_dict = deal_count(false_file_list)
    undefined_count_dict = deal_count(undefined_file_list)
    
    err_alarm_rate_dict = {}
    for key in true_count_dict:
	total_count = true_count_dict[key] + false_count_dict[key] + undefined_count_dict[key]
	err_count = false_count_dict[key] + undefined_count_dict[key]
	if total_count == 0:
	    err_alarm_rate = 0
	else:
	    err_alarm_rate = err_count*1.0/total_count
	err_alarm_rate_dict[key] = "%0.2f%s"%(err_alarm_rate*100,"%")
	print "score>=%s; err count:%s; total count:%s; err alarm rate:%0.2f%s\r\n"%(str(key),str(err_count),str(total_count),
              err_alarm_rate*100,"%")
    return err_alarm_rate_dict
    

def deal_count(file_list):
    count_dict = {}
    for i in range(start_score,101):
        count_dict[i] = 0 
    for item in file_list:
        score = eval(item[3].split("%")[0])
        for i in range(start_score,101):
            if score >= i:
                count_dict[i] += 1
    return count_dict

def deal_excel(filename):
    file_list = []
    data = xlrd.open_workbook(filename)
    table = data.sheets()[0]
    nrows = table.nrows
    for i in range(1,nrows):
        line = table.row_values(i)
	file_list.append(line)
    return file_list

if __name__ == '__main__':
    workbook = xlwt.Workbook(encoding = 'utf-8')
    worksheet = workbook.add_sheet("Sheet1")
    row0 = [u"报警阈值",u"召回率",u"报警正确率",u"布控误报率",u"得分"]
    for i in range(0,len(row0)):
        worksheet.write(0,i,row0[i])

    #recall_rate_dict = recall_rate()
    recall_rate_dict,accuracy_rate_dict,monitor_rate_dict,score_dict = accuracy_rate()
    #err_alarm_rate_dict = err_alarm_rate()
    row_num = 1
    for i in range(start_score,101):
	worksheet.write(row_num,0,i)
	worksheet.write(row_num,1,recall_rate_dict[i])
	worksheet.write(row_num,2,accuracy_rate_dict[i])
	worksheet.write(row_num,3,monitor_rate_dict[i])
	worksheet.write(row_num,4,score_dict[i])
	row_num += 1
    workbook.save(xlsname)
