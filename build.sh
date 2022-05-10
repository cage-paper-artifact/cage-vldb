#!/bin/bash

if [ $# -lt 3 ]
then
    printf "%b" "Error. Not enough arguments.\n" >&2
    printf "%b" "usage: ./build.sh experiment model tag\n" >&2
    printf "%b" "usage: ./build.sh experiment model tag customDockerfile\n" >&2
    printf "%b" "Ex: ./build.sh sockets rf10.skl test\n" >&2
    printf "%b" "Ex: ./build.sh parq rf10.skl test_parq Dockerfile_mariner\n" >&2
    printf "%b" "Ex: ./build.sh mlflow rf10 REPO.azurecr.io/bench/mlflow:attempt1" >&2

    exit 1
fi
if [ $# -eq 4 ]
then
    DOCKERFILE=$4
else
    DOCKERFILE=$1"/Dockerfile"
fi
echo "Using Dockerfile: " $DOCKERFILE


# TODO, either parameterize rest of build args, or rename the MAIN script to be the same.
if [ $1 == "sockets" ]
then
    echo $1
    DOCKER_BUILDKIT=1 docker build --file $DOCKERFILE --build-arg MODELNAME=models/skl/$2 --build-arg REQS=$1/myreqs-skl.txt --build-arg SCRIPT=models/skl/runskl.py --build-arg MAIN=$1/ipc_server.py  -t $3 .
elif [ $1 == "parq" ]
then
    echo $1
    DOCKER_BUILDKIT=1 docker build --file $DOCKERFILE --build-arg MODELNAME=models/skl/$2 --build-arg REQS=$1/myreqs-skl.txt --build-arg SCRIPT=models/skl/runskl.py --build-arg MAIN=$1/container_main.py  -t $3 .
elif [ $1 == "arrowflight" ]
then
    echo $1
    DOCKER_BUILDKIT=1 docker build --file $DOCKERFILE --build-arg MODELNAME=models/skl/$2 --build-arg REQS=$1/myreqs-skl.txt --build-arg SCRIPT=models/skl/runskl.py --build-arg MAIN=$1/_server.py  -t $3 .
elif [ $1 == "mlflow" ]
then
    echo $1
    DOCKER_BUILDKIT=1 docker build --file $DOCKERFILE --build-arg MODELNAME=models/mlflow/$2  -t $3 .
else
    echo "no such experiement: " + $1
fi


