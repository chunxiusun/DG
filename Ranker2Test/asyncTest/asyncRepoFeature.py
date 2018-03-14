#!/home/dell/anaconda3/bin/python
#coding=utf-8

import string
import random
import re 
from repoRanker2 import Ranker2Repo
from featureCreate import featureCreate
from featureRanker2 import Ranker2Feature
from multiprocessing import Pool
from queue import Queue
import threading
import time

# Get random string
def getRandomString(strLen=None, type_=0):

    '''
    type = 0, means number
    type = 1, means string
    '''

    retStr = ""

    if type_ == 0:
        str_ = string.digits    
    else:
        str_ = string.hexdigits

    for _index in range(int(strLen)):
        i = random.randint(0, 9)
        tmp = str_[i-1]
        retStr += tmp
    
    retStr = re.sub(r"\b0*([1-9][0-9]*|0)", r"\1", retStr)  

    return retStr

# Get choice num
def getChoiceNum(nList):

    return random.choice(nList)    

# repo add operation
def repoAdd():

    # Assign ranker2 repo instance
    repo = Ranker2Repo("http://192.168.2.19:6501/rank/repo")
        
    # Repo name
    repoid = 'repo1'

    # Do the repo add operation

    add_source = {"Context":{},"Repo":{"Operation":1,"RepoId":repoid,"Level":3,"FeatureLen":384,"Capacity":11000,"Params":[{"key":"GPUThreads","value":"[1,1,1,1]"}]}}
    repo.addRepo(add_source)
    
# repo delete operation
def repoDelete():
    
    # Assign ranker2 repo instance
    repo = Ranker2Repo("http://192.168.2.19:6501/rank/repo")
        
    # Do the repo delete operation
    delete_source = {"Context":{},"Repo":{"Operation":2,"RepoId":"repo1"}}
    repo.deleteRepo(delete_source)
    
# repo update operation
def repoUpdate():

    # Assign ranker2 repo instance
    repo = Ranker2Repo("http://192.168.2.19:6501/rank/repo")
        
    # Do the repo add operation
    update_source = {"Context":{},"Repo":{"Operation":3,"RepoId":"repo1","Level":3,"FeatureLen":384,"Capacity":11000000,"Params":[{"key":"GPUThreads","value":"[0,0,0,1]"}]}}
    
    repo.updateRepo(update_source)
    
# repo query operation
def repoQuery():
    
    repo = Ranker2Repo("http://192.168.2.19:6501/rank/repo")
    query_source = {"Context":{},"Repo":{"Operation":4}}
    repo.queryRepo(query_source)
    
# feature add opeartion
def featureAdd():
    
    feature = featureCreate(384)
    fea = Ranker2Feature("http://192.168.2.19:6501/rank/feature")
    add_source = {"Features":{"Operation":1,"RepoId":"repo1","ObjectFeatures":[{"Feature":feature,"Attributes":[{"value":43,"key":"k43"}],"Time":1509480666000,"Id":'featureid1',"Location":"0"}]},"Context":{"SessionId":"ss_743"}}
    fea.addFeature(add_source)
    
# feature delete operation
def featureDelete():
    
    fea = Ranker2Feature("http://192.168.2.19:6501/rank/feature")
    delete_source = {"Context":{},"Features": {"Operation":2,"ObjectFeatures":[{"Id":"repo1"}]}}
    fea.deleteFeature(delete_source)
    
def test(p):
    
    oMap = {"0":repoAdd,"1":repoDelete,"2":repoUpdate,"3":repoQuery, "4":featureAdd, "5":featureDelete}
    op = random.choice(["0", "1", "2", "3", "4", "5"])
    print('op:', op)
    oMap[op]()
    time.sleep(0.001)
    if p == 10000:
        return True
    else:
        return False

if __name__ == "__main__":
    
    result = Queue()
    pool = Pool()

    def pool_th():
        for i in range(50000000):
            try:
                result.put(pool.apply_async(test, args=(i, )))
            except:
                break

    def result_th():
        while True:
            a = result.get().get()
            if a:
                pool.terminate()
                break

    t1 = threading.Thread(target=pool_th)
    t2 = threading.Thread(target=result_th)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    pool.join()
    
