"""
Create an histogram from a csv through RDataFrame csv data source.
Also tweak some graphics options.
"""
import argparse
import numpy
import ROOT

parser = argparse.ArgumentParser()
parser.add_argument("filename", help="Path to the csv file.")
parser.add_argument(
    "column",
    help="The RDataFrame column from which the histogram will be created.")
parser.add_argument("-n", "--name", help="Name of the histogram.")
parser.add_argument("-t", "--title", help="Title of the histogram.")
parser.add_argument("-x", "--xtitle", help="Title of the X axis.")
parser.add_argument("-y", "--ytitle", help="Title of the Y axis.")
parser.add_argument("--xmin", help="Minimum value of the X axis.", type=int)
parser.add_argument("--xmax", help="Maximum value of the X axis.", type=int)
args = parser.parse_args()


filename = args.filename
filenoext = filename.partition(".csv")[0]
hcolumn = args.column
print("Creating histogram from file {} and column {}".format(filename, hcolumn))
MakeCsvDataFrame = ROOT.RDF.MakeCsvDataFrame
rdf = MakeCsvDataFrame(filename)

timearray = numpy.genfromtxt(filename, skip_header=True)
median = numpy.median(timearray)

nbins = 100
xmin = args.xmin if args.xmin else numpy.min(timearray) - 1
xmax = args.xmax if args.xmax else numpy.quantile(timearray, .95)
print("xmin {}, xmax {}".format(xmin, xmax))
hname = args.name if args.name else "Name"
htitle = args.title if args.title else filenoext
print("Name: {}, Title: {}".format(hname, htitle))

d = ROOT.TCanvas("d", "", 800, 700)
histo = rdf.Histo1D((hname, htitle, nbins, xmin, xmax), hcolumn)


xaxName = args.xtitle if args.xtitle else "X"
yaxName = args.ytitle if args.ytitle else "Y"
axSize = 0.04
hlinecolor = ROOT.kBlack
hfillcolor = ROOT.kAzure - 9

ROOT.gStyle.SetOptStat("nemr")
histo.GetXaxis().SetTitle(xaxName)
histo.GetXaxis().SetTitleSize(0.04)
histo.GetYaxis().SetTitle(yaxName)
histo.GetYaxis().SetTitleSize(0.04)
histo.SetFillStyle(1001)
histo.SetLineColor(hlinecolor)
histo.SetFillColor(hfillcolor)
histo.Draw()
d.Update()

medianline = ROOT.TLine(median, 0, median, histo.GetMaximum())
medianline.SetLineWidth(2)
medianline.SetLineColor(ROOT.kRed)
medianline.Draw()

stats = d.GetPrimitive("stats")
stats.SetName("Stats")
histo.SetStats(0)
statslines = stats.GetListOfLines()
medianstat = ROOT.TLatex(0, 0, "Median = {}".format(median))
medianstat.SetTextFont(42)
medianstat.SetTextColor(ROOT.kRed)
medianstat.SetTextSize(0.025)
statslines.Add(medianstat)


d.Modified()
d.SaveAs("{}.png".format(filenoext))
