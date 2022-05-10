# Build container: run this from root of dir:

$ ./build.sh sockets [name of your model stored] [tag for your container] [option docker file]`
```bash
$ ./build.sh sockets rf10.skl REPONAME/bench/socket_pyslim:test
```

# Running
There are scripts to run locally before trying in Spark.

## Example 1: Run your container locally (outside of spark):
Remember your tag name of your container (last arg) from above, such as ` REPONAME.azurecr.io/bench/socket_pyslim:test`.  Don't forget to add the port forwarding in.
```bash
docker run --rm -p 9898:9898 REPONAME.azurecr.io/bench/socket_pyslim:test
```

Then call the client:
```bash
python3 ipc_client.py
```

You should see from the server:

```bash
$ docker run --rm -p 9898:9898 my_skl_container
Waiting for connection
Connected by ('172.17.0.1', 46782)
exciting recv, done.
Sending back prediction.
exiting recv, no data
```

and from the client:

```bash
$ python ipc_client.py
Received prediction:  array([0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 1, 0,
    1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 0, 1, 1])
```

