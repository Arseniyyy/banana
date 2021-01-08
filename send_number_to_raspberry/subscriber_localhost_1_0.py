import sys
import zmq
import pickle
import time
import numpy as np
from settings_1_0 import PORT

port = PORT
if len(sys.argv) > 1:
    port =  sys.argv[1]
    int(port)
    
if len(sys.argv) > 2:
    port1 =  sys.argv[2]
    int(port1)

# Socket to talk to server
context = zmq.Context()
socket = context.socket(zmq.SUB)

print("Collecting updates from weather server...")
socket.connect("tcp://localhost:%s" % port)


# Subscribe to zipcode, default is NYC, 10001
# topicfilter = "10001"
socket.setsockopt_string(zmq.SUBSCRIBE, np.unicode(''))

# Process 5 updates
total_value = 0
while True:
    z = socket.recv()
    p = pickle.loads(z)
    print(p)

print("Average messagedata value for topic '%s' was %dF" % (topicfilter, total_value / update_nbr))
