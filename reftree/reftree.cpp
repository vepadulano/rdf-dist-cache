#include <iostream>
#include <string>
#include <stdexcept>

#include <ROOT/RDataFrame.hxx>
#include <ROOT/RSnapshotOptions.hxx>
#include <RtypesCore.h>
#include <TRandomGen.h>

int main(int argc, char *argv[])
{
   TRandomMixMax r;
   ULong64_t entries = 1000;
   std::string filename{"reftree_1000entry.root"};

   if (argc > 1) {
      std::string arg{argv[1]};
      try {
         std::size_t pos;
         entries = std::stoull(arg, &pos);
         if (pos < arg.size()) {
            std::cerr << "Trailing characters after number: " << arg << '\n';
         }
      } catch (std::invalid_argument const &ex) {
         std::cerr << "Invalid number: " << arg << '\n';
      } catch (std::out_of_range const &ex) {
         std::cerr << "Number out of range: " << arg << '\n';
      }

      filename = "reftree_" + arg + "entry.root";
   }

   ROOT::RDataFrame df{entries};

   ROOT::RDF::RSnapshotOptions opts;
   opts.fAutoFlush = entries / 10;

   df.Define("b1", [](ULong64_t e) { return e; }, {"rdfentry_"})
      .Define("b2", [](ULong64_t e) { return 2 * e; }, {"b1"})
      .Define("b3", [&r] { return r.Gaus(10, 1); })
      .Define("b4", [&r] { return r.PoissonD(10); })
      .Define("b5", [&r] { return r.Rndm(); })
      .Snapshot<ULong64_t, ULong64_t, Double_t, Double_t, Double_t>("reftree", filename, {"b1", "b2", "b3", "b4", "b5"},
                                                                    opts);
}