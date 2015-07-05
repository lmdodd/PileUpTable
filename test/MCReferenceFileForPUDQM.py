import FWCore.ParameterSet.Config as cms

process = cms.Process("myDQM")
process.load("DQMServices.Core.DQM_cfg")
process.load("DQMServices.Components.DQMEnvironment_cfi")


from FWCore.ParameterSet.VarParsing import VarParsing
options = VarParsing ('analysis')
options.outputFile = "emulator.root"
options.parseArguments()

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(options.maxEvents)
)

process.source = cms.Source("PoolSource",
                            fileNames = cms.untracked.vstring(
                                options.inputFiles
)
)

process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 1
process.MessageLogger = cms.Service("MessageLogger",
    destinations = cms.untracked.vstring('detailedInfo'),
    detailedInfo = cms.untracked.PSet(
            default = cms.untracked.PSet( limit = cms.untracked.int32(-1) ),
            threshold = cms.untracked.string('DEBUG')
           #threshold = cms.untracked.string('ERROR')
    )
)
process.load('Configuration.StandardSequences.Services_cff')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration/StandardSequences/FrontierConditions_GlobalTag_cff')
process.load('Configuration.EventContent.EventContent_cff')
process.load('Configuration.Geometry.GeometryIdeal_cff')



# Other statements
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag.connect = cms.string('frontier://FrontierProd/CMS_COND_31X_GLOBALTAG')
process.GlobalTag.globaltag = cms.string('MCRUN2_72_V4A::All')


process.load('L1Trigger.L1TCalorimeter.L1TCaloStage1_PPFromRaw_cff')

process.p1 = cms.Path(
    process.L1TCaloStage1_PPFromRaw
)


process.dqmSaver.workflow = cms.untracked.string('/L1TMonitor/Calo/CTP7')

process.l1tctp7 = cms.EDAnalyzer("L1TCTP7",
    DQMStore = cms.untracked.bool(True),
    disableROOToutput = cms.untracked.bool(False),
    outputFile = cms.untracked.string('./CTP7DQMMC.root'),
    ctp7Source = cms.InputTag("simRctDigis"),
    verbose = cms.untracked.bool(False),
    filterTriggerType  = cms.int32(-1)
)

#This creates DQM-compatible plots
process.p = cms.Path(process.l1tctp7+process.dqmSaver)


# For faster debugging & extra couts we can also work with a standard analyzer
#process.ctp7protodqm = cms.EDAnalyzer('CTP7DQM')
#process.TFileService = cms.Service(
#  "TFileService",
#  fileName = cms.string("test.root")
#  )
#process.p2 = cms.Path(process.ctp7protodqm)




