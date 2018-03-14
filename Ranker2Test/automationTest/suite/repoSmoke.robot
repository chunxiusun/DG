*** Settings ***
Library           RequestsLibrary
Library           Collections
Library           XML
Library           ../util/helper.py
Variables         ../variable/smokeVariable.py
Variables         ../variable/globalVariable.py
Resource          ../Resource/repoResource.txt

*** Test Cases ***
repo_add
    Log    :::Step1: Delete the same repo to avoid name conflict
    ${repoDelete}    deleteRepo    ${repoId}
    Log    :::Step2: Create a repo
    ${repoCreate}    createRepo    ${repoId}    ${repoLevel}    ${featureLen}    ${featureDataType}    ${featureCapacity}
    ...    ${featureGpuThread}
    ${responseData}    To Json    ${repoCreate.content}
    Log    :::Step3: Check the repo when creating
    checkRepoAdd    ${responseData}    ${repoId}    ${repoLevel}    ${featureLen}    ${featureDataType}    ${featureCapacity}
    ...    ${featureGpuThread}
    Log    :::Step4: Do the repo query to check the repo
    ${repoQuery}    queryRepo    ${repoId}
    ${repoQueryResult}    To Json    ${repoQuery.content}
    checkRepoAdd    ${repoQueryResult}    ${repoId}    ${repoLevel}    ${featureLen}    ${featureDataType}    ${featureCapacity}
    ...    ${featureGpuThread}
    Log    :::Step5: Delete the repo
    ${repoDelete}    deleteRepo    ${repoId}
    Log    :::Step6: Delete all sessions
    Delete All Sessions

repo_delete
    Log    :::Step1: Delete non-exist repo
    ${repoDelete}    deleteRepo    ${repoId}
    ${responseData}    To Json    ${repoDelete.content}
    Log    :::Step2: Check the status code when delete
    checkRepoDelete    ${responseData}    ${deleteStatusCode["Abnormal"]}
    Log    :::Step3, Add a repo and do the delete
    ${repoCreate}    createRepo    ${repoId}    ${repoLevel}    ${featureLen}    ${featureDataType}    ${featureCapacity}
    ...    ${featureGpuThread}
    ${repoDelete}    deleteRepo    ${repoId}
    ${responseData}    To Json    ${repoDelete.content}
    checkRepoDelete    ${responseData}    ${deleteStatusCode["Normal"]}    ${deleteMessage["Success"]}
    Log    :::Step4, Do the repo delete for ${deleteTimes} times, then check rankers status is normal or not
    : FOR    ${i}    IN RANGE    ${deleteTimes}
    \    ${repoDelete}    deleteRepo    ${repoId}
    \    ${responseData}    To Json    ${repoDelete.content}
    \    checkRepoDelete    ${responseData}    ${deleteStatusCode["Abnormal"]}
    Log    :::Step5: Delete all sessions
    Delete All Sessions

repo_update
    Log    :::Step1: Delete the same repo to avoid name conflict
    ${repoDelete}    deleteRepo    ${repoId}
    Log    :::Step2: Create a repo
    ${repoCreate}    createRepo    ${repoId}    ${repoLevel}    ${featureLen}    ${featureDataType}    ${featureCapacity}
    ...    ${featureGpuThread}
    Log    :::Step3, update level,capacity,gpuThread of repo
    ${repoUpdate}    updateRepo    ${repoId}    ${updateRepoLevel}    ${featureLen}    ${featureDataType}    ${updateFeatureCapacity}
    ...    ${updateFeatureGpuThread}
    ${responseData}    To Json    ${repoUpdate.content}
    Log    :::Step4, check the update repoLevel, capacity,gpuThread of repo query result
    checkRepoUpdate    ${responseData}    ${repoId}    ${updateRepoLevel}    ${featureLen}    ${featureDataType}    ${updateFeatureCapacity}
    ...    ${updateFeatureGpuThread}
    Log    :::Step5: Do the repo query to check the repo
    ${repoQuery}    queryRepo    ${repoId}
    ${repoQueryResult}    To Json    ${repoQuery.content}
    checkRepoUpdate    ${repoQueryResult}    ${repoId}    ${updateRepoLevel}    ${featureLen}    ${featureDataType}    ${updateFeatureCapacity}
    ...    ${updateFeatureGpuThread}
    Log    :::Step6, delete the repo
    ${repoDelete}    deleteRepo    ${repoId}
    Log    :::Step7, delete all sessions
    Delete All Sessions
