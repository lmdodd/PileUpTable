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
    ('L1RCTParametersRcd', None) : ('L1RCTParametersRcd_L1TDevelCollisions_ExtendedScaleFactorsV4' , None)
}
process.GlobalTag = GlobalTag(process.GlobalTag, '74X_dataRun2_Prompt_v1', recordOverrides)
process.es_prefer_GlobalTag = cms.ESPrefer('PoolDBESSource', 'GlobalTag')

process.PUMcalcCentralBX = cms.EDAnalyzer("PUMcalc",
    regionSource = cms.InputTag("rctDigis"),
    bunchCrossingsToUse = cms.vint32(0)
)

process.PUMcalcSideBX = cms.EDAnalyzer("PUMcalc",
    regionSource = cms.InputTag("rctDigis"),
    bunchCrossingsToUse = cms.vint32(-2,2)
)

process.load('EventFilter.RctRawToDigi.l1RctHwDigis_cfi')

process.PUMtables = cms.Sequence( process.PUMcalcCentralBX + process.PUMcalcSideBX )

process.p = cms.Path(process.rctDigis*process.PUMtables)

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(options.maxEvents)
)

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
        #options.inputFiles
        '/store/express/Run2015C/ExpressPhysics/FEVT/Express-v1/000/254/790/00000/02014D7F-D947-E511-9C78-02163E0143DD.root',
        '/store/express/Run2015C/ExpressPhysics/FEVT/Express-v1/000/254/790/00000/0495D5E5-D147-E511-B20D-02163E01374D.root',
        '/store/express/Run2015C/ExpressPhysics/FEVT/Express-v1/000/254/790/00000/0A8C1296-DD47-E511-9C95-02163E0142E1.root',
        '/store/express/Run2015C/ExpressPhysics/FEVT/Express-v1/000/254/790/00000/0C744D1E-D647-E511-AD02-02163E012A4C.root',
        '/store/express/Run2015C/ExpressPhysics/FEVT/Express-v1/000/254/790/00000/0CEFD0A4-C447-E511-ABF0-02163E0133EC.root',
        '/store/express/Run2015C/ExpressPhysics/FEVT/Express-v1/000/254/790/00000/0EAF2413-D747-E511-9D0D-02163E014488.root',
        '/store/express/Run2015C/ExpressPhysics/FEVT/Express-v1/000/254/790/00000/0ED00BA8-E447-E511-AF97-02163E0137EF.root',
        '/store/express/Run2015C/ExpressPhysics/FEVT/Express-v1/000/254/790/00000/12B1859B-DD47-E511-98C5-02163E01559C.root',
        '/store/express/Run2015C/ExpressPhysics/FEVT/Express-v1/000/254/790/00000/165C8DFF-D147-E511-9A00-02163E015529.root',
        '/store/express/Run2015C/ExpressPhysics/FEVT/Express-v1/000/254/790/00000/16B9F0AE-DA47-E511-BDCF-02163E0139A4.root',
        '/store/express/Run2015C/ExpressPhysics/FEVT/Express-v1/000/254/790/00000/16CC9222-C647-E511-8135-02163E0143DD.root',
        '/store/express/Run2015C/ExpressPhysics/FEVT/Express-v1/000/254/790/00000/16FA7D5D-CC47-E511-A27A-02163E01549A.root',
        '/store/express/Run2015C/ExpressPhysics/FEVT/Express-v1/000/254/790/00000/1A072900-E147-E511-B998-02163E0145A2.root',
        '/store/express/Run2015C/ExpressPhysics/FEVT/Express-v1/000/254/790/00000/1A0E6D0F-D747-E511-A7D3-02163E014752.root',
        '/store/express/Run2015C/ExpressPhysics/FEVT/Express-v1/000/254/790/00000/1AE46E23-C847-E511-81CB-02163E012A4C.root',
        '/store/express/Run2015C/ExpressPhysics/FEVT/Express-v1/000/254/790/00000/1C7F5372-D947-E511-A600-02163E01374D.root',
        '/store/express/Run2015C/ExpressPhysics/FEVT/Express-v1/000/254/790/00000/1C8CA2AB-E447-E511-B854-02163E014652.root',
        '/store/express/Run2015C/ExpressPhysics/FEVT/Express-v1/000/254/790/00000/1E7912B1-DA47-E511-AEEE-02163E011CBD.root',
        '/store/express/Run2015C/ExpressPhysics/FEVT/Express-v1/000/254/790/00000/203BD416-D647-E511-B0E6-02163E0146D4.root',
        '/store/express/Run2015C/ExpressPhysics/FEVT/Express-v1/000/254/790/00000/208A9FD8-DB47-E511-BE6F-02163E014434.root',
        '/store/express/Run2015C/ExpressPhysics/FEVT/Express-v1/000/254/790/00000/208F0F99-DD47-E511-A93C-02163E015529.root',
        '/store/express/Run2015C/ExpressPhysics/FEVT/Express-v1/000/254/790/00000/2209C7F0-DE47-E511-A77E-02163E0146D4.root',
        '/store/express/Run2015C/ExpressPhysics/FEVT/Express-v1/000/254/790/00000/22B36D11-E147-E511-AEBA-02163E0143DD.root',
        '/store/express/Run2015C/ExpressPhysics/FEVT/Express-v1/000/254/790/00000/22CE3E48-C847-E511-8BF6-02163E016C4C.root',
        '/store/express/Run2015C/ExpressPhysics/FEVT/Express-v1/000/254/790/00000/26E895BC-CA47-E511-B633-02163E01385E.root',
        '/store/express/Run2015C/ExpressPhysics/FEVT/Express-v1/000/254/790/00000/282476EA-E247-E511-A603-02163E014434.root',
        '/store/express/Run2015C/ExpressPhysics/FEVT/Express-v1/000/254/790/00000/2AD2FC77-D347-E511-9394-02163E014243.root',
        '/store/express/Run2015C/ExpressPhysics/FEVT/Express-v1/000/254/790/00000/2C7530F6-D147-E511-AFF4-02163E012AAF.root',
        '/store/express/Run2015C/ExpressPhysics/FEVT/Express-v1/000/254/790/00000/32F0E8F3-D147-E511-BA0A-02163E0143DD.root',
        '/store/express/Run2015C/ExpressPhysics/FEVT/Express-v1/000/254/790/00000/3607EA55-CC47-E511-A855-02163E014488.root',
        '/store/express/Run2015C/ExpressPhysics/FEVT/Express-v1/000/254/790/00000/3C29EFC0-CA47-E511-8EBE-02163E01354F.root',
        '/store/express/Run2015C/ExpressPhysics/FEVT/Express-v1/000/254/790/00000/40EEBEAE-DA47-E511-9A5B-02163E0139A4.root',
        '/store/express/Run2015C/ExpressPhysics/FEVT/Express-v1/000/254/790/00000/441DF867-D347-E511-AB00-02163E0133C6.root',
        '/store/express/Run2015C/ExpressPhysics/FEVT/Express-v1/000/254/790/00000/4427E500-DF47-E511-82FD-02163E01475A.root',
        '/store/express/Run2015C/ExpressPhysics/FEVT/Express-v1/000/254/790/00000/46B954BC-CA47-E511-A57B-02163E014348.root',
        '/store/express/Run2015C/ExpressPhysics/FEVT/Express-v1/000/254/790/00000/481590B6-CD47-E511-BC0C-02163E014488.root',
        '/store/express/Run2015C/ExpressPhysics/FEVT/Express-v1/000/254/790/00000/48948A96-DD47-E511-99E7-02163E0145A2.root',
        '/store/express/Run2015C/ExpressPhysics/FEVT/Express-v1/000/254/790/00000/48BEDE8B-D847-E511-B925-02163E0137EF.root',
        '/store/express/Run2015C/ExpressPhysics/FEVT/Express-v1/000/254/790/00000/4A5AFF1A-D647-E511-B5F0-02163E012790.root',
        '/store/express/Run2015C/ExpressPhysics/FEVT/Express-v1/000/254/790/00000/4C71411E-C347-E511-848B-02163E01354F.root',
        '/store/express/Run2015C/ExpressPhysics/FEVT/Express-v1/000/254/790/00000/4E34D767-D347-E511-AC1E-02163E0133C6.root',
        '/store/express/Run2015C/ExpressPhysics/FEVT/Express-v1/000/254/790/00000/5010D916-D647-E511-BBFD-02163E014243.root',
        '/store/express/Run2015C/ExpressPhysics/FEVT/Express-v1/000/254/790/00000/5036ABB2-DD47-E511-A357-02163E016C4C.root',
        '/store/express/Run2015C/ExpressPhysics/FEVT/Express-v1/000/254/790/00000/52D806B1-DA47-E511-BA83-02163E011CBD.root',
        '/store/express/Run2015C/ExpressPhysics/FEVT/Express-v1/000/254/790/00000/5439B69B-DD47-E511-9870-02163E01559C.root',
        '/store/express/Run2015C/ExpressPhysics/FEVT/Express-v1/000/254/790/00000/5647846E-C847-E511-806A-02163E014549.root',
        '/store/express/Run2015C/ExpressPhysics/FEVT/Express-v1/000/254/790/00000/567F7986-D847-E511-99CD-02163E0146D4.root',
        '/store/express/Run2015C/ExpressPhysics/FEVT/Express-v1/000/254/790/00000/56D2E878-D347-E511-9736-02163E012AAF.root',
        '/store/express/Run2015C/ExpressPhysics/FEVT/Express-v1/000/254/790/00000/5830E2EC-E247-E511-8F42-02163E011CBD.root',
        '/store/express/Run2015C/ExpressPhysics/FEVT/Express-v1/000/254/790/00000/58344BFC-CF47-E511-ACED-02163E014488.root',
        '/store/express/Run2015C/ExpressPhysics/FEVT/Express-v1/000/254/790/00000/5843BDFB-E047-E511-9B07-02163E014376.root',
        '/store/express/Run2015C/ExpressPhysics/FEVT/Express-v1/000/254/790/00000/5AC12C1D-C647-E511-BBCF-02163E01475A.root',
        '/store/express/Run2015C/ExpressPhysics/FEVT/Express-v1/000/254/790/00000/5C0D19FC-CF47-E511-9A69-02163E014376.root',
        '/store/express/Run2015C/ExpressPhysics/FEVT/Express-v1/000/254/790/00000/5C89E171-D947-E511-B32D-02163E014488.root',
        '/store/express/Run2015C/ExpressPhysics/FEVT/Express-v1/000/254/790/00000/5E915212-D747-E511-A797-02163E0141FC.root',
        '/store/express/Run2015C/ExpressPhysics/FEVT/Express-v1/000/254/790/00000/5EAA7C8C-D847-E511-BC8E-02163E0137EF.root',
        '/store/express/Run2015C/ExpressPhysics/FEVT/Express-v1/000/254/790/00000/62371000-E147-E511-9CD5-02163E011CBD.root',
        '/store/express/Run2015C/ExpressPhysics/FEVT/Express-v1/000/254/790/00000/64B7FD03-E147-E511-ADBB-02163E01559C.root',
        '/store/express/Run2015C/ExpressPhysics/FEVT/Express-v1/000/254/790/00000/6884C488-D847-E511-A340-02163E012AB5.root',
        '/store/express/Run2015C/ExpressPhysics/FEVT/Express-v1/000/254/790/00000/6894CF95-DD47-E511-979E-02163E014775.root',
        '/store/express/Run2015C/ExpressPhysics/FEVT/Express-v1/000/254/790/00000/6E2124AC-E447-E511-A2F3-02163E013529.root',
        '/store/express/Run2015C/ExpressPhysics/FEVT/Express-v1/000/254/790/00000/720EE885-D847-E511-B2C3-02163E0139A4.root',
        '/store/express/Run2015C/ExpressPhysics/FEVT/Express-v1/000/254/790/00000/72C1EAD6-E547-E511-BAFC-02163E011BE4.root',
        '/store/express/Run2015C/ExpressPhysics/FEVT/Express-v1/000/254/790/00000/74A105F0-DE47-E511-AC0C-02163E011862.root',
        '/store/express/Run2015C/ExpressPhysics/FEVT/Express-v1/000/254/790/00000/7691D7D9-DB47-E511-8EDC-02163E014466.root',
        '/store/express/Run2015C/ExpressPhysics/FEVT/Express-v1/000/254/790/00000/76CB5B58-CC47-E511-8394-02163E014652.root',
        '/store/express/Run2015C/ExpressPhysics/FEVT/Express-v1/000/254/790/00000/7A2B1B20-C847-E511-BE37-02163E01202A.root',
        '/store/express/Run2015C/ExpressPhysics/FEVT/Express-v1/000/254/790/00000/7A442DE2-D047-E511-9B26-02163E014466.root',
        '/store/express/Run2015C/ExpressPhysics/FEVT/Express-v1/000/254/790/00000/7A8F5522-C347-E511-A2F8-02163E014652.root',
        '/store/express/Run2015C/ExpressPhysics/FEVT/Express-v1/000/254/790/00000/7C105004-D247-E511-9398-02163E01549A.root',
        '/store/express/Run2015C/ExpressPhysics/FEVT/Express-v1/000/254/790/00000/7C12E574-D947-E511-B643-02163E0139A4.root',
        '/store/express/Run2015C/ExpressPhysics/FEVT/Express-v1/000/254/790/00000/7C6D16AB-DA47-E511-9D6A-02163E014466.root',
        '/store/express/Run2015C/ExpressPhysics/FEVT/Express-v1/000/254/790/00000/7CC4F174-D947-E511-BB77-02163E0139A4.root',
        '/store/express/Run2015C/ExpressPhysics/FEVT/Express-v1/000/254/790/00000/7E60C095-DD47-E511-A44F-02163E014466.root',
        '/store/express/Run2015C/ExpressPhysics/FEVT/Express-v1/000/254/790/00000/80F3BF02-E147-E511-A407-02163E011BE4.root',
        '/store/express/Run2015C/ExpressPhysics/FEVT/Express-v1/000/254/790/00000/82AB35F9-CE47-E511-9C8C-02163E01559C.root',
        '/store/express/Run2015C/ExpressPhysics/FEVT/Express-v1/000/254/790/00000/862554B2-C947-E511-980B-02163E014103.root',
        '/store/express/Run2015C/ExpressPhysics/FEVT/Express-v1/000/254/790/00000/8C14E208-E147-E511-9F7A-02163E013529.root',
        '/store/express/Run2015C/ExpressPhysics/FEVT/Express-v1/000/254/790/00000/8CDBAA95-DD47-E511-B833-02163E0143DD.root',
        '/store/express/Run2015C/ExpressPhysics/FEVT/Express-v1/000/254/790/00000/8CF63897-DD47-E511-8A01-02163E013529.root',
        '/store/express/Run2015C/ExpressPhysics/FEVT/Express-v1/000/254/790/00000/904CEAA2-E447-E511-AFD5-02163E011CBD.root',
        '/store/express/Run2015C/ExpressPhysics/FEVT/Express-v1/000/254/790/00000/90CB99A3-C447-E511-BC2B-02163E0137EF.root',
        '/store/express/Run2015C/ExpressPhysics/FEVT/Express-v1/000/254/790/00000/926820EC-E247-E511-A0CD-02163E011F8E.root',
        '/store/express/Run2015C/ExpressPhysics/FEVT/Express-v1/000/254/790/00000/985117FE-E047-E511-8AC6-02163E014775.root',
        '/store/express/Run2015C/ExpressPhysics/FEVT/Express-v1/000/254/790/00000/98B6B30C-C747-E511-8FC7-02163E014222.root',
        '/store/express/Run2015C/ExpressPhysics/FEVT/Express-v1/000/254/790/00000/98C8C2D3-D447-E511-9A0F-02163E014434.root',
        '/store/express/Run2015C/ExpressPhysics/FEVT/Express-v1/000/254/790/00000/9E4AC1F3-CE47-E511-B639-02163E0133EC.root',
        '/store/express/Run2015C/ExpressPhysics/FEVT/Express-v1/000/254/790/00000/A20E077D-D347-E511-9149-02163E012A4C.root',
        '/store/express/Run2015C/ExpressPhysics/FEVT/Express-v1/000/254/790/00000/A645CADA-DB47-E511-8621-02163E011F8E.root',
        '/store/express/Run2015C/ExpressPhysics/FEVT/Express-v1/000/254/790/00000/A67C1386-D847-E511-B1BD-02163E011F8E.root',
        '/store/express/Run2015C/ExpressPhysics/FEVT/Express-v1/000/254/790/00000/A8DBD7E2-CE47-E511-9D4B-02163E011CBD.root',
        '/store/express/Run2015C/ExpressPhysics/FEVT/Express-v1/000/254/790/00000/AA621FEA-E247-E511-8533-02163E0155B9.root',
        '/store/express/Run2015C/ExpressPhysics/FEVT/Express-v1/000/254/790/00000/AA7D20E5-D047-E511-ADE1-02163E0141FC.root',
        '/store/express/Run2015C/ExpressPhysics/FEVT/Express-v1/000/254/790/00000/AA92AA84-D847-E511-B6D2-02163E014376.root',
        '/store/express/Run2015C/ExpressPhysics/FEVT/Express-v1/000/254/790/00000/AC4554DF-CE47-E511-8D6F-02163E014466.root',
        '/store/express/Run2015C/ExpressPhysics/FEVT/Express-v1/000/254/790/00000/AE593BC9-C947-E511-8949-02163E0133FE.root',
        '/store/express/Run2015C/ExpressPhysics/FEVT/Express-v1/000/254/790/00000/AED8EBFA-D147-E511-92B0-02163E01559C.root',
        '/store/express/Run2015C/ExpressPhysics/FEVT/Express-v1/000/254/790/00000/B05114F8-D147-E511-9F1D-02163E0141FC.root',
        '/store/express/Run2015C/ExpressPhysics/FEVT/Express-v1/000/254/790/00000/B0E75FDA-DB47-E511-9746-02163E0143DD.root',
        '/store/express/Run2015C/ExpressPhysics/FEVT/Express-v1/000/254/790/00000/B49A0AC1-D447-E511-BCAD-02163E014222.root',
        '/store/express/Run2015C/ExpressPhysics/FEVT/Express-v1/000/254/790/00000/B6B2EF15-D647-E511-83E7-02163E014243.root',
        '/store/express/Run2015C/ExpressPhysics/FEVT/Express-v1/000/254/790/00000/B6FBDAB7-CD47-E511-B681-02163E014376.root',
        '/store/express/Run2015C/ExpressPhysics/FEVT/Express-v1/000/254/790/00000/BAAD82AC-E447-E511-BBD2-02163E014488.root',
        '/store/express/Run2015C/ExpressPhysics/FEVT/Express-v1/000/254/790/00000/BC615EBC-CA47-E511-835C-02163E014348.root',
        '/store/express/Run2015C/ExpressPhysics/FEVT/Express-v1/000/254/790/00000/BEF22897-DD47-E511-8F7C-02163E0146D4.root',
        '/store/express/Run2015C/ExpressPhysics/FEVT/Express-v1/000/254/790/00000/C4176AE1-DB47-E511-8ED9-02163E012790.root',
        '/store/express/Run2015C/ExpressPhysics/FEVT/Express-v1/000/254/790/00000/C67F0EB4-CD47-E511-8817-02163E0143DD.root',
        '/store/express/Run2015C/ExpressPhysics/FEVT/Express-v1/000/254/790/00000/C6FE9018-D647-E511-8606-02163E011CBD.root',
        '/store/express/Run2015C/ExpressPhysics/FEVT/Express-v1/000/254/790/00000/C8DB54B5-CD47-E511-AD96-02163E014222.root',
        '/store/express/Run2015C/ExpressPhysics/FEVT/Express-v1/000/254/790/00000/CAEA07F7-D147-E511-82D6-02163E014752.root',
        '/store/express/Run2015C/ExpressPhysics/FEVT/Express-v1/000/254/790/00000/D05CE996-DD47-E511-A331-02163E0139A4.root',
        '/store/express/Run2015C/ExpressPhysics/FEVT/Express-v1/000/254/790/00000/D0E3A6F1-DE47-E511-B484-02163E0126BC.root',
        '/store/express/Run2015C/ExpressPhysics/FEVT/Express-v1/000/254/790/00000/D2931A1B-D647-E511-8C95-02163E0134D1.root',
        '/store/express/Run2015C/ExpressPhysics/FEVT/Express-v1/000/254/790/00000/D8164669-D347-E511-B9A3-02163E0133C6.root',
        '/store/express/Run2015C/ExpressPhysics/FEVT/Express-v1/000/254/790/00000/D8427AFD-CF47-E511-8737-02163E014652.root',
        '/store/express/Run2015C/ExpressPhysics/FEVT/Express-v1/000/254/790/00000/DAF2D016-D647-E511-BC8D-02163E0145A2.root',
        '/store/express/Run2015C/ExpressPhysics/FEVT/Express-v1/000/254/790/00000/DC232597-DD47-E511-89FD-02163E011CBD.root',
        '/store/express/Run2015C/ExpressPhysics/FEVT/Express-v1/000/254/790/00000/DCE04BB1-E447-E511-B550-02163E0155B9.root',
        '/store/express/Run2015C/ExpressPhysics/FEVT/Express-v1/000/254/790/00000/DE42A5F7-D147-E511-B301-02163E0137EF.root',
        '/store/express/Run2015C/ExpressPhysics/FEVT/Express-v1/000/254/790/00000/DEB4F56F-D847-E511-AE83-02163E012A4C.root',
        '/store/express/Run2015C/ExpressPhysics/FEVT/Express-v1/000/254/790/00000/E061E1F6-DE47-E511-AB0D-02163E0143CC.root',
        '/store/express/Run2015C/ExpressPhysics/FEVT/Express-v1/000/254/790/00000/E0CB6C1A-C647-E511-A5F5-02163E014103.root',
        '/store/express/Run2015C/ExpressPhysics/FEVT/Express-v1/000/254/790/00000/E0F3DC25-E147-E511-BA87-02163E013765.root',
        '/store/express/Run2015C/ExpressPhysics/FEVT/Express-v1/000/254/790/00000/E22F8518-D647-E511-ADC3-02163E012AAF.root',
        '/store/express/Run2015C/ExpressPhysics/FEVT/Express-v1/000/254/790/00000/E2FDE31D-D647-E511-8BEB-02163E012A4C.root',
        '/store/express/Run2015C/ExpressPhysics/FEVT/Express-v1/000/254/790/00000/E4220214-E147-E511-A3D1-02163E0133C6.root',
        '/store/express/Run2015C/ExpressPhysics/FEVT/Express-v1/000/254/790/00000/E4C81AAC-DA47-E511-BAEB-02163E011851.root',
        '/store/express/Run2015C/ExpressPhysics/FEVT/Express-v1/000/254/790/00000/EC33FA17-D647-E511-BE63-02163E011CBD.root',
        '/store/express/Run2015C/ExpressPhysics/FEVT/Express-v1/000/254/790/00000/EC363072-D947-E511-914F-02163E014752.root',
        '/store/express/Run2015C/ExpressPhysics/FEVT/Express-v1/000/254/790/00000/EC5CD6EC-E247-E511-A8F5-02163E0142E1.root',
        '/store/express/Run2015C/ExpressPhysics/FEVT/Express-v1/000/254/790/00000/EE667CAD-CA47-E511-ABB8-02163E012AB5.root',
        '/store/express/Run2015C/ExpressPhysics/FEVT/Express-v1/000/254/790/00000/EED79768-D347-E511-B854-02163E011851.root',
        '/store/express/Run2015C/ExpressPhysics/FEVT/Express-v1/000/254/790/00000/F08A41DE-DB47-E511-AF63-02163E01559C.root',
        '/store/express/Run2015C/ExpressPhysics/FEVT/Express-v1/000/254/790/00000/F22F0F89-D547-E511-A7AE-02163E0134D1.root',
        '/store/express/Run2015C/ExpressPhysics/FEVT/Express-v1/000/254/790/00000/F284A675-D947-E511-AAB0-02163E0139A4.root',
        '/store/express/Run2015C/ExpressPhysics/FEVT/Express-v1/000/254/790/00000/F2B99102-E147-E511-86D5-02163E0141FC.root',
        '/store/express/Run2015C/ExpressPhysics/FEVT/Express-v1/000/254/790/00000/F6C43626-D747-E511-A294-02163E015529.root',
        '/store/express/Run2015C/ExpressPhysics/FEVT/Express-v1/000/254/790/00000/F83528E0-DB47-E511-9A23-02163E0137EF.root',
        '/store/express/Run2015C/ExpressPhysics/FEVT/Express-v1/000/254/790/00000/FA265A10-D747-E511-8283-02163E0143DD.root',
    ),
)

import FWCore.PythonUtilities.LumiList as LumiList
process.source.lumisToProcess = LumiList.LumiList(filename = 'Run2015C.json').getVLuminosityBlockRange()

process.TFileService = cms.Service(
    "TFileService",
    fileName = cms.string(options.outputFile)
)

