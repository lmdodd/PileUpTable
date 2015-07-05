#!/bin/bash

EXPECTED_ARGS=1
if [ $# -ne $EXPECTED_ARGS ]
then
  echo "Usage: $0 JOB_NAME"
fi

farmoutAnalysisJobs $1-WJets-GT \
  --infer-cmssw-path \
  --input-file-list=WJets.txt \
  --input-dir=root://cmsxrootd.fnal.gov/ \
  --assume-input-files-exist \
  ./sumsCalc.py  \
  'inputFiles=$inputFileNames' 'outputFile=$outputFileName'

farmoutAnalysisJobs $1-WJets-Payload \
  --infer-cmssw-path \
  --input-file-list=WJets.txt \
  --input-dir=root://cmsxrootd.fnal.gov/ \
  --assume-input-files-exist \
  ./sumsCalcPayload.py  \
  'inputFiles=$inputFileNames' 'outputFile=$outputFileName'


