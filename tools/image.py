#!/usr/bin/env python
#-*- coding:utf-8 -*-

from PIL import Image
import os

imgDir = "/home/dell/python/sun/image/01"

def get_resolution():
    for img_name in os.listdir(imgDir):
        filename = os.path.join(imgDir,img_name)
        print filename
        img = Image.open(filename)
        imgSize = img.size #图片的长和宽
        maxSize = max(imgSize)
        minSize = min(imgSize)
        print imgSize
        print maxSize, minSize

if __name__ == '__main__':
    get_resolution()
