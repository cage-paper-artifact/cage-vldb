#!/usr/bin/env python3
# coding: utf-8


import pandas as pd
import numpy as np
import os
from pyspark.sql.functions import pandas_udf, col, expr
from typing import Iterator
import pandas as pd
import time
import subprocess


#scala> spark.sql("show tables").show
#+--------+---------------+------+
#|database|      tableName|  rows|
#+--------+---------------+------+
#| default|     alphabet1k|    1k|
#| default|    alphabet10k|   10k|
#| default|       alphabet|  100k|   
#| default|     alphabet1m|    1m|
#| default|    alphabet10m|   10m|
#+--------+---------------+------+


from pyspark import SparkContext
from pyspark.sql import HiveContext

sc = SparkContext()
print(sc.defaultParallelism)
hive_context = HiveContext(sc)


from pyspark.sql import SparkSession
spark = SparkSession.builder \
                    .master('yarn') \
                    .appName('SKLrf1Mpd') \
                    .getOrCreate()
batch = 10000
spark.conf.set("spark.sql.execution.arrow.pyspark.enabled", "true")
spark.conf.set('spark.sql.execution.arrow.maxRecordsPerBatch', batch)
numexec = (len(spark.sparkContext._jsc.sc().statusTracker().getExecutorInfos()) - 1)
print("set batch size to {} for {} executors".format(batch, numexec))

# This will be used to register UDF
from pyspark.sql import SQLContext
sql_context = SQLContext(spark)

def reset():
    # make sure docker killed properly on last run
    print("resetting")
    process = subprocess.Popen(["/home/sshuser/YOURPATH/containers/killd.sh"], stdout=subprocess.PIPE)
    output, error = process.communicate()


reset()

# ## Pre-spin all the things
print("pre-spinning up ")
process = subprocess.Popen(["/home/sshuser/YOURPATH/containers/prespind.sh", "prespin_lpf_af" ], stdout=subprocess.PIPE)
output, error = process.communicate()



@pandas_udf("long")
def udf_lpf_azfunc_container_per_thread(c1: pd.Series) -> pd.Series:
    import pandas as pd
    import os, time
    import docker
    from time import sleep
    import requests
    import urllib3
    import json
    
    from pyspark import TaskContext
    ctx = TaskContext()
    partid = str(ctx.partitionId())
    
    port = 8080 + (int(partid) % 3)  # The port used by the server
    

    url = "http://localhost:"+str(port)+"/api/primefactor?"    
    payload = c1.values.tolist()
    r = requests.post(url, data=json.dumps(payload))
    res = np.array(json.loads(r.text))
    return pd.Series(res)
    
    

sql_context.udf.register("LPF_CONTAINER_WARM", udf_lpf_azfunc_container_per_thread)

print("Starting the rest endpoint")
resultfile = open("results-6rest.txt", "a")
for table in ["L10nums10m", "L10nums1m", "L10nums100k"]:
    print("on table " + table)
    resultfile.write("local AF fixed nums lpf rows = " + table + "\n")
    for x in range(7):
        print("starting")
        start = time.time()
        query = sql_context.sql("SELECT LPF_CONTAINER_WARM(longnums) as result FROM " + table)
        query.write.parquet('/opt/data/'+str(time.time())+'sqlout.txt')
        elapse = time.time()-start
        print("ON  LOOP {}, got time{}".format(x, elapse))
        resultfile.write(str(elapse)+"\n")
        resultfile.flush()





