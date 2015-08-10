#!/usr/bin/env python
import ROOT
ROOT.gROOT.SetBatch(True)
import sys
from collections import OrderedDict

ROOT.gStyle.SetOptDate(0)

attributes = ['LineColor', 'LineStyle', 'LineWidth', 'MarkerColor', 'MarkerStyle', 'MarkerSize']

plotFolders = {
        'pumtable_ecallaser.root' : {
            'ECal Laser ZeroBias' : {
                'folderName' : 'PUMcalcCentralBX',
                'LineColor' : ROOT.kBlack,
                'LineWidth' : 2,
            },
        },
        'pumtable_rctlaser.root' : {
            'RCT Laser ZeroBias' : {
                'folderName' : 'PUMcalcCentralBX',
                'LineColor' : ROOT.kGray,
                'LineWidth' : 2,
            },
        },
    }

plots = {}
for fileName, folders in plotFolders.iteritems() :
    dqmFile = ROOT.TFile.Open(fileName)
    for labelName, info in folders.iteritems() :
        folder = dqmFile.Get(info['folderName'])
        folderPlots = (k.ReadObj() for k in folder.GetListOfKeys())
        for plot in folderPlots :
            if not plot.GetName() in plots :
                plots[plot.GetName()] = OrderedDict()
            newPlot = plot.Clone(plot.GetName()+labelName.replace(' ','_'))
            newPlot.SetTitle(labelName)
            for attr, value in info.iteritems() :
                if attr is 'folderName' :
                    continue
                if hasattr(newPlot, 'Set'+attr) :
                    getattr(newPlot, 'Set'+attr)(value)
            plots[plot.GetName()][labelName] = newPlot
            newPlot.SetDirectory(0)

etaPads = []
pumVector = []
print '# eta pum_bin avg_rank'
for ieta in range(22) :
    canvas = ROOT.TCanvas()
    multi = ROOT.THStack('multiplot%02d' % ieta, ';PUM Bin;Average Region Rank')

    for plot in plots['regionsPUMEta%d' % ieta].values() :
        prof = plot.ProfileX()
        if plot.GetTitle() == 'ECal Laser ZeroBias' :
            prevpum = 0.
            for pumbin in range(prof.GetNbinsX()) :
                pumval = prof.GetBinContent(pumbin+1)
                if pumval == 0. :
                    pumval = prevpum
                print '%d %d %f' % (ieta, pumbin, pumval)
                pumVector.append(pumval/2.)
                prevpum = pumval
        for attr in attributes :
            getattr(prof, 'Set'+attr)(getattr(plot, 'Get'+attr)())
        multi.Add(prof, 'ep')

    multi.Draw('nostack')
    legend = canvas.BuildLegend(0.2, 0.6, 0.6, 0.9)
    legend.SetHeader('RCT eta = %d' % ieta)
    canvas.Print('plots/PUMavgRankEta%02d_PUM.pdf' % ieta)
    canvas.Print('plots/PUMavgRankEta%02d_PUM.root' % ieta)
    ROOT.SetOwnership(multi, False)
    etaPads.append(canvas)

print 'regionSubtraction_DataDrivenPUM0vX = cms.vdouble(' + ', '.join(['%f' % v for v in pumVector]) + ')'

