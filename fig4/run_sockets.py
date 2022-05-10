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
import pickle as pkl

print("This is known to work with numpy 1.16.5.  Older versions conflict with arrow. newer versions conflict with serialization.")
print(np.__version__)



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


# util functions
def bytes_to_numpy(data):
    return pkl.loads(data)

def numpy_to_bytes(data):
    return pkl.dumps(data)

def send_data_length(s, buffer):
    s.send(str(len(buffer)).encode())
    #ACK
    sz = int(s.recv(4096))


def recv_data_length(s):
    sz = s.recv(4096)
    #ACK
    s.send(sz)
    return sz


def reset():
    # make sure docker killed properly on last run
    print("resetting")
    process = subprocess.Popen(["/home/sshuser/YOURPATH/containers/killd.sh"], stdout=subprocess.PIPE)
    output, error = process.communicate()


reset()


# ## Pre-spin all the things
print("pre-spinning up ")
process = subprocess.Popen(["/home/sshuser/YOURPATH/containers/prespind.sh", "prespin"], stdout=subprocess.PIPE)
output, error = process.communicate()



@pandas_udf("long")
def udf_skl_predict_container_multibatch2(iterator: Iterator[pd.Series]) -> Iterator[pd.Series]:
    import pandas as pd
    import os
    from time import sleep
    from pyarrow.parquet import read_table
    import docker


    import socket, io
    import numpy as np
    import pickle as pkl


    from pyspark import TaskContext
    ctx = TaskContext()
    stage = str(ctx.stageId())
    partid = str(ctx.partitionId())
    path  = "/opt/data/"
    stagepart = "{}-{}-".format(stage,partid)
    HOST = '127.0.0.1' # The server's hostname or IP address
    port = 9898 + (int(partid) % 3)  

    batch = 0


    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Setup connection to container
    s.connect((HOST, port))

    # Here is the actual UDF iterator
    for args in iterator:
        batch_str = str(batch)

        # Setup the data
        X = pd.concat([feature for feature in args], axis=1).to_numpy()

        buffer = numpy_to_bytes(X)

        # Send the length to expect
        send_data_length(s, buffer)
        # Send the data
        s.sendall(buffer)
        sz = recv_data_length(s)

        request = None
        while True:
            data = s.recv(4096)
            print("Received {} bytes.".format(len(data)))
            if not data:
                print("exiting recv")
                break

            if  request is None:
                request = data
            else:
                request = request+data
            if len(request) >= int(sz):
                print("LEN DONE")
                break
        # convert to numpy
        as_np = bytes_to_numpy(request)


        batch +=1

        yield pd.Series(as_np)


sql_context.udf.register("PREDICT_SOCKET_CONTAINER", udf_skl_predict_container_multibatch2)

print("Starting sockets example")
resultfile = open("results-sockets.txt", "a")
for table in ["alphabet10m" ]:
#for table in ["alphabet100m", "alphabet10m", "alphabet1m", "alphabet" ]:
    print("on table " + table)
    resultfile.write("sockets. rows = " + table + "\n")
    for x in range(7):
        print("starting")
        start = time.time()
        query = sql_context.sql("SELECT PREDICT_SOCKET_CONTAINER(A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X,Y,Z,1,2) as prediction FROM " + table)

        query.write.parquet('/opt/data/'+str(time.time())+'sqlout.txt')
        elapse = time.time()-start
        print("ON  LOOP {}, got time{}".format(x, elapse))
        resultfile.write(str(elapse)+"\n")
        resultfile.flush()
