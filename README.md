PileUpTable
===========

Pile Up Multiplicity calculation code

To Set up 

```
cmsrel CMSSW_7_4_5
cd CMSSW_7_4_5/src/
cmsenv
git cms-addpkg L1Trigger/RegionalCaloTrigger     
git clone https://github.com/lmdodd/PileUpTable.git L1Trigger/PileUpTable

scram b -j 8
```


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
