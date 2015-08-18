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
        'zerobias_run251883.root' : {
            'No Correction ZeroBias' : {
                'folderName' : 'DQMData/Run 251883/L1T/Run summary/L1TPUM/BX0',
                'LineColor' : ROOT.kBlue,
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

regionSubtraction_PU20_MC13TeV = [
        0.000000, 0.120605, 0.169256, 0.268826, 0.382774, 0.513016, 0.663822, 0.832437, 1.027508, 1.243615, 1.484510, 1.748505, 2.046062, 2.398011, 2.850694, 3.134921, 0.000000, 0.000000,
        0.000000, 0.156470, 0.206591, 0.316716, 0.437151, 0.575129, 0.724797, 0.900622, 1.100065, 1.319216, 1.566611, 1.840780, 2.146836, 2.512393, 2.978403, 3.746032, 0.000000, 0.000000,
        0.000000, 0.123418, 0.266302, 0.359626, 0.484167, 0.622231, 0.777349, 0.951710, 1.152564, 1.374389, 1.628914, 1.912047, 2.231072, 2.600804, 3.047708, 3.246032, 0.000000, 0.000000,
        0.000000, 0.073136, 0.119262, 0.170035, 0.220106, 0.275605, 0.345793, 0.421699, 0.516175, 0.624704, 0.753339, 0.897683, 1.068766, 1.261715, 1.510694, 1.773810, 0.000000, 0.000000,
        0.055556, 0.246835, 0.273910, 0.336138, 0.416017, 0.486257, 0.575602, 0.688235, 0.841946, 1.037108, 1.312716, 1.656287, 2.139884, 2.717933, 3.581944, 4.833333, 0.000000, 0.000000,
        0.027778, 0.081575, 0.159538, 0.185340, 0.203983, 0.233673, 0.261819, 0.298637, 0.346385, 0.404360, 0.478642, 0.565410, 0.688215, 0.843343, 1.077222, 1.757937, 0.000000, 0.000000,
        0.000000, 0.140999, 0.150780, 0.173510, 0.211846, 0.234709, 0.266815, 0.302040, 0.350794, 0.405643, 0.469773, 0.544242, 0.643746, 0.772390, 0.966111, 1.341270, 0.000000, 0.000000,
        0.027778, 0.073136, 0.168649, 0.194531, 0.217132, 0.257744, 0.288562, 0.330748, 0.380863, 0.433790, 0.506866, 0.593113, 0.698211, 0.848414, 1.000417, 1.559524, 0.000000, 0.000000,
        0.027778, 0.182138, 0.189746, 0.215618, 0.241512, 0.278904, 0.310158, 0.358551, 0.408175, 0.472616, 0.550445, 0.642227, 0.759521, 0.896945, 1.104861, 1.801587, 0.000000, 0.000000,
        0.055556, 0.146273, 0.191632, 0.227958, 0.274799, 0.314503, 0.360935, 0.407808, 0.466380, 0.537669, 0.622278, 0.738058, 0.858959, 1.020501, 1.268681, 1.182540, 0.000000, 0.000000,
        0.027778, 0.298875, 0.194157, 0.266737, 0.302445, 0.352081, 0.396646, 0.445615, 0.510057, 0.585290, 0.678849, 0.792132, 0.923268, 1.092671, 1.272917, 1.674603, 0.000000, 0.000000,
        0.027778, 0.196906, 0.215701, 0.272407, 0.314203, 0.350184, 0.403693, 0.451630, 0.513017, 0.591138, 0.684406, 0.794723, 0.934995, 1.096773, 1.263472, 2.682540, 0.000000, 0.000000,
        0.000000, 0.203586, 0.211865, 0.234317, 0.279873, 0.326339, 0.363821, 0.417158, 0.477276, 0.548621, 0.640194, 0.746714, 0.881186, 1.042592, 1.211389, 2.154762, 0.000000, 0.000000,
        0.000000, 0.176864, 0.175042, 0.210207, 0.240979, 0.280980, 0.319586, 0.361009, 0.415540, 0.478681, 0.556795, 0.650872, 0.764839, 0.917022, 1.078958, 1.361111, 0.000000, 0.000000,
        0.083333, 0.138186, 0.148255, 0.183218, 0.226484, 0.255919, 0.297690, 0.336035, 0.384665, 0.441222, 0.510402, 0.604469, 0.712385, 0.839121, 0.968333, 1.460317, 0.000000, 0.000000,
        0.000000, 0.118495, 0.143076, 0.176666, 0.196477, 0.232085, 0.263392, 0.302656, 0.341165, 0.396920, 0.460773, 0.541928, 0.640016, 0.757635, 0.937917, 0.928571, 0.000000, 0.000000,
        0.000000, 0.163502, 0.137706, 0.171678, 0.199074, 0.227707, 0.257758, 0.294587, 0.336764, 0.397252, 0.466851, 0.558507, 0.674198, 0.830031, 1.021111, 1.325397, 0.000000, 0.000000,
        0.000000, 0.207103, 0.280303, 0.339056, 0.406884, 0.482201, 0.571267, 0.680040, 0.830221, 1.028213, 1.286050, 1.642039, 2.097342, 2.676099, 3.580764, 4.214286, 0.000000, 0.000000,
        0.000000, 0.075246, 0.109896, 0.171037, 0.223973, 0.276169, 0.343961, 0.423382, 0.515281, 0.625262, 0.754821, 0.898535, 1.065229, 1.261645, 1.510694, 1.674603, 0.000000, 0.000000,
        0.116737, 0.241242, 0.361715, 0.486229, 0.621300, 0.777202, 0.951448, 1.153620, 1.373879, 1.629597, 1.911760, 2.235784, 2.591466, 3.051528, 3.539683, 0.000000, 0.000000, 0.000000,
        0.088608, 0.199431, 0.315091, 0.434705, 0.572647, 0.728147, 0.901087, 1.100828, 1.318835, 1.568081, 1.839141, 2.157059, 2.508234, 2.937361, 3.087302, 0.000000, 0.000000, 0.,
        0.111111, 0.103024, 0.169000, 0.268494, 0.380306, 0.512103, 0.664542, 0.835524, 1.027807, 1.242631, 1.484586, 1.748726, 2.050053, 2.398987, 2.804097, 2.888889, 0.000000, 0.000000]

regionSubtraction_PU20_MC13TeV = [2*x for x in regionSubtraction_PU20_MC13TeV]

ecallaserEtaRank = ROOT.TH2F('ecallaserEtaRank', 'ECal Recipe;RCT #eta;Region Rank;Counts', 22, -0.5, 21.5, 1024, -0.5, 1023.5)
rctlaserEtaRank = ROOT.TH2F('rctlaserEtaRank', 'RCT Full Laser Correction;RCT #eta;Region Rank;Counts', 22, -0.5, 21.5, 1024, -0.5, 1023.5)

pumVector = []
print '# eta pum_bin avg_rank'
for ieta in range(22) :
    canvas = ROOT.TCanvas()
    multi = ROOT.THStack('multiplot%02d' % ieta, ';PUM Bin;Average Region Rank')

    for plot in plots['regionsPUMEta%d' % ieta].values() :
        if plot.GetTitle() == 'RCT Laser ZeroBias' :
            for i in range(1024) :
                rctlaserEtaRank.SetBinContent(ieta, i, sum([plot.GetBinContent(pumbin, i) for pumbin in range(18)]))
        if plot.GetTitle() == 'ECal Laser ZeroBias' :
            for i in range(1024) :
                ecallaserEtaRank.SetBinContent(ieta, i, sum([plot.GetBinContent(pumbin, i) for pumbin in range(18)]))

        prof = plot.ProfileX()
        if plot.GetTitle() == 'RCT Laser ZeroBias' :
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

    mcTable = ROOT.TH1F('mcTable%d' % ieta, '13TeV PU20 MC', 18, -0.5, 17.5)
    mcTable.SetMarkerStyle(ROOT.kOpenCircle)
    mcTable.SetMarkerColor(ROOT.kOrange)
    for pumbin in range(18) :
        mcTable.SetBinContent(pumbin, regionSubtraction_PU20_MC13TeV[18*ieta+pumbin])
    multi.Add(mcTable, 'p')

    multi.Draw('nostack')
    legend = canvas.BuildLegend(0.2, 0.6, 0.6, 0.9)
    legend.SetHeader('RCT eta = %d' % ieta)
    canvas.Print('plots/PUMavgRankEta%02d_PUM.pdf' % ieta)
    canvas.Print('plots/PUMavgRankEta%02d_PUM.root' % ieta)

print 'regionSubtraction_DataDrivenPUM0_RCTFullEG_v1 = cms.vdouble(' + ', '.join(['%f' % v for v in pumVector]) + ')'

canvas = ROOT.TCanvas()
canvas.SetLogz(True)
canvas.SetRightMargin(.16)
ecallaserEtaRank.Draw('colz')
canvas.Print('plots/ecalLaserEtaRank2D.pdf')
rctlaserEtaRank.Draw('colz')
canvas.Print('plots/rctLaserEtaRank2D.pdf')
