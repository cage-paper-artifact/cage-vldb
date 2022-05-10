These experiments were done outside the Spark cluster on a special VM with two disks.

## Instructions:
ssh pullhd


## From that machine:
Once you are on the `pullhd` machine:


Step 0. 
- From the `pullhd` machine, first login:
~/docker_login.sh

cd ~/pull_experiments


You will run all scripts twice. 

Step 1.
 - First, setup the slow disk

sudo cp /etc/docker/slow.json /etc/docker/daemon.json
sudo service docker restart

Then run the BUILD/PULL/RUN below

Step 2.
 - Now, setup the fast disk:
sudo cp /etc/docker/fast.json /etc/docker/daemon.json
sudo service docker restart


### BUILD:

- NOTE: This time may be faster or slower than the one shown for 'build' in
the paper depending on network speed of pulling the python packages and system
upgrades that occurred since the original experiment, but times should be
consistent and proportional across the 5 runs.

./buildtime.sh


### PUSH: 

This one cannot be replicated due to security policy permissions of allowing random pushing to the repo.

### PULL:

./pulltime.sh

### RUN:

 - Note that times may vary from the paper due to system upgrade, but
   experiment should be consistent and proportional.

./runtime.sh
