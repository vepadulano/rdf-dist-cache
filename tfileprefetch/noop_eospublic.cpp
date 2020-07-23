#include <iostream>
#include <fstream>
#include <string_view>
#include <ROOT/RDataFrame.hxx>
#include <TEnv.h>
#include <RtypesCore.h>
#include <TStopwatch.h>

int main()
{
   // Activate TFilePrefetch functionality
   gEnv->SetValue("TFile.AsyncPrefetching", 1);
   gEnv->SetValue("Cache.Directory", "file:cache/");

   // Default TTree
   std::string_view treename{"Events"};
   std::string_view filename{"root://eospublic.cern.ch//eos/opendata/cms/derived-data/AOD2NanoAODOutreachTool/"
                             "Run2012BC_DoubleMuParked_Muons.root"};

   // Open a .csv file in append mode
   std::ofstream timecsv("xrootd_noop_eospublic.csv", std::ofstream::out | std::ofstream::app);

   // Create a TStopwatch to measure the time needed for a noop on the "b3"
   // column of the RDataFrame. This should be a good measure of the time needed
   // to open and read the branch from the remote file or from the cached one.
   TStopwatch t;
   ROOT::RDataFrame df(treename, filename);
   df.Foreach([](UInt_t e) {}, {"nMuon"});
   Double_t elapsed{t.RealTime()};
   timecsv << std::fixed << std::setprecision(2) << elapsed << "\n";

   timecsv.close();
}