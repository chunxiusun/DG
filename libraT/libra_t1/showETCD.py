# -*- coding: utf-8 -*-
'''
testLibra-TConfig
@author    :   inazhang<mailto:yanzhang@deepglint.com>
@copyright :   deepglint
@date      :   2015-11-02
@version   :   1.0.0
'''
import os, urllib2, json, re

url_prefix = "http://127.0.0.1:4001/v2/keys/config/"

def get_sensor_id():
    '''
    @note:get seneor id from etcd
    '''
    url = url_prefix+"global/sensor_uid"
    json_data = urllib2.urlopen(url).read()
    dict_data = json.loads(json_data)
    sensor_id = dict_data['node']['value']
    return sensor_id

sensor_id = get_sensor_id()

def time_range(rangelist):
    '''
    @param rangelist:etcd中的TimeRange值
    @type flag:list
    
    @note:将分钟转换为H:M的格式
    '''
    h1 = int(rangelist[0])/60
    m1 = int(rangelist[0])%60
    h2 = int(rangelist[1])/60
    m2 = int(rangelist[1])%60
    start = "%d:%d" % (h1, m1)
    end = "%d:%d" % (h2, m2)
    return [start, end]


def weekday_range(week):
    '''
    @param week:etcd中的WeekdayRange值
    @type week:int
    
    @note:将WeekdayRange转换为星期
    '''
    weeknum = bin(128 + week)[2:]
    weekday = []
    if weeknum[6:7] == '0':
       weekday.append('星期一')
    if weeknum[5:6] == '0':
       weekday.append('星期二')
    if weeknum[4:5] == '0':
       weekday.append('星期三')
    if weeknum[3:4] == '0':
       weekday.append('星期四')
    if weeknum[2:3] == '0':
       weekday.append('星期五')
    if weeknum[1:2] == '0':
       weekday.append('星期六')
    if weeknum[7:8] == '0':
       weekday.append('星期日')

    return weekday

def get_all_id(name, hotspots = 0):
    '''
    @param name:要查找的名称
    @type name:str
    @param hotspots:默认为0，当不为0时为door或者fence
    @type hotspots:str

    @note:查找所有前缀为name的Id
    '''
    if hotspots == 0:
       url = url_prefix + "eventbrain/alertrule/"+sensor_id
    else:
       url = url_prefix + "eventbrain/alertrule/"+sensor_id+"/"+hotspots
    json_data =  urllib2.urlopen(url).read()
    dict_data = json.loads(json_data)
    node_data = dict_data['node']
    nodes_data = node_data['nodes']
    #print len(nodes_data)
    idlist = []
    #print nodes_data
    for item in nodes_data:
       #print item
       #print item['value'] 
       try: #door_1没有value值
          s = "".join(item['value'].split())
          s = s.replace('true', 'True')
          s = s.replace('false', 'False')
          dict1 = eval(s)
          #if hotspots == 0:
          if name in dict1['Id']:
             idlist.append(dict1['Id'])
         # else:
         #    if name in dict1['Id']:
         #       idlist.append(dict1['Id'])
           #  if "hotspot_legacy" in dict1['Id']:
           #     idlist.append(dict1['Id'])
       except:
          continue
    return idlist

def get_hotspots_num(name):
    '''
    @param name:etcd中door或者fence
    @type name:str
    
    @note:查找有几个door或者fence
    '''
    url = url_prefix + "eventbrain/alertrule/"+sensor_id
    json_data =  urllib2.urlopen(url).read()
    dict_data = json.loads(json_data)
    node_data = dict_data['node']
    nodes_data = node_data['nodes']
    #print len(nodes_data)
    idlist = []
    #print nodes_data
    for item in nodes_data:
       #print item
       #print item['key'] 
       s = item['key']
       h = []
       regex = re.compile(name+'_\d*')
       if name in s:
          h = regex.findall(s)
          idlist.append(h[0])
    #print idlist
    return idlist


