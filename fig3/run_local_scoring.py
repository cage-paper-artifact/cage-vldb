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
process = subprocess.Popen(["/home/sshuser/YOURPATH/containers/prespind.sh", "prespin_arrow_scoring"], stdout=subprocess.PIPE)
output, error = process.communicate()


# UDF definition
@pandas_udf("long")
def udf_skl_predict(iterator: Iterator[pd.Series]) -> Iterator[pd.Series]:

    import pyarrow as pa
    import pyarrow.flight as fl

    from pyspark import TaskContext
    ctx = TaskContext()
    partid = str(ctx.partitionId())
    port = 8815 + (int(partid) % 3)

    path = 'scoreit'
    client = fl.connect("grpc://127.0.0.1:" + str(port))


    # Here is the actual UDF iterator
    for args in iterator:
        data_unmangled = pd.concat([feature for feature in args], axis=1)

        table = pa.Table.from_pandas(data_unmangled)

        # write the data to an array on the server
        writer, _ = client.do_put(fl.FlightDescriptor.for_path(path), table.schema)
        writer.write_table(table, table.num_rows)
        writer.close()

        # Do the action to makeit SCORE the array on the server
        response = client.do_action(pa.flight.Action('score', pa.allocate_buffer(0)))
        for _ in response:  #must consume iterator, i think this is what actually triggers the action
            pass

        response = client.do_get(fl.Ticket(b'scored')).read_pandas()
        yield response.squeeze()


sql_context.udf.register("PREDICT_PYARROW", udf_skl_predict)


print("Starting the pyarrow")
resultfile = open("results-2-score-local.txt", "a")
resultfile.write("scoring local:\n")
for table in [ "alphabet10m", "alphabet1m", "alphabet" ]:
    print("on table " + table)
    resultfile.write("prespun. rows = " + table + "\n")
    if table == 'alphabet':
        resultfile.write("(table _alphabet_ has 100k rows)\n")
    for x in range(7):
        print("starting")
        start = time.time()
        query = sql_context.sql("SELECT PREDICT_PYARROW(A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X,Y,Z,1,2) as prediction FROM " + table)

        query.write.parquet('/opt/data/'+str(time.time())+'sqlout.txt')
        elapse = time.time()-start
        print("ON  LOOP {}, got time{}".format(x, elapse))
        resultfile.write(str(elapse)+"\n")
        resultfile.flush()




