#!/usr/bin/env python

import sys

# Append path
sys.path.append("../utils")
sys.path.append("../lib")

# Load the iso
from detector import *

# Entrance 
def main():

    # Load the config file
    from dgface_config_py import Config

    # Read the json file 
    pipeline_cfg = Config()
    pipeline_cfg.load("../config/pipeline_test_config.json")

    # Assign detec, align, regonize method 
    detect_methods = pipeline_cfg.getStringArray("FaceDetector")
    align_methods = pipeline_cfg.getStringArray("FaceAlignment")
    recog_methods = pipeline_cfg.getStringArray("FaceRecognition")

    # Assign all_feature and final_parent_path
    all_feature = []
    final_parent_path = ""

    # Assing Detector, Alignment, Recognition
    detector =  Detector()   
