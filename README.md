PileUpTable
===========

Pile Up Multiplicity calculation code

To Set up 

```
cmsrel CMSSW_8_0_9
cd CMSSW_8_0_9/src
cmsenv
git cms-init
git remote add cms-l1t-offline git@github.com:cms-l1t-offline/cmssw.git
git fetch cms-l1t-offline
git cms-merge-topic cms-l1t-offline:dasu-dev-$CMSSW_VERSION
cd L1Trigger
git clone git@github.com:SridharaDasu/L1TCaloSummary.git
git clone git@github.com:lmdodd/PileUpTable.git
cd ..
scram b -j 8
```

the submit file 
```
cmsRun makeUCTPUMTable.py runNumber=276282 dataStream=/ZeroBias/Run2016C-PromptReco-v2/RAW
```

A two file solution is needed. 




###DEPRECATED INSTRUCTIONS IGNORE###
To run PUM tables:
The root file can be changed directly in makePUMTable_cfg.py, or a condor job submission can be used as in submit_pum.sh
There is a options tag for MC and for DAta you must specify what you are running over with 

```
cd L1Trigger/PileUpTable/test/
cmsRun makePUMTableMC_cfg.py isMC=1 #for MC or isMC=0 for data
```
this generates the file 'pum.root'
```
cd L1Trigger/PileUpTable/bin/
nohup python pythonError.py /path/to/pum.root &
```
Note the CTP7todigi Method (validated) can be used as well.
