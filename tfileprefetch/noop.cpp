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
   std::string_view treename{"reftree"};
   std::string_view filename{"root://eosuser.cern.ch//eos/user/v/vpadulan/reftree/reftree_100000000entry.root"};

   // Open a .csv file in append mode
   std::ofstream timecsv("tfileprefetch_noop.csv", std::ofstream::out | std::ofstream::app);

   // Create a TStopwatch to measure the time needed for a noop on the "b3"
   // column of the RDataFrame. This should be a good measure of the time needed
   // to open and read the branch from the remote file or from the cached one.
   TStopwatch t;
   ROOT::RDataFrame df(treename, filename);
   df.Foreach([](Double_t e) {}, {"b3"});
   Double_t elapsed{t.RealTime()};
   timecsv << std::fixed << std::setprecision(2) << elapsed << "\n";

   timecsv.close();
}