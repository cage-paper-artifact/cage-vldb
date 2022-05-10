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
process = subprocess.Popen(["/home/sshuser/YOURPATH/containers/prespind.sh", "prespin_arrow_primes"], stdout=subprocess.PIPE)
output, error = process.communicate()


@pandas_udf("long")
def udf_lpf_azfunc_container_per_thread(c1: pd.Series) -> pd.Series:
    import pandas as pd
    import os, time
    
    import pyarrow as pa
    import pyarrow.flight as fl
    from pyspark import TaskContext
    
        
    ctx = TaskContext()
    partid = str(ctx.partitionId())
    port = 8815 + (int(partid) % 3)  # Horrifically creative hack to make each task grab a unique container (mod the number of cores)
        
    client = fl.connect("grpc://127.0.0.1:" + str(port))

    table = pa.Table.from_pandas(pd.DataFrame(c1))

    # write the data to an array on the server
    writer, _ = client.do_put(fl.FlightDescriptor.for_path('scoreit'), table.schema)
    writer.write_table(table, table.num_rows)
    writer.close()

    # Do the action to makeit SCORE the array on the server
    response = client.do_action(pa.flight.Action('prime', pa.allocate_buffer(0)))
    for _ in response:  #must consume iterator, i think this is what actually triggers the action
        pass

    return client.do_get(fl.Ticket(b'scored')).read_pandas().squeeze()

    
sql_context.udf.register("LPF_CONTAINER_WARM", udf_lpf_azfunc_container_per_thread)



print("Starting the pyarrow")
resultfile = open("results-5-local.txt", "a")
resultfile.write("primes local:\n")
for table in ["L10nums10m", "L10nums1m", " L10nums100k" ]:
    print("on table " + table)
    resultfile.write("prespun. rows = " + table + "\n")
    for x in range(7):
        print("starting")
        start = time.time()
        query = sql_context.sql("SELECT LPF_CONTAINER_WARM(longnums) as result FROM " + table)

        query.write.parquet('/opt/data/'+str(time.time())+'sqlout.txt')
        elapse = time.time()-start
        print("ON  LOOP {}, got time{}".format(x, elapse))
        resultfile.write(str(elapse)+"\n")
        resultfile.flush()




