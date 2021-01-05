import zmq
import pickle
import time
import cv2
import numpy as np

ctx = zmq.Context()
footage_socket = ctx.socket(zmq.SUB)
footage_socket.connect('tcp://localhost:5555')
footage_socket.setsockopt_string(zmq.SUBSCRIBE, np.unicode(''))

ctx2 = zmq.Context()
footage_socket2 = ctx2.socket(zmq.PUB)
footage_socket2.bind('tcp://*:5556')
while True:
    # getting string
    buffer = footage_socket.recv()
    data = pickle.loads(buffer)

    print(f'Received: {data}')

    time.sleep(1)