def show_mininum_height():
    '''
    @note:显示ETCD中人员最低身高设置
    '''
    url = url_prefix + "libra/data/detection_minimum_height"
    json_data = urllib2.urlopen(url).read()
    dict_data = json.loads(json_data)
    etcd_value = dict_data['node']['value']
    height_etcd = float(etcd_value)/10
    print "人员识别最低身高: " + str(height_etcd) + "厘米"


def show_fall_detection():
    '''
    @note:显示ETCD中倒地侦测是否开启
    '''
    url = url_prefix + "libra/data/enable_fall_detection"
    json_data = urllib2.urlopen(url).read()
    dict_data = json.loads(json_data)
    etcd_value = dict_data['node']['value']
    if etcd_value == '1':
       flag = 'True'
    else:
       flag = 'False'
    print "开启倒地侦测: " + flag


def show_abnormal_action_detection():
    '''
    @note:显示ETCD中剧烈运动侦测是否开启
    '''
    url = url_prefix + "libra/data/enable_abnormal_action_detection"
    json_data = urllib2.urlopen(url).read()
    dict_data = json.loads(json_data)
    etcd_value = dict_data['node']['value']
    if etcd_value == '1':
       flag = 'True'
    else:
       flag = 'False'
    print "开启剧烈运动侦测: " + flag


def show_abnormal_threshold():
    '''
    @note:显示ETCD中剧烈运动阈值
    '''
    url = url_prefix + "libra/data/abnormal_threshold"
    json_data = urllib2.urlopen(url).read()
    dict_data = json.loads(json_data)
    etcd_value = dict_data['node']['value'].encode('utf8')
    print "剧烈运动阈值: " + etcd_value


def show_lens_protection_detection():
    '''
    @note:显示ETCD中镜头异常侦测是否开启
    '''
    url = url_prefix + "libra/data/enable_lens_protection"
    json_data = urllib2.urlopen(url).read()
    dict_data = json.loads(json_data)
    etcd_value = dict_data['node']['value']
    if etcd_value == '1':
       flag = 'True'
    else:
       flag = 'False'
    print "开启镜头异常侦测: " + flag

def show_darkness_detection():
    '''
    @note:显示ETCD中光线变化侦测是否开启
    '''
    url = url_prefix + "libra/data/enable_darkness_detection"
    json_data = urllib2.urlopen(url).read()
    dict_data = json.loads(json_data)
    etcd_value = dict_data['node']['value']
    if etcd_value == '1':
       flag = 'True'
    else:
       flag = 'False'
    print "开启光线变化侦测: " + flag

def show_invalid_operation_detection():
    '''
    @note:显示ETCD中单人加钞侦测是否开启
    '''
    url = url_prefix + "libra/data/enable_invalid_operation_detection"
    json_data = urllib2.urlopen(url).read()
    dict_data = json.loads(json_data)
    etcd_value = dict_data['node']['value']
    if etcd_value == '1':
       flag = 'True'
    else:
       flag = 'False'
    print "开启单人加钞侦测: " + flag

def show_invalid_operation_time_threshold():
    '''
    @note:显示ETCD中单人加钞触发时间
    '''
    url = url_prefix + "libra/data/invalid_operation_time_threshold"
    json_data = urllib2.urlopen(url).read()
    dict_data = json.loads(json_data)
    etcd_value = dict_data['node']['value'].encode('utf8')
    print "单人加钞触发时间: " + etcd_value

def show_velocity_legacy():
    '''
    @note:显示ETCD中移动过快速度全时段和分时段设置
    '''
    idlist = sorted(get_all_id('velocity'),reverse=True)
    for item in idlist:
       url = url_prefix + "eventbrain/alertrule/"+sensor_id+"/"+item
       json_data = urllib2.urlopen(url).read()
       dict_data = json.loads(json_data)
       node_data = json.loads(dict_data['node']['value'])
       etcd_value = str(float(node_data['UpperBound'])/1000)
       etcd_flag = str(node_data['Enabled'])
       if item == "velocity_legacy":
          print "移动过快触发速度 【全时段】: %s, %s米/秒" % (etcd_flag, etcd_value)
       else:
          time_value = time_range(node_data['TimeRange'])
          weekday_value = weekday_range(node_data['WeekdayRange'])
          print "移动过快触发速度 ----分时段: %s, %s米/秒, %s, %s" % (etcd_flag, etcd_value, time_value, str(weekday_value).decode('string_escape'))

