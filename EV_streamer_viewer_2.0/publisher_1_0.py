import zmq
import pickle
import time
import cv2
import numpy as np

cap = cv2.VideoCapture(0)

ctx = zmq.Context()
footage_socket = ctx.socket(zmq.PUB)
footage_socket.bind('tcp://*:5555')

ctx2 = zmq.Context()
footage_socket2 = ctx2.socket(zmq.SUB)
footage_socket2.connect('tcp://localhost:5556')
footage_socket2.setsockopt_string(zmq.SUBSCRIBE, np.unicode(''))

while True:
    # video capture
    a, frame = cap.read()
    cv2.imshow('frame', frame)

    buffer = pickle.dumps('hi new string')
    footage_socket.send(buffer)
    print('sent')

    time.sleep(1)