#!/bin/bash

if [ "$HOSTNAME" = pullhd ]; then
    printf '%s\n' "on the right host"
else
    printf '%s\n' "Please ssh to pullhd before running"
    exit
fi

images=( "REPO.azurecr.io/bench/pullexp:DTstgnovenv" "REPO.azurecr.io/bench/pullexp:GBRstgnovenv" )

rm pull.txt
cat /etc/docker/daemon.json >> pull.txt

for i in "${!images[@]}"; do

    IMAGE=${images[i]}
    echo $IMAGE >> pull.txt
    
    for x in {1..5}; do
	if [ "$IMAGE" = "REPO.azurecr.io/bench/pullexp:DTstgnovenv" ]; then
            # wipe everything for "original" image
            docker system prune --volumes --all -f
	else
	    # wipe only second image for incremental image
            docker rmi $IMAGE
	fi
    	docker rmi $IMAGE
    	start=$(date +%s.%N)
    	docker pull $IMAGE
    	stop=$(date +%s.%N)
    	sum=`echo "$stop -  $start" | bc -l`
    	echo $sum >> pull.txt
    done
done

echo "If set to /mnt, then fast disk.  If set to {}, then slow disk:"
cat /etc/docker/daemon.json
cat pull.txt
