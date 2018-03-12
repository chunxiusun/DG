#!/usr/bin/python
# -*- coding:utf-8 -*-
# author:chunxiusun

import fileinput

def deal_biaozhu():
    in_file = "dalian_3_12_label.txt"
    out_file = "dalian_3_12_label.txt.1"
    id_list = ["2","3","4","5"]

    fi = open(in_file,'r')
    fo = open(out_file,'w')
    for line in fi.readlines():
        person_id = line.split(",")[1]
        #print type(line.split(",")[1])
        #print line.split(",")[1]
        #break
        if person_id in id_list:
	    fo.write(line)
    fi.close()
    fo.close()

def deal_ratio():
    in_file = "dalian_3_12_label.txt"
    out_file = "dalian_3_12_label.txt.1"

    
    fi = open(in_file,'r')
    fo = open(out_file,'w')
    for line in fi.readlines():
	l = line.strip().split(",")
	fo.write(l[0]+","+l[1]+",")
        cut_board = l[2:]
	print cut_board
	for i in range(2,6):
	    data = eval(l[i])*6
	    if i == 5:
		fo.write(str(data)+"\r\n")
		continue
	    fo.write(str(data)+",")
	#break
    fi.close()
    fo.close()

if __name__ == '__main__':
    deal_biaozhu()
    #deal_ratio()
