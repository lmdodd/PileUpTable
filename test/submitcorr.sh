
farmoutAnalysisJobs PUMstudy \
  --infer-cmssw-path \
  --input-file-list=ZeroBiasMINIAOD.txt \
  --input-dir=root://cmsxrootd.fnal.gov/ \
  --assume-input-files-exist \
  --input-files-per-job=1 \
  PUMcorrelation_Run2015B_ECalTPLaserCorrection.py \
    'inputFiles=$inputFileNames' 'outputFile=$outputFileName' 
