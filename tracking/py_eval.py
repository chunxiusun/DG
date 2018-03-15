
# coding: utf-8

# In[34]:


import os
import cv2
import matplotlib.pyplot as plt
import scipy.io as scio
import numpy as np
from scipy import spatial
import copy
import math
from tqdm import tqdm
import util


# In[35]:


class Rect:
    def __init__(self,rect_vec):
        self.x=rect_vec[0]
        self.y=rect_vec[1]
        self.w=rect_vec[2]
        self.h=rect_vec[3]

    @property #属性函数
    def width(self):
        return self.w
    @property
    def height(self):
        return self.h
    @property
    def center_x(self):
        return self.x+self.w/2
    @property
    def center_y(self):
        return self.y+self.h/2
    
    def keepLegal(self,pic_width,pic_height):
        self.x=max(self.x,0)
        self.y=max(self.y,0)
        self.w=max(self.w,0)
        self.h=max(self.h,0)
        if self.x+self.w>pic_width:
            if self.x >=pic_width:
                self.x=pic_width-1
                self.w=0
            else:
                self.w=pic_width-self.x-1
        if self.y+ self.h>pic_height:
            if self.y>= pic_height:
                self.y=pic_height-1
                self.h=0
            else:
                self.h=pic_height-self.y-1
        
    def addAndGetNew(self,dx,dy,pic_width=1000000,pic_height=1000000):
        rect=Rect([self.x+dx,self.y+dy,self.w,self.h])
        rect.keepLegal(pic_width,pic_height)
        return rect
    
    def __str__(self):
        return '%d %d %d %d' % (self.x,self.y,self.w,self.h)


# In[36]:


class GroundBox:
    def __init__(self,frameid,info):
        self.frame=frameid
        self.location=Rect([info[2],info[3],info[4],info[5]])
        self.trackid=info[0]
        self.type=info[1]
    def __str__(self):
        return '[frame]:%d [location]:%s [trackid]:%d [type]:%d' %         (self.frame,str(self.location),self.trackid,self.type)
class GroundBoxSystem:
    def _iou(self,i,j):
        overlap_w=min(i.x+i.w,j.x+j.w)-max(i.x,j.x);
        overlap_h=min(i.y+i.h,j.y+j.h)-max(i.y,j.y);
        if overlap_w<=0 or overlap_h<=0:
            return 0.0
        else:
            overlap_s=overlap_w*overlap_h
            return overlap_s*1.0/(i.w*i.h+j.w*j.h-overlap_s);

    def __init__(self,track_groundtruth_file):
        frameids,infos=util.read_imagelist(track_groundtruth_file)
        frameids=map(int,frameids)
        self.objectset={}
        self.id_objects_map={}
        for i in xrange(len(frameids)):
            groundbox=GroundBox(frameids[i],infos[i])
            if frameids[i] not in self.objectset:
                self.objectset[frameids[i]]=[]
            self.objectset[frameids[i]].append(groundbox)
            if groundbox.trackid not in self.id_objects_map:
                self.id_objects_map[groundbox.trackid]=[]
            self.id_objects_map[groundbox.trackid].append(groundbox)
        
        
        
    def getMaxIOUBox(self,frameindex,location):
        if frameindex not in self.objectset:
            return None,0
        box_set=self.objectset[frameindex]
        max_iou=0
        max_box=None
        for box in box_set:
            iou=self._iou(box.location,location)
            if iou>max_iou:
                max_box=box
                max_iou=iou
        return max_box,max_iou

    def show(self,frame_index,show=True):
        img=cv2.imread(pictures[frame_index])
        if show:
            plt.figure(figsize=(20,20))
        for obj in self.objectset[frame_index]:
            color=[255,0,0]
            hid=0
            obj=obj.location
            cv2.rectangle(img,tuple(map(int,[obj.x,obj.y])),tuple(map(int,[obj.x+obj.w,obj.y+obj.h])),color,thickness=4)
            cv2.putText(img, str(hid)+':', tuple(map(int,[obj.x,obj.y])), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2,False)

class AutoListMap:
    def __init__(self):
        self.data={}
        
    def __getitem__(self, key):
        return self.data[key]
    
    def add(self, key,value):
        if key not in self.data:
            self.data[key]=[]
        self.data[key].append(value)
        
    def keys(self):
        return self.data.keys()
# smap=AutoListMap()
# smap.add(342,65)
# smap.add(342,635)
# print smap[342]


# In[37]:

import argparse
parser=argparse.ArgumentParser()
parser.add_argument('dataset_id')
parser.add_argument('--origin',action='store_true')
args=parser.parse_args()



dataset_num=args.dataset_id
print 'dataset_num: ',dataset_num
if args.origin:
    track_file='origin_track_n'+dataset_num+'.log'
else:
    track_file='track_n'+dataset_num+'.txt'
tracksystem=GroundBoxSystem(track_file)
ground_file='12groundtruth/n'+dataset_num+'.txt'
groundsystem=GroundBoxSystem(ground_file)
pictures,_=util.read_imagelist('images_all/n'+dataset_num+'.list')

