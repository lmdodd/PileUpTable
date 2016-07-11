import FWCore.ParameterSet.Config as cms
from FWCore.ParameterSet.VarParsing import VarParsing
options = VarParsing('analysis')
options.parseArguments()

process = cms.Process("TEST")

process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport = cms.untracked.PSet( reportEvery = cms.untracked.int32(1000) )
process.options = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )

process.load('Configuration/StandardSequences/FrontierConditions_GlobalTag_condDBv2_cff')
from Configuration.AlCa.GlobalTag_condDBv2 import GlobalTag
recordOverrides = {}
process.GlobalTag = GlobalTag(process.GlobalTag, '74X_dataRun2_Prompt_v1', recordOverrides)
process.es_prefer_GlobalTag = cms.ESPrefer('PoolDBESSource', 'GlobalTag')

process.load('EventFilter.RctRawToDigi.l1RctHwDigis_cfi')

process.PUMcalc = cms.EDAnalyzer("PUMcalc",
    regionSource = cms.InputTag("rctDigis"),
    bunchCrossingsToUse = cms.vint32(0)
)

process.p = cms.Path(process.rctDigis*process.PUMcalc)

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(options.maxEvents)
)

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
            options.inputFiles
        ),
)

lumilist = {
    '254833' : [[42,920], [927,1505], [1507,1632]]
}
import FWCore.PythonUtilities.LumiList as LumiList
process.source.lumisToProcess = LumiList.LumiList(compactList=lumilist).getVLuminosityBlockRange()

process.TFileService = cms.Service(
    "TFileService",
    fileName = cms.string(options.outputFile)
)

