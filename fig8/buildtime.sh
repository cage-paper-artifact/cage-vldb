#!/bin/bash

if [ "$HOSTNAME" = pullhd ]; then
    printf '%s\n' "on the right host"
else
    printf '%s\n' "Please ssh to pullhd before running"
    exit
fi

images=( "REPO.azurecr.io/bench/pullexp:DTstgnovenv" "REPO.azurecr.io/bench/pullexp:GBRstgnovenv" )
args=( "Dockerfile_1"  "Dockerfile_2"  )


rm build.txt

echo "Checking if fast or slow disk:"
cat /etc/docker/daemon.json >> build.txt

for i in "${!images[@]}"; do

    IMAGE=${images[i]}
    ARGS=${args[i]}
    echo $IMAGE >> build.txt
    
    for x in {1..5}; do
	if [ "$ARGS" = "Dockerfile_1" ]; then
            # wipe everything for "original" image
            docker system prune --volumes --all -f
	else
	    # wipe only second image for incremental image
            docker rmi $IMAGE
	fi
    	start=$(date +%s.%N)
        DOCKER_BUILDKIT=1 docker build   --file $DOCKERFILE $ARGS -t $IMAGE .
    	stop=$(date +%s.%N)
    	sum=`echo "$stop -  $start" | bc -l`
    	echo $sum >> build.txt
    done
done

echo "If set to /mnt, then fast disk.  If set to {}, then slow disk:"
cat build.txt
