import FWCore.ParameterSet.Config as cms
from FWCore.ParameterSet.VarParsing import VarParsing
options = VarParsing('analysis')
options.register('globalTag', 'MCRUN2_74_V9', VarParsing.multiplicity.singleton, VarParsing.varType.string, 'Global Tag to use')
options.parseArguments()

process = cms.Process("PUMCalc")

process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport = cms.untracked.PSet( reportEvery = cms.untracked.int32(1000) )
#process.MessageLogger.cerr.INFO = cms.untracked.PSet( limit = cms.untracked.int32(100000) )
process.options = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )

process.load('Configuration/StandardSequences/FrontierConditions_GlobalTag_condDBv2_cff')
from Configuration.AlCa.GlobalTag_condDBv2 import GlobalTag
recordOverrides = {
    ('L1RCTParametersRcd', None) : ('L1RCTParametersRcd_L1TDevelCollisions_ExtendedScaleFactorsV4' , None)
}
if 'PHYS14' in options.globalTag :
    recordOverrides = {}
process.GlobalTag = GlobalTag(process.GlobalTag, options.globalTag, recordOverrides)
process.es_prefer_GlobalTag = cms.ESPrefer('PoolDBESSource', 'GlobalTag')

process.load("Configuration.Geometry.GeometryIdeal_cff")
process.load('Configuration.StandardSequences.RawToDigi_Data_cff')

process.hcalSequence = cms.Sequence(process.hcalDigis)
rctHcalSrc = 'hcalDigis'
# Phys14 had some hcal tp bug...
if 'PHYS14' in options.globalTag :
    process.load('SimCalorimetry.HcalTrigPrimProducers.hcaltpdigi_cff')
    process.reEmulHcalTPs = process.simHcalTriggerPrimitiveDigis.clone()
    process.reEmulHcalTPs.inputLabel = cms.VInputTag(
        cms.InputTag('hcalDigis'),
        cms.InputTag('hcalDigis')
    )

    process.hcalSequence = cms.Sequence(
        process.hcalDigis * process.reEmulHcalTPs
    )
    rctHcalSrc = 'reEmulHcalTPs'

from L1Trigger.Configuration.SimL1Emulator_cff import simRctDigis
process.rctReEmulDigis = simRctDigis.clone()
process.rctReEmulDigis.ecalDigis = cms.VInputTag( cms.InputTag( 'ecalDigis' ) )
process.rctReEmulDigis.hcalDigis = cms.VInputTag( cms.InputTag( rctHcalSrc ) )

process.PUMcalc = cms.EDAnalyzer("PUMcalc",
    regionSource = cms.InputTag("rctReEmulDigis"),
    bunchCrossingsToUse = cms.vint32(0)
)

process.PUMtables = cms.Sequence( process.PUMcalc )

process.p = cms.Path((process.ecalDigis+process.hcalSequence)*process.rctReEmulDigis*process.PUMtables)

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

