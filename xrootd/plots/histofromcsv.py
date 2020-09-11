"""
Create an histogram from a csv through RDataFrame csv data source.
Retrieve the median of the column data, draw it over the histogram and show it
in the stats box.
Tweak some graphics options.
"""
import argparse
import numpy
import ROOT

# Define command line arguments
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
parser.add_argument("--logx", help="Draw the X axis with a logarithmic scale.",
                    action="store_true")
parser.add_argument("--logy", help="Draw the Y axis with a logarithmic scale.",
                    action="store_true")
parser.add_argument("--width", help="Pixel width of the image", type=int)
parser.add_argument("--height", help="Pixel height of the image", type=int)
args = parser.parse_args()

# Create RDataFrame from .csv file
filename = args.filename
filenoext = filename.partition(".csv")[0]
hcolumn = args.column
print("Creating histogram from file {} and column {}".format(filename, hcolumn))
rdf = ROOT.RDF.MakeCsvDataFrame(filename)

# Extract median statistic to be drawn over histogram.
timearray = numpy.genfromtxt(filename, skip_header=True)
median = numpy.median(timearray)

# Decide Histo1D arguments
nbins = 100
xmin = args.xmin if args.xmin else numpy.min(timearray) - 1
xmax = args.xmax if args.xmax else numpy.quantile(timearray, .95)
hname = args.name if args.name else "Stats"
htitle = args.title if args.title else filenoext
print(
    "Histo1D Model: (name, title, nbins, xmin, xmax) = ({}, {}, {}, {}, {})"
    .format(hname, htitle, nbins, xmin, xmax))

width = args.width if args.width else 1280
height = args.height if args.height else 720
d = ROOT.TCanvas("d", "", width, height)
histo = rdf.Histo1D((hname, htitle, nbins, xmin, xmax), hcolumn)

# Graphics
xaxname = args.xtitle if args.xtitle else "X"
yaxname = args.ytitle if args.ytitle else "Y"
axtitlesize = 0.04
fillstyle = 1001  # Solid histogram fill area
hlinecolor = ROOT.kBlack
hfillcolor = ROOT.kAzure - 9

histo.GetXaxis().SetTitle(xaxname)
histo.GetXaxis().SetTitleSize(axtitlesize)
histo.GetYaxis().SetTitle(yaxname)
histo.GetYaxis().SetTitleSize(axtitlesize)
histo.SetFillStyle(fillstyle)
histo.SetLineColor(hlinecolor)
histo.SetFillColor(hfillcolor)
histo.Draw()
d.Update()

# Draw median over histogram
# TLine arguments : (x1, y1, x2, y2)
medianline = ROOT.TLine(median, 0, median, histo.GetMaximum())
medianline.SetLineWidth(2)
medianline.SetLineColor(ROOT.kRed)
medianline.Draw()

# Retrieve stats box and add median value
stats = d.GetPrimitive("stats")
stats.SetName("Stats")
histo.SetStats(0)  # Avoid redrawing histo default stats box
statslines = stats.GetListOfLines()
medianstat = ROOT.TLatex(0, 0, "Median = {}".format(median))
medianstat.SetTextFont(42)
medianstat.SetTextColor(ROOT.kRed)
medianstat.SetTextSize(0.025)
statslines.Add(medianstat)

# Optionally set logarithmic scales on axes
if args.logx:
    d.SetLogx()
if args.logy:
    d.SetLogy()

d.Modified()
d.SaveAs("{}.png".format(filenoext))