trackframes=tracksystem.objectset.keys()
trackframes=sorted(trackframes)
trackids=tracksystem.id_objects_map.keys()


# In[38]:


mcount,scount=0,0
keepd_ground_box=set()
location_count=0
location_set=[]

        
        
track_data=[]
track_data_index=AutoListMap()
track_data_location_index={}
ground_data=[]
ground_data_index=AutoListMap()
ground_data_location_index={}

for trackid in trackids:
    for gbox in tracksystem.id_objects_map[trackid]:
        mbox,miou=groundsystem.getMaxIOUBox(gbox.frame,gbox.location)
        if miou>0.5:
            track_data.append([gbox.trackid,location_count,gbox.frame])
            ground_data.append([mbox.trackid,location_count,mbox.frame])
            
            track_data_index.add(gbox.trackid,location_count)
            ground_data_index.add(mbox.trackid,location_count)
            track_data_location_index[location_count]=gbox.trackid
            ground_data_location_index[location_count]=mbox.trackid
            location_set.append([gbox.frame,gbox.location,mbox.location])
            location_count+=1
            gbox.id=mbox.trackid
            mcount+=1
            keepd_ground_box.add(mbox)
        else:
#             tracksystem.id_objects_map[trackid].remove(gbox)
#             tracksystem.objectset[gbox.frame].remove(gbox)
            pass
#             print gbox
        scount+=1
print 'Detect box in ground rate: ',mcount*1.0/scount


# In[39]:


mid_keeped=set()
sum_shang=0
for trackid in track_data_index.keys():
    shang=0
    countmap=util.countmap()
    sum_count=len(track_data_index[trackid])
    for i in track_data_index[trackid]:
        countmap.add(ground_data_location_index[i])
    countmap=countmap.getmap()
    max_oi=-1
    max_oi_num=0
    for i in countmap:
        if countmap[i]>max_oi_num:
            max_oi=i
            max_oi_num=countmap[i]
    mid_keeped.add(max_oi)
mid_all=set(ground_data_index.keys())
print '['+dataset_num+']losted rate:\t%f\t, repeated rate:\t%f\t, ground: %d, keepd: %d, tracked: %d' % (len(mid_all-mid_keeped)*100.0/len(mid_all),len(track_data_index.keys())*100/len(mid_all)-100,len(mid_all),len(mid_keeped),len(track_data_index.keys()))
# print sum_shang,sum_shang/len(track_data_index.keys())


# In[40]:


import math
sum_shang=0
for trackid in track_data_index.keys():
    shang=0
    countmap=util.countmap()
    sum_count=len(track_data_index[trackid])
    for i in track_data_index[trackid]:
        countmap.add(ground_data_location_index[i])
    countmap=countmap.getmap()
    for i in countmap:
        p=countmap[i]*1.0/sum_count
        shang+=-p*math.log(p)
    sum_shang+=shang
print 'Track purity: %f %f' % (sum_shang,sum_shang/len(track_data_index.keys()))


# In[41]:


sum_shang=0
for groundid in ground_data_index.keys():
    shang=0
    countmap=util.countmap()
    sum_count=len(ground_data_index[groundid])
    for i in ground_data_index[groundid]:
        countmap.add(track_data_location_index[i])
    countmap=countmap.getmap()
    for i in countmap:
        p=countmap[i]*1.0/sum_count
        shang+=-p*math.log(p)
    sum_shang+=shang
print 'Ground purity: %f %f' % (sum_shang,sum_shang/len(ground_data_index.keys()))


# In[16]:


def show(imagefile,locations):
    img=cv2.imread(imagefile)
    plt.figure(figsize=(20,20))    
    for loc in locations:
        cv2.rectangle(img,(loc.x,loc.y),(loc.x+loc.width,loc.y+loc.height),(255,0,0),thickness=2)
    plt.imshow(img[:,:,::-1])
# show(pictures[location_set[1703][0]],[location_set[1703][1]])
    


# In[44]:


# for trackid in groundsystem.id_objects_map:
#     toremove=[]
#     for z in groundsystem.id_objects_map[trackid]:
#         if z not in keepd_ground_box:
#             toremove.append(z)
#     for z in toremove:
#         groundsystem.id_objects_map[trackid].remove(z)
# for frame in groundsystem.objectset:
#     toremove=[]
#     for z in groundsystem.objectset[frame]:
#         if z not in keepd_ground_box:
#             toremove.append(z)    
#     for z in toremove:
#         groundsystem.objectset[frame].remove(z)


# In[45]:


# mcount=0
# for trackid in groundsystem.id_objects_map:
#     if len(groundsystem.id_objects_map[trackid])>0:
#         mcount+=1
# print mcount


# In[ ]:





# In[46]:


# mcount=0
# for trackid in tracksystem.id_objects_map:
#     if len(tracksystem.id_objects_map[trackid])>0:
#         mcount+=1
# print mcount


# In[17]:


# for frame in groundsystem.objectset:
#     for z in groundsystem.objectset[frame]:
#         for x in groundsystem.objectset[frame]:

