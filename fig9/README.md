Note: Since this experiment relies on some external services that have had
updates since the paper, the times will not match exactly. However, the
relative times should be the same

Note: To prevent early termination of experiments due to termination of the ssh connection, prepend `nohup` to each command or run the command in a screen session.


### WebServ-local
Command: `spark-submit run_az_func_bench.py`
Output: The results (times) will be written to a file in this directory called `results-rest.txt`.

### WebServ-Remote
Command: `spark-submit run_remote_az_func_bench.py`
Output: The results (times) will be written to a file in this directory called `results-rest.txt`.

### MLflow-local
Command: `spark-submit run_mlflow.py`
Output: The results (times) will be written to a file in this directory called `results-mlflow.txt`.

### MLflow-remote
Replicating this experiment is not possible because we used custom settings in
the remote instance that we no longer have access to. (We requested special
quota for the experiment that has now expired).

