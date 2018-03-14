*** Settings ***
Library           RequestsLibrary
Library           Collections
Library           XML
Library           ../util/helper.py
Variables         ../variable/smokeVariable.py
Resource          ../Resource/repoResource.txt
Resource          ../Resource/featureResource.txt
Resource          ../Resource/rankerResource.txt

*** Test Cases ***
ranker_1v1
    Log    :::Step1: Do the 1vn ranker when there is no repo and feature
    ${ranker1v1}    1v1Ranker    ${ranker1v1ObjectFeature}    ${ranker1v1ObjectCandidates}
    Log    :::Step2: Do the 1vn ranker check
    scoreCheck1v1Ranker    ${ranker1v1.content}    ${ranker1v1ScoreExpect}
    Log    :::Step3: Create repo and add feature
    ${repoCreate}    createRepo    ${repoId}    ${repoLevel}    ${featureLen}    ${featureDataType}    ${featureCapacity}
    ...    ${featureGpuThread}
    ${featureAdd}    addFeature    ${repoId}    ${featureString}    ${featureId}    ${featureLocation}    ${featureTime}
    ...    ${featureAttributes}
    Log    :::Step4: Do the 1vn ranker when there is repo and feature
    ${ranker1v1}    1v1Ranker    ${ranker1v1ObjectFeature}    ${ranker1v1ObjectCandidates}
    Log    :::Step4: Do the 1vn ranker check
    scoreCheck1v1Ranker    ${ranker1v1.content}    ${ranker1v1ScoreExpect}
    Log    :::Step5: Delete all the repo
    ${repoDelete}    deleteRepo    ${repoId}
    Log    :::Step6: Delete all sessions
    Delete All Sessions

ranker_1vN
    Log    :::Step1: Create repo and add feature
    ${repoCreate}    createRepo    ${ranker1vNRepoId}    ${ranker1vNRepoLevel}    ${ranker1vNFeatureLen}    ${ranker1vNFeatureDataType}    ${ranker1vNFeatureCapacity}
    ...    ${ranker1vNFeatureGpuThread}
    ${featureAdd}    addFeature    ${ranker1vNRepoId}    ${ranker1vNFeatureString}    ${ranker1vNFeatureId}    ${ranker1vNFeatureLocation}    ${ranker1vNFeatureTime}
    ...    ${ranker1vNFeatureAttributes}
    Log    :::Step2: Add more feature
    ${featureAdd}    addFeature1vNRanker    ${ranker1vNRepoId}    ${ranker1vNObjectFeature}    ${ranker1vNFeatureId}    ${ranker1vNFeatureLocation}    ${ranker1vNFeatureTime}
    ...    ${ranker1vNFeatureAttributes}
    Log    :::Step3: Do the 1vN ranker when there is repo and feature
    Sleep    2 seconds
    ${ranker1vN}    1vNRanker    ${ranker1vNObjectFeature}    ${ranker1vNFeatureLocation}
    Log    :::Step4: Do the 1vN ranker check
    scoreCheck1vNRanker    ${ranker1vN.content}    ${ranker1vNScoreExpect}
    Log    :::Step5: Add more feature
    ${response}    addMoreFeature1vNRanker    ${ranker1vNRepoId}    ${ranker1vNFeatureLen}
    Log    :::Step6: Do the 1vN ranker when there are more feature
    Sleep    2 seconds
    ${ranker1vN}    1vNRanker    ${ranker1vNObjectFeature}    ${ranker1vNFeatureLocation}
    Log    :::Step7: Do the 1vN ranker check
    scoreCheck1vNRanker    ${ranker1vN.content}    ${ranker1vNScoreExpect}
    Log    :::Step8: Delete all the repo
    ${repoDelete}    deleteRepo    ${ranker1vNRepoId}
    Log    :::Step9: Delete all sessions
    Delete All Sessions
