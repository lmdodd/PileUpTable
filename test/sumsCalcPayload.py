import FWCore.ParameterSet.Config as cms
import os
#from L1Trigger.PileUpTable.Lut import *
# Get command line options
from FWCore.ParameterSet.VarParsing import VarParsing
options = VarParsing ('analysis')
# Set useful defaults
#options.inputFiles = '/store/mc/RunIISpring15DR74/SingleNeutrino/GEN-SIM-RAW/Asympt25ns_magnetOff_MCRUN2_74_V9-v1/50000/FC2C0363-A412-E511-9521-002590E3A0D4.root'
#options.inputFiles = '/store/mc/RunIISpring15Digi74/SingleNeutrino/GEN-SIM-RAW/AVE_20_BX_25ns_tsg_MCRUN2_74_V7-v1/00000/F26A2A59-E6F7-E411-8993-0025905A612E.root'
#options.inputFiles = '/store/mc/RunIISpring15DR74/SingleNeutrino/GEN-SIM-RAW/Asympt50nsRaw_MCRUN2_74_V9A-v2/10000/028EC41F-6E09-E511-95F0-0002C92DB4CC.root'
#options.inputFiles = 'file:/nfs_scratch/laura/DY.root'
options.inputFiles = '/store/mc/RunIISpring15Digi74/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/GEN-SIM-RAW/AVE_30_BX_50ns_tsg_MCRUN2_74_V6-v1/00000/048543B8-4FEF-E411-96E5-C4346BC7AAE0.root'

options.outputFile = "test_sums.root"


options.register(
    'isMC',
    1,
    VarParsing.multiplicity.singleton,
    VarParsing.varType.int,
    'Set to 1 for simulated samples - updates GT, emulates HCAL TPGs.')

options.parseArguments()

process = cms.Process("TauTable")

# Other statements
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')
from Configuration.AlCa.GlobalTag_condDBv2 import GlobalTag
# Format: map{(record,label):(tag,connection),...}
recordOverrides = { ('L1RCTParametersRcd', None) : ('L1RCTParametersRcd_L1TDevelCollisions_ExtendedScaleFactorsV2', None) }
process.GlobalTag = GlobalTag(process.GlobalTag, 'MCRUN2_74_V8', recordOverrides)

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
)

process.source = cms.Source(
    "PoolSource",
    fileNames = cms.untracked.vstring(options.inputFiles),
    noEventSort = cms.untracked.bool(True),
    duplicateCheckMode = cms.untracked.string('noDuplicateCheck')
)

process.TFileService = cms.Service(
    "TFileService",
    fileName = cms.string(options.outputFile)
)

# Load emulation and RECO sequences
process.load("L1Trigger.PileUpTable.emulation_cfi")

process.load("Configuration.Geometry.GeometryIdeal_cff")

# Read inst. lumi. info from the scalers
process.load("EventFilter.ScalersRawToDigi.ScalersRawToDigi_cfi")
process.scalersRawToDigi.scalersInputTag = 'rawDataCollector'

print 'processes loaded'


# Tree producers
process.tree = cms.EDAnalyzer(
    "sumcalculator",
    regionLSB = cms.double(0.5)#RCTConfigProducers.jetMETLSB
)

process.p1 = cms.Path(
    process.emulationSequence *
    process.scalersRawToDigi
)


process.p1 += process.tree

# Make the framework shut up.
process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 100

# Spit out filter efficiency at the end.
process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(True))

