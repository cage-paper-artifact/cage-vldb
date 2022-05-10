FROM python:3.8-slim-buster

# The model to copy into the container
ARG MODELNAME

# A requirements.txt file to install in the environment.
ARG REQS

# A simple python script that performs inference (or other user script) on the model
ARG SCRIPT

# The main program of the conatiner
ARG MAIN

# '/workdir/' is base directory
WORKDIR /workdir/


COPY $REQS /workdir/requirements.txt
RUN pip install  -r /workdir/requirements.txt
RUN rm /workdir/requirements.txt


COPY $MODELNAME /workdir/model
COPY $SCRIPT /workdir/user_script.py
COPY $MAIN /workdir/container_main.py

# needed for socket image
COPY sockets/numpybytes.py /workdir

# Expose port 9898 in the container for the socket server
EXPOSE 9898
# execute the command
CMD [ "python3", "-u", "/workdir/container_main.py" ]
