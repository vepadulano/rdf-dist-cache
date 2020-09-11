#include <iostream>
#include <fstream>
#include <string_view>
#include <ROOT/RDataFrame.hxx>
#include <RtypesCore.h>
#include <TStopwatch.h>

int main()
{
   // Default TTree
   std::string_view treename{"reftree"};
   std::string_view filename{"root://eosuser.cern.ch//eos/user/v/vpadulan/reftree/reftree_100000000entry.root"};

   // Open a .csv file in append mode
   std::ofstream timecsv("baseline_sum.csv", std::ofstream::out | std::ofstream::app);

   // Create a TStopwatch to measure the time needed for a noop on the "b3"
   // column of the RDataFrame. This should be a good measure of the time needed
   // to open and read the branch from the remote file or from the cached one.
   ROOT::RDataFrame df(treename, filename);
   TStopwatch t;
   df.Sum<Double_t>("b3").GetValue();
   Double_t elapsed{t.RealTime()};
   timecsv << std::fixed << std::setprecision(2) << elapsed << "\n";

   timecsv.close();
}