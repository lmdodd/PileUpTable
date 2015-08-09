# use `source $filename`

farmoutAnalysisJobs PUMcalc \
  --infer-cmssw-path \
  --input-file-list=ZeroBias.txt \
  --input-dir=root://cmsxrootd.fnal.gov/ \
  --assume-input-files-exist \
  --input-files-per-job=20 \
  makePUMtable_Run2015B_ECalTPLaserCorrection.py \
    'inputFiles=$inputFileNames' 'outputFile=$outputFileName' 

farmoutAnalysisJobs PUMcalc \
  --infer-cmssw-path \
  --input-file-list=ZeroBias.txt \
  --input-dir=root://cmsxrootd.fnal.gov/ \
  --assume-input-files-exist \
  --input-files-per-job=20 \
  makePUMtable_Run2015B_RCTFullEGTransparency.py \
    'inputFiles=$inputFileNames' 'outputFile=$outputFileName' 
