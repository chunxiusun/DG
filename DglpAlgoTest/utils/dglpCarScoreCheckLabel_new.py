#!/usr/bin/env python
#!coding=utf-8

import re
import sys

# dglp score check 
def dglpScoreCheck(filename):

    # open the file
    try:
        fobj = open(filename)
    except:
        print 'filename %s is not exist' % filename
        return

    # loop the filename
    totalCount = 0
    errCount = 0
    for line in fobj:
        
        lines = line.split(" ")
        if len(lines) == 1:
            continue

        elif len(lines) == 2:
            if len(lines[1].strip()) == 0:
                continue
            totalCount += 1
            errCount += 1
            for tmp in lines:
                print tmp.decode('string_escape'),
            #print 'lines:', lines
        elif len(lines) == 3:
            totalCount += 1
            if lines[1].strip() != lines[2].strip():
                print lines[0], lines[1].decode('string_escape'), lines[2].decode('string_escape')
                errCount += 1


    # Print the total and err
    print 'total:', totalCount
    print 'err:', errCount

    # Print the result
    print 'errRate:', 1.0*errCount/totalCount
    print 'acccurate:', 1-1.0*errCount/totalCount

"""
/home/zhouping/algoSdk/testData/newEnergyVehicle_100/38570_1518056951000_part.jpg 粤B07408D UDD118SN

/home/zhouping/algoSdk/testData/newEnergyVehicle_100/38546_1518056931000_part.jpg 陕B02175D 陕B02175

/home/zhouping/algoSdk/testData/newEnergyVehicle_100/38585_1518056963000_part.jpg 粤B37792D
/home/zhouping/algoSdk/testData/newEnergyVehicle_100/38582_1518056960000_part.jpg 粤B36770D
/home/zhouping/algoSdk/testData/newEnergyVehicle_100/38565_1518056946000_part.jpg 粤B05800D 粤B0580D1

/home/zhouping/algoSdk/testData/newEnergyVehicle_100/38603_1518056975000_part.jpg 粤BT9413
/home/zhouping/algoSdk/testData/newEnergyVehicle_100/38533_1518056924000_part.jpg 粤B02133D D2133

/home/zhouping/algoSdk/testData/newEnergyVehicle_100/38598_1518056972000_part.jpg 粤BDL503 GBDL503

/home/zhouping/algoSdk/testData/newEnergyVehicle_100/38584_1518056962000_part.jpg 粤B37659D 蒙H37659D

/home/zhouping/algoSdk/testData/newEnergyVehicle_100/38608_1518056977000_part.jpg 粤BZ9589
/home/zhouping/algoSdk/testData/newEnergyVehicle_100/38561_1518056943000_part.jpg 粤B05198D
/home/zhouping/algoSdk/testData/newEnergyVehicle_100/38578_1518056958000_part.jpg 粤B34037D
total: 78
err: 12
errRate: 0.153846153846
acccurate: 0.846153846154
"""
if __name__ == "__main__":
    #filename = sys.argv[1:]
    filename = "../data/newEnergyVehicle100_new.result"
    dglpScoreCheck("%s" % filename)  
