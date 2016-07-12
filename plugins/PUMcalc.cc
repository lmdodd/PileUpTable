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

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "TTree.h"
#include "TH2F.h"

#include "L1Trigger/PileUpTable/interface/helpers.h"

// TODO: move to configuration?
namespace {
  const unsigned int R10BINS = 1024;
  const float R10MIN = -0.5;
  const float R10MAX = 1023.5;

  const unsigned int PUMETABINS = 26;
  const unsigned int PUMNORMALIZE = 26;

  const unsigned int PUMBINS = 18;
  const float PUMMIN = -0.5;
  const float PUMMAX = 17.5;
}

class PUMcalc : public edm::EDAnalyzer {
  public:
    explicit PUMcalc(const edm::ParameterSet& pset);

  private:
    virtual void analyze(const edm::Event& evt, const edm::EventSetup& es);
    virtual void beginLuminosityBlock(const edm::LuminosityBlock&, const edm::EventSetup&);

    edm::EDGetTokenT<L1CaloRegionCollection> regionSource_;
    std::vector<int> bunchCrossingsToUse_;
    std::vector<TH2F*> regionsPUMEta_;
    TH2F* regionBxPopulation_;
    TH2F* regionBxEtSum_;
    bool checkFEDInLumis_;
    int FEDIdToCheck_;


    bool lumiIsValid_{false};
};


PUMcalc::PUMcalc(const edm::ParameterSet& pset) :
  regionSource_(consumes<L1CaloRegionCollection>(pset.getParameter<edm::InputTag>("regionSource"))),
  bunchCrossingsToUse_(pset.getParameter<std::vector<int>>("bunchCrossingsToUse")),
  checkFEDInLumis_(pset.getUntrackedParameter<bool>("checkFEDInLumis", false)),
  FEDIdToCheck_(pset.getUntrackedParameter<int>("FEDIdToCheck", 1350))
{
  edm::Service<TFileService> fs;

  regionsPUMEta_.resize(PUMETABINS);
  for (size_t ieta=0; ieta<PUMETABINS; ++ieta) {
    regionsPUMEta_[ieta] = fs->make<TH2F>(("regionsPUMEta"+std::to_string(ieta)).c_str(), "PUM Bin rank distribution;PU bin;Rank", PUMBINS, PUMMIN, PUMMAX, R10BINS, R10MIN, R10MAX);
  }

  regionBxPopulation_ = fs->make<TH2F>("regionBxPopulation", "Event counts per region per bunch crossing;Region index (18*eta+phi);BX index;Counts", 396, -0.5, 395.5, 5, -2.5, 2.5);
  regionBxEtSum_ = fs->make<TH2F>("regionBxEtSum", "Et per region per bunch crossing;Region index (18*eta+phi);BX index;Counts*et", 396, -0.5, 395.5, 5, -2.5, 2.5);
}


void PUMcalc::analyze(const edm::Event& event, const edm::EventSetup& es)
{
  if ( ! lumiIsValid_ ) return;

  edm::Handle<L1CaloRegionCollection> regionCollection;
  event.getByToken(regionSource_, regionCollection);

  std::array<int, 5> nonzeroRegionsBX;
  nonzeroRegionsBX.fill(0);
  for (const auto& region : *regionCollection) {
    if ( region.et() > 0 ) {
      assert( std::abs(region.bx()) < 3 );
      nonzeroRegionsBX[region.bx()+2]++;
    }
    size_t etaBin = 0xDEADBEEF;
    if(isNegativeEtaSide(region.gctEta())) etaBin = getRegionNumber(region.gctEta()) + (PUMETABINS / 2);
    else etaBin = getRegionNumber(region.gctEta());
    if(etaBin < PUMETABINS) {
      regionBxPopulation_->Fill(etaBin*18+region.gctPhi(), region.bx());
      regionBxEtSum_->Fill(etaBin*18+region.gctPhi(), region.bx(), region.et());
    }
  }
 
  for ( auto bx : bunchCrossingsToUse_ ) {
    for (const auto& region : *regionCollection) {
      size_t etaBin = 0xDEADBEEF;
      if(isNegativeEtaSide(region.gctEta())) etaBin = getRegionNumber(region.gctEta()) + (PUMETABINS / 2);
      else etaBin = getRegionNumber(region.gctEta());
      if(etaBin < PUMETABINS) {
	if ( region.bx() == bx ) {
	  assert( std::abs(bx) < 3 );
	  regionsPUMEta_[etaBin]->Fill(nonzeroRegionsBX[bx+2]/PUMNORMALIZE, region.et());
	}
      }
    }
  }
}

void
PUMcalc::beginLuminosityBlock(const edm::LuminosityBlock& lumi, const edm::EventSetup& es)
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
DEFINE_FWK_MODULE(PUMcalc);