def show_population_legacy():
    '''
    @note:显示ETCD中最大人数全时段和分时段设置
    '''
    idlist = sorted(get_all_id('population'),reverse=True)
    for item in idlist:
       url = url_prefix + "eventbrain/alertrule/"+sensor_id+"/"+item
       json_data = urllib2.urlopen(url).read()
       dict_data = json.loads(json_data)
       node_data = json.loads(dict_data['node']['value'])
       etcd_value = str(node_data['UpperBound'])
       etcd_flag = str(node_data['Enabled'])
       if item == "population_legacy":
          print "场景内允许的最大人数 【全时段】: %s, %s" % (etcd_flag, etcd_value)
       else:
          weekday_value = weekday_range(node_data['WeekdayRange'])
          time_value = time_range(node_data['TimeRange'])
          print "场景内允许的最大人数 ----分时段: %s, %s, %s, %s" % (etcd_flag, etcd_value, time_value, str(weekday_value).decode('string_escape'))


def show_route_overlength():
    '''
    @note:显示ETCD中行程过长全时段和分时段设置
    '''
    idlist = sorted(get_all_id('distance'),reverse=True)
    for item in idlist:
       url = url_prefix + "eventbrain/alertrule/"+sensor_id+"/"+item
       json_data = urllib2.urlopen(url).read()
       dict_data = json.loads(json_data)
       node_data = json.loads(dict_data['node']['value'])
       etcd_value = str(float(node_data['UpperBound'])/1000)
       etcd_flag = str(node_data['Enabled'])
       if item == "distance_legacy":
          print "行程过长触发距离 【全时段】: %s, %s米" % (etcd_flag, etcd_value)
       else:
          time_value = time_range(node_data['TimeRange'])
          weekday_value = weekday_range(node_data['WeekdayRange'])
          print "行程过长触发距离 ----分时段: %s, %s米, %s, %s" % (etcd_flag, etcd_value, time_value, str(weekday_value).decode('string_escape'))

def show_dwellingtime_legacy():
    '''
    @note:显示ETCD中逗留过久时间全时段和分时段设置
    '''
    idlist = sorted(get_all_id('dwellingtime'),reverse=True)
    for item in idlist:
       url = url_prefix + "eventbrain/alertrule/"+sensor_id+"/"+item
       json_data = urllib2.urlopen(url).read()
       dict_data = json.loads(json_data)
       node_data = json.loads(dict_data['node']['value'])
       etcd_value = str(node_data['UpperBound'])
       etcd_flag = str(node_data['Enabled'])
       if item == "dwellingtime_legacy":
          print "逗留过久触发时间 【全时段】: %s, %s秒" % (etcd_flag, etcd_value)
       else:
          time_value = time_range(node_data['TimeRange'])
          weekday_value = weekday_range(node_data['WeekdayRange'])
          print "逗留过久触发时间 ----分时段: %s, %s秒, %s, %s" % (etcd_flag, etcd_value, time_value, str(weekday_value).decode('string_escape'))

