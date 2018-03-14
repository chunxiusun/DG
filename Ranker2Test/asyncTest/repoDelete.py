#!/usr/bin/env python
#!coding=utf-8 


from repoRanker2 import Ranker2Repo

# Assign ranker2 repo instance
repo = Ranker2Repo("http://192.168.2.19:6501/rank/repo")
        
# Do the repo delete operation
print '::Do the repo delete'
delete_source = {"Context":{},"Repo":{"Operation":2,"RepoId":"repo1"}}
repo.deleteRepo(delete_source)

# Do the repo query operation
print '\r::Do the repo query'
query_source = {"Context":{},"Repo":{"Operation":4,"RepoId":"repo1"}}
repo.queryRepo(query_source)