### Build and run:


```bash
./build.sh mlflow rf10 REPO.azurecr.io/bench/mlflow:attempt
docker run -it --rm -p 5001:5001 REPO.azurecr.io/bench/mlflow:attempt1
```

### Test it:
```bash
$ curl -X POST -H "Content-Type:application/json; format=pandas-split" --data '{"data":[[1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]]}' 127.0.0.1:5001/invocations
```

