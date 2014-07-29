#!/bin/bash

EXPECTED_ARGS=1
if [ $# -ne $EXPECTED_ARGS ]
then
  echo "Usage: $0 JOB_NAME"
  exit 1
fi

farmoutAnalysisJobs $1 \
  --infer-cmssw-path \
  --input-file-list=../submission/DY40bs25.txt  \
  --input-files-per-job=1 \
  makePUMTable_cfg.py isMC=1 \
    'inputFiles=$inputFileNames' 'outputFile=$outputFileName' 

#farmoutAnalysisJobs $1-NoHF \
#  --infer-cmssw-path \
#  --input-file-list=jet_skim_files.txt \
#  --input-files-per-job=1 \
#  makePuMultTrees_cfg.py isMC=0 inclHF=0 \
#    'inputFiles=$inputFileNames' 'outputFile=$outputFileName' 
