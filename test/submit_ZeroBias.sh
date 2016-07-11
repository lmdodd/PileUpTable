# use `source $filename`

farmoutAnalysisJobs PUMcalc \
  --infer-cmssw-path \
  --input-file-list=ZeroBias.txt \
  --input-dir=root://cmsxrootd.fnal.gov/ \
  --assume-input-files-exist \
  --input-files-per-job=5 \
  makePUMtable_Run2015C.py \
    'inputFiles=$inputFileNames' 'outputFile=$outputFileName' 

