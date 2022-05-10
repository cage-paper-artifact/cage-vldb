#!/bin/bash
SPARK_HOSTS="172.29.0.10 172.29.0.11 172.29.0.12 172.29.0.14"
echo "PRESPINNING w $1"
for host in $SPARK_HOSTS ; do ssh $host ./$1.py  ;done
for host in $SPARK_HOSTS ; do ssh $host docker ps -a;done
