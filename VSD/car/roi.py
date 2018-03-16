#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
from PIL import Image, ImageDraw

img = sys.argv[1]
print img
im = Image.open(img)
draw = ImageDraw.Draw(im)
roi = sys.argv[2].split(",")
print roi
x = eval(roi[0])
y = eval(roi[1])
x1 = eval(roi[0]) + eval(roi[2])
y1 = eval(roi[1]) + eval(roi[3])
cut_board = (x,y,x1,y1)
print cut_board 
draw.rectangle(cut_board)
im.show()
