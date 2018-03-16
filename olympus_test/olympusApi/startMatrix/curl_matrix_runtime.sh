#!/bin/bash

curl $1 -XPOST -d 'config_json=
{
  "Version": {
    "Code": "1.0.0",
    "Model": "1.9"
  },
  "ProtocolType": "rpc|restful",
  "InstanceType": "ranker",
  "System": {
    "Ip": "0.0.0.0",
    "Port": 1111,
    "Threads": [1, 1, 1, 1]
  },
  "RankerType": "face",
  "Pack":{
    "Enable": true,
    "BatchSize": 8,
    "TimeOut": 100
  },
  "Feature": {
    "Vehicle": {
      "Enable": false,
      "EnableDetection": true,
      "EnableType": true,
      "EnableColor": true,
      "EnableGpuPlate": true,
      "EnablePlateEnhanced": false,
      "EnableMarker": true,
      "EnableDriverBelt": true,
      "EnableCoDriverBelt": true,
      "EnablePhone": true,
      "EnableFeatureVector": true,
      "EnableNonMotorVehicle": true,
      "EnablePedestrianAttr": true
    },
    "Face": {
      "Enable": true,
      "EnableDetection": true,
      "EnableAlignment": true,
      "EnableQuality": true,
      "EnableFeatureVector": true
    }
  },
  "Advanced": {
    "Detection": {
      "TargetMinSize": 400.0,
      "TargetMaxSize": 600.0
    },
    "PlateMxnet": {
      "BatchSize": 1,
      "EnableLocalProvince": false,
      "LocalProvinceConfidence": 0.6,
      "LocalProvinceText": "\u4eac"
    },
    "DriverPhone":{
      "Threshold": 0.9
    },
    "DriverBelt": {
      "Threshold": 0.9
    },
    "CoDriverBelt": {
      "Threshold": 0.9
    },
    "FaceDetect": {
      "Method": 3,
      "BatchSize": 8,
      "BodyRelativeFaceLeft": 0.2,
      "BodyRelativeFaceRight": 0.2,
      "BodyRelativeFaceTop": 0.2,
      "BodyRelativeFaceBottom": 6.0
    },
    "FaceAlignment":{
      "Method": 2,
      "BatchSize": 8,
      "Threshold": 0,
      "FaceCheck": true
    },
    "FaceQuality": {
      "BatchSize": 8,
      "BlurThreshold": 0,
      "BorderThreshold":0.7
    },
    "FaceExtract": {
      "Method": 3,
      "BatchSize": 8,
      "EnableConcurrency": false
    },

    "Ranker": {
      "NormalizeAlpha": -0.02,
      "NormalizeBeta": 1.1,
      "Maximum": 5000000,
      "FeatureLen": 128,
      "SaveToFile": true,
      "SaveToFileIterval": 100, 
      "Static": false,
      "DynamicLoadNumber": 3000000,
      "RepoPath": "/home/dell/face/matrix_face/latest/repo/runtime",
      "ImageRootPath": ""
    },
    "ParseImageTimeout": 60
  },
  "Log": {
    "Dir": "",
    "Level": ""
  },
  "Render": {
    "NonMotorVehicle": {
      "NonMotorAttr": "data/mapping/bitri_attr_type.txt",
      "NonMotorCategory": "data/mapping/bitri_attr_category.txt"
    },
    "Pedestrian": {
      "PedestrianAttr": "data/mapping/pedestrian_attr_type.txt",
      "PedestrianCategory": "data/mapping/pedestrian_attr_category.txt"
    },
    "Vehicle": {
      "Color": "data/mapping/vehicle_color.txt",
      "Model": "data/mapping/vehicle_style_v1.12_4063.txt",
      "Plate": {
        "Color": "data/mapping/plate_color.txt",
        "ColorGpu": "data/mapping/plate_gpu_color.txt",
        "Type": "data/mapping/plate_type.txt"
      },
      "Symbol": "data/mapping/vehicle_symbol.txt",
      "Type": "data/mapping/vehicle_type.txt"
    }
  },
  "Debug": {
    "Enable": true,
    "EnableCutboard": true,
    "Encrypt": false,
    "Visualization": false
  },
  "Storage": {
    "Address": [
      "192.168.2.119:9004",
      "192.168.2.132:9877",
      "./"
    ],
    "DBType": [
      0,
      1,
      2
    ],
    "Enabled": false
  },
  "ModelLevel": 0,
  "ModelPath":{
    "dgvehicle": "data/dgvehicle",
    "dgLP":"data/dgLP/Product",
    "dgface":"data/dgface"
  }
}'\
 -d 'pre_executor=[{
      "before_fetch_cmd": "echo hello framework!!"
}
]'