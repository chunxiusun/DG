#!/bin/bash

ps -ef|grep add_feature_truth.py|awk '{print $2}'|xargs kill -9
ps -ef|grep ranker_1vN.py|awk '{print $2}'|xargs kill -9
