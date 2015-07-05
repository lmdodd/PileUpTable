import FWCore.ParameterSet.Config as cms
from FWCore.ParameterSet.VarParsing import VarParsing

options = VarParsing('analysis')

options.parseArguments()

process = cms.Process("myDQM2")
process.load("DQMServices.Core.DQM_cfg")
process.load("DQMServices.Components.DQMEnvironment_cfi")
process.load("CTP7Tests.CTP7DQM.linkFilter_cfi")

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

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(options.maxEvents)
)


process.source = cms.Source("PoolSource",
noEventSort = cms.untracked.bool(True), duplicateCheckMode = cms.untracked.string('noDuplicateCheck'),
                            fileNames = cms.untracked.vstring(
                                options.inputFiles
)
)

process.dqmSaver.workflow = cms.untracked.string('/L1TMonitor/Calo/CTP7')

process.l1tctp7 = cms.EDAnalyzer("L1TCTP7",
    DQMStore = cms.untracked.bool(True),
    disableROOToutput = cms.untracked.bool(False),
    outputFile = cms.untracked.string('./CTP7DQM.root'),
    ctp7Source = cms.InputTag("ctp7ToDigi"),
    verbose = cms.untracked.bool(False),
    filterTriggerType  = cms.int32(-1)
)

#This creates DQM-compatible plots
process.p = cms.Path(process.l1tctp7+process.dqmSaver)


process.o1 = cms.OutputModule("PoolOutputModule",
                              outputCommands = cms.untracked.vstring('keep *'),
                              fileName = cms.untracked.string('CTP7ToDigi.root'))
process.outpath = cms.EndPath(process.o1)
