#!/usr/bin/python
#-*- coding:utf-8 -*-

# author : chunxiusun


import logging
import logging.handlers

import os
import config

os.system("mkdir -p ./log")

formatter = logging.Formatter(
    '%(asctime)s %(filename)s %(funcName)s [line:%(lineno)d] %(levelname)s: %(message)s')

debug_log_file = './log/libraf.log'
debug_logger_handler = logging.handlers.TimedRotatingFileHandler(debug_log_file, 'D')
debug_logger_handler.setLevel(logging.DEBUG)
debug_logger_handler.setFormatter(formatter)


logger_stream = logging.StreamHandler()
logger_stream.setLevel(logging.DEBUG)
logger_stream.setFormatter(formatter)


logger = logging.getLogger('LibraFLogger')
logger.setLevel(logging.DEBUG)
logger.addHandler(debug_logger_handler)
#logger.addHandler(logger_stream)
