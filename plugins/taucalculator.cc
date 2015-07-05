/*
 * =====================================================================================
 *
 *       Filename:  taucalculator.cc
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
#include "DataFormats/PatCandidates/interface/MET.h"
#include "DataFormats/METReco/interface/GenMET.h"
#include "DataFormats/METReco/interface/GenMETFwd.h"
#include "DataFormats/METReco/interface/CaloMET.h"
#include "DataFormats/METReco/interface/MET.h"
//typedef std::vector<edm::InputTag> VInputTag;
//typedef std::vector<unsigned int> PackedUIntCollection;

#include "L1Trigger/PileUpTable/interface/helpers.h"
#include "L1Trigger/PileUpTable/interface/UCTCandidate.h"



using namespace std;
using namespace edm;


class taucalculator : public edm::EDAnalyzer {
	public:
		explicit taucalculator(const edm::ParameterSet& pset);

	private:
		virtual void analyze(const edm::Event& evt, const edm::EventSetup& es);
		double regionPhysicalEt(const L1CaloRegion& cand) const {
			return regionLSB_*cand.et();
		}

		void makeSums();
		TTree* tree;
		unsigned int run_;
		unsigned int lumi_;
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
		Handle<reco::GenParticleCollection> genParticles;
		Handle<reco::GenMETCollection> genMETColl;


		vector<float> tauPt_;
		vector<float> tauEta_;
		vector<float> tauPhi_;
		vector<float> tauGenPt_;
		vector<float> tauGenEta_;
		vector<float> tauGenPhi_;

		vector<double> sinPhi;
		vector<double> cosPhi;


		double regionLSB_;
};









taucalculator::taucalculator(const edm::ParameterSet& pset) 
{
	// Initialize the ntuple builder
	edm::Service<TFileService> fs;
	tree = fs->make<TTree>("Ntuple", "Ntuple");
	tree->Branch("tauPt", "std::vector<float>", &tauPt_);
	tree->Branch("tauEta", "std::vector<float>", &tauEta_);
	tree->Branch("tauPhi", "std::vector<float>", &tauPhi_);
	tree->Branch("tauGenPt", "std::vector<float>", &tauGenPt_);
	tree->Branch("tauGenEta", "std::vector<float>", &tauGenEta_);
	tree->Branch("tauGenPhi", "std::vector<float>", &tauGenPhi_);
	tree->Branch("run", &run_, "run/i");
	tree->Branch("lumi", &lumi_, "lumi/i");
	tree->Branch("evt", &event_, "evt/l");
	tree->Branch("npvs", &npvs_, "npvs/i");
	tree->Branch("instlumi", &instLumi_, "instlumi/F");
	scalerSrc_ = pset.exists("scalerSrc") ? pset.getParameter<InputTag>("scalerSrc") : InputTag("scalersRawToDigi");
	genSrc_ = pset.exists("genSrc") ? pset.getParameter<InputTag>("genSrc") : InputTag("genParticles");
	//emulation variables
	//53x
	vertexSrc_ = pset.exists("vertexSrc") ? pset.getParameter<InputTag>("vertexSrc") : InputTag("offlinePrimaryVertices");
	pvSrc_ = pset.exists("pvSrc") ? pset.getParameter<InputTag>("pvSrc") : InputTag("addPileupInfo");
	regionLSB_ = pset.getParameter<double>("regionLSB");
	for(unsigned int i = 0; i < L1CaloRegionDetId::N_PHI; i++) {
		sinPhi.push_back(sin(2. * 3.1415927 * i * 1.0 / L1CaloRegionDetId::N_PHI));
		cosPhi.push_back(cos(2. * 3.1415927 * i * 1.0 / L1CaloRegionDetId::N_PHI));
	}

}


void taucalculator::analyze(const edm::Event& evt, const edm::EventSetup& es) {

	// Setup meta info
	run_ = evt.id().run();
	lumi_ = evt.id().luminosityBlock();
	event_ = evt.id().event();

	evt.getByLabel(scalerSrc_, lumiScalers);
	evt.getByLabel("rctProd", newRegions);
	evt.getByLabel(pvSrc_, puInfo);
	evt.getByLabel(vertexSrc_, vertices_r);
	evt.getByLabel(genSrc_, genParticles);

	//evt.getByLabel("genMetCalo", genMETColl);
	//float genMET = (*genMETColl)[0].pt(); 
	//cout<<"genMet: "<<genMET<<endl;
	//evt.getByLabel(tauSrc_, tauObjects);


	tauPt_.clear();
	tauEta_.clear();
	tauPhi_.clear();
	tauGenPt_.clear();
	tauGenEta_.clear();
	tauGenPhi_.clear();

	instLumi_ = -1;
	npvs_ = -1;
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

	for(size_t i = 0; i < genParticles->size(); ++ i) {
		const reco::GenParticle & p = (*genParticles)[i];
		int id = p.pdgId();
		double eta = p.eta();
		int status = p.status();
		double pt = p.pt();
		if (pt>20&&abs(id)==15&&fabs(eta)<3.0&&status==2){
			//cout<<"~!~!=== IT'S A TAU ===!~!~ "<<id<<endl;
			double phi = p.phi();
			//double mass = p.mass();
			//cout<<"GenPt: "<<pt<<"     GenEta: "<<eta<<"     GenPhi: "<<phi<<endl;
			tauGenPt_.push_back(pt);
			tauGenEta_.push_back(eta);
			tauGenPhi_.push_back(phi);
			unsigned int regnEta=convertGenEta(eta);
			//cout<<"GenPhi: "<<phi<<endl;
			unsigned int regnPhi=convertGenPhi(phi);
			//cout<<"Gen->RegionPhi: "<<regnPhi<<endl;
			for(L1CaloRegionCollection::const_iterator newRegion = newRegions->begin(); newRegion != newRegions->end(); newRegion++)
			{
				if (regnEta==newRegion->gctEta() && regnPhi==newRegion->gctPhi()){

					double regionET =  regionPhysicalEt(*newRegion);
					unsigned int regionEta = newRegion->gctEta(); 
					unsigned int regionPhi = newRegion->gctPhi(); 
					//double neighborET =-999;
					double neighborET =0;
					for(L1CaloRegionCollection::const_iterator neighbor = newRegions->begin(); neighbor != newRegions->end(); neighbor++)
					{       
						double tmpET = regionPhysicalEt(*neighbor);
						if (deltaGctPhi(*newRegion, *neighbor) == 1 && (newRegion->gctEta() == neighbor->gctEta()))
						{neighborET += tmpET;}
						else if (deltaGctPhi(*newRegion, *neighbor) ==-1 && (newRegion->gctEta() == neighbor->gctEta()))
						{neighborET += tmpET;}
						else if (deltaGctPhi(*newRegion, *neighbor) ==0 && (newRegion->gctEta() - neighbor->gctEta()) == 1)
						{neighborET += tmpET;}
						else if (deltaGctPhi(*newRegion, *neighbor) == 0 && (neighbor->gctEta() - newRegion->gctEta()) == 1)
						{neighborET += tmpET;}
					}                                      

					tauPt_.push_back(regionET+neighborET);
					tauEta_.push_back(regionEta);
					tauPhi_.push_back(regionPhi);
				}//end matched region
			}//end for region loop 

			tree->Fill();
		}//end gen tau loop
	}//end genparticle loop



	//cout<< "====Make Sums===="<<std::endl;
	//makeSums();
	//cout<< "====Push Back===="<<std::endl;
	//cout<< "MET: "<<MET<<std::endl;

	//cout<< "====Fill Tree===="<<std::endl;
	//	tree->Fill();
}

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(taucalculator);
