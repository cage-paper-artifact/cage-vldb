#!/usr/bin/python3
import docker
import sys
from time import sleep
client = docker.from_env()


if len(sys.argv) > 1:
    image = sys.argv[1]
    STARTPORT= int(sys.argv[2])
else:
    image = 'REPO.azurecr.io/bench/sockets_pyslim:prespin2' 
    STARTPORT=9898
print("spinning up " + image)

for i in range(3):
    port = STARTPORT + i
    try:
        c = client.containers.run(image, remove=True,  detach=True,  ports={str(STARTPORT)+'/tcp': port})  
    except Exception as e: 
        print("maybe already running?")
        print(e)
        continue

    ## wait for it to be ready
    print("WAITING\n")
    sleep(1)
    while c.exec_run('ls /workdir/ready')[0] != 0:
        print("WAITING\n")
        sleep(.5)
        
    print("DONE")
