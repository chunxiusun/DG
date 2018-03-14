#!/bin/bash

ps -ef|grep -E "1vNRanker.py|addFeature.py" |awk '{print $2}'|xargs kill -9
