#/bin/bash

#filename = "./matrix_apps.0.7.4.INFO"

grep 'FaceDetectProcessor' matrix_apps.INFO  | awk '{print $8}' > FaceDetectProcessor
grep 'FaceQualityProcessor' matrix_apps.INFO  | awk '{print $8}' > FaceQualityProcessor
grep 'FaceAlignmentProcessor' matrix_apps.INFO  | awk '{print $8}' > FaceAlignmentProcessor

