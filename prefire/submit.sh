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


# hadd -f ~/www/JetHT_run254833.root /hdfs/store/user/ncsmith/PrefireStudy-runPrefire/*.root
# find /data/ncsmith/PrefireStudy-runPrefire/ -name *.err -size +0 -exec grep -l 'gsiftp' '{}' \; |xargs sed -n 's:.*Events total = \([0-9]*\) passed.*:\1:p' |awk '{s+=$1} END {print s}'
