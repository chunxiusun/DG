#/usr/bin/env python
#!coding=utf-8

from helper import getChoiceNum, getRandomString, featureCreate
import random 
import uuid 
import time 
import json 

# repo
repoId = getRandomString(5, 1)

# repo create
repoLevelList = [1, 3]
repoLevel = getChoiceNum(repoLevelList)
repoLevelMap = {1: "REPO_LEVEL_ON_STORAGE", 3: "REPO_LEVEL_ON_GPU"}

# repo update
updateRepoLevelList = [1, 3]
updateRepoLevel = getChoiceNum(repoLevelList)
updateFeatureCapacity = getRandomString(5)
updateFeatureGpuThread = random.choice(['[1]', '[1,1,1,1]'])

# repo delete
deleteStatusCode = {"Normal": 200, "Abnormal":400}
deleteMessage = {"Success":"success", "Fail":"not exist"}
deleteTimes = 10

# feature add
featureLenList = [128, 256, 384]
featureLen = getChoiceNum(featureLenList)
featureDataTypeList = [0, 1, 2]
featureDataTypeMap = {0:"FEATURE_DATA_TYPE_FLOAT", 1:"FEATURE_DATA_TYPE_SHORT", 2:"FEATURE_DATA_TYPE_INT8"}
featureDataType = getChoiceNum(featureDataTypeList)
featureCapacity = getRandomString(5)
featureGpuThread = random.choice(['[1]', '[1,1,1,1]'])

featureString = featureCreate(featureLen)
featureId = str(uuid.uuid4())
featureLocation = getRandomString(5, 1)

cur_ts = time.localtime()
tsstr = "%d %d 17 %d:%d:%d" % (random.randint(1,30), 9, cur_ts.tm_sec, cur_ts.tm_min, cur_ts.tm_hour)
featureTime = int(time.mktime(time.strptime(tsstr, "%d %m %y %S:%M:%H"))) 

attrKey = getRandomString(5, 1)
attrValue = getRandomString(5)
featureAttributes = '{"%s":%s}' % (attrKey, attrValue)
featureSessionId = getRandomString(5, 1)

# feature update
updateFeatureString = featureCreate(featureLen)
updateFeatureLocation = getRandomString(5, 1)

cur_ts = time.localtime()
tsstr = "%d %d 17 %d:%d:%d" % (random.randint(1,30), 9, cur_ts.tm_sec, cur_ts.tm_min, cur_ts.tm_hour)
updateFeatureTime = int(time.mktime(time.strptime(tsstr, "%d %m %y %S:%M:%H"))) 

attrKey = getRandomString(5, 1)
attrValue = getRandomString(5)
updateFeatureAttributes = '{"%s":%s}' % (attrKey, attrValue)

# 1vn ranker 
ranker1v1FeatureLen = getChoiceNum(featureLenList)
ranker1v1ObjectFeature = featureCreate(ranker1v1FeatureLen)

ranker1v1ObjectCandidates = []
ranker1v1ObjectCandidatesNumber = 100
for i in range(0, ranker1v1ObjectCandidatesNumber):
    if i == 0:
        ranker1v1ObjectCandidates.append({"Id":"0", "Feature":"%s" % ranker1v1ObjectFeature},)
    elif i == ranker1v1ObjectCandidatesNumber -1:
        ranker1v1ObjectCandidates.append({"Id":"%s" % i, "Feature":featureCreate(ranker1v1FeatureLen)})
    else:
        ranker1v1ObjectCandidates.append({"Id":"%s" % i, "Feature":featureCreate(ranker1v1FeatureLen)},)
        

ranker1v1ObjectCandidates = json.dumps(ranker1v1ObjectCandidates)
ranker1v1ScoreExpect = 0.9999

# 1vN ranker
ranker1vNRepoId = getRandomString(5, 1)
ranker1vNRepoLevelList = [1, 3]
ranker1vNRepoLevel = getChoiceNum(ranker1vNRepoLevelList)
ranker1vNFeatureLenList = [128, 256, 384]
ranker1vNFeatureLen = getChoiceNum(ranker1vNFeatureLenList)
ranker1vNObjectFeature = featureCreate(ranker1vNFeatureLen)
ranker1vNFeatureDataTypeList = [0, 1, 2]
ranker1vNFeatureDataTypeMap = {0:"FEATURE_DATA_TYPE_FLOAT", 1:"FEATURE_DATA_TYPE_SHORT", 2:"FEATURE_DATA_TYPE_INT8"}
ranker1vNFeatureDataType = getChoiceNum(ranker1vNFeatureDataTypeList)
ranker1vNFeatureCapacity = getRandomString(5)
ranker1vNFeatureId = str(uuid.uuid4())
ranker1vNFeatureLocation = getRandomString(5, 1)
ranker1vNFeatureGpuThread = random.choice(['[1]', '[1,1,1,1]'])
ranker1vNFeatureString = ranker1vNObjectFeature

cur_ts = time.localtime()
tsstr = "%d %d 17 %d:%d:%d" % (random.randint(1,30), 9, cur_ts.tm_sec, cur_ts.tm_min, cur_ts.tm_hour)
ranker1vNFeatureTime = int(time.mktime(time.strptime(tsstr, "%d %m %y %S:%M:%H"))) 

attrKey = getRandomString(5, 1)
attrValue = getRandomString(5)
ranker1vNFeatureAttributes = '{"%s":%s}' % (attrKey, attrValue)

ranker1vNMoreFeatureNumber = 100
ranker1vNScoreExpect = 0.9999