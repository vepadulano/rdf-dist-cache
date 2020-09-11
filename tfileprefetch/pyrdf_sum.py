"""
Simple sum operation on a column of the reference dataset.
Connects to the OpenStack VMs Spark cluster. If there is another cluster change
arguments of PyRDF.use() accordingly.
"""
import ROOT
import PyRDF

PyRDF.use("spark", conf={
    'npartitions': 3,
    'spark.master': 'spark://137.138.55.13:7077',
    'spark.driver.port': 40000,
    'spark.blockManager.port': 30000,
    'spark.app.name': 'PyRDF',
    'spark.executor.instances': 3,
})

rdf = PyRDF.RDataFrame(
    "reftree",
    "root://eosuser.cern.ch//eos/user/v/vpadulan/reftree/reftree_100000000entry.root")
s = rdf.Sum("b3")

t = ROOT.TStopwatch()
s.GetValue()
t.Stop()
realtime = round(t.RealTime(), 2)

with open("tfileprefetch_pyrdf_sum.csv", "a+") as f:
    f.write(str(realtime))
    f.write("\n")
