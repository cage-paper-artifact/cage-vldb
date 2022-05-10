# Arrow flight code

Code adapted from:
* From this [blog](https://mirai-solutions.ch/news/2020/06/11/apache-arrow-flight-tutorial/)
* Original [code](https://github.com/miraisolutions/apache-arrow-flight-python-example)

**First, some instructions on how to build and test the ArrowFlight client outside of Spark:**

## First build the container  _(note: build.sh script up one directory from this):_

```bash
$ ./build.sh arrowflight rf10.skl YOUR_REGISTRY_NAME:TAG arrowflight/Dockerfile
```

## Then start the server:
```
docker run -d --rm -p 8815:8815  YOUR_REGISTRY_NAME:TAG
```

##### Side note: For debugging outside container
* If debugging only: Copy 'rf10.skl' in this dir, and name it `model` (bad hardcode sorry)
* If debugging only: run `python _server.py`


## Now, start the client (script in this folder):

```bash
$ python3 ./_client.py do_scoreit -v random,6
b'scored: 6 rows'
=== Response ===
  0
0  1
1  1
2  1
3  1
4  1
5  1
================
