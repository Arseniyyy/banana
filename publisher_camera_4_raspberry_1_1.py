import zmq
import time
import pickle
import cv2
import threading
from settings_1_1 import RASEPBERRY_PI_IP, PORT, FPS


img_row, img_col = 320, 240

class Publisher():
    """Receive data from laptop's camera"""
    def __init__(self, src=0):
        """Iniitiates the class"""
        self.capture = cv2.VideoCapture(src)
        self.capture.set(cv2.CAP_PROP_FPS, 60)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, img_row)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, img_col)
        self.thread = threading.Thread(target=self.update, args=())
        self.thread.daemon = True
        self.thread.start()
        self.status, self.frame = self.capture.read()

    def create_pub_socket(self, port):
        """Creates the socket, PUB set to default"""
        ctx = zmq.Context()
        socket = ctx.socket(zmq.PUB)
        socket.bind(f'tcp://*:{port}')

        return socket

    def send_data(self, socket, data):
        """Sends data to SUB socket"""
        socket.send(data)

    def update(self):
        """Used for threading"""
        while True:
            (self.status, self.frame) = self.capture.read()

    def get_frame(self):
        if self.frame is not None:
            return self.frame
