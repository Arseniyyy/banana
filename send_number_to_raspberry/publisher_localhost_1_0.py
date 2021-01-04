import zmq
import random
import sys
import time
import pickle
import numpy as np
from settings_1_0 import PORT

port = PORT

context = zmq.Context()
footage_socket = context.socket(zmq.PUB)
footage_socket.bind("tcp://*:%s" % port)

while True:
    arr = [1, 2, 3, 4] 
    p = pickle.dumps(arr, protocol=-1)
    footage_socket.send(p)
    time.sleep(1)

    print('sent')