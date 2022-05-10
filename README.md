# CAGE (Containerized And Generic Execution) artifact eval

## About the cluster we are providing for artifact eval

This Spark cluster deployed using Azure HDInsight with vanilla Spark 3.0.0. It has 4 nodes in addition to this head node.

On each of the nodes, we installed Docker. We also provisioned all of our Docker repo keys (our container images/container regsistry are only accessible from within this vnet by company security policy that we cannot get around). 

To recreate this cluster, the Docker images for all of the experiments would need to be rebuilt and pushed to either a local or remote repo such as dockerhub (account required). The scripts would need to be modified to point to the new container repo, in addition to updating the IP addresses of the Spark nodes in all of our scripts. Also, all 20+ of the tables we used would need to be recreated. 

To simplify this process and to focus on the experiments, we're providing access to our Spark cluster. Please feel free to poke around at anything and let us know if you have questions! 

#### Where stuff is:
* You can see the node IPs by running `echo $SPARK_HOSTS`, and can ssh into them by IP (ex: `ssh REDACT`)
* You can view all of the pre-loaded tables/data stored as parquet with: `hdfs dfs -ls /apps/spark/warehouse/`, ex: `hdfs dfs -ls -h /apps/spark/warehouse/alphabet10m`. 
* This cluster follows Hortonworks-styple install (HDP), so binaries/Spark files are at : `/usr/hdp/current/...`
* And configs are at: `/etc/spark3/conf/...`

## Experiments

Each folder has scripts with instructions in a README of how to run them. Included are:

* tab2 
* fig3
* fig4
* fig6
* fig8
* fig9
* fig10

## Graphs

In each of the folders, the output is stored in a results-name.txt file.  We made all of our graphs using excel.  We included the .xls file that you can paste the output of these scripts into to regenearate the graphs

Please follow the instructions on each of the tabs and simply paste the results files to generate the table/graphs into artifact_eval_graphs.xlsx



