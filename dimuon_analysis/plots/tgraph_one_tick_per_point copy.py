import ROOT
import numpy as np
import pandas as pd
import math

# Benchmark: dimuon analysis tutorial, reading 100 replicas of the dataset

# Cores used in the benchmark
# 2,4,8,16 are in a single node
# 32, 40, 48 cores are spanning 2,3,4 nodes respectively

cores = [2, 4, 8, 16, 32, 40, 48]
idealspeedup = [ core / cores[0] for core in cores]

# Best times with XRootD proxies on all `sg` machines
# caching on /local/scratch/ssd/vpadulano

xrdssdtimes = [4073.3, 2193.15, 1264.17, 869.67, 444.22, 342.15, 276.2]
xrdssdtimes2 = [6980.98, 3177.02, 1646.96, 974.62, 444.22, 352.49, 297.28]
xrdssdspeedup = [ 1. / (time / xrdssdtimes2[0]) for time in xrdssdtimes2 ]

# Best times with XRootD proxies on all `sg` machines
# caching on /htda/cache/vpadulan

xrdhddtimes = [4133.3, 2136.8, 1225.11, 849.08, 1864.79, 1252.24, 1013.45]
xrdhddtimes2 = [6980.98, 3429.12, 1729.7, 974.62, 1864.79, 1252.24, 1013.45]
xrdhddspeedup = [ 1. / (time / xrdhddtimes2[0]) for time in xrdhddtimes2 ]

# Best times reading files from EOS

eostimes = [6980.98, 3429.12, 1729.7, 974.62, 601.53, 490.11, 422.02]
eosspeedup = [ 1. / (time / eostimes[0]) for time in eostimes ]

c = ROOT.TCanvas("","",0,0,800,800)

numpoints = 7

eosgraph = ROOT.TGraph(numpoints)
for i in range(numpoints):
    eosgraph.SetPoint(i, cores[i], eosspeedup[i])

eosgraph.GetXaxis().SetLabelSize(0)
eosgraph.GetXaxis().SetTickLength(0.03)
eosgraph.GetYaxis().SetLabelSize(0)
eosgraph.GetYaxis().SetTickLength(0.03)
eosgraph.SetMarkerColor(ROOT.kRed)
eosgraph.SetMarkerStyle(20)
eosgraph.SetMarkerSize(1.2)
eosgraph.SetLineColorAlpha(ROOT.kRed,1)
eosgraph.SetLineWidth(2)
eosgraph.SetTitle("Dimuon Analysis - 210 GB dataset speedup ")
eosgraph.GetXaxis().SetTitle("Cores")
eosgraph.GetYaxis().SetTitle("Speedup")
eosgraph.GetYaxis().SetTitleOffset(1.2)
eosgraph.Draw("APL")

eosgraph.GetXaxis().SetRangeUser(0,50)
eosgraph.GetYaxis().SetRangeUser(0,25)

ymin = eosgraph.GetHistogram().GetMinimum()
ymax = eosgraph.GetHistogram().GetMaximum()
dy = ymax - ymin


xrdgraph = ROOT.TGraph(7)
for i in range(7): # only start plotting from 16 cores
    xrdgraph.SetPoint(i, cores[i], xrdssdspeedup[i])

xrdgraph.SetMarkerColor(30)
xrdgraph.SetMarkerStyle(23)
xrdgraph.SetMarkerSize(1.2)
xrdgraph.SetLineColorAlpha(30,1)
xrdgraph.SetLineWidth(2)
# xrdgraph.SetLineStyle(2)
xrdgraph.Draw("PL SAME")

xlabels = []
xticks = []
ylabels = []
yticks = []
separators = []

# xrdhddgraph = ROOT.TGraph(4)
# for i in range(4): # only start plotting from 16 cores
#     xrdhddgraph.SetPoint(i, cores[i+3], xrdhddspeedup[i+3])

# xrdhddgraph.SetMarkerColor(39)
# xrdhddgraph.SetMarkerStyle(24)
# xrdhddgraph.SetMarkerSize(1.2)
# xrdhddgraph.SetLineColorAlpha(39,1)
# xrdhddgraph.SetLineWidth(2)
# # xrdgraph.SetLineStyle(2)
# xrdhddgraph.Draw("PL SAME")

# Draw custom X axis points aligned with x values of TGraph287.28
for i in range(numpoints):
    x = eosgraph.GetPointX(i)
    t = ROOT.TLatex(x, ymin - 0.04 * dy, str(int(x)))
    t.SetTextSize(0.035)
    t.SetTextFont(42)
    t.SetTextAlign(21)
    t.Draw()
    xlabels.append(t)
    l = ROOT.TLine(x, ymin, x,ymin+0.02*dy)
    # Draw lines to separate node boundaries
    if i >= 3:
        sepline = ROOT.TLine(x, ymin, x,25)
        sepline.SetLineColorAlpha(16,0.3)
        sepline.SetLineStyle(9)
        sepline.SetLineWidth(1)
        sepline.Draw("SAME")
        separators.append(sepline)
    l.Draw()
    xticks.append(l)

graphlin = ROOT.TGraph()
for i in range(7):
    graphlin.SetPoint(i, cores[i], idealspeedup[i])
graphlin.SetLineStyle(2)
graphlin.SetLineColor(38)
graphlin.SetLineWidth(3)
graphlin.Draw("SAME")

# Draw custom Y axis points aligned with y values of TGraph
for i in range(numpoints):
    y = graphlin.GetPointY(i)
    t = ROOT.TLatex(-1.2, y, str(int(y)))
    t.SetTextSize(0.035)
    t.SetTextFont(42)
    t.SetTextAlign(22)
    t.Draw()
    ylabels.append(t)
    l = ROOT.TLine(y, ymin, y,ymin+0.02*dy)
    l.Draw()
    yticks.append(l)

legend = ROOT.TLegend(0.15,0.7,0.6,0.9)
legend.AddEntry(eosgraph, "Reading remote files")
legend.AddEntry(xrdgraph, "With XRootD caching (SSD)")
# legend.AddEntry(xrdhddgraph, "With XRootD caching (HDD)")
legend.AddEntry(graphlin, "Ideal speedup", "L")
legend.AddEntry(separators[0], "Physical Node", "L")

legend.Draw()

c.Draw()
c.SaveAs("dimuon_speedup_210GB.png")