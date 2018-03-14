#!/usr/bin/env python
# -*- coding: utf8 -*-
import base64
import json
import numpy as np
import requests
import signal
import sys
import threading
import time
import random
import uuid
from sklearn import preprocessing
from threading import Thread

# sys.path.append(os.getcwd()+'/proto/python')
#
# reload(sys)
# sys.setdefaultencoding("utf-8")

# Ranker service address
# IP = "192.168.2.130"
IP = "192.168.2.19"
RestfulPort = 6501

ServiceRestful = "http://" + IP + ":" + str(RestfulPort) + "/rank"
feature_len = 384
totalPerThread = 10000000
small_n = 100

ss_mutex = threading.Lock()
cur_rankered_succ = 1
cur_rankered_fail =0
cur_rankered_num = 0
req_failed = 0
req_time = 0
status_interval = 2


def signal_handler(signum, aaa):
    sys.exit()


def start_restful(threadindex):
    global cur_rankered_succ
    global cur_rankered_num
    global cur_rankered_fail
    global req_failed
    global req_time

    for index in range(totalPerThread):
        source = {"Context": {"SessionId": "ss_%s" % index}, "ObjectFeature": {"Feature":""},"Params":[{"key":"Normalization","value":"false"},{"key":"MaxCandidates","value":str(small_n)}],"ObjectCandidates":[]}
        featureFloat = np.random.random_sample((feature_len,))
        featureFloat = featureFloat.astype('float32')
        featureFloat = preprocessing.normalize(featureFloat.reshape(1, feature_len), norm='l2')
        featureString = base64.b64encode(featureFloat)
        source["ObjectFeature"]["Feature"]=featureString
        for i in range(1,small_n+1):
            featureFloat = np.random.random_sample((feature_len,))
            featureFloat = featureFloat.astype('float32')
            featureFloat = preprocessing.normalize(featureFloat.reshape(1, feature_len), norm='l2')
            featureString = base64.b64encode(featureFloat)
            candidates = {"Id":str(i),"Feature":featureString}
            source["ObjectCandidates"].append(candidates)

        #print source
        # if index % batchsize == 0:
        post_data = json.dumps(source)
        # print post_data
        try:
            timestart = time.time()
            resp = requests.post(ServiceRestful, data=post_data)
            req_time = time.time() - timestart + req_time
        except requests.RequestException as e:
            resp.close()
            continue

        if resp.status_code != 200:
            req_failed = req_failed + 1
            resp.close()
            continue

        content = json.loads(resp.content)
        if content["Context"]["Status"]=="200" and len(content["Candidates"]) == small_n:
            cur_rankered_succ = cur_rankered_succ+ 1
        else:
            cur_rankered_fail = cur_rankered_fail+ 1
        resp.close()


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    threads = []
    start_time = time.time()
    t = Thread(target=start_restful, args=(1,))
    t.start()
    while True:
        print "Rankered succ: %d,    rankered failed: %d,     req failed: %d" % (cur_rankered_succ, cur_rankered_fail, req_failed)
        print "Rankered QPS: %f"%((cur_rankered_succ+cur_rankered_fail)/(time.time() - start_time))
        print "Rankered Latency: %f"%(req_time/(cur_rankered_succ+cur_rankered_fail))
        time.sleep(status_interval)
