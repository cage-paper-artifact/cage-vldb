# Reproduciblity Instructions for "Containerized Execution of UDFs: An Experimental Evaluation"

## Artifact Eval Setup

To simplify setup, we're providing access to our Spark cluster. 

Our experiments were performed on a vanilla Spark 3.0 cluster with 2 head and 4 worker nodes (provisioned by HDInsight), each with Intel®Xeon®Platinum 8171M CPU @ 2.60GHz (8 Cores), 64GB RAM, and Python 3.7.  Each of the 4 worker nodes had 1 executor each, with 3 cores (tasks) and 40288mb RAM. 

In our cluster, we built ~50+ Docker images for the experiments, pushed to an internal-only repo (built with the provided `build.sh` file). Most our scripts point specifically to our container repo and contain all of the IP addresses of the Spark nodes (and would need to be modified with new IPs/repo address if run elsewhere).  We have pre-loaded 20+ Spark tables with publicly available and random data specified in the paper, also available to be accessed within the cluster (see below). 

## Quickstart:
See the notebook [quickstart.ipynb](https://github.com/cage-paper-artifact/cage-vldb/blob/main/quickstart.ipynb) to see a quick local example

#### In the cluster:
* You can see the node IPs by running `echo $SPARK_HOSTS`, and can ssh into them by IP to poke around
* You can view all of the pre-loaded tables/data stored as parquet with: `hdfs dfs -ls /apps/spark/warehouse/`, ex: `hdfs dfs -ls -h /apps/spark/warehouse/alphabet10m`. 
* This cluster follows Hortonworks-style install (HDP), so binaries/Spark files are at : `/usr/hdp/current/...`
* And configs are at: `/etc/spark3/conf/...`

## Experiments

Each folder has scripts with instructions in a README of how to run them. Included are:

* tab2 
* fig3
* fig4
* fig5
* fig6
* fig8
* fig9


## Reproducing the Graphs

In each of the folders, the output is stored in a results-name.txt file.  We made all of our graphs using excel.  We included the .xls file that you can paste the output of these scripts into to regenearate the graphs

Please follow the instructions on each of the tabs and simply paste the results files to generate the table/graphs into artifact_eval_graphs.xlsx



