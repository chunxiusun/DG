#!/usr/bin/env python
#-*- coding:utf-8 -*-

import requests,json

IP = "192.168.2.19"
PORT = 9809

repoId = "2000w"
capacity = 20000000 #库容量


def add_repo():
    url = "http://%s:%s/rank/repo"%(IP,str(PORT))
    post_data = {
	         "Context":{},
	         "Repo": {"Operation": 1,
		          "RepoId": repoId,
		          "Level": 3, #Level 1-CPU,3-GPU
		          "FeatureLen": 384,
		          "Capacity": capacity,
		          "FeatureDataType": 2, #0-float,1-short,2-int8
		          "Params": [{"key": "GPUThreads",
				      "value": "[10]"
			             }]
	                 }
                }

    resp = requests.post(url,data=json.dumps(post_data))
    print resp.status_code
    print resp.content

def query_repo():
    url = "http://%s:%s/rank/repo"%(IP,str(PORT))
    post_data = {
	      "Context":{},
	      "Repo": {"Operation": 4}
                }
    resp = requests.post(url,data=json.dumps(post_data))
    print resp.status_code
    r_data = json.loads(resp.content)
    status = r_data["Context"]["Status"]
    for repo in r_data["Repos"]:
        repo_id = repo["RepoId"]
        if repo_id == repoId:
            repo_capacity = repo["Capacity"]
            repo_size = repo["Size"]
            print "RepoId:%s, Capacity:%d, Size:%d"%(repo_id,repo_capacity,repo_size)
            break

if __name__ == '__main__':
    add_repo()
    query_repo()
