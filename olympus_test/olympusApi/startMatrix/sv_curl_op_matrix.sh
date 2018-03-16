#!/bin/bash
op=$1
for id in `cat iid.list`
do
	curl 192.168.2.18:8900/olympus/v1/instance/delete?iid=${op} -X POST
done
