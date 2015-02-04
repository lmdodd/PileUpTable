PileUpTable
===========

Pile Up Multiplicity calculation code

To Set up 

My area was set up for CMSSW_6_2_5, so using that as example

Master was checked for 7_3_0_pre1

cmsrel CMSSW_6_2_5
cd CMSSW_6_2_5/src/
cmsenv
git cms-addpkg DataFormats/L1CaloTrigger
git cms-addpkg L1TriggerConfig/L1ScalesProducers
git cms-addpkg L1Trigger/RegionalCaloTrigger     

git clone https://github.com/lmdodd/PileUpTable.git L1Trigger/PileUpTable

scram b



To run PUM tables:
The root file can be changed directly in makePUMTable_cfg.py, or a condor job submission can be used as in submit_pum_DY.sh


cmsenv
cd L1Trigger/PileUpTable/test/
cmsRun makePUMTable_cfg.py isMC=1

this generates the file 'uct_pum.root'

cmsenv
cd L1Trigger/PileUpTable/bin/
nohup python pythonError.py ../test/uct_pum.root SaveLabel[optional] &
