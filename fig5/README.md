**HEADSUP:** this is a long one, particularly the 10m sized ones. If in a hurry, run only the 100k/1m, or do less than 7 trials.


Note: To prevent early termination of experiments due to termination of the ssh connection, prepend `nohup` to each command or run the command in a screen session.

### Data-intensive (scoring)
To obtain the ratios that have been plotted in Figure 5, divide the Web Server timings by the no container timings.

To get the *no container* timings:
Command: `spark-submit run_nocontainer.py`
Output: The results (times) will be written to a file in this directory called `results_1nocontainer.txt`.

To get the *Web Server* timings:
Command: `spark-submit run_az_func_bench.py`
Output: The results (times) will be written to a file in this directory called `results-2rest.txt`.


### Compute/data-intensive (primes on table with 28 columns)
To obtain the ratios that have been plotted in Figure 5, divide the Web Server timings by the no container timings.

To get the *no container* timings:
Command: `spark-submit run_prime_factor_28_nco_bench.py`
Output: The results (times) will be written to a file in this directory called `results_3nocontainer.txt`.

To get the *Web Server* timings:
Command: `spark-submit run_prime_factor_28_bench.py`
Output: The results (times) will be written to a file in this directory called `results-4rest.txt`.

### Compute-intensive (primes)
To obtain the ratios that have been plotted in Figure 5, divide the Web Server timings by the no container timings.

To get the *no container* timings:
Command: `spark-submit run_prime_factor_nco_bench.py`
Output: The results (times) will be written to a file in this directory called `results_5nocontainer.txt`.

To get the *Web Server* timings:
Command: `spark-submit run_prime_factor_bench.py`
Output: The results (times) will be written to a file in this directory called `results-6rest.txt`.
