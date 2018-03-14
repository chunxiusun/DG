*** Settings ***
Library           RequestsLibrary
Library           Collections
Library           XML
Library           ../util/helper.py
Variables         ../variable/smokeVariable.py
Resource          ../Resource/repoResource.txt
Resource          ../Resource/featureResource.txt

*** Test Cases ***
feature_add
    Log    :::Step1: Delete the same repo to avoid name conflict
    ${repoDelete}    deleteRepo    ${repoId}
    Log    :::Step2: Create a repo
    ${repoCreate}    createRepo    ${repoId}    ${repoLevel}    ${featureLen}    ${featureDataType}    ${featureCapacity}
    ...    ${featureGpuThread}
    ${responseData}    To Json    ${repoCreate.content}
    Log    :::Step3: Check the repo when creating
    checkRepoAdd    ${responseData}    ${repoId}    ${repoLevel}    ${featureLen}    ${featureDataType}    ${featureCapacity}
    ...    ${featureGpuThread}
    Log    :::Step4: Add the feature
    ${featureAdd}    addFeature    ${repoId}    ${featureString}    ${featureId}    ${featureLocation}    ${featureTime}
    ...    ${featureAttributes}
    ${responseData}    To Json    ${featureAdd.content}
    Log    :::Step5: Check the feature
    ${featureQuery}    queryFeature    ${featureId}
    checkFeatureAdd    ${featureQuery.content}    ${repoId}    ${featureString}    ${featureId}    ${featureLocation}    ${featureTime}
    ...    ${featureAttributes}
    Log    :::Step6: Delete the repo
    ${repoDelete}    deleteRepo    ${repoId}
    Log    :::Step7: Delete all sessions
    Delete All Sessions

feature_delete
    Log    :::Step1: Delete non-exist feature
    ${featureDelete}    deleteFeature    ${featureId}
    ${responseData}    Set Variable    ${featureDelete.content}
    Log    :::Step2: Check the status code when delete
    checkFeatureDelete    ${responseData}    ${deleteStatusCode["Normal"]}
    Log    :::Step3, Add a repo and do the delete
    ${repoCreate}    createRepo    ${repoId}    ${repoLevel}    ${featureLen}    ${featureDataType}    ${featureCapacity}
    ...    ${featureGpuThread}
    Log    :::Step4, Add the feature into repo
    ${featureAdd}    addFeature    ${repoId}    ${featureString}    ${featureId}    ${featureLocation}    ${featureTime}
    ...    ${featureAttributes}
    Log    :::Step5, Delete the feature
    ${featureDelete}    deleteFeature    ${featureId}
    ${responseData}    Set Variable    ${featureDelete.content}
    Log    :::Step6, Check the delete feature status
    checkFeatureDelete    ${responseData}    ${deleteStatusCode["Normal"]}
    Log    :::Step7, Do the feature delete for ${deleteTimes} times, then check rankers status is normal or not
    : FOR    ${i}    IN RANGE    ${deleteTimes}
    \    ${featureDelete}    deleteFeature    ${featureId}
    \    ${responseData}    Set Variable    ${featureDelete.content}
    \    checkFeatureDelete    ${responseData}    ${deleteStatusCode["Normal"]}
    Log    :::Step8: Delete the repo
    ${repoDelete}    deleteRepo    ${repoId}
    Log    :::Step9: Delete all sessions
    Delete All Sessions

feature_update
    Log    :::Step1: Delete the same repo to avoid name conflict
    ${repoDelete}    deleteRepo    ${repoId}
    Log    :::Step2: Create a repo
    ${repoCreate}    createRepo    ${repoId}    ${repoLevel}    ${featureLen}    ${featureDataType}    ${featureCapacity}
    ...    ${featureGpuThread}
    ${responseData}    To Json    ${repoCreate.content}
    Log    :::Step3: Check the repo when creating
    checkRepoAdd    ${responseData}    ${repoId}    ${repoLevel}    ${featureLen}    ${featureDataType}    ${featureCapacity}
    ...    ${featureGpuThread}
    Log    :::Step4: Add the feature
    ${featureAdd}    addFeature    ${repoId}    ${featureString}    ${featureId}    ${featureLocation}    ${featureTime}
    ...    ${featureAttributes}
    Log    :::Step5: Check the feature
    ${featureQuery}    queryFeature    ${featureId}
    checkFeatureAdd    ${featureQuery.content}    ${repoId}    ${featureString}    ${featureId}    ${featureLocation}    ${featureTime}
    ...    ${featureAttributes}
    Log    :::Step6: Update the feature
    ${featureUpdate}    updateFeature    ${repoId}    ${updateFeatureString}    ${featureId}    ${updateFeatureLocation}    ${updateFeatureTime}
    ...    ${updateFeatureAttributes}
    Log    :::Step7: Check the feature
    ${featureQuery}    queryFeature    ${featureId}
    checkFeatureUpdate    ${featureQuery.content}    ${repoId}    ${updateFeatureString}    ${featureId}    ${updateFeatureLocation}    ${updateFeatureTime}
    ...    ${updateFeatureAttributes}
    Log    :::Step8: Delete the repo
    ${repoDelete}    deleteRepo    ${repoId}
    Log    :::Step9: Delete all sessions
    Delete All Sessions
