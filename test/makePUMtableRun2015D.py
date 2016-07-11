import FWCore.ParameterSet.Config as cms
from FWCore.ParameterSet.VarParsing import VarParsing
options = VarParsing('analysis')
options.parseArguments()

process = cms.Process("PUMCalc")

process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport = cms.untracked.PSet( reportEvery = cms.untracked.int32(10000) )
process.options = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )

process.load('Configuration/StandardSequences/FrontierConditions_GlobalTag_condDBv2_cff')
from Configuration.AlCa.GlobalTag_condDBv2 import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '74X_dataRun2_Prompt_v1')
process.es_prefer_GlobalTag = cms.ESPrefer('PoolDBESSource', 'GlobalTag')

# ExpressPhysics is more than just ZeroBias
process.triggerSelection = cms.EDFilter( "TriggerResultsFilter",
    triggerConditions = cms.vstring( 'HLT_ZeroBias_v2' ),
    hltResults = cms.InputTag( "TriggerResults", "", "HLT" ),
    l1tResults = cms.InputTag( "gtDigis" ),
    l1tIgnoreMask = cms.bool( False ),
    l1techIgnorePrescales = cms.bool( False ),
    daqPartitions = cms.uint32( 1 ),
    throw = cms.bool( True )
)

process.load('EventFilter.RctRawToDigi.l1RctHwDigis_cfi')

process.PUMcalcCentralBX = cms.EDAnalyzer("PUMcalc",
    regionSource = cms.InputTag("rctDigis"),
    bunchCrossingsToUse = cms.vint32(0)
)

process.PUMcalcSideBX = cms.EDAnalyzer("PUMcalc",
    regionSource = cms.InputTag("rctDigis"),
    bunchCrossingsToUse = cms.vint32(-2,2)
)

process.PUMtables = cms.Sequence( process.PUMcalcCentralBX + process.PUMcalcSideBX )

process.PUMcorrelation = cms.EDAnalyzer("PUMcorrelation",
    regionSource = cms.InputTag("rctDigis"),
    lumiScalerSource = cms.InputTag("scalersRawToDigi"),
    vertexSource = cms.InputTag("offlinePrimaryVertices"),
    vertexCut = cms.string("ndof > 4 && abs(z) <= 50. && abs(position.rho) <= 2"),
    bunchCrossingsToUse = cms.vint32(0)
)

process.p = cms.Path(
        process.triggerSelection
        *process.rctDigis
        *process.PUMtables
        *process.PUMcorrelation
)

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(options.maxEvents)
)

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
            options.inputFiles
        ),
)

Express2015D_sep17 = {
  "256675": [[1, 106], [109, 164]],
  "256676": [[7, 160], [162, 208], [213, 417], [430, 470], [473, 509], [511, 735], [738, 798], [811, 854], [856, 1086]]
}
import FWCore.PythonUtilities.LumiList as LumiList
process.source.lumisToProcess = LumiList.LumiList(compactList = Express2015D_sep17).getVLuminosityBlockRange()


process.TFileService = cms.Service(
    "TFileService",
    fileName = cms.string(options.outputFile)
)

