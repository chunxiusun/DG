#!/usr/bin/env python

import sys
sys.path.append("../lib")

from dgface_config import Config
c = Config()
print c
print c.DumpValues()
