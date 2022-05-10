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


@pandas_udf("long")
def lpf_nco(c1: pd.Series) -> pd.Series:
    #f = open("/tmp/spark_temp_logging","a")

    #all_data = pd.concat([c1, c2], axis=1)
#     f.write("group by data type: " + str(type(all_data))+"\n")
    def largest_prime_factor(n):
        i = 2
        while i * i <= n:
            if n % i:
                i += 1
            else:
                n //= i
        return n
    #return str(np_payload.shape)
    return c1.apply(largest_prime_factor)
    #f.write("group by shape of data: " + str(np_payload.shape) + "\n")
    #payload = np_payload.tolist()
    #f.write("-------payload----------"+ "\n")
    #f.write(str(payload)+ "\n")
    #f.write(str(type(payload))+ "\n")
    #f.write(str(type(payload[0]))+ "\n")
    #f.close()

sql_context.udf.register("LPF_NCO", lpf_nco)
    

print("Starting the rest endpoint")
resultfile = open("results-4-nocontainer.txt", "a")
for table in ["L10nums10m", "L10nums1m", " L10nums100k" ]:
    print("on table " + table)
    resultfile.write("no container lpf rows = " + table + "\n")
    for x in range(7):
        print("starting")
        start = time.time()
        query = sql_context.sql("SELECT LPF_NCO(longnums) as result FROM " + table)
        query.write.parquet('/opt/data/'+str(time.time())+'sqlout.txt')
        elapse = time.time()-start
        print("ON  LOOP {}, got time{}".format(x, elapse))
        resultfile.write(str(elapse)+"\n")
        resultfile.flush()





