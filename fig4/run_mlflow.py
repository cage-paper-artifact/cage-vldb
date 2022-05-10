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
process = subprocess.Popen(["/home/sshuser/YOURPATH/containers/prespind.sh", "prespin_mlflow"], stdout=subprocess.PIPE)
output, error = process.communicate()

# UDF definition  \
@pandas_udf("long")
def udf_skl_predict(iterator: Iterator[pd.Series]) -> Iterator[pd.Series]:

    import requests
    import json

    from pyspark import TaskContext
    ctx = TaskContext()
    partid = str(ctx.partitionId())
    port = 5001 + (int(partid) % 3) 

    ## If local container, it's "/invocations".  if it's the AML-built container, it's "/score"
    scoring_uri  = 'http://127.0.0.1:' + str(port) + '/score'
    headers = {'Content-Type': 'application/json',}


    for args in iterator:
       data_unmangled = pd.concat([feature for feature in args], axis=1)
       payload = data_unmangled.values.tolist()
       data  = json.dumps({  "data" : payload })
       r = requests.post(scoring_uri, data, headers=headers)
       predictions = np.array(json.loads(r.text))
       yield pd.Series(np.array(predictions))



sql_context.udf.register("PREDICT_MLFLOW", udf_skl_predict)


print("Starting the mlflow")
resultfile = open("results-mlflow.txt", "a")
#for table in ["alphabet100m", "alphabet10m", "alphabet1m", "alphabet" ]:
for table in [ "alphabet10m" ]:
    print("on table " + table)
    resultfile.write("prespun. rows = " + table + "\n")
    for x in range(7):
        print("starting")
        start = time.time()
        query = sql_context.sql("SELECT PREDICT_MLFLOW(A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X,Y,Z,1,2) as prediction FROM " + table)

        query.write.parquet('/opt/data/'+str(time.time())+'sqlout.txt')
        elapse = time.time()-start
        print("ON  LOOP {}, got time{}".format(x, elapse))
        resultfile.write(str(elapse)+"\n")
        resultfile.flush()






