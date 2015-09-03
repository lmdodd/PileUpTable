# source me

if [ ! -f neutrinoGunHF.txt ]
then
   das_client.py --query='file dataset=/SingleNeutrino/RunIISpring15DR74-NhcalZSHFscaleFlat10to30Asympt25ns_MCRUN2_74_V9-v1/GEN-SIM-RAW' --format plain --limit 0 > neutrinoGunHF.txt
fi

farmoutAnalysisJobs PrefireStudy \
  --infer-cmssw-path \
  --input-file-list=neutrinoGunHF.txt \
  --input-dir=root://cmsxrootd.fnal.gov/ \
  --assume-input-files-exist \
  --input-files-per-job=5 \
  --job-count=40 \
  makePUMtable_MC.py \
    'inputFiles=$inputFileNames' 'outputFile=$outputFileName' 


# hadd -f ~/www/neutrinoGunHF.root /hdfs/store/user/ncsmith/PrefireStudy-runPrefire/*.root
# find /data/ncsmith/PrefireStudy-runPrefire/ -name *.err -size +0 -exec grep -l 'gsiftp' '{}' \; |xargs sed -n 's:.*Events total = \([0-9]*\) passed.*:\1:p' |awk '{s+=$1} END {print s}'
