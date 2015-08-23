// N. Smith, L. Dodd

#include <memory>
#include <vector>

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"

#include "FWCore/Framework/interface/ESHandle.h"
#include "CondFormats/RunInfo/interface/RunInfo.h"
#include "CondFormats/DataRecord/interface/RunSummaryRcd.h"

#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/L1CaloTrigger/interface/L1CaloCollections.h"
#include "DataFormats/L1CaloTrigger/interface/L1CaloRegion.h"
#include "DataFormats/Scalers/interface/LumiScalers.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "TTree.h"

class PUMcorrelation : public edm::EDAnalyzer {
  public:
    explicit PUMcorrelation(const edm::ParameterSet& pset);

  private:
    virtual void analyze(const edm::Event& evt, const edm::EventSetup& es);
    virtual void beginLuminosityBlock(const edm::LuminosityBlock&, const edm::EventSetup&);

    edm::EDGetTokenT<L1CaloRegionCollection> regionSource_;
    edm::EDGetTokenT<LumiScalersCollection> lumiScalerSource_;
    edm::EDGetTokenT<reco::VertexCollection> vertexSource_;

    // For when using CTP7
    bool checkFEDInLumis_;
    int FEDIdToCheck_;

    TTree * tree_;
    // branches
    int run_;
    int lumi_;
    int event_;
    int npvs_;
    float instlumi_;
    float fixedGridRhoAll_;
    float fixedGridRhoFastjetAllCalo_;
    float fixedGridRhoFastjetAll_;
    int nonZeroRegions_;

    bool lumiIsValid_{false};
};


PUMcorrelation::PUMcorrelation(const edm::ParameterSet& pset) :
  regionSource_(consumes<L1CaloRegionCollection>(pset.getParameter<edm::InputTag>("regionSource"))),
  lumiScalerSource_(consumes<LumiScalersCollection>(pset.getParameter<edm::InputTag>("lumiScalerSource"))),
  vertexSource_(consumes<reco::VertexCollection>(pset.getParameter<edm::InputTag>("vertexSource"))),
  checkFEDInLumis_(pset.getUntrackedParameter<bool>("checkFEDInLumis", false)),
  FEDIdToCheck_(pset.getUntrackedParameter<int>("FEDIdToCheck", 1350))
{
  edm::Service<TFileService> fs;

	tree_ = fs->make<TTree>("Ntuple", "Ntuple");
	tree_->Branch("run", &run_, "run/i");
	tree_->Branch("lumi", &lumi_, "lumi/i");
	tree_->Branch("event", &event_, "event/l");
	tree_->Branch("npvs", &npvs_, "npvs/i");
	tree_->Branch("instlumi", &instlumi_, "instlumi/F");
  tree_->Branch("fixedGridRhoAll", &fixedGridRhoAll_, "fixedGridRhoAll/F");
  tree_->Branch("fixedGridRhoFastjetAllCalo", &fixedGridRhoFastjetAllCalo_, "fixedGridRhoFastjetAllCalo/F");
  tree_->Branch("fixedGridRhoFastjetAll", &fixedGridRhoFastjetAll_, "fixedGridRhoFastjetAll/F");
  tree_->Branch("nonZeroRegions", &nonZeroRegions_, "nonZeroRegions/i");
}


void PUMcorrelation::analyze(const edm::Event& event, const edm::EventSetup& es)
{
  if ( ! lumiIsValid_ ) return;

	run_ = event.id().run();
	lumi_ = event.id().luminosityBlock();
	event_ = event.id().event();

  edm::Handle<reco::VertexCollection> vertexCollection;
  event.getByToken(vertexSource_, vertexCollection);
  npvs_ = vertexCollection->size();

  edm::Handle<LumiScalersCollection> lumiScalerCollection;
  event.getByToken(lumiScalerSource_, lumiScalerCollection);
	if ( lumiScalerCollection->size() > 0 ) {
		instlumi_ = lumiScalerCollection->begin()->instantLumi();
  } else {
    instlumi_ = -1.;
  }

  // Hardcoded :<
  edm::Handle<double> rhoHandle;
  event.getByLabel(edm::InputTag("fixedGridRhoAll"), rhoHandle);
  fixedGridRhoAll_ = *rhoHandle;
  event.getByLabel(edm::InputTag("fixedGridRhoFastjetAllCalo"), rhoHandle);
  fixedGridRhoFastjetAllCalo_ = *rhoHandle;
  event.getByLabel(edm::InputTag("fixedGridRhoFastjetAll"), rhoHandle);
  fixedGridRhoFastjetAll_ = *rhoHandle;

  edm::Handle<L1CaloRegionCollection> regionCollection;
  event.getByToken(regionSource_, regionCollection);
  nonZeroRegions_ = 0;
  for (const auto& region : *regionCollection) {
    if ( region.bx() == 0 && region.et() > 0 ) {
      nonZeroRegions_++;
    }
  }

  tree_->Fill();
}

void
PUMcorrelation::beginLuminosityBlock(const edm::LuminosityBlock& lumi, const edm::EventSetup& es)
{
  if ( checkFEDInLumis_ ) {
    edm::ESHandle<RunInfo> runInfoHandle;
    es.get<RunInfoRcd>().get(runInfoHandle);

    const std::vector<int> & fedsIn = runInfoHandle->m_fed_in;
    if ( std::find(begin(fedsIn), end(fedsIn), FEDIdToCheck_) == end(fedsIn) ) {
      lumiIsValid_ = false;
    } else {
      lumiIsValid_ = true;
    }
  } else {
    lumiIsValid_ = true;
  }
}

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(PUMcorrelation);
