import os
import FWCore.ParameterSet.Config as cms
from Configuration.StandardSequences.Eras import eras

import EventFilter.L1TXRawToDigi.util as util

from FWCore.ParameterSet.VarParsing import VarParsing

options = VarParsing()
options.register('runNumber', 0, VarParsing.multiplicity.singleton, VarParsing.varType.int, 'Run to analyze')
options.register('lumis', '1-max', VarParsing.multiplicity.singleton, VarParsing.varType.string, 'Lumis')
options.register('dataStream', '/ExpressPhysics/Run2015D-Express-v4/FEVT', VarParsing.multiplicity.singleton, VarParsing.varType.string, 'Dataset to look for run in')
options.register('inputFiles', [], VarParsing.multiplicity.list, VarParsing.varType.string, 'Manual file list input, will query DAS if empty')
options.register('inputFileList', '', VarParsing.multiplicity.singleton, VarParsing.varType.string, 'Manual file list input, will query DAS if empty')
options.register('outputFile', 'outputFile.root', VarParsing.multiplicity.singleton, VarParsing.varType.string, 'outputFile.root')
options.register('useORCON', False, VarParsing.multiplicity.singleton, VarParsing.varType.bool, 'Use ORCON for conditions.  This is necessary for very recent runs where conditions have not propogated to Frontier')
options.register('farmout',False, VarParsing.multiplicity.singleton, VarParsing.varType.bool, 'options to set up cfi it is able to submit to condor')
options.register('data',True, VarParsing.multiplicity.singleton, VarParsing.varType.bool, 'option to switch between data and mc')
options.register('maxEvents', 100000, VarParsing.multiplicity.singleton, VarParsing.varType.int, 'Maximum number of events to process')
options.parseArguments()

def formatLumis(lumistring, run) :
    lumis = (lrange.split('-') for lrange in lumistring.split(','))
    runlumis = (['%d:%s' % (run,lumi) for lumi in lrange] for lrange in lumis)
    return ['-'.join(l) for l in runlumis]

if options.farmout is False :
    print 'Getting files for run %d...' % options.runNumber
    if len(options.inputFiles) is 0 and options.inputFileList is '' :
        inputFiles = util.getFilesForRun(options.runNumber, options.dataStream)
    elif len(options.inputFileList) > 0 :
        with open(options.inputFileList) as f :
            inputFiles = list((line.strip() for line in f))
    else :
        inputFiles = cms.untracked.vstring(options.inputFiles)
        if len(inputFiles) is 0 :
            raise Exception('No files found for dataset %s run %d' % (options.dataStream, options.runNumber))
        print 'Ok, time to analyze'

process = cms.Process("makeUCTPUMTable", eras.Run2_2016)

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('Configuration.Geometry.GeometryExtended2016Reco_cff')
process.load('Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff')
process.load('Configuration.StandardSequences.RawToDigi_Data_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

from Configuration.AlCa.GlobalTag import GlobalTag
if options.data is True :
    process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run2_data', '')
else :
    process.GlobalTag = GlobalTag(process.GlobalTag, '80X_mcRun2_asymptotic_ForTSGStudies_fromRunIIFall15DR76_v1', '')

#reduce output messages
process.MessageLogger.cerr.FwkReport = cms.untracked.PSet( reportEvery = cms.untracked.int32(100) )


# To get L1 CaloParams
process.load('L1Trigger.L1TCalorimeter.caloStage2Params_2016_v2_2_cfi')
# To get CaloTPGTranscoder
process.load('SimCalorimetry.HcalTrigPrimProducers.hcaltpdigi_cff')

process.HcalTPGCoderULUT.LUTGenerationMode = cms.bool(False)

process.load("Configuration.Geometry.GeometryExtended2016Reco_cff")

process.es_pool = cms.ESSource("PoolDBESSource",
     process.CondDBSetup,
     timetype = cms.string('runnumber'),
     toGet = cms.VPSet(
         cms.PSet(record = cms.string("HcalLutMetadataRcd"),
             tag = cms.string("HcalLutMetadata_HFTP_1x1")
             ),
         cms.PSet(record = cms.string("HcalElectronicsMapRcd"),
             tag = cms.string("HcalElectronicsMap_HFTP_1x1")
             )
         ),
     connect = cms.string('frontier://FrontierProd/CMS_CONDITIONS'),
     authenticationMethod = cms.untracked.uint32(0)
     )
process.es_prefer_es_pool = cms.ESPrefer( "PoolDBESSource", "es_pool" )

process.load('EventFilter.L1TXRawToDigi.caloLayer1Stage2Digis_cfi')

process.load('L1Trigger.L1TCaloLayer1.simCaloStage2Layer1Digis_cfi')
process.simCaloStage2Layer1Digis.useECALLUT = cms.bool(True)
process.simCaloStage2Layer1Digis.useHCALLUT = cms.bool(True)
process.simCaloStage2Layer1Digis.useHFLUT = cms.bool(True)
process.simCaloStage2Layer1Digis.useLSB = cms.bool(True)
process.simCaloStage2Layer1Digis.verbose = cms.bool(True)
process.simCaloStage2Layer1Digis.ecalToken = cms.InputTag("l1tCaloLayer1Digis")
process.simCaloStage2Layer1Digis.hcalToken = cms.InputTag("l1tCaloLayer1Digis")

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(options.maxEvents) )

#PUMcalc can be run on RAW. Does not need RAW+MINI
process.PUMcalcCentralBX = cms.EDAnalyzer("PUMcalc",
    regionSource = cms.InputTag("simCaloStage2Layer1Digis"),
    regionLSB = cms.double(0.5),
    bunchCrossingsToUse = cms.vint32(0)
)


process.p = cms.Path(process.l1tCaloLayer1Digis*process.simCaloStage2Layer1Digis*process.PUMcalcCentralBX)
