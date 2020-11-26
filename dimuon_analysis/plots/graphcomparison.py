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
gtitle = args.title if args.title else "Graph Comparison"
xtitle = args.xtitle if args.xtitle else "Run"
ytitle = args.ytitle if args.ytitle else "Time [s]"
xmin = args.xmin if args.xmin else 0
xmax = args.xmax if args.xmax else 100
width = args.width if args.width else 1280
height = args.height if args.height else 720

# Retrieve file names
filesnoext = [filename.partition(".csv")[0] for filename in filenames]
print("Drawing graph comparison from files {}".format(filenames))

# Create graphs
comparisoncolumn = "Time"
graphs = [ROOT.RDF.MakeCsvDataFrame(filename)
          .Graph("rdfentry_", comparisoncolumn)
          .GetValue()
          for filename in filenames]

# Graphics
d = ROOT.TCanvas("d", "", width, height)
ROOT.gStyle.SetOptTitle(ROOT.kFALSE)
ROOT.gStyle.SetPalette(ROOT.kSolar)

# Create MultiGraph
mg = ROOT.TMultiGraph()
for graph, name in zip(graphs, filesnoext):
    graph.SetLineWidth(3)
    graph.SetTitle(name)
    mg.Add(graph, "L")

mg.SetTitle("{};{};{}".format(gtitle, xtitle, ytitle))
mg.Draw("A PLC PMC")

if args.yrange:
    mg.GetYaxis().SetRangeUser(*args.yrange)
d.BuildLegend()

d.Modified()
d.SaveAs("pyrdf_smartscheduler_graphs.png")
