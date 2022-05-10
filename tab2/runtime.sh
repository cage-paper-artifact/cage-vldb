#!/bin/bash

if [ "$HOSTNAME" = wn5-spark3 ]; then
    printf '%s\n' "on the right host"
else
    printf '%s\n' "Please ssh to wn5-spark3 before running"
    exit
fi

rm wn5-spark3.txt

images=( "REPO.azurecr.io/bench/parq:010522" "REPO.azurecr.io/bench/pullexp:afiv1.0.1"  "REPO.azurecr.io/bench/sockets_pyslim:prespin" "REPO.azurecr.io/bench/mlflow:aml"  "REPO.azurecr.io/bench/arrowflight:paperversion"  )
args=(   "-v /mnt/data/:/workdir/data -e PARQ=2" "-p 127.0.0.1:80:8080/tcp" "-p 9898:9898"  "-p 5001:5001"  "-p 8815:8815" )


echo -e "Rows appear out of order. In this file, they are Row 1, Row 4, Row 2, Row 5, Row 3" >> $HOSTNAME.txt
echo -e "If this script fails or stalls (by connecting to open socket accidentally), please rerun"

for i in "${!images[@]}"; do

    IMAGE=${images[i]}
    ARGS=${args[i]}

    # use this to run a specific experiment only
    #if [[ $i != 3 ]] ; then
    #    continue
    #fi

    echo "" >>  $HOSTNAME.txt
    echo "" >>  $HOSTNAME.txt
    echo "docker run --rm -d $ARGS $IMAGE"
    echo "docker run --rm -d $ARGS $IMAGE" >> $HOSTNAME.txt
    for x in {1..5}; do
        

	# kill the last one
    	docker kill $(docker ps -q) >> /dev/null
        sleep 5
	# measure docker run
    	start=$(date +%s.%N)
    	docker run --rm -d $ARGS $IMAGE
    	stop=$(date +%s.%N)
    	sum=`echo "$stop -  $start" | bc -l`
    	echo -e "docker run: \t$sum\c" >> $HOSTNAME.txt
        echo -e "docker run: \t$sum\c"

	# now measure "ready" time on sockets and disk

	if [[  $i == 0 ]] ; then
		while true
		do
			ls /mnt/data/ready
			# check if file is there
			if  [[  $? == 0 ]] ; then
				init=$(date +%s.%N)
				sum=`echo "$init	-  $stop" | bc -l`
				echo -e "\tinit\t	\t$sum" >> $HOSTNAME.txt
				echo -e "\tinit\t	\t$sum"
				rm -rf /mnt/data/ready
				break
			fi
		done

	fi
	if [[  $i == 1 ]] ; then
                COUNTER=0
		while true
		do
			curl 127.0.0.1:80
			# check if socket returns error
			if  [[  $? == 52 ]] ; then
				init=$(date +%s.%N)
				sum=`echo "$init	-  $stop" | bc -l`
				echo -e "\tinit\t	$sum" >> $HOSTNAME.txt
				echo -e "\tinit\t	$sum"
				break
			fi
                        let COUNTER++
			if  [[  $COUNTER == 1000 ]] ; then
                            break
                        fi

		done

	fi
	if [[  $i == 2 ]] ; then
                COUNTER=0
		while true
		do
			curl 127.0.0.1:9898
			# check if socket returns error
			if  [[  $? == 52 ]] ; then
				init=$(date +%s.%N)
				sum=`echo "$init	-  $stop" | bc -l`
				echo -e "\tinit\t	$sum" >> $HOSTNAME.txt
				echo -e "\tinit\t	$sum"
				break
			fi
                        let COUNTER++
			if  [[  $COUNTER == 500 ]] ; then
                            break
                        fi
		done

	fi
	if [[  $i == 3 ]] ; then
                COUNTER=0
		while true
		do
			# check if socket returns error
			if  [[  `curl localhost:5001` == 'Healthy' ]] ; then
				init=$(date +%s.%N)
				sum=`echo "$init	-  $stop" | bc -l`
				echo -e "\tinit\t	$sum" >> $HOSTNAME.txt
				echo -e "\tinit\t	$sum"
				break
			fi
                        let COUNTER++
			if  [[  $COUNTER == 500 ]] ; then
                            break
                        fi
		done

	fi
	if [[  $i == 4 ]] ; then
                COUNTER=0
		while true
		do
			curl 127.0.0.1:8815
			# check if socket returns error
			if  [[  $? == 52 ]] ; then
				init=$(date +%s.%N)
				sum=`echo "$init	-  $stop" | bc -l`
				echo -e "\tinit\t	$sum" >> $HOSTNAME.txt
				echo -e "\tinit\t	$sum"
				break
			fi
                        if  [[  $COUNTER == 500 ]] ; then
                            break
                        fi
		done

	fi
    done

done
