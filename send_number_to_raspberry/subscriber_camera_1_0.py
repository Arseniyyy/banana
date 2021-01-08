import zmq
import cv2
import numpy as np

fps = 60

class Subscriber:
    def __init__(self, port, socket_type):
        self.socket_type = socket_type
        self.port = port

    def create_sub_socket(self):
        """Creates sub socket"""
        ctx = zmq.Context()
        socket = ctx.socket(self.socket_type)
        socket.connect(f'tcp://localhost:{self.port}')

        socket.setsockopt_string(zmq.SUBSCRIBE, np.unicode(''))

        return socket

    def receive(self, socket):
        """Receives frames"""
        buffer = socket.recv()

        array = np.frombuffer(buffer, dtype=np.uint8)
        image = cv2.imdecode(array, flags=1)

        return image
        
if __name__ == "__main__":
    sub_instance = Subscriber(5555, zmq.SUB)
    socket = sub_instance.create_sub_socket()

    while True:
        image = sub_instance.receive(socket)

        cv2.imshow('frame', image)

        if cv2.waitKey(fps) == ord('q'):
            break