def show_door_legacy():
    '''
    @note:显示ETCD中越线设置所有door的全时段和分时段设置
    '''
    numlist = get_hotspots_num('door') #找到有几个door
    for item in sorted(numlist):
       #url = url_prefix + "eventbrain/alertrule/"+sensor_id+"/"+item
       hotspots_url =  url_prefix + "eventbrain/hotspots/"+sensor_id+"/door/"+item
       json_data = urllib2.urlopen(hotspots_url).read()
       dict_data = json.loads(json_data)
       node_data = json.loads(dict_data['node']['value'])
       door_InwardAlert_etcd = str(node_data['InwardAlert'])
       door_OutwardAlert_etcd = str(node_data['OutwardAlert'])
       print "%s越线设置: " % item.encode('utf8')
       print "进入方向侦测: %s, 离开方向侦测: %s" % (door_InwardAlert_etcd, door_OutwardAlert_etcd)
       #idlist = get_all_id('door', item) #进入door_*目录下找到有几个分时段设置的door_***以及hotspot_legacy
       idlist = get_all_id('hotspot', item) #分时段的改为hotspot_***
       for item1 in sorted(idlist, reverse=True):
          url = url_prefix + "eventbrain/alertrule/"+sensor_id+"/"+item+"/"+item1
          json_data = urllib2.urlopen(url).read()
          dict_data = json.loads(json_data)
          node_data = json.loads(dict_data['node']['value'])
          #etcd_value = str(node_data['UpperBound'])
          etcd_flag = str(node_data['Enabled'])
          #print item1
          if item1 == "hotspot_legacy":
             print "--【全时段】: %s" % (etcd_flag)
          else:
             time_value = time_range(node_data['TimeRange'])
             weekday_value = weekday_range(node_data['WeekdayRange'])
             print "----分时段: %s, %s, %s" % (etcd_flag, time_value, str(weekday_value).decode('string_escape'))

def show_fence_legacy():
    '''
    @note:显示ETCD中区域设置所有fence的全时段和分时段设置
    '''
    numlist = get_hotspots_num('fence') #找到有几个fence
    for item in sorted(numlist):
       #url = url_prefix + "eventbrain/alertrule/"+sensor_id+"/"+item
       hotspots_url =  url_prefix + "eventbrain/hotspots/"+sensor_id+"/fence/"+item
       json_data = urllib2.urlopen(hotspots_url).read()
       dict_data = json.loads(json_data)
       node_data = json.loads(dict_data['node']['value'])
       fence_InwardAlert_etcd = str(node_data['InwardAlert'])
       fence_OutwardAlert_etcd = str(node_data['OutwardAlert'])
       fence_PopulationAlert = str(node_data['InsidePopulationAlert'])
       fence_PopulationThreshold = node_data['PopulationThreshold'][0:2]
       idlist = get_all_id('hotspot', item) 
       print "%s区域设置: " % item.encode('utf8')
       print "进入区域侦测: %s, 离开区域侦测: %s" % (fence_InwardAlert_etcd, fence_OutwardAlert_etcd)
       print "区域人数异常侦测: %s, 下限: %s 上限: %s" % (fence_PopulationAlert, fence_PopulationThreshold[0], fence_PopulationThreshold[1])
       for item1 in sorted(idlist, reverse=True):
          url = url_prefix + "eventbrain/alertrule/"+sensor_id+"/"+item+"/"+item1
          json_data = urllib2.urlopen(url).read()
          dict_data = json.loads(json_data)
          node_data = json.loads(dict_data['node']['value'])
          #etcd_value = str(node_data['UpperBound'])
          etcd_flag = str(node_data['Enabled'])
          #print item1
          if item1 == "hotspot_legacy":
             print "--【全时段】: %s" % (etcd_flag)
          else:
             weekday_value = weekday_range(node_data['WeekdayRange'])
             time_value = time_range(node_data['TimeRange'])
             print "----分时段: %s, %s, %s" % (etcd_flag, time_value, str(weekday_value).decode('string_escape'))



def run():
   print "========================================="
   show_mininum_height()
   print "========================================="
   show_fall_detection()
   print "========================================="
   show_abnormal_action_detection()
   show_abnormal_threshold()
   print "========================================="
   show_lens_protection_detection()
   print "========================================="
   show_darkness_detection()
   print "========================================="
   show_invalid_operation_detection()
   show_invalid_operation_time_threshold()
   print "========================================="
   show_velocity_legacy()
   print "========================================="
   show_population_legacy()
   print "========================================="
   show_route_overlength()
   print "========================================="
   show_dwellingtime_legacy()
   print "========================================="
   show_door_legacy()
   print "========================================="
   show_fence_legacy()


if __name__ == "__main__":
   run()
