#!/usr/bin/env python
import os 
import errno 
import ROOT
ROOT.gROOT.SetBatch(True)
from sys import argv
import sys
from collections import OrderedDict

if len(argv) < 3:
   print 'Usage:python table.py pumbins RunNumber'
   exit()

pumbinStr = argv[1]
dirname = "plots"+pumbinStr
pbs = int(sys.argv[1])
RunNumber = argv[2]

try:
    os.mkdir(dirname)
except OSError as exc:
    if exc.errno != errno.EEXIST:
        raise exc
    pass

text_file = open("PUMLut-"+pumbinStr+".txt","w")

ROOT.gStyle.SetOptDate(0)

attributes = ['LineColor', 'LineStyle', 'LineWidth', 'MarkerColor', 'MarkerStyle', 'MarkerSize']


plotFolders = {
        '/data/ldodd/UCTPUMTable-'+RunNumber+'-'+pumbinStr+'.root' : {
            'Run 2016C ZeroBias BX0' : {
                'folderName' : 'PUMcalcCentralBX',
                'LineColor' : ROOT.kPink-3,
                'LineStyle' : ROOT.kDashed,
                'LineWidth' : 4,
            },
   }
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


regionSubtraction_PU40_MC13TeV = [
        0.000000, 0.000000, 0.000000, 0.000000, 0.444444, 0.551170, 0.770085, 0.958352, 1.214790, 1.486655, 1.801059, 2.146229, 2.522583, 2.944799, 3.429136, 3.984393, 4.673410, 6.388889,
        0.000000, 0.000000, 0.000000, 0.000000, 0.319444, 0.548246, 0.810256, 0.977690, 1.229211, 1.510501, 1.826860, 2.178931, 2.562520, 2.993610, 3.489558, 4.060866, 4.757649, 5.527778,
        0.000000, 0.000000, 0.000000, 0.000000, 0.513889, 0.618421, 0.801496, 1.010128, 1.248957, 1.524992, 1.843374, 2.196967, 2.585665, 3.024237, 3.525665, 4.104405, 4.837409, 5.277778,
        0.000000, 0.000000, 0.000000, 0.000000, 0.138889, 0.178363, 0.328846, 0.438023, 0.537074, 0.655743, 0.818238, 0.997956, 1.198403, 1.428185, 1.693293, 1.998691, 2.428744, 2.861111,
        0.000000, 0.000000, 0.000000, 0.000000, 0.222222, 0.355263, 0.568803, 0.681711, 0.776114, 0.999194, 1.286749, 1.690190, 2.228222, 2.944096, 3.893814, 5.151409, 7.084399, 8.500000,
        0.000000, 0.000000, 0.000000, 0.000000, 0.347222, 0.260234, 0.282479, 0.305702, 0.330235, 0.386729, 0.472834, 0.574252, 0.713821, 0.883901, 1.117625, 1.419786, 1.887530, 2.583333,
        0.000000, 0.000000, 0.000000, 0.000000, 0.333333, 0.181287, 0.294444, 0.311500, 0.324732, 0.380449, 0.447851, 0.537887, 0.643667, 0.770106, 0.932555, 1.137137, 1.425775, 1.138889,
        0.000000, 0.000000, 0.000000, 0.000000, 0.069444, 0.144737, 0.329701, 0.345149, 0.361473, 0.428805, 0.500501, 0.595122, 0.709161, 0.849070, 1.019010, 1.234842, 1.563255, 3.944444,
        0.000000, 0.000000, 0.000000, 0.000000, 0.083333, 0.195906, 0.232692, 0.309886, 0.383756, 0.439078, 0.515435, 0.615713, 0.735333, 0.879855, 1.062850, 1.299136, 1.575533, 1.861111,
        0.000000, 0.000000, 0.000000, 0.000000, 0.222222, 0.181287, 0.245085, 0.393035, 0.422420, 0.496332, 0.583994, 0.694272, 0.829494, 0.990583, 1.194619, 1.450821, 1.804499, 2.361111,
        0.000000, 0.000000, 0.000000, 0.000000, 0.388889, 0.435673, 0.398077, 0.391201, 0.464790, 0.536569, 0.632543, 0.749761, 0.889213, 1.059990, 1.267241, 1.540288, 1.857136, 2.194444,
        0.000000, 0.000000, 0.000000, 0.000000, 0.125000, 0.576023, 0.420513, 0.396154, 0.485091, 0.546055, 0.641076, 0.754781, 0.897755, 1.070265, 1.278160, 1.532439, 1.927529, 1.805556,
        0.000000, 0.000000, 0.000000, 0.000000, 0.694444, 0.235380, 0.311111, 0.368633, 0.424446, 0.499583, 0.595857, 0.712276, 0.844093, 1.011457, 1.216950, 1.472430, 1.853009, 1.722222,
        0.000000, 0.000000, 0.000000, 0.000000, 0.166667, 0.336257, 0.301923, 0.313005, 0.387602, 0.441673, 0.524899, 0.625752, 0.744597, 0.888570, 1.073132, 1.318219, 1.614533, 1.333333,
        0.000000, 0.000000, 0.000000, 0.000000, 0.111111, 0.368421, 0.269231, 0.302253, 0.380310, 0.436402, 0.508579, 0.607197, 0.718574, 0.857328, 1.033980, 1.245847, 1.534823, 1.972222,
        0.000000, 0.000000, 0.000000, 0.000000, 0.027778, 0.228070, 0.195085, 0.278585, 0.322639, 0.374968, 0.446104, 0.529719, 0.631725, 0.758136, 0.916622, 1.111448, 1.417572, 2.277778,
        0.000000, 0.000000, 0.000000, 0.000000, 0.041667, 0.157895, 0.186752, 0.254513, 0.320827, 0.378098, 0.463270, 0.570900, 0.696241, 0.871445, 1.097610, 1.396127, 1.857488, 2.750000,
        0.000000, 0.000000, 0.000000, 0.000000, 0.138889, 0.612573, 0.624573, 0.634669, 0.790229, 0.989867, 1.282201, 1.672201, 2.205610, 2.922829, 3.850628, 5.104290, 6.823571, 10.972222,
        0.000000, 0.000000, 0.000000, 0.000000, 0.194444, 0.345029, 0.353846, 0.411016, 0.509851, 0.661643, 0.814750, 0.995329, 1.199998, 1.431079, 1.694189, 2.000995, 2.378925, 3.111111,
        0.000000, 0.000000, 0.000000, 0.000000, 0.541667, 0.573099, 0.766453, 0.977836, 1.239705, 1.530437, 1.840524, 2.197025, 2.585155, 3.027299, 3.525292, 4.112540, 4.873339, 5.972222,
        0.000000, 0.000000, 0.000000, 0.000000, 0.486111, 0.513158, 0.721581, 0.976956, 1.225950, 1.510261, 1.824951, 2.179360, 2.561912, 2.995865, 3.485821, 4.053826, 4.729921, 5.805556,
        0.000000, 0.000000, 0.000000, 0.000000, 0.319444, 0.564327, 0.694872, 0.950903, 1.201596, 1.488093, 1.801121, 2.145727, 2.523690, 2.946160, 3.422785, 3.963287, 4.633907, 5.972222
    ]

#want energy above, not rank
#regionSubtraction_PU40_MC13TeV = [2*x for x in regionSubtraction_PU40_MC13TeV]




pumVector = []
print '# eta pum_bin avg_rank'
for ieta in range(26) :
    canvas = ROOT.TCanvas()
    multi = ROOT.THStack('multiplot%02d' % ieta, ';PUM Bin;Average Region Et [GeV]')

    profiles = []
    tablePlot = None
    for plot in plots['regionsPUMEta%d' % ieta].values() :
        prof = plot.ProfileX("_pfx", 1, -1, "i")
        for attr in attributes :
            getattr(prof, 'Set'+attr)(getattr(plot, 'Get'+attr)())
        multi.Add(prof, 'ep')
        profiles.append(prof)
        if '2016C' in plot.GetTitle() :
            if tablePlot :
                tablePlot.Add(plot)
            else :
                tablePlot = plot.Clone('tablePlot')

    tableProf = tablePlot.ProfileX("_pfx", 1, -1, "i")
    prevpum = 0.
    for pumbin in range(tableProf.GetNbinsX()) :
        pumval = tableProf.GetBinContent(pumbin+1)
        if pumval == 0. :
            pumval = prevpum
        #print '%d %f' % (ieta*pbs+pumbin, pumval)
        pumVector.append(pumval)
        prevpum = pumval

    if pbs==18: 
       mcTable = ROOT.TH1F('mcTable%d' % ieta, '13TeV PU40 MC', 18, -0.5, 17.5)
       mcTable.SetMarkerStyle(ROOT.kOpenCircle)
       mcTable.SetMarkerColor(ROOT.kOrange)
       mcTable.SetLineColor(ROOT.kOrange)
       if ieta==0 or ieta==1 or ieta==24 or ieta==25:
          for pumbin in range(18) :
              mcTable.SetBinContent(pumbin+1, 0)
              mcTable.SetBinError(pumbin+1, 0.)
       else: 
          print 'in else'
          ietap = ieta -2
          for pumbin in range(18) :
              mcTable.SetBinContent(pumbin+1, regionSubtraction_PU40_MC13TeV[18*ietap+pumbin])
              mcTable.SetBinError(pumbin+1, 0.5)
       multi.Add(mcTable, 'ep')

    multi.Draw('nostack')
    legend = ROOT.TLegend(0.2, 0.6, 0.6, 0.9)
    legend.SetHeader('RCT eta = %d' % ieta)
    for prof in profiles :
        legend.AddEntry(prof, '', 'le')
    if pbs==18: 
       legend.AddEntry(mcTable, '', 'pf')
    legend.Draw()
    canvas.Print('plots'+pumbinStr+'/PUMavgRankEta%02d_PUM.pdf' % ieta)
    canvas.Print('plots'+pumbinStr+'/PUMavgRankEta%02d_PUM.root' % ieta)

#old table
#print 'regionSubtraction_DataDrivenPUM0_Run2016C_v1 = cms.vdouble([' + ', '.join(['%4.2f' % v for v in pumVector]) + '])'

for pumbin in range(0,pbs):
    pumVectorPos = []
    pumVectorNeg = []
    for ieta in range(0,26):
        if ieta>12: 
           pumVectorPos.insert(ieta-13,pumVector[ieta*pbs+pumbin])
        else: 
   	   pumVectorNeg.insert(ieta,pumVector[ieta*pbs+pumbin])
    #print 'pumLUT%02.f' % pumbin + 'n=  cms.vdouble(' + ', '.join(['%4.2f' % v for v in pumVectorNeg]) + '),'
    #print 'pumLUT%02.f' % pumbin + 'p=  cms.vdouble(' + ', '.join(['%4.2f' % v for v in pumVectorPos]) + '),'
    text_file.write('pumLUT%02.f' % pumbin + 'n=  cms.vdouble(' + ', '.join(['%4.2f' % v for v in pumVectorNeg]) + '), \n')
    if pumbin!=pbs-1: 
       text_file.write('pumLUT%02.f' % pumbin + 'p=  cms.vdouble(' + ', '.join(['%4.2f' % v for v in pumVectorPos]) + '), \n')
    else:
       text_file.write('pumLUT%02.f' % pumbin + 'p=  cms.vdouble(' + ', '.join(['%4.2f' % v for v in pumVectorPos]) + ')')

text_file.close()
    
