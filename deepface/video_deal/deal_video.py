#!/usr/bin/env python
#-*- coding:utf-8 -*-
#author : chunxiusun

import os,time
import xlrd

input_video = "104.mkv"
input_file = "104new.xlsx"
output_video = "output104"
video_format = "mp4"

fd = open("filelist.txt","w")

data = xlrd.open_workbook(input_file)
table = data.sheets()[0]
nrows = table.nrows
for i in range(nrows):
    line = table.row_values(i)
    time_start = line[0]
    print time_start
    time_end = line[1]
    print time_end
    cut_video = "cutout%s.mkv"%str(i)
    os.system("ffmpeg -i %s -vcodec copy -acodec copy -ss %s -to %s %s -y"%(input_video,time_start,time_end,cut_video))
    switch_video = "result%s.%s"%(str(i),video_format)
    os.system("ffmpeg  -i %s -f %s  %s"%(cut_video,video_format,switch_video))
    fd.write("file %s\r\n"%switch_video)
fd.close()
os.system("ffmpeg -f concat -i filelist.txt -c copy %s.%s"%(output_video,video_format))
