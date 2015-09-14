# source me

dataset='/SingleNeutrino/RunIISpring15DR74-NhcalZSHFscaleFlat10to30Asympt25ns_MCRUN2_74_V9-v1/GEN-SIM-RAW'
cachefile=neutrinoGunHF.txt
globalTag=MCRUN2_74_V9

#dataset='/SingleNeutrino/RunIISpring15DR74-Asympt25nsRaw_MCRUN2_74_V9-v2/GEN-SIM-RAW'
#cachefile=neutrinoGunSpring15Asympt.txt
#globalTag=MCRUN2_74_V9

#dataset='/SingleNeutrino/RunIISpring15Digi74-Flat_10_50_25ns_tsg_MCRUN2_74_V7-v1/GEN-SIM-RAW'
#cachefile=neutrinoGunSpring15Flat.txt
#globalTag=MCRUN2_74_V7

#dataset='/Neutrino_Pt-2to20_gun/Phys14DR-AVE40BX25_tsg_PHYS14_25_V3-v2/GEN-SIM-RAW'
#cachefile=neutrinoGunPhys14.txt
#globalTag=PHYS14_25_V3

if [ ! -f $cachefile ]
then
   das_client.py --query="file dataset=${dataset}" --format plain --limit 0 > $cachefile
fi

farmoutAnalysisJobs $(echo ${cachefile}|sed 's:.txt::') \
  --infer-cmssw-path \
  --input-file-list=${cachefile} \
  --input-dir=root://cmsxrootd.fnal.gov/ \
  --assume-input-files-exist \
  --input-files-per-job=4 \
  --job-count=250 \
  makePUMtable_MC.py \
    'inputFiles=$inputFileNames' 'outputFile=$outputFileName' "globalTag=${globalTag}"


# hadd -f ~/www/neutrinoGunHF.root /hdfs/store/user/ncsmith/PUMtables-makePUMtable_MC/*.root
# find /data/ncsmith/PUMtables-makePUMtable_MC/ -name *.err -size +0 -exec grep -l 'gsiftp' '{}' \; |xargs sed -n 's:.*Events total = \([0-9]*\) passed.*:\1:p' |awk '{s+=$1} END {print s}'
