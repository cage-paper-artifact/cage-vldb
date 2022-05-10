import numpy as np
import pickle as pkl

# https://docs.python.org/3/library/socket.html#socket.socket.recv
# "Note For best match with hardware and network realities, the value of bufsize
# should be a relatively small power of 2, for example, 4096.
SIZE = 4096        # max size bytes to send in a single socket burst
PORT = 9898        # Port to listen on (non-privileged ports are > 1023)

def bytes_to_numpy(data):
    return pkl.loads(data)

def numpy_to_bytes(data):
    return pkl.dumps(data)

def send_data_length(s, buffer):
    s.send(str(len(buffer)).encode())
    #ACK
    sz = int(s.recv(SIZE))


def recv_data_length(s):
    sz = s.recv(SIZE)
    #ACK 
    s.send(sz)
    return sz
