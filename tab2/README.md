## These experiments were run on a worker node.


## IMPORTANT: First: 

ssh wn5-spark3 


## There are 5 images in table 2:

Parquet: REPO.azurecr.io/bench/parq:010522
Sockets: REPO.azurecr.io/bench/sockets_pyslim:prespin
ArrowFlight: REPO.azurecr.io/bench/arrowflight:paperversion 
WebServer: REPO.azurecr.io/bench/pullexp:afiv1.0.1
MLFlow: REPO.azurecr.io/bench/mlflow:aml


## After you have ssh'ed to the worker node:

Command: `./runtime.sh`
Output: In `wn5-spark3.txt`, you'll see the columns `docker run` and `init (UDF init)` 


## Notes:

- Rows appear out of order in the output.  (Row 1, Row 4, Row 2, Row 5, Row 3 ) This is because the last experiment fails occasionally due to a timing issue.
--- Occassionally the script will get stuck on "curl: (7) Failed to connect to 127.0.0.1 port 80: Connection refused".  If this continues for more than 10 seconds, kill the script and restart it. This is due to a timing issue in trying to measure the container ready time.

- You will see a bunch of error messages such as "cannot access /mnt/data/ready".  This is us polling to see if the container is running.

