import argparse
import os
import PyRDF
import socket

# logger = PyRDF.create_logger("DEBUG")

import ROOT
ROOT.gROOT.SetBatch(True)

os.environ["XRD_PLUGIN"]="/lib64/libXrdClProxyPlugin.so"
os.environ["XROOT_PROXY"]="root://pcphsft112.cern.ch:1094//"

parser = argparse.ArgumentParser()
parser.add_argument(
    "cores",
    help="Number of cores to use for the analysis.",
    type=int)
args = parser.parse_args()

# The driver is started with the application in the standalone mode of Spark
hostname = socket.gethostname()
PyRDF.use("spark", conf={
    'npartitions': args.cores,
    'spark.master': f'spark://{hostname}:7077',
    'spark.app.name': 'dimuon-sft',
    'spark.executor.instances': 1,
    'spark.executor.cores': args.cores,
    'spark.max.cores': args.cores,
})

PyRDF.current_backend.sparkContext.addPyFile("PyRDF.zip")

def dimuonSpectrum(df):
    tfile = ROOT.TFile("dimuon_histogram.root", "RECREATE")
    print("Starting dimuon simplified")
    tbegin = ROOT.TStopwatch()

    # Book histogram of dimuon mass spectrum
    bins = 30000  # Number of bins in the histogram
    low = 0.25  # Lower edge of the histogram
    up = 300.0  # Upper edge of the histogram

    hists = []
    for var in ["nMuon", "Muon_pt", "Muon_eta", "Muon_phi", "Muon_mass", "Muon_charge"]:
        hist = df.Histo1D(ROOT.RDF.TH1DModel(var, var, bins, low, up), var)
        hists.append(hist)

    tbegin.Stop()
    begintime = round(tbegin.RealTime(), 3)

    # Draw histogram
    print("Starting event loop.")
    tevloop = ROOT.TStopwatch()
    for hist in hists:
        hist.Write()
    tevloop.Stop()
    evlooptime = round(tevloop.RealTime(), 3)
    print("Finished event loop.")

    with open("pyrdf_dimuon_simplified_analysistimes.csv", "a+") as f:
        f.write("{},{}".format(begintime, evlooptime))
        f.write("\n")


officialdataset = (
    "root://eospublic.cern.ch//eos/opendata/cms/derived-data/"
    "AOD2NanoAODOutreachTool/Run2012BC_DoubleMuParked_Muons.root")

filenames = [("root://eospublic.cern.ch/"
              "/eos/root-eos/benchmark/CMSOpenDataDimuon/"
              "Run2012BC_DoubleMuParked_Muons_{}.root").format(i)
             for i in range(1, 11)]

df = PyRDF.RDataFrame("Events", filenames)

for i in range(1,4):
    print("Iteration {}".format(i))
    t = ROOT.TStopwatch()
    dimuonSpectrum(df)
    t.Stop()
    realtime = round(t.RealTime(), 2)

    with open("pyrdf_dimuon_simplified_sft112_xrdcache_{}cores.csv"
              .format(args.cores), "a+") as f:
        f.write(str(realtime))
        f.write("\n")

