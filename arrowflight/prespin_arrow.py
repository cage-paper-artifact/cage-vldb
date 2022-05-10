#!/usr/bin/python3
import docker
import sys
from time import sleep
client = docker.from_env()


if len(sys.argv) > 1:
    image = sys.argv[1]
    STARTPORT= int(sys.argv[2])
else:
    #image = 'REPO.azurecr.io/bench/arrowflight:paperversion' #scoring
    image = 'REPO.azurecr.io/bench/arrowflight:prime'
    STARTPORT=8815
print("spinning up " + image)

for i in range(3):
    port = STARTPORT + i
    try:
        c = client.containers.run(image, remove=True,  detach=True,  ports={str(STARTPORT)+'/tcp': port})  
    except Exception as e: 
        print("maybe already running?")
        print(e)
        continue

    print("DONE")
