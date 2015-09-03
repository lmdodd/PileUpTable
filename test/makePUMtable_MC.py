import FWCore.ParameterSet.Config as cms
from FWCore.ParameterSet.VarParsing import VarParsing
options = VarParsing('analysis')
options.parseArguments()

process = cms.Process("PUMCalc")

process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport = cms.untracked.PSet( reportEvery = cms.untracked.int32(1000) )
process.MessageLogger.cerr.INFO = cms.untracked.PSet( )
process.options = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )

process.load('Configuration/StandardSequences/FrontierConditions_GlobalTag_condDBv2_cff')
from Configuration.AlCa.GlobalTag_condDBv2 import GlobalTag
recordOverrides = {
    ('L1RCTParametersRcd', None) : ('L1RCTParametersRcd_L1TDevelCollisions_ExtendedScaleFactorsV4' , None)
}
process.GlobalTag = GlobalTag(process.GlobalTag, 'MCRUN2_74_V9', recordOverrides)
process.es_prefer_GlobalTag = cms.ESPrefer('PoolDBESSource', 'GlobalTag')

process.load('Configuration.StandardSequences.RawToDigi_Data_cff')

process.PUMcalc = cms.EDAnalyzer("PUMcalc",
    regionSource = cms.InputTag("gctDigis"),
    bunchCrossingsToUse = cms.vint32(0)
)

process.PUMtables = cms.Sequence( process.PUMcalc )

process.p = cms.Path(process.gctDigis*process.PUMtables)

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(options.maxEvents)
)

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
            options.inputFiles
        ),
)

process.TFileService = cms.Service(
    "TFileService",
    fileName = cms.string(options.outputFile)
)

