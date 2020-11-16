import PyRDF

import ROOT

PyRDF.use("spark")


def dimuonSpectrum(df):

    entries_total = df.Count()

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

    entries_final = df_mass.Count()

    # Create canvas for plotting
    ROOT.gStyle.SetOptStat(0)
    ROOT.gStyle.SetTextFont(42)
    c = ROOT.TCanvas("c", "", 800, 700)
    c.SetLogx()
    c.SetLogy()

    # Draw histogram
    hist.GetXaxis().SetTitle("m_{#mu#mu} (GeV)")
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

    print("Initial total entries: {}".format(entries_total.GetValue()))
    print("Entries after processing: {}".format(entries_final.GetValue()))
    # Save Canvas to image
    c.SaveAs("dimuonSpectrum.png")


dataset = ("root://eospublic.cern.ch//eos/opendata/cms/derived-data/"
           "AOD2NanoAODOutreachTool/Run2012BC_DoubleMuParked_Muons.root")

df = PyRDF.RDataFrame("Events", [dataset])

for i in range(1, 101):
    print("Iteration {} with rdf {}".format(i, str(df)))
    t = ROOT.TStopwatch()
    dimuonSpectrum(df)
    t.Stop()
    realtime = round(t.RealTime(), 2)

    with open("baseline_pyrdf_dimuon.csv", "a+") as f:
        f.write(str(realtime))
        f.write("\n")
