#flake8: noqa
'''

Emulate the L1 and UCT upgrade primitives, and put them in the event.

Authors: Isobel Ojalvo, Sridhara Dasu (kludger)

'''

import FWCore.ParameterSet.Config as cms


from Configuration.StandardSequences.RawToDigi_Data_cff import *


# Modify the HCAL TPGs according to the proposed HTR modification.  If the HCAL
# is above a given energy threshold, set the MIP bit.
# HCAL TP hack

from SimCalorimetry.HcalTrigPrimProducers.hcaltpdigi_cff import *
simHcalTriggerPrimitiveDigis.inputLabel = cms.VInputTag(
    cms.InputTag('hcalDigis'),
    cms.InputTag('hcalDigis')
)

HcalTPGCoderULUT.LUTGenerationMode = cms.bool(True)

L1TRerunHCALTP_FromRAW = cms.Sequence(
    hcalDigis
    * simHcalTriggerPrimitiveDigis
)

rctProd = cms.EDProducer(
    "L1RCTProducer",
    hcalDigis = cms.VInputTag(cms.InputTag("simHcalTriggerPrimitiveDigis")),
    #hcalDigis = cms.VInputTag(cms.InputTag("hcalDigis")),
    useEcal = cms.bool(True),
    useHcal = cms.bool(True),
    ecalDigis = cms.VInputTag(cms.InputTag("ecalDigis:EcalTriggerPrimitives")),
    BunchCrossings = cms.vint32(0),
    getFedsFromOmds = cms.bool(False),
    queryDelayInLS = cms.uint32(10),
    queryIntervalInLS = cms.uint32(100),
    conditionsLabel = cms.string("")
)

digiStep = cms.Sequence(
    # Only do the digitization of objects that we care about
    #RawToDigi
    gctDigis
    * gtDigis
    * ecalDigis
)

uctEmulatorStep = cms.Sequence(
    # Now make UCT and L1 objects
    rctProd
)

emulationSequence = cms.Sequence(L1TRerunHCALTP_FromRAW + digiStep + uctEmulatorStep)
