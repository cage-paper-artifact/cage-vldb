#!/usr/bin/env python3

#from user_script import run
from pyarrow.parquet import write_table, read_table
import pyarrow as pa
import pandas as pd
import os
import time


MODEL = "model"
root = '/workdir/data/'
part = os.environ['PARQ']
path = root + part
path = path.strip()


batch = 0

#from user_script import run  # Not used for now, instead moving here.
import pickle as pkl
loaded_model = pkl.load(open(MODEL, 'rb'))

# Healthcheck
open('/workdir/ready', 'a')

while True:


    incoming = path + str(batch) + 'example.parquet'.strip()

    # read in the parquet file as pandas
    as_np = None
    while as_np is None:
        try:
            as_np = read_table(incoming).to_pandas()
        except:
            time.sleep(.1)


    # call the UDF/run the predcition
    #prediction = run(MODEL,as_np) # using a pre-unpickled model
    prediction = loaded_model.predict(as_np)

    # convert the numpy data to a dataframe and write to parquet
    df = pd.DataFrame(prediction, columns=['pred'])
    table = pa.Table.from_pandas(df,schema = pa.schema( [pa.field('pred', pa.int32())] ))

    write_table(table, path + str(batch) + 'example_ret.parquet')
    batch += 1
