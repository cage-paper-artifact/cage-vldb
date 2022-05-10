#!/usr/bin/env python3
# https://medium.com/techanic/docker-containers-ipc-using-sockets-part-1-2ee90885602c

import socket
from numpybytes import *
MODEL = "model"

HOST = '0.0.0.0'   # Remember, loopback addresses inside a container are not accessible outside of it

#from user_script import run  # Not used for now, instead moving here.
import pickle as pkl
loaded_model = pkl.load(open(MODEL, 'rb'))

# connection phase
print('Waiting for connection')
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
s.listen()
open('/workdir/ready', 'a')
conn, addr = s.accept()
print('Connected by', addr)

while True: # loop for pandas iterator

    #get LEN
    sz = recv_data_length(conn)

    # send/recv phase
    request = None
    while True:  # loop for single batch
        data = conn.recv(SIZE)
        if not data:
            print("exiting recv, no data")
            import sys
            sys.exit(0)
        if  request is None:
            request = data
        else:
            request = request+data
        if len(request) >= int(sz):
            print("exciting recv, done.")
            break
    # convert to numpy
    as_np = bytes_to_numpy(request)

    # call the UDF/run the predcition
    prediction = loaded_model.predict(as_np)

    # convert the numpy data to a bytes and write to socket
    buffer = numpy_to_bytes(prediction)
    print("Sending back prediction.")
    send_data_length(conn, buffer)
    conn.sendall(buffer)

