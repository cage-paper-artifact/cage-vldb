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

# UDF definition   
@pandas_udf("long")
def udf_skl_predict(iterator: Iterator[pd.Series]) -> Iterator[pd.Series]:

    # This is code "provided by the user"
    def run(model, data):
        import pickle as pkl

        loaded_model = pkl.load(open(model, 'rb'))
        return loaded_model.predict(data)


    from pyspark import TaskContext
    ctx = TaskContext()
    stage = str(ctx.stageId())
    partid = str(ctx.partitionId())
    path  = "/opt/data/"
    stagepart = "{}-{}-".format(stage,partid)


    # Here is the actual UDF iterator
    for args in iterator:
        data_unmangled = pd.concat([feature for feature in args], axis=1)
        predictions = run(path+"rf10.skl", data_unmangled.values)  
        yield pd.Series(np.array(predictions))

sql_context.udf.register("PREDICT", udf_skl_predict)



print("Starting baseline/no container example")
resultfile = open("results-1-score-nocontainer.txt", "a")
for table in ["alphabet10m", "alphabet1m", "alphabet" ]:
    print("on table " + table)
    resultfile.write("no container. rows = " + table + "\n")
    if table == 'alphabet':
        resultfile.write("(table _alphabet_ has 100k rows)\n")
    for x in range(7):
        print("starting")
        start = time.time()
        query = sql_context.sql("SELECT PREDICT(A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X,Y,Z,1,2) as prediction FROM " + table)

        query.write.parquet('/opt/data/'+str(time.time())+'sqlout.txt')
        elapse = time.time()-start
        print("ON  LOOP {}, got time{}".format(x, elapse))
        resultfile.write(str(elapse)+"\n")
        resultfile.flush()
