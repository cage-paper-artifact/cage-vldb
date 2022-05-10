#!/bin/bash
PYSPARK_PYTHON=`which python3` PYSPARK_DRIVER_PYTHON=jupyter  PYSPARK_DRIVER_PYTHON_OPTS="notebook --port 8889" pyspark
