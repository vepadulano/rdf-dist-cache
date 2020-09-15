# Distributed caching of input datasets in an RDataFrame analysis

This repository aims at exploring different technologies for caching input data of an RDataFrame analysis in a distributed environment.
Its layout is as follows:

* [`baseline`](baseline): Baseline tests. No caching mechanism enabled.
* [`comparison`](comparison): Applications to compare results of the tests.
* [`reftree`](reftree): Code to recreate the reference `.root` file.
* [`tfileprefetch`](tfileprefetch): Tests with the `TFilePrefetch` ROOT class.
* [`xrootd`](xrootd): Tests with an XRootD proxy plugin.

The master branch only shows test applications and configuration scripts. Checkout the `data-plots` branch to see data and relative plots for tests and comparisons.

# Hardware Setup
A first round of tests has been executed on a cluster with the following setup:
* 5 [CERN OpenStack](https://clouddocs.web.cern.ch/) VMs with:
  * 1 VCPU
  * 1.8 GB RAM
  * 10 GB HDD
  * CERN-VM 4 Image
* 1 physical computer with the following specs:
  * Intel(R) Core(TM) i7-6700 CPU @ 3.40GHz, 4 cores, 8 threads
  * 16 GB RAM
  * 256 GB SSD
  * CentOS 7

The roles of the various machines can be found in the different test folders READMEs

# Spark Cluster Setup

WIP
