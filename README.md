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

To setup the Spark cluster one needs to modify some environment variables and open a few ports according to the Spark services needed for running a Spark application. 

## 1. Configuration file

The configuration is stored inside `$SPARK_HOME/conf/spark-env.sh` . If the user has no permissions over the Spark installation folder (as it happens for example when sourcing Spark from CVMFS), the environment variable `SPARK_CONF_DIR` should be set to the path of a new configuration file, which should be a copy of `spark-env.sh`.

The configuration file should be created and modified on the master node and then copied over to all the worker nodes. The configuration file for this repository modifies the following parameters:
* `SPARK_MASTER_HOST`: Hostname of the machine that will act as Spark master.
* `SPARK_LOG_DIR`: Directory where the log files will be stored (same path for all the machines in the cluster).
* `SPARK_WORKER_DIR`: Directory for the worker processes.

## 2. Minimal set of ports to open
* 4040: SparkUI service. This is linked to the duration of the SparkContext, i.e. the connection between the Spark Driver and the Spark cluster. 
* 7077: Default port for the Spark Master. The workers will connect to the master via this port.
* 7377: Default port for the external shuffle service. This service is needed if the dynamic allocation of cluster resources is enabled. See the [docs](https://spark.apache.org/docs/latest/job-scheduling.html#dynamic-resource-allocation)
* 8080: Default port for the Master WebUI. A dashboard showing the status of the cluster, the workers connected and the jobs history.
* 8081: Default port for the Worker WebUI. A dashboard showing the status of the single worker and its job history.
* 30000: Port for all block managers to listen on. These exist on both the driver and the executors. It is random by default.
* 40000: Port for the driver to listen on. This is used for communicating with the executors and the standalone Master. It is random by default.

## 3. Starting the cluster

All the launch scripts are in `$SPARK_HOME/sbin`. In particular:
* `sbin/start-master.sh` - Starts a master instance on the machine the script is executed on.
* `sbin/start-slave.sh spark://<MASTER_HOSTNAME>:<MASTER_PORT>` - Starts a worker instance on the machine the script is executed on and connects it to the master.

More options at the [Spark Standalone docs](https://spark.apache.org/docs/latest/spark-standalone.html#cluster-launch-scripts).
