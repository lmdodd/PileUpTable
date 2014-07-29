import FWCore.ParameterSet.Config as cms
import os
from L1Trigger.PileUpTable.Lut import *
# Get command line options
from FWCore.ParameterSet.VarParsing import VarParsing
options = VarParsing ('analysis')
# Set useful defaults
#options.inputFiles = 'file:/nfs_scratch/laura/pion0test.root'
#options.inputFiles = '/store/user/laura/SinglePi0Pt30/SinglePi0Pt30-0093.root'
#options.inputFiles = 'file:/hdfs/store/user/laura/SinglePi0Pt30/SinglePi0Pt30-0093.root'
#options.inputFiles = '/store/user/laura/SinglePiPlusPt30/SinglePiPlusPt30-0093.root'
options.inputFiles = 'file:/hdfs/store/user/ldodd/TT_Tune4C_13TeV-pythia8-tauola/TT_Tune4C_13TeV-pythia8-tauola-tsg_PU40bx25_POSTLS162_V2-v1/fb508503c16d6e4b02bc25104d11f7c2/skim_112_1_xxl.root'

options.outputFile = "uct_pum.root"
#options.outputFile = "uct_pt_pipl_30.root"


options.register(
    'isMC',
    1,
    VarParsing.multiplicity.singleton,
    VarParsing.varType.int,
    'Set to 1 for simulated samples - updates GT, emulates HCAL TPGs.')

options.parseArguments()

process = cms.Process("L1UCTRates")

process.load('Configuration/StandardSequences/FrontierConditions_GlobalTag_cff')
# Load the correct global tag, based on the release
if 'CMSSW_6' in os.environ['CMSSW_VERSION']:
    process.GlobalTag.globaltag = 'POSTLS162_V2::All'
    print "Using global tag for upgrade MC: %s" % process.GlobalTag.globaltag
    if not options.isMC:
        raise ValueError("There is no data in CMSSW 6, you must mean isMC=1")
else:
    raise ValueError("Why aren't you using CMSSW 6?")
    if not options.isMC:
        # CMSSW 5 data
        process.GlobalTag.globaltag = 'GR_H_V28::All'
    else:
        # CMSSW 5 MC
        process.GlobalTag.globaltag = 'START53_V7B::All'
    process.GlobalTag.connect   = 'frontier://FrontierProd/CMS_COND_31X_GLOBALTAG'
    process.GlobalTag.pfnPrefix = cms.untracked.string('frontier://FrontierProd/')
    print "Using global tag for 52X data: %s" % process.GlobalTag.globaltag

# UNCOMMENT THIS LINE TO RUN ON SETTINGS FROM THE DATABASE
# process.es_prefer_GlobalTag = cms.ESPrefer('PoolDBESSource', 'GlobalTag')

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(options.maxEvents)
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
if not options.isMC:
    process.load("L1Trigger.PileUpTable.emulation_cfi")
else:
    process.load("L1Trigger.PileUpTable.emulationMC_cfi")
process.load("Configuration.Geometry.GeometryIdeal_cff")

# Read inst. lumi. info from the scalers
process.load("EventFilter.ScalersRawToDigi.ScalersRawToDigi_cfi")
process.scalersRawToDigi.scalersInputTag = 'rawDataCollector'

print 'processes loaded'

common_ntuple_branches = cms.PSet(
#    index = cms.string("index"), # Index of reco object in the event
#    nRecoObjects = cms.string("nTotalObjects"), # Number of reco objects in the event
#    nPVs = cms.string("nPVs"), # number of reco'ed vertices in the event
)

# Tree producers
process.tree = cms.EDAnalyzer(
    "pum0calculator",
    regionLSB = RCTConfigProducers.jetMETLSB
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

