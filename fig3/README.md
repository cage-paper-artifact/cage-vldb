Note: Since this experiment relies on some external services that have had
updates since the paper, the times will not match exactly. However, the
relative times should be the same.

Note: To prevent early termination of experiments due to termination of the ssh connection, prepend `nohup` to each command or run the command in a screen session.

HEADSUP:  Azure Functions often breaks in specatular ways that are out of our
control.  For our "remote" scripts, we wrote a "try again" loop.  Error
messages from the remote service are unfortunately expected.


###Scoring experiments
To run the experiment for scoring *no container*:
Command: `spark-submit run_nocontainer.py`
Output: The results (times) will be written to a file in this directory called `results-1-score-nocontainer.txt`.

To run the experiment for scoring *local with arrow flight*:
Command: `spark-submit run_local_scoring.py`
Output: The results (times) will be written to a file in this directory called `results-2-score-local.txt`.

To run the experiment for scoring *remote with Azure Functions*:
Command: `spark-submit run_remote_az_func_bench.py`
Output: The results (times) will be written to a file in this directory called `results-3-score-rest.txt`.

###Primes  (note, this takes a while to run)
To run the experiment for primes *no container*:
Command: `spark-submit run_prime_factor_nco_bench.py`
Output: The results (times) will be written to a file in this directory called `results-4-nocontainer.txt`.

To run the experiment for primes *local with arrow flight*:
Command: `spark-submit run_local_primes.py`
Output: The results (times) will be written to a file in this directory called `results-5-local.txt`.

To run the experiment for primes *remote with Azure Functions*:
Command: `spark-submit run_remote_prime_factor_bench.py`  
Output: The results (times) will be written to a file in this directory called `results-6-rest.txt`.

### To just run them all:
```
spark-submit run_nocontainer.py;spark-submit run_local_scoring.py ;spark-submit run_remote_az_func_bench.py ;spark-submit run_prime_factor_nco_bench.py ;spark-submit run_local_primes.py ;spark-submit run_remote_prime_factor_bench.py
```
