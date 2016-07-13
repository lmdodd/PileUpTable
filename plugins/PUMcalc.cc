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
  //Rank 10 / RegionLSB 
  const unsigned int R10BINS = 2048;
  const float R10MIN = -0.5;
  const float R10MAX = 2047.5;
  //ETABINS is number of uct region eta bins
  const unsigned int ETABINS = 26;
  //PUMBINS moved to parameters
  //PUMNORMALIZE calculated from TotRegions/PUMBINS 
  //const unsigned int PUMBINS = 18;
  //const unsigned int PUMNORMALIZE = 26;
  //PUMNORAMLIZE is the number you divide the NonZeroRegions by to get 
  //the pumbin. e.g. if you have 396 regions and 18 pum bins, you divide
  //by 22 to get which pumbin the event should be categorized as.
  //26 eta* 18 Phi = 486 Total regions
  //For 18 pumbins this should be 26
  //For 39 pumbins this should be 12 
  const float PUMMIN = -0.5;
  const float TOTREGIONS = 486;
  //Defined later
  //const float PUMMAX = 17.5;
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
    unsigned int PUMBINS;
    unsigned int PUMNORMALIZE;

    bool lumiIsValid_{false};
    double regionLSB_;
};


PUMcalc::PUMcalc(const edm::ParameterSet& pset) :
  regionSource_(consumes<L1CaloRegionCollection>(pset.getParameter<edm::InputTag>("regionSource"))),
  bunchCrossingsToUse_(pset.getParameter<std::vector<int>>("bunchCrossingsToUse")),
  checkFEDInLumis_(pset.getUntrackedParameter<bool>("checkFEDInLumis", false)),
  FEDIdToCheck_(pset.getUntrackedParameter<int>("FEDIdToCheck", 1350)),
  PUMBINS(pset.getUntrackedParameter<int>("pumbins", 18)),
  regionLSB_(pset.getParameter<double>("regionLSB"))
{
  edm::Service<TFileService> fs;

  PUMNORMALIZE=TOTREGIONS/PUMBINS;

  regionsPUMEta_.resize(ETABINS);
  for (size_t ieta=0; ieta<ETABINS; ++ieta) {
    regionsPUMEta_[ieta] = fs->make<TH2F>(("regionsPUMEta"+std::to_string(ieta)).c_str(), "PUM Bin rank distribution;PU bin;Rank", PUMBINS, PUMMIN, PUMMIN+PUMBINS, R10BINS, R10MIN, R10MAX);
  }

  regionBxPopulation_ = fs->make<TH2F>("regionBxPopulation", "Event counts per region per bunch crossing;Region index (PUMBINS*eta+phi);BX index;Counts", TOTREGIONS, R10MIN, R10MIN+TOTREGIONS, 5, -2.5, 2.5);
  regionBxEtSum_ = fs->make<TH2F>("regionBxEtSum", "Et per region per bunch crossing;Region index (PUMBINS*eta+phi);BX index;Counts*et",TOTREGIONS, R10MIN, R10MIN+TOTREGIONS, 5, -2.5, 2.5);
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
    if(isNegativeEtaSide(region.gctEta())) etaBin = getRegionNumber(region.gctEta()) + (ETABINS / 2);
    else etaBin = getRegionNumber(region.gctEta());
    if(etaBin < ETABINS) {
      regionBxPopulation_->Fill(etaBin*PUMBINS+region.gctPhi(), region.bx());
      regionBxEtSum_->Fill(etaBin*PUMBINS+region.gctPhi(), region.bx(), region.et());
    }
  }
 
  for ( auto bx : bunchCrossingsToUse_ ) {
    for (const auto& region : *regionCollection) {
      size_t etaBin = 0xDEADBEEF;
      if(isNegativeEtaSide(region.gctEta())) etaBin = getRegionNumber(region.gctEta()) + (ETABINS / 2);
      else etaBin = getRegionNumber(region.gctEta());
      if(etaBin < ETABINS) {
	if ( region.bx() == bx ) {
	  assert( std::abs(bx) < 3 );
	  double regionET =  region.et() * regionLSB_;
	  regionsPUMEta_[etaBin]->Fill(nonzeroRegionsBX[bx+2]/PUMNORMALIZE, regionET);
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
