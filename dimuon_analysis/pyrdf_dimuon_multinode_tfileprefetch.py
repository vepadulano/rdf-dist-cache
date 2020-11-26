import ROOT
import PyRDF
import argparse
import os
import sys
sys.path.insert(0, os.getcwd()+"/PyRDF")


ROOT.gROOT.SetBatch(True)

parser = argparse.ArgumentParser()
parser.add_argument(
    "npartitions",
    help="Number of partitions of the dataset.",
    type=int)
args = parser.parse_args()

PyRDF.use("spark", conf={
    'npartitions': args.npartitions,
    'use_tfileprefetch': True,
    #    'reuse_parallel_collection': True,
    'spark.master': 'spark://sg03:7077',
    'spark.app.name': 'PyRDF-kit',
    'spark.files': 'PyRDF.zip',
})

PyRDF.current_backend.sparkContext.addPyFile("PyRDF.zip")


def dimuonSpectrum(df):
    print("Starting dimuon analysis")
    tbegin = ROOT.TStopwatch()

    # Select events with exactly two muons
    df_2mu = df.Filter("nMuon == 2", "Events with exactly two muons")

    # Select events with two muons of opposite charge
    df_os = df_2mu.Filter(
        "Muon_charge[0] != Muon_charge[1]", "Muons with opposite charge")

    # Compute invariant mass of the dimuon system
    df_mass = df_os.Define(
        "Dimuon_mass",
        "ROOT::VecOps::InvariantMass(Muon_pt, Muon_eta, Muon_phi, Muon_mass)")

    # Book histogram of dimuon mass spectrum
    bins = 30000  # Number of bins in the histogram
    low = 0.25  # Lower edge of the histogram
    up = 300.0  # Upper edge of the histogram

    hist = df_mass.Histo1D(ROOT.RDF.TH1DModel(
        "", "", bins, low, up), "Dimuon_mass")

    # Create canvas for plotting
    ROOT.gStyle.SetOptStat(0)
    ROOT.gStyle.SetTextFont(42)
    c = ROOT.TCanvas("c", "", 800, 700)
    c.SetLogx()
    c.SetLogy()

    tbegin.Stop()
    begintime = round(tbegin.RealTime(), 3)

    # Draw histogram
    print("Starting event loop.")
    tevloop = ROOT.TStopwatch()
    hist.GetXaxis().SetTitle("m_{#mu#mu} (GeV)")
    tevloop.Stop()
    evlooptime = round(tevloop.RealTime(), 3)
    print("Finished event loop.")
    tpost = ROOT.TStopwatch()
    hist.GetXaxis().SetTitleSize(0.04)
    hist.GetYaxis().SetTitle("N_{Events}")
    hist.GetYaxis().SetTitleSize(0.04)
    hist.SetStats(False)
    hist.Draw()

    # Draw labels
    label = ROOT.TLatex()
    label.SetTextAlign(22)
    label.DrawLatex(0.55, 3.0e4, "#eta")
    label.DrawLatex(0.77, 7.0e4, "#rho,#omega")
    label.DrawLatex(1.20, 4.0e4, "#phi")
    label.DrawLatex(4.40, 1.0e5, "J/#psi")
    label.DrawLatex(4.60, 1.0e4, "#psi'")
    label.DrawLatex(12.0, 2.0e4, "Y(1,2,3S)")
    label.DrawLatex(91.0, 1.5e4, "Z")
    label.SetNDC(True)
    label.SetTextAlign(11)
    label.SetTextSize(0.04)
    label.DrawLatex(0.10, 0.92, "#bf{CMS Open Data}")
    label.SetTextAlign(31)
    label.DrawLatex(0.90, 0.92, "#sqrt{s} = 8 TeV, L_{int} = 11.6 fb^{-1}")

    # Save Canvas to image
    c.SaveAs("dimuonSpectrum.png")

    tpost.Stop()
    posttime = round(tpost.RealTime(), 3)
    print("Finished post processing.")

    with open("pyrdf_dimuon_multinode_tfileprefetch_analysistimes.csv", "a+") as f:
        f.write("{},{},{}".format(begintime, evlooptime, posttime))
        f.write("\n")


officialdataset = (
    "root://eospublic.cern.ch//eos/opendata/cms/derived-data/"
    "AOD2NanoAODOutreachTool/Run2012BC_DoubleMuParked_Muons.root")

filenames = [("root://eospublic.cern.ch/"
              "/eos/root-eos/benchmark/CMSOpenDataDimuon/"
              "Run2012BC_DoubleMuParked_Muons_{}.root").format(i)
             for i in range(1, 101)]

df = PyRDF.RDataFrame("Events", filenames)

for i in range(1, 6):
    print("Iteration {}".format(i))
    t = ROOT.TStopwatch()
    dimuonSpectrum(df)
    t.Stop()
    realtime = round(t.RealTime(), 2)

    with open("pyrdf_dimuon_multinode_tfileprefetch_{}partitions.csv"
              .format(args.npartitions), "a+") as f:
        f.write(str(realtime))
        f.write("\n")
