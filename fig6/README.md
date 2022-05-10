Notes:
This script takes a fairly long time to run, as it spins containers up/down a lot, and uses a large data size.
To prevent early termination of experiments due to termination of the ssh connection, prepend `nohup` to each command or run the com
mand in a screen session.

Command: `spark-submit run_parquet_warm_cold.py`
Output: The results (times) will be written to a file in this directory called `results-parquet-warmcold.txt`.

The results will be posted to the file after each iteration while the script runs, so you can check the numbers without full completion.

Note that the 1 billion experiment takes a very long time (~8-10 hours) to run, so it is commented out, but could be added back.
