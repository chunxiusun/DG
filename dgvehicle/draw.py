#!/usr/bin/env python
#-*- coding:utf-8 -*-

import xlrd
import matplotlib.pyplot as plt


fileOld = "12_1.xls"
fileNew = "12.xls"
#flag = 0 #0 meas recall,1 means accuracy

def deal(filename):
    vehicle = {}
    tricycle = {}
    pedestrian = {}
    bicycle = {}
    type_list = ["vehicle","tricycle","pedestrian","bicycle"]
    type_rate = ["recall_y","accuracy_y","recall_x","accuracy_x"]
    for item in type_list:
        for ty in type_rate:
            if ty not in item:
                eval(item)[ty] = []
    data = xlrd.open_workbook(filename)
    table = data.sheets()[0]
    nrows = table.nrows
    ncols = table.ncols
    for i in range(2,nrows):
        if table.row(i)[1].value != "":
            vehicle["recall_x"].append(int(table.row(i)[0].value))
            vehicle["recall_y"].append(eval(table.row(i)[1].value.split("%")[0]))
        if table.row(i)[2].value != "":
            vehicle["accuracy_x"].append(int(table.row(i)[0].value))
            vehicle["accuracy_y"].append(eval(table.row(i)[2].value.split("%")[0]))
        
        if table.row(i)[7].value != "":
            tricycle["recall_x"].append(int(table.row(i)[0].value))
            tricycle["recall_y"].append(eval(table.row(i)[7].value.split("%")[0]))
        if table.row(i)[8].value != "":
            tricycle["accuracy_x"].append(int(table.row(i)[0].value))
            tricycle["accuracy_y"].append(eval(table.row(i)[8].value.split("%")[0]))

        if table.row(i)[3].value != "":
            pedestrian["recall_x"].append(int(table.row(i)[0].value))
            pedestrian["recall_y"].append(eval(table.row(i)[3].value.split("%")[0]))
        if table.row(i)[4].value != "":
            pedestrian["accuracy_x"].append(int(table.row(i)[0].value))
            pedestrian["accuracy_y"].append(eval(table.row(i)[4].value.split("%")[0]))

        if table.row(i)[5].value != "":
            bicycle["recall_x"].append(int(table.row(i)[0].value))
            bicycle["recall_y"].append(eval(table.row(i)[5].value.split("%")[0]))
        if table.row(i)[6].value != "":
            bicycle["accuracy_x"].append(int(table.row(i)[0].value))
            bicycle["accuracy_y"].append(eval(table.row(i)[6].value.split("%")[0]))
            
    #print vehicle
    return vehicle,tricycle,pedestrian,bicycle

def draw(flag):
    vehicle_1,tricycle_1,pedestrian_1,bicycle_1 = deal(fileOld)
    vehicle_2,tricycle_2,pedestrian_2,bicycle_2 = deal(fileNew)
    plt.subplot(221)
    plt.xlim(xmax=13,xmin=0)
    plt.ylim(ymax=110,ymin=0)
    #plt.xlabel("video")
    plt.ylabel("rate(%)")
    plt.title("vehicle")
    if flag == 0:
        plt.plot(vehicle_1["recall_x"],vehicle_1["recall_y"],'ro')#,label="sine")
        plt.plot(vehicle_2["recall_x"],vehicle_2["recall_y"],'bo')
    elif flag == 1:
        plt.plot(vehicle_1["accuracy_x"],vehicle_1["accuracy_y"],'ro')
        plt.plot(vehicle_2["accuracy_x"],vehicle_2["accuracy_y"],'bo')

    plt.subplot(222)
    plt.xlim(xmax=13,xmin=0)
    plt.ylim(ymax=110,ymin=0)
    #plt.xlabel("video")
    plt.ylabel("rate(%)")
    plt.title("tricycle")
    if flag == 0:
        plt.plot(tricycle_1["recall_x"],tricycle_1["recall_y"],'ro')
        plt.plot(tricycle_2["recall_x"],tricycle_2["recall_y"],'bo')
    elif flag == 1:
        plt.plot(tricycle_1["accuracy_x"],tricycle_1["accuracy_y"],'ro')
        plt.plot(tricycle_2["accuracy_x"],tricycle_2["accuracy_y"],'bo')

    plt.subplot(223)
    plt.xlim(xmax=13,xmin=0)
    plt.ylim(ymax=110,ymin=0)
    #plt.xlabel("video")
    plt.ylabel("rate(%)")
    plt.title("pedestrian")
    if flag == 0:
        plt.plot(pedestrian_1["recall_x"],pedestrian_1["recall_y"],'ro')
        plt.plot(pedestrian_2["recall_x"],pedestrian_2["recall_y"],'bo')
    elif flag == 1:
        plt.plot(pedestrian_1["accuracy_x"],pedestrian_1["accuracy_y"],'ro')
        plt.plot(pedestrian_2["accuracy_x"],pedestrian_2["accuracy_y"],'bo')

    plt.subplot(224)
    plt.xlim(xmax=13,xmin=0)
    plt.ylim(ymax=110,ymin=0)
    #plt.xlabel("video")
    plt.ylabel("rate(%)")
    plt.title("bicycle")
    if flag == 0:
        plt.plot(bicycle_1["recall_x"],bicycle_1["recall_y"],'ro')
        plt.plot(bicycle_2["recall_x"],bicycle_2["recall_y"],'bo')
    elif flag == 1:
        plt.plot(bicycle_1["accuracy_x"],bicycle_1["accuracy_y"],'ro')
        plt.plot(bicycle_2["accuracy_x"],bicycle_2["accuracy_y"],'bo')

    #legend(loc='upper left')
    #plt.show()
    if flag == 0:
        img_name = "recallRate.png"
    elif flag == 1:
        img_name = "accuracyRate.png"
    plt.savefig(img_name)
    plt.close()

if __name__ == '__main__':
    for i in range(2):
        draw(i)
