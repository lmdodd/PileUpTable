# source me

cachefile=Express2015D_sep17.txt

farmoutAnalysisJobs $(echo ${cachefile}|sed 's:.txt::') \
  --infer-cmssw-path \
  --input-file-list=${cachefile} \
  --input-dir=root://cmsxrootd.fnal.gov/ \
  --assume-input-files-exist \
  --input-files-per-job=20 \
  makePUMtableRun2015D.py \
    'inputFiles=$inputFileNames' 'outputFile=$outputFileName'

# hadd -f Express2015D_sep17.root /hdfs/store/user/ncsmith/Express2015D_sep17-makePUMtable_MC/*.root
# find /data/ncsmith/Express2015D_sep17-makePUMtable_MC/ -name *.err -size +0 -exec grep -l 'gsiftp' '{}' \; |xargs sed -n 's:.*Events total = \([0-9]*\) passed = \([0-9]*\).*:\2:p' |awk '{s+=$1} END {print s}'
