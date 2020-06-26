#include <iostream>
#include <ROOT/RDataFrame.hxx>
#include <TEnv.h>
#include <RtypesCore.h>

int main()
{
   gEnv->SetValue("TFile.AsyncPrefetching", 1);
   gEnv->SetValue("Cache.Directory", "file:cache/");

   ROOT::RDataFrame df("reftree", "root://eosuser.cern.ch//eos/user/v/vpadulan/reftree/reftree_100000000entry.root");

   auto mean_op = df.Mean<Double_t>("b3"); // b3 is a Gaussian with mean 10

   std::cout << "b3 mean: " << *mean_op << "\n";
}