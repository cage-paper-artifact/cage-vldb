#!/bin/bash
# This will stop  docker on all nodes  and wait until it's done.

SPARK_HOSTS="172.29.0.10 172.29.0.11 172.29.0.12 172.29.0.14"
for host in  $SPARK_HOSTS ; do ssh $host "sh -c ' nohup ./kill_docker.sh '" ;done
for host in $SPARK_HOSTS; do ssh $host rm /mnt/data/* ; done

