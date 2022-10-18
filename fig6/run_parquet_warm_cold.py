#!/usr/bin/env python
# coding: utf-8

###   Call with: spark-submit run_warm_cold.py


# # pandas_udf on the cluster


import pandas as pd
import numpy as np
import os
from pyspark.sql.functions import pandas_udf, col, expr
from typing import Iterator
import pandas as pd
import time
import subprocess

def reset():
    # make sure docker killed properly on last run
    print("resetting")
    process = subprocess.Popen(["/home/sshuser/YOURPATH/containers/killd.sh"], stdout=subprocess.PIPE)
    output, error = process.communicate()




# #### Start spark, pick a  batch size (ex: 100k is best for filesharing exeperiment (this one), else use 10k)



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
batch = 100000
spark.conf.set("spark.sql.execution.arrow.pyspark.enabled", "true")
spark.conf.set('spark.sql.execution.arrow.maxRecordsPerBatch', batch)
numexec = (len(spark.sparkContext._jsc.sc().statusTracker().getExecutorInfos()) - 1)
print("set batch size to {} for {} executors".format(batch, numexec))

# This will be used to register UDF
from pyspark.sql import SQLContext
sql_context = SQLContext(spark)




# First, make sure the cluster doesn't have a lot of containers already running on it.
reset()


# ## In this UDF, all containers are spun up cold and back down
@pandas_udf("long")
def udf_skl_predict_container_multibatch(iterator: Iterator[pd.Series]) -> Iterator[pd.Series]:
    import pandas as pd
    import os, time
    from pyarrow.parquet import read_table
    import docker
    from time import sleep
    
    from pyspark import TaskContext
    ctx = TaskContext()
    stage = str(ctx.stageId())
    partid = str(ctx.partitionId())
    path  = "/mnt/data/"
    stagepart = "{}-{}-".format(stage,partid)

    
    batch = 0
    
    # launch the container 
    client = docker.from_env()
    c = client.containers.run('REPO.azurecr.io/bench/parq:062921', remove=True, detach=True,  volumes={ path: {'bind': '/workdir/data', 'mode': 'rw'}}, environment=["PARQ="+stage+"-"+partid+"-"] )  

    # wait for it to be ready
    while c.exec_run('ls /workdir/ready')[0] != 0:
        sleep(.25)   
        
    
    # Here is the actual UDF iterator
    for args in iterator:
        batch_str = str(batch)
        prefix = path+stagepart+batch_str
        outgoing = prefix + 'example.parquet'
        incoming = prefix + 'example_ret.parquet'
        data_unmangled = pd.concat([feature for feature in args], axis=1)
        data_unmangled.to_parquet(outgoing)
        
        # read and return the data from the container
        table = None
        while table is None:
            try:
                table  = read_table(incoming).to_pandas()
            except:
                sleep(.1)
        batch +=1
        yield pd.Series(table.squeeze())     

        os.remove(outgoing)
        os.remove(incoming)
        
    # now teardown the container. Should be non-blocking.
    try:
        c.kill()
    except:
        pass



sql_context.udf.register("PREDICT_CONTAINER", udf_skl_predict_container_multibatch)



print("starting cold start")
resultfile = open("results-parquet-warmcold.txt", "a")
#for table in ["alphabet1b" ]:  # This is a lonnng one.
for table in ["alphabet100m", "alphabet10m", "alphabet1m", "alphabet" ]:
    print("on table " + table)
    resultfile.write("cold start. rows = " + table + "\n")
    for x in range(7):
        print("starting")
        start = time.time()
        query = sql_context.sql("SELECT PREDICT_CONTAINER(A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X,Y,Z,1,2) as prediction FROM " + table)
    
        query.write.parquet('/opt/data/'+str(time.time())+'sqlout.txt')
        elapse = time.time()-start
        print("ON  LOOP {}, got time{}".format(x, elapse))
        resultfile.write(str(elapse)+"\n")
        resultfile.flush()
        
        reset()


###


# ## Pre-spin all the things
print("pre-spinning up ")
process = subprocess.Popen(["/home/sshuser/YOURPATH/containers/prespind.sh", "prespin_volume"], stdout=subprocess.PIPE)
output, error = process.communicate()



@pandas_udf("long")
def udf_skl_predict_container_multibatch(iterator: Iterator[pd.Series]) -> Iterator[pd.Series]:
    import pandas as pd
    import os, time
    from pyarrow.parquet import read_table
    import docker
    from time import sleep
    from pathlib import Path
    
    # This is just for logging
    from pyspark import TaskContext
    ctx = TaskContext()
    stage = str(ctx.stageId())
    partid = str(ctx.partitionId())
    path  = "/mnt/data/"
    #stagepart = "{}-{}-".format(stage,partid)
    
    stagepart = str(int(partid) % 3) + '-'
    restart_file = path + stagepart + "restart"
    
    if os.path.isfile(restart_file):
        os.remove(restart_file)
    
    
    # dbg
    batch = 0
   
    
    # Here is the actual UDF iterator
    for args in iterator:
        batch_str = str(batch)
        prefix = path+stagepart+batch_str
        data_unmangled = pd.concat([feature for feature in args], axis=1)
        outgoing = prefix + 'example.parquet'
        data_unmangled.to_parquet(outgoing)
        
        # read and return the data from the container
        incoming = prefix + 'example_ret.parquet'
        table = None
        while table is None:
            try:
                table  = read_table(incoming).to_pandas()
            except:
                sleep(.1)
        batch +=1
        
        os.remove(outgoing)
        os.remove(incoming)
    
        yield pd.Series(table.squeeze())     

        
    # Don't kill the container here. :)
    ###  IMPORTANT: we must now write the "restart" file so the container knows to expect a new set of batches
    Path(restart_file).touch()    


sql_context.udf.register("PREDICT_CONTAINER_PRESPIN", udf_skl_predict_container_multibatch)



print("Starting the prespun")
#for table in ["alphabet1b" ]:  # This is a lonnng one.
for table in ["alphabet100m", "alphabet10m", "alphabet1m", "alphabet" ]:
    print("on table " + table)
    resultfile.write("prespun. rows = " + table + "\n")
    for x in range(4):
        print("starting")
        start = time.time()
        query = sql_context.sql("SELECT PREDICT_CONTAINER_PRESPIN(A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X,Y,Z,1,2) as prediction FROM " + table)
    
        query.write.parquet('/opt/data/'+str(time.time())+'sqlout.txt')
        elapse = time.time()-start
        print("ON  LOOP {}, got time{}".format(x, elapse))
        resultfile.write(str(elapse)+"\n")
        resultfile.flush()
        
