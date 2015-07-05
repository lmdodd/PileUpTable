/*
 * =====================================================================================
 *
 *       Filename:  pum0calculator.cc
 *
 *    Description:  
 *
 *         Author:  Laura Dodd, laura.dodd@cern.ch
 *        Company:  UW Madison
 *
 * =====================================================================================
 */
#include <memory>
#include <math.h>
#include <vector>
#include <list>
#include <TTree.h>
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"

#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/Math/interface/deltaPhi.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/L1Trigger/interface/L1JetParticle.h"
#include "DataFormats/L1Trigger/interface/L1EmParticle.h"
#include "DataFormats/Common/interface/DetSet.h"
#include "DataFormats/L1CaloTrigger/interface/L1CaloCollections.h"
#include "DataFormats/L1CaloTrigger/interface/L1CaloRegion.h"
#include "DataFormats/L1CaloTrigger/interface/L1CaloEmCand.h"
#include "DataFormats/L1CaloTrigger/interface/L1CaloRegionDetId.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/Scalers/interface/LumiScalers.h"
#include "TTree.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "SimDataFormats/PileupSummaryInfo/interface/PileupSummaryInfo.h"
// user include files
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "DataFormats/Provenance/interface/EventAuxiliary.h"
#include "DataFormats/L1Trigger/interface/Tau.h"
#include "DataFormats/Math/interface/LorentzVector.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "DataFormats/Common/interface/RefToPtr.h"
#include "DataFormats/TauReco/interface/PFTau.h"
#include "DataFormats/TauReco/interface/PFTauDiscriminator.h"
#include "DataFormats/PatCandidates/interface/Tau.h"

#include "L1Trigger/PileUpTable/interface/helpers.h"
//typedef std::vector<edm::InputTag> VInputTag;
//typedef std::vector<unsigned int> PackedUIntCollection;


using namespace std;
using namespace edm;


class pum0calculator : public edm::EDAnalyzer {
	public:
		explicit pum0calculator(const edm::ParameterSet& pset);

	private:
		virtual void analyze(const edm::Event& evt, const edm::EventSetup& es);
		double regionPhysicalEt(const L1CaloRegion& cand) const {
			return regionLSB_*cand.et();
		}


		TTree* tree;
		unsigned int run_;
		unsigned int lumi_;
		unsigned int puMult0_;
		unsigned long int event_;

		InputTag scalerSrc_;
		InputTag uctDigis_;
		InputTag pvSrc_;
		InputTag vertexSrc_;
		InputTag genSrc_;

		float instLumi_;
		unsigned int npvs_;

		Handle<L1CaloRegionCollection> newRegions;
		Handle<LumiScalersCollection> lumiScalers;
		Handle<std::vector<PileupSummaryInfo> > puInfo;
		//53X
		Handle<reco::VertexCollection> vertices_r;

		vector<float> regionPt_;
		vector<int> regionEta_;
		vector<float> regionPhi_;

		vector<double> sinPhi;
		vector<double> cosPhi;

		double regionLSB_;
		// Add UCT-only variables
		unsigned int minGctEtaForSums;
		unsigned int maxGctEtaForSums;
};


pum0calculator::pum0calculator(const edm::ParameterSet& pset) 
{
	// Initialize the ntuple builder
	edm::Service<TFileService> fs;
	tree = fs->make<TTree>("Ntuple", "Ntuple");
	tree->Branch("regionPt", "std::vector<float>", &regionPt_);
	tree->Branch("regionEta", "std::vector<int>", &regionEta_);
	tree->Branch("regionPhi", "std::vector<float>", &regionPhi_);
	tree->Branch("run", &run_, "run/i");
	tree->Branch("lumi", &lumi_, "lumi/i");
	tree->Branch("evt", &event_, "evt/l");
	tree->Branch("npvs", &npvs_, "npvs/i");
	tree->Branch("instlumi", &instLumi_, "instlumi/F");
	tree->Branch("puMult0", &puMult0_, "puMult0/i");
	scalerSrc_ = pset.exists("scalerSrc") ? pset.getParameter<InputTag>("scalerSrc") : InputTag("scalersRawToDigi");
	genSrc_ = pset.exists("genSrc") ? pset.getParameter<InputTag>("genSrc") : InputTag("genParticles");
	//emulation variables
	//53x
	vertexSrc_ = pset.exists("vertexSrc") ? pset.getParameter<InputTag>("vertexSrc") : InputTag("offlinePrimaryVertices");
	pvSrc_ = pset.exists("pvSrc") ? pset.getParameter<InputTag>("pvSrc") : InputTag("addPileupInfo");
	regionLSB_ = pset.getParameter<double>("regionLSB");
}


void pum0calculator::analyze(const edm::Event& evt, const edm::EventSetup& es) {

	// Setup meta info
	run_ = evt.id().run();
	lumi_ = evt.id().luminosityBlock();
	event_ = evt.id().event();

	// Get instantaneous lumi from the scalers
	// thx to Carlo Battilana
	//Handle<LumiScalersCollection> lumiScalers;
	//Handle<L1CaloRegionCollection> newRegions;
	//edm::DetSetVector<L1CaloRegionCollection> newRegion;
	//edm::Handle<L1CaloRegionCollection>::const_iterator newRegion;

	evt.getByLabel(scalerSrc_, lumiScalers);
	evt.getByLabel("rctProd", newRegions);
	evt.getByLabel(pvSrc_, puInfo);
	evt.getByLabel(vertexSrc_, vertices_r);

	regionEta_.clear();
	regionPhi_.clear();
	regionPt_.clear();

	instLumi_ = -1;
	npvs_ = -1;
	puMult0_ = 0;

        //53X
	//npvs_ = vertices->size();
	
        for (vector<PileupSummaryInfo>::const_iterator PVI = puInfo->begin(); PVI != puInfo->end(); ++PVI){	
            int BX = PVI->getBunchCrossing();
            if (BX==0){
               npvs_ = PVI->getPU_NumInteractions();
	     }
         }

	if (lumiScalers->size())
		instLumi_ = lumiScalers->begin()->instantLumi();



	for(L1CaloRegionCollection::const_iterator newRegion = newRegions->begin(); newRegion != newRegions->end(); newRegion++)
	{
		double regionET =  regionPhysicalEt(*newRegion);
		unsigned int regionEta = newRegion->gctEta(); 
		unsigned int regionPhi = newRegion->gctPhi(); 

		regionPt_.push_back(regionET);
		regionEta_.push_back(regionEta);
		regionPhi_.push_back(regionPhi);

		if (regionET > 0) {puMult0_++; }//this calculates pum0
	} //end Pum0, pionPT

	tree->Fill();
}

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(pum0calculator);
