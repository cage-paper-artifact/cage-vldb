FROM python:3.8-slim-buster as build
RUN python3 -m venv /venv

# A requirements.txt file to install in the environment.
ARG REQS

COPY $REQS /workdir/requirements.txt
RUN /venv/bin/pip install  -r /workdir/requirements.txt

# '/workdir/' is base directory
WORKDIR /workdir/


FROM python:3.8-slim-buster
COPY --from=build /venv /venv

# A simple python script that performs inference (or other user script) on the model
ARG SCRIPT

# The main program of the conatiner
ARG MAIN

# The model to copy into the container
ARG MODELNAME


COPY $SCRIPT /workdir/user_script.py
COPY $MAIN /workdir/container_main.py

# Expose port 8815 in the container for GRPC
EXPOSE 8815

# Do this as late as possible
COPY $MODELNAME /workdir/model

# '/workdir/' is base directory
WORKDIR /workdir/

# execute the command
CMD [ "/venv/bin/python3", "-u", "/workdir/container_main.py" ]
