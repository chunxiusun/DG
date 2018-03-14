#!/usr/bin/env python
#coding=utf-8

import string
import random
import re 
import numpy as np
import math
import base64

# Get random string
def getRandomString(strLen=None, type_=0):

    '''
    type = 0, means number
    type = 1, means string
    '''

    retStr = ""

    if type_ == 0:
        str_ = string.digits    
    else:
        str_ = string.hexdigits

    for _index in range(int(strLen)):
        i = random.randint(0, 9)
        tmp = str_[i-1]
        retStr += tmp
    
    retStr = re.sub(r"\b0*([1-9][0-9]*|0)", r"\1", retStr)  

    return retStr

# Get choice num
def getChoiceNum(nList):

    return random.choice(nList)    

# create feature based on length
def featureCreate(featureLen=None):

    # Check the feature lenght is valid or not
    if featureLen is None:
        return
        
    # Create the the feature
    f_list = []
    ff_sum = 0.0
    for _ in range(featureLen):
        f = random.uniform(-1,1)
        ff = f*f
        f_list.append(f)
        ff_sum = ff_sum + ff
    t = math.sqrt(ff_sum)
    featureFloat = []
    for f in f_list:
        featureFloat.append(f/t)
    featureFloat = np.array(featureFloat,dtype=np.float32)
    featureString = base64.b64encode(featureFloat)
    
    return featureString

# print the data type
def printDataType(aData):
    
    print(type(aData))

# string to dict
def stringToDict(aDictString):
    
    return eval(aDictString)

