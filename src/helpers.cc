#include "L1Trigger/PileUpTable/interface/helpers.h"
#include "DataFormats/L1CaloTrigger/interface/L1CaloRegion.h"
#include <cmath>
#include <math.h>

uint32_t getRegionNumber(uint32_t gctEta) {
  uint32_t region = 0xDEADBEEF;
  if(gctEta < 11) region = 10 - gctEta;  // - eta regions 0-10, 0-6 barrel/endcap, 7-10 forward
  else if(gctEta < 24) region = gctEta - 11; // + eta regions 0-12, 0-6 barrel/endcap, 7-12 forward
  else if (gctEta == 30) region = 11; // - eta region 11
  else if(gctEta == 31) region = 12;  // - eta region 23
  return region;
}

bool isNegativeEtaSide(uint32_t gctEta) {
  if(gctEta < 11 || gctEta > 29) return true;
  return false;
}

int deltaPhiWrapAtN(unsigned int N, int phi1, int phi2) {
  int difference = phi1 - phi2;
  if (std::abs(phi1 - phi2) == N-1) {
    difference = -difference/std::abs(difference);
  }
  return difference;
}

int deltaPhi(const L1CaloRegion& r1, const L1CaloRegion& r2) {
  return deltaPhiWrapAtN(18, r1.gctPhi(), r2.gctPhi());
}

double convertRegionPhi(int iPhi) {
  if (iPhi < 10)
    return 2. * M_PI * iPhi / 18.;
  if (iPhi < 18)
    return -M_PI + 2. * M_PI * (iPhi - 9) / 18.;
  return -9;
}

double convertRegionEta(uint32_t region) {
  const double rgnEtaValues[13] = {
     0.174, // HB and inner HE bins are 0.348 wide
     0.522,
     0.870,
     1.218,
     1.566,
     1.956, // Last two HE bins are 0.432 and 0.828 wide
     2.586,
     (2.98+3.33)/2., // HF bins are approximately 0.33 wide
     (3.33+3.68)/2.,
     (3.68+3.85)/2.,
     (3.85+4.20)/2.,
     (4.20+4.74)/2.,
     (4.74+5.21)/2.
  };
  if(region < 13) return rgnEtaValues[region];
  return -999;
}

double getRegionArea(uint32_t regionNumber) {
  switch (regionNumber) {
  case 0: return 0.348*0.348;
  case 1: return 0.348*0.348;
  case 2: return 0.348*0.348;
  case 3: return 0.348*0.348;
  case 4: return 0.348*0.348;
  case 5: return 0.432*0.348;
  case 6: return 0.828*0.348;
  case 7: return 0.33*0.348;
  case 8: return 0.33*0.348;
  case 9: return 0.33*0.348;
  case 10: return 0.33*0.348;
  case 11: return 0.33*0.348;
  case 12: return 0.33*0.348;
  }
  return 0;
}
