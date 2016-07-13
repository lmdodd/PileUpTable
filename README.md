PileUpTable
===========

Pile Up Multiplicity calculation code

To Set up 

```
cmsrel CMSSW_8_0_14
cd CMSSW_8_0_14/src
cmsenv
git cms-init
git remote add cms-l1t-offline git@github.com:cms-l1t-offline/cmssw.git
git fetch cms-l1t-offline
git cms-merge-topic cms-l1t-offline:dasu-dev-$CMSSW_VERSION
cd L1Trigger
git clone git@github.com:lmdodd/PileUpTable.git
cd ..
scram b -j 8
```


To run PUM tables:
the pum bin can be any divisor of 486
So pumbin can be 18, 26, 36, 39, 52, etc., but the examples below uses 39. The pumbin argument can be changed.
```
cd L1Trigger/PileUpTable/test/
nohup cmsRun makeUCTPUMTable_RAW.py runNumber=275832 inputFileList=Run2016C-275832-ZeroBias-RAW.txt pumbins=39 maxEvents=20000 &
nohup cmsRun makeUCTPUMTable_RAW.py runNumber=275832 inputFileList=Run2016C-275832-ZeroBias-RAW.txt pumbins=18 maxEvents=20000 &
```
This generates a file in the /data/USER/UCTPUMTable-runNumber-pumbins.root area on uwlogin, where "runNumber" and "pumbins" are the arguments you gave to makeUCTPUMTable_RAW.py.

```
cd L1Trigger/PileUpTable/test/
#python table.py [pumbins] [runrunmber]
python table 18 275832 #produces plots and table (see "PUMLut-18.txt") and plots comparing to 2015 40PU MC (directory plots18/)
python table 39 275832 #produces plots and table (see "PUMLut-39.txt") and plots (directory plots39/ ) 
```
