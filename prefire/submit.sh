# source me

if [ ! -f JetHT_run254833.txt ]
then
   das_client.py --query='file dataset=/JetHT/Run2015C-v1/RAW run=254833' --format plain --limit 0 > JetHT_run254833.txt
fi

farmoutAnalysisJobs PrefireStudy \
  --infer-cmssw-path \
  --input-file-list=JetHT_run254833.txt \
  --input-dir=root://cmsxrootd.fnal.gov/ \
  --assume-input-files-exist \
  --input-files-per-job=10 \
  runPrefire.py \
    'inputFiles=$inputFileNames' 'outputFile=$outputFileName' 
