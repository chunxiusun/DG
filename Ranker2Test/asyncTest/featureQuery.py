#!/usr/bin/env python
#!coding=utf-8 


from featureRanker2 import Ranker2Feature

# Assign ranker2 repo and feature instance
repoid = 'repo1'
FeatureLen = 256
featureid = "4dd5b46a-b227-11e7-a604-408d5c1565b5"
feature_url = "http://192.168.2.19:6501/rank/feature"

fea = Ranker2Feature(feature_url)
        
# Do the feature query operation
print '\r::Do the feature query'
query_source = {"Context":{},"Features": {"Operation":4,"ObjectFeatures":[{"Id":featureid}]}}
fea.queryFeature(query_source)
