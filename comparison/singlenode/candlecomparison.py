"""
Draw a comparison between execution times for a single setup.
Creates TGraphs through RDataFrame from csv files and draws them on the same
canvas.
"""
import argparse
import ROOT

parser = argparse.ArgumentParser()
parser.add_argument("filenames", nargs="+", help="Path to the csv files")
parser.add_argument("-t", "--title", help="Title of the Plot")
parser.add_argument("-x", "--xtitle", help="Title of the X axis.")
parser.add_argument("-y", "--ytitle", help="Title of the Y axis.")
parser.add_argument("--xmin", help="Minimum value of the X axis.", type=int)
parser.add_argument("--xmax", help="Maximum value of the X axis.", type=int)
parser.add_argument(
    "--yrange",
    help="Zoom on this range of the Y axis.",
    type=int,
    nargs=2)
parser.add_argument("--width", help="Pixel width of the image", type=int)
parser.add_argument("--height", help="Pixel height of the image", type=int)
args = parser.parse_args()

# Retrieve command line arguments
filenames = args.filenames
gtitle = args.title if args.title else "Candle Plot Comparison"
xtitle = args.xtitle if args.xtitle else "Caching Mechanism"
ytitle = args.ytitle if args.ytitle else "Time [s]"
xmin = args.xmin if args.xmin else 0
xmax = args.xmax if args.xmax else 100
width = args.width if args.width else 1280
height = args.height if args.height else 720

# Retrieve file names
filesnoext = [filename.partition(".csv")[0] for filename in filenames]
print("Drawing candle plots from files {}".format(filenames))

# Create graphs
comparisoncolumn = "Time"
histos = [ROOT.RDF.MakeCsvDataFrame(filename)
          .Histo2D(("Stats", "Candle Plot", 1, 0, 1000, 100, xmin, xmax),
                   "rdfentry_", comparisoncolumn)
          .GetValue()
          for filename in filenames]

# Graphics
d = ROOT.TCanvas("d", "", width, height)
ROOT.gStyle.SetOptTitle(ROOT.kFALSE)
ROOT.gStyle.SetPalette(ROOT.kRainBow)

# Create THStack
hs = ROOT.THStack("hs", "Single Node Comparison")
for histo, name in zip(histos, filesnoext):
    histo.SetTitle(name)
    hs.Add(histo)

# Draw the histograms as candles.
# String option for drawing: "CANDLE(zhpawMmb)"
# p = 1 outliers
# a = 1 anchors
# w = 2 whiskers 1.5*iqr
# m = 3 median as circle
hs.Draw("CANDLE(00112030) PLC PFC")
hs.GetXaxis().SetLabelSize(0)
hs.GetXaxis().SetTickLength(0)
hs.GetYaxis().SetTitle("Time [s]")
d.BuildLegend(0.6, 0.7, 0.9, 0.9)

if args.yrange:
    hs.GetYaxis().SetRangeUser(*args.yrange)

d.Modified()
d.SaveAs("singlenode_candles.png")
