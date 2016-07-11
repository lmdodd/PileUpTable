import FWCore.ParameterSet.Config as cms
from FWCore.ParameterSet.VarParsing import VarParsing
options = VarParsing('analysis')
options.parseArguments()

process = cms.Process("PUMCalc")

process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport = cms.untracked.PSet( reportEvery = cms.untracked.int32(1000) )
process.options = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )

process.load('Configuration/StandardSequences/FrontierConditions_GlobalTag_condDBv2_cff')
from Configuration.AlCa.GlobalTag_condDBv2 import GlobalTag
recordOverrides = {
    ('L1RCTParametersRcd', None) : ('L1RCTParametersRcd_L1TDevelCollisions_ExtendedScaleFactors_NewTau_FullEGTransparency_v1' , None)
}
process.GlobalTag = GlobalTag(process.GlobalTag, '74X_dataRun2_Prompt_v1', recordOverrides)
process.es_prefer_GlobalTag = cms.ESPrefer('PoolDBESSource', 'GlobalTag')

from L1Trigger.Configuration.SimL1Emulator_cff import simRctDigis
process.rctReEmulDigis = simRctDigis.clone()
process.rctReEmulDigis.ecalDigis = cms.VInputTag( cms.InputTag( 'ecalDigis' ) )
process.rctReEmulDigis.hcalDigis = cms.VInputTag( cms.InputTag( 'hcalDigis' ) )

process.load("Configuration.Geometry.GeometryIdeal_cff")

process.load("Configuration.StandardSequences.RawToDigi_Data_cff")
process.useFullEGCorrectionSF = cms.Sequence( (process.ecalDigis + process.hcalDigis) * process.rctReEmulDigis )

process.PUMcalcCentralBX = cms.EDAnalyzer("PUMcalc",
    regionSource = cms.InputTag("rctReEmulDigis"),
    bunchCrossingsToUse = cms.vint32(0)
)

process.PUMtables = cms.Sequence( process.PUMcalcCentralBX )

process.p = cms.Path(process.useFullEGCorrectionSF*process.PUMtables)

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(options.maxEvents)
)

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
        options.inputFiles
    ),
)

import FWCore.PythonUtilities.LumiList as LumiList
process.source.lumisToProcess = LumiList.LumiList(filename = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions15/13TeV/Cert_246908-251883_13TeV_PromptReco_Collisions15_JSON_v2.txt').getVLuminosityBlockRange()

process.TFileService = cms.Service(
    "TFileService",
    fileName = cms.string(options.outputFile)
)

