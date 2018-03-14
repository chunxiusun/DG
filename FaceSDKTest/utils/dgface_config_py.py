#!/usr/bin/env python

import json

class Config:
    def __init__(self):
        self.jsonobj = None

    def load(self, configFile):
        print "Load config file: ", configFile
        with open(configFile) as f:
            self.jsonobj = json.load(f) 

    def getStringArray(self, key):
        jsonValue = []
        for value in self.jsonobj[key]:
            jsonValue.append(value.encode('ascii'))

        return jsonValue       

if __name__ == "__main__":
    pipeline_cfg = Config()
    pipeline_cfg.load("../config/pipeline_test_config.json")
    print pipeline_cfg.getStringArray("FaceDetector")
