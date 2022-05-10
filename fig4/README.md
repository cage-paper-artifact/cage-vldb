
Note: To prevent early termination of experiments due to termination of the ssh connection, prepend `nohup` to each command or run the command in a screen session.

To run the experiment for scoring *no container*:
Command: `spark-submit run_nocontainer.py`
Output: The results (times) will be written to a file in this directory called `results_nocontainer.txt`.

To run the experiment for scoring *arrow flight*:
Command: `spark-submit run_arrow.py`
Output: The results (times) will be written to a file in this directory called `results-pyarrow.txt`.

To run the experiment for scoring *Sockets*:
Command: `spark-submit run_sockets.py`
Output: The results (times) will be written to a file in this directory called `results-sockets.txt`.

To run the experiment for scoring *Parquet*:
Command: `spark-submit run_parq.py`
Output: The results (times) will be written to a file in this directory called `results-parquet.txt`.

To run the experiment for scoring *MLFlow*:
Command: `spark-submit run_mlflow.py`
Output: The results (times) will be written to a file in this directory called `results-mlflow.txt`.

To run the experiment for scoring *WebServer* (local with Azure Functions):
Command: `spark-submit run_az_func_bench.py`
Output: The results (times) will be written to a file in this directory called `results-rest.txt`.

