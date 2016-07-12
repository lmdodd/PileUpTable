/*
 * =====================================================================================
 *
 *       Filename:  Helpers.h
 *
 *    Description:  Common UCT functions.
 *
 *         Author:  M. Cepeda, S. Dasu, E. Friis
 *        Company:  UW Madison
 *
 * =====================================================================================
 */

#include <stdint.h>

#ifndef HELPERS_W9QK6HND
#define HELPERS_W9QK6HND

class L1CaloRegion;

// Compute the difference in phi between two towers, wrapping at phi = N
int deltaPhiWrapAtN(unsigned int N, int phi1, int phi2);

int deltaPhi(const L1CaloRegion& r1, const L1CaloRegion& r2);

// Convert a region index into physical phi (at center of region)
double convertRegionPhi(int iPhi);

// Convert a region index into physical eta (at center of region)
double convertRegionEta(uint32_t regionNumber);

// Get the effective area of a region in a given eta slice.
double getRegionArea(uint32_t regionNumber);

// Get region number

uint32_t getRegionNumber(uint32_t gctEta);

// Get eta sign

bool isNegativeEtaSide(uint32_t gctEta);

#endif /* end of include guard: HELPERS_W9QK6HND */
