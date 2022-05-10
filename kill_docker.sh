#!/bin/bash

# Put this script on all nodes, then call this script in a loop as:
#  for host in $SPARK_NODES ; do ssh $host "sh -c ' nohup ./kill_docker.sh > /dev/null 2>&1 &'" ;done

docker container stop $(docker container list -q)
docker rm $(docker container list -qa)
