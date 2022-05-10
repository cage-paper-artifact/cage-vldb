#!/bin/bash

if [ "$HOSTNAME" = pullhd ]; then
    printf '%s\n' "on the right host"
else
    printf '%s\n' "Please ssh to pullhd before running"
    exit
fi

images=( "REPO.azurecr.io/bench/pullexp:DTstgnovenv" "REPO.azurecr.io/bench/pullexp:GBRstgnovenv" )
args=( "-p 9898:9898" "-p 9898:9898" )


rm run.txt
cat /etc/docker/daemon.json >> run.txt

for i in "${!images[@]}"; do

    IMAGE=${images[i]}
    ARGS=${args[i]}
    echo $IMAGE >> run.txt
    
    for x in {1..5}; do
	docker kill $(docker ps -q)
    	start=$(date +%s.%N)
	docker run --rm -d $ARGS $IMAGE
    	stop=$(date +%s.%N)
    	sum=`echo "$stop -  $start" | bc -l`
    	echo $sum >> run.txt
    done
done

echo "If set to /mnt, then fast disk.  If set to {}, then slow disk:"
cat /etc/docker/daemon.json
cat run.txt
