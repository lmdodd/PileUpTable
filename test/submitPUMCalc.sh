#!/bin/sh                                                                                                                              

voms-proxy-init --voms cms --valid 100:00                                                                                              

cat submitUCTPUMTableRAW.py > SUBStage3.py
cat submit.py >> SUBStage3.py

rm -rf /data/ldodd/ZeroBias-Run2016C-$1-SUBStage3/
mkdir /data/ldodd/ZeroBias-Run2016C-$1-SUBStage3/
##make dag dir
mkdir -p /data/ldodd/ZeroBias-Run2016C-$1-SUBStage3/dags
mkdir -p /data/ldodd/ZeroBias-Run2016C-$1-SUBStage3/dags/daginputs

## outputdir = srm://cmssrm.hep.wisc.edu:8443/srm/$1/server?SFN=/hdfs/store/user/ldodd/ZeroBias-Run2016C-$1-SUBStage3/
#Matching E and H activity
#farmoutAnalysisJobs  --input-file-list=RAW-Run2015D.txt --no-shared-fs  --submit-dir=/data/ldodd/ZeroBias-Run2016C-$1-SUBStage3/submit --output-dag-file=/data/ldodd/ZeroBias-Run2016C-$1-SUBStage3/dags/dag --output-dir=srm://cmssrm.hep.wisc.edu:8443/srm/$1/server?SFN=/hdfs/store/user/ldodd/ZeroBias-Run2016C-$1-SUBStage3/ ZeroBias-Run2016C-$1   $CMSSW_BASE  $CMSSW_BASE/src/L1Trigger/L1TNtuplizer/test/SUBStage3.py 

farmoutAnalysisJobs --assume-input-files-exist  --input-file-list=ZeroBias2016C.txt  \
--submit-dir=/data/ldodd/ZeroBias-Run2016C-$1-SUBStage3/submit \
--output-dag-file=/data/ldodd/ZeroBias-Run2016C-$1-SUBStage3/dags/dag \
--output-dir=. \
ZeroBias-Run2016C-$1  \
$CMSSW_BASE  \
$CMSSW_BASE/src/L1Trigger/PileUpTable/test/SUBStage3.py farmout=True data=True 

rm -f SUBStage3.py

#farmoutAnalysisJobs PUMcalc \
#  --infer-cmssw-path \
#  --input-file-list=Run2015C-Run2016C-ZeroBias-RAW.txt \
#  --assume-input-files-exist \
#  --input-files-per-job=2 \
#  makeUCTPUMTableRAW.py runNumber=Run2016C \
#    'inputFiles=$inputFileNames' 'outputFile=$outputFileName' 

