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
    ('L1RCTParametersRcd', None) : ('L1RCTParametersRcd_L1TDevelCollisions_ExtendedScaleFactorsV4' , None),
    ('EcalTPGLinearizationConstRcd', None) : ('EcalTPGLinearizationConst_weekly_test2_hlt', 'frontier://FrontierPrep/CMS_CONDITIONS')
}
process.GlobalTag = GlobalTag(process.GlobalTag, '74X_dataRun2_Prompt_v1', recordOverrides)
process.es_prefer_GlobalTag = cms.ESPrefer('PoolDBESSource', 'GlobalTag')

process.load("SimCalorimetry.EcalTrigPrimProducers.ecalTriggerPrimitiveDigis_readDBOffline_cff")

process.load("EventFilter.EcalRawToDigi.EcalUnpackerMapping_cfi")
process.load("EventFilter.EcalRawToDigi.EcalUnpackerData_cfi")

process.load("Geometry.EcalMapping.EcalMapping_cfi")
process.load("Geometry.EcalMapping.EcalMappingRecord_cfi")

process.load("Geometry.CaloEventSetup.CaloGeometry_cfi")
process.load("Geometry.CaloEventSetup.EcalTrigTowerConstituents_cfi")
process.load("Geometry.CMSCommonData.cmsIdealGeometryXML_cfi")

from SimCalorimetry.EcalTrigPrimProducers.ecalTriggerPrimitiveDigis_cff import simEcalTriggerPrimitiveDigis
process.ecalReEmulDigis = simEcalTriggerPrimitiveDigis.clone()
process.ecalReEmulDigis.InstanceEB = cms.string('ebDigis')
process.ecalReEmulDigis.InstanceEE = cms.string('eeDigis')
process.ecalReEmulDigis.Label = cms.string('ecalDigis')

from L1Trigger.Configuration.SimL1Emulator_cff import simRctDigis
process.rctReEmulDigis = simRctDigis.clone()
process.rctReEmulDigis.ecalDigis = cms.VInputTag( cms.InputTag( 'ecalReEmulDigis' ) )
process.rctReEmulDigis.hcalDigis = cms.VInputTag( cms.InputTag( 'hcalDigis' ) )

process.load("Configuration.StandardSequences.RawToDigi_Data_cff")
process.fixLaserCorrections = cms.Sequence( (process.ecalDigis * process.ecalReEmulDigis + process.hcalDigis) * process.rctReEmulDigis )

process.PUMcorrelation = cms.EDAnalyzer("PUMcorrelation",
    regionSource = cms.InputTag("rctReEmulDigis"),
    lumiScalerSource = cms.InputTag("scalersRawToDigi"),
    vertexSource = cms.InputTag("offlineSlimmedPrimaryVertices"),
    bunchCrossingsToUse = cms.vint32(0)
)

process.p = cms.Path(process.scalersRawToDigi*process.fixLaserCorrections*process.PUMcorrelation)

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
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

def dasQuery(queryString, entryTitle) :
    import das_client
    dasinfo = das_client.get_data('https://cmsweb.cern.ch', queryString, 0, 0, False)
    if dasinfo['status'] != 'ok' :
        raise Exception('DAS query failed.\nQuery: %s\nDAS Status returned: %s' % (queryString, dasinfo['status']))

    for entry in dasinfo['data'] :
        if len(entry[entryTitle]) > 0 :
            yield entry[entryTitle][0]

def getSecondaryFiles(primaryFileList) :
    import re
    secondaryFiles = []
    for primaryFile in primaryFileList :
        lfn = re.search('/store/.*', primaryFile).group()
        query = 'parent file=%s' % lfn
        for entry in dasQuery(query, 'parent') :
            secondaryFiles.append(entry['name'].encode('ascii','ignore'))
    return secondaryFiles

process.source.secondaryFileNames = cms.untracked.vstring(getSecondaryFiles(process.source.fileNames))

