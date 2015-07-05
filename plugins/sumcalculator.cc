/*
 * =====================================================================================
 *
 *       Filename:  sumcalculator.cc
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


class sumcalculator : public edm::EDAnalyzer {
	public:
		explicit sumcalculator(const edm::ParameterSet& pset);

	private:
		virtual void analyze(const edm::Event& evt, const edm::EventSetup& es);
		double regionPhysicalEt(const L1CaloRegion& cand) const {
			return regionLSB_*cand.et();
		}

		void makeSums();
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
		Handle<reco::GenParticleCollection> genParticles;
		Handle<reco::GenMETCollection> genMETColl;


		vector<float> sumET_;
		vector<float> MET_;
		vector<float> metPhi_;
		vector<float> MHT_;
		vector<float> mhtPhi_;
		vector<float> sumGenET_;
		vector<float> genMET_;
		vector<float> genMETPhi_;
		vector<float> genMHT_;

		unsigned int sumET;
		int sumEx;
		int sumEy;
		unsigned int MET;
		unsigned int sumHT;
		int sumHx;
		int sumHy;
		unsigned int MHT;
		double physicalPhiMET; 
		unsigned int metIPhi;
		double physicalPhiHT; 
		unsigned int mhtIPhi;

		vector<double> sinPhi;
		vector<double> cosPhi;


		double regionLSB_;
};




void sumcalculator::makeSums()
{
	//cout<<"===In makeSums==="<<endl;
	sumET = 0;
	sumEx = 0;
	sumEy = 0;
	sumHT = 0;
	sumHx = 0;
	sumHy = 0;

	//cout<<"===makeSums:for loop==="<<endl;
	for(L1CaloRegionCollection::const_iterator newRegion = newRegions->begin();
			newRegion != newRegions->end(); newRegion++){
		// Remove forward stuff
		if (newRegion->gctEta() < 4 || newRegion->gctEta() > 17) {
			continue;
		}

		double regionET =  regionPhysicalEt(*newRegion);     

		unsigned int regionETCutForMET=0;
		unsigned int regionETCutForHT=7;
		unsigned int regionETCutForNeighbor=0;

		if(regionET >= regionETCutForMET){
	                //cout<<"===makeSums:regionET >= regionETCutForMET==="<<endl;
			sumET += regionET;
			sumEx += (int) (((double) regionET) * cosPhi[newRegion->gctPhi()]);
			sumEy += (int) (((double) regionET) * sinPhi[newRegion->gctPhi()]);
		}
		if(regionET >= regionETCutForHT) {
	                 //cout<<"===makeSums:regionET >= regionETCutForMHT==="<<endl;
			sumHT += regionET;
			sumHx += (int) (((double) regionET) * cosPhi[newRegion->gctPhi()]);
			sumHy += (int) (((double) regionET) * sinPhi[newRegion->gctPhi()]);
		}
		else if(regionET >= regionETCutForNeighbor) {
	                 //cout<<"===makeSums:regionET >= regionETCutForNeighbor==="<<endl;
			bool goodNeighbor = false;
			for(L1CaloRegionCollection::const_iterator neighbor = newRegions->begin();
					neighbor != newRegions->end(); neighbor++) {
				if((deltaGctPhi(*newRegion, *neighbor) == 1 && (newRegion->gctEta() == neighbor->gctEta())) ||
						(deltaGctPhi(*newRegion, *neighbor) == -1 && (newRegion->gctEta() == neighbor->gctEta())) ||
						(deltaGctPhi(*newRegion, *neighbor) == 0 && (newRegion->gctEta() - neighbor->gctEta()) == 1) ||
						(deltaGctPhi(*newRegion, *neighbor) == 0 && (neighbor->gctEta() - newRegion->gctEta()) == 1)) {
					double neighborET = regionPhysicalEt(*neighbor);
					if(neighborET >= regionETCutForHT) {
						goodNeighbor = true;
					}
				}
			}
			if(goodNeighbor ) {
				sumHT += regionET;
				sumHx += (int) (((double) regionET) * cosPhi[newRegion->gctPhi()]);
				sumHy += (int) (((double) regionET) * sinPhi[newRegion->gctPhi()]);
			}
		}
	}
	//cout<<"===makeSums:after for loop==="<<endl;
	MET = ((unsigned int) sqrt(sumEx * sumEx + sumEy * sumEy));
	//cout<<"===MET: "<<MET<<"==="<<endl;
	MHT = ((unsigned int) sqrt(sumHx * sumHx + sumHy * sumHy));
	//cout<<"===MHT: "<<MHT<<"==="<<endl;

	physicalPhiMET = atan2(sumEy, sumEx)+3.1415927;
	metIPhi = L1CaloRegionDetId::N_PHI * physicalPhiMET / (2 * 3.1415927);
	physicalPhiHT = atan2(sumHy, sumHx)+3.1415927;
	mhtIPhi = L1CaloRegionDetId::N_PHI * physicalPhiHT / (2 * 3.1415927);
	//cout<<"metIPhi: "<< metIPhi <<"     mhtIPhi: "<<mhtIPhi<<endl;
	//MET, MHT, metPhi, mhtPhi, physicalPhiHT, physicalPhiMET, sumET,sumHT

	//cout<<"===makeSums:after for loop==="<<endl;
}







sumcalculator::sumcalculator(const edm::ParameterSet& pset) 
{
	// Initialize the ntuple builder
	edm::Service<TFileService> fs;
	tree = fs->make<TTree>("Ntuple", "Ntuple");
	tree->Branch("sumET", "std::vector<float>", &sumET_);
	tree->Branch("sumGenET", "std::vector<float>", &sumGenET_);
	tree->Branch("MET", "std::vector<float>", &MET_);
	tree->Branch("METPhi", "std::vector<float>", &metPhi_);
	tree->Branch("genMET", "std::vector<float>", &genMET_);
	tree->Branch("genMETPhi", "std::vector<float>", &genMETPhi_);
	tree->Branch("MHT", "std::vector<float>", &MHT_);
	tree->Branch("genMHT", "std::vector<float>", &genMHT_);
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
	for(unsigned int i = 0; i < L1CaloRegionDetId::N_PHI; i++) {
		sinPhi.push_back(sin(2. * 3.1415927 * i * 1.0 / L1CaloRegionDetId::N_PHI));
		cosPhi.push_back(cos(2. * 3.1415927 * i * 1.0 / L1CaloRegionDetId::N_PHI));
	}

}


void sumcalculator::analyze(const edm::Event& evt, const edm::EventSetup& es) {

	// Setup meta info
	run_ = evt.id().run();
	lumi_ = evt.id().luminosityBlock();
	event_ = evt.id().event();

	evt.getByLabel(scalerSrc_, lumiScalers);
	evt.getByLabel("rctProd", newRegions);
	evt.getByLabel(pvSrc_, puInfo);
	evt.getByLabel(vertexSrc_, vertices_r);
	evt.getByLabel(genSrc_, genParticles);

        evt.getByLabel("genMetCalo", genMETColl);
        float genMET = (*genMETColl)[0].pt(); 
        float genMETPhi = (*genMETColl)[0].phi(); 
        //cout<<"genMet: "<<genMET<<endl;
	//evt.getByLabel(tauSrc_, tauObjects);


	MET_.clear();
	metPhi_.clear();
	genMET_.clear();
	genMETPhi_.clear();
	MHT_.clear();
	genMHT_.clear();
	sumET_.clear();
	sumGenET_.clear();

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

	//cout<< "====Make Sums===="<<std::endl;
	makeSums();
	//cout<< "====Push Back===="<<std::endl;
	//cout<< "sumET: "<<sumET<<std::endl;
	//cout<< "MET: "<<MET<<std::endl;
	//cout<< "MET Phi: "<<physicalPhiMET<<std::endl;
	//cout<< "MHT: "<<MHT<<std::endl;
	//cout<< "MHT Phi: "<<physicalPhiHT<<std::endl;
	sumET_.push_back(sumET);
	MET_.push_back(MET);
	metPhi_.push_back(physicalPhiMET);
	//metPhi_.push_back(physicalPhiMET);
	MHT_.push_back(MHT);
	mhtPhi_.push_back(physicalPhiHT);
	sumGenET_.push_back(sumET);
	genMET_.push_back(genMET);
	genMETPhi_.push_back(genMETPhi);
	genMHT_.push_back(MHT);

	//cout<< "====Fill Tree===="<<std::endl;
	tree->Fill();
}

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(sumcalculator);
