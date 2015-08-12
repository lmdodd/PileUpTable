#!/usr/bin/env python
import sys
import glob
import ROOT
if not sys.ps1 :
    ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptDate(0)

tree = ROOT.TChain('PUMcorrelation/Ntuple')
#for f in glob.glob('/hdfs/store/user/ncsmith/PUMstudy-PUMcorrelation_Run2015B_ECalTPLaserCorrection/*.root') :
#    bettername = f.replace('/hdfs', 'root://cmsxrootd.hep.wisc.edu/')
#    tree.Add(bettername)
tree.Add('correlation.root')

nonzeroVsRho = ROOT.TH2F('nonzeroVsRho', 'Nonzero Regions vs. Rho;# Regions > 0;fixedGridRhoAll;Counts', 396, -.5, 395.5, 250, 0., 50.)
tree.Draw('fixedGridRhoAll : nonZeroRegions >> nonzeroVsRho', '', 'goff')

nonzeroVsCaloRho = ROOT.TH2F('nonzeroVsCaloRho', 'Nonzero Regions vs. Calo Rho;# Regions > 0;fixedGridRhoFastjetAllCalo;Counts', 396, -.5, 395.5, 250, 0., 50.)
tree.Draw('fixedGridRhoAll : nonZeroRegions >> nonzeroVsCaloRho', '', 'goff')

nonzeroVsPV = ROOT.TH2F('nonzeroVsPV', 'Nonzero Regions vs. Primary Vertices;# Regions > 0;# Primary Vertices;Counts', 396, -.5, 395.5, 50, 0., 50.)
tree.Draw('npvs : nonZeroRegions >> nonzeroVsPV', '', 'goff')

canvas = ROOT.TCanvas()
canvas.SetRightMargin(.16)
canvas.SetLogz(True)

nonzeroVsRho.Draw('colz')
canvas.Print('plots/nonzeroRegionsVsRho.pdf')
canvas.Print('plots/nonzeroRegionsVsRho.root')

nonzeroVsCaloRho.Draw('colz')
canvas.Print('plots/nonzeroRegionsVsCaloRho.pdf')
canvas.Print('plots/nonzeroRegionsVsCaloRho.root')

nonzeroVsPV.Draw('colz')
canvas.Print('plots/nonzeroRegionsVsPV.pdf')
canvas.Print('plots/nonzeroRegionsVsPV.root')
