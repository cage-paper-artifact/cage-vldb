#!/usr/bin/env python3
# https://medium.com/techanic/docker-containers-ipc-using-sockets-part-1-2ee90885602c


# Use this script if you don't use the notebook.
# (If you use the notebook, this is unneeded.)


import sys
assert sys.version_info >= (3, 6), "run with python3, not python"

import socket
import numpy as np
from numpybytes import *

HOST = '127.0.0.1' # The server's hostname or IP address



# Setup connection to container
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

# Make some random data
rows=10201
X = np.random.rand(rows, 28)
buffer = numpy_to_bytes(X)

# Send the length to expect
send_data_length(s, buffer)

s.sendall(buffer)

sz = recv_data_length(s)

request = None
while True:
    data = s.recv(SIZE)
    print("Received {} bytes.".format(len(data)))
    if not data:
        print("exiting recv")
        break

    if  request is None:
        request = data
    else:
        request = request+data
    if len(request) >= int(sz):
        print("LEN DONE")
        break
# convert to numpy
as_np = bytes_to_numpy(request)


print('Received prediction: ', repr(as_np))
