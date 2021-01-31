import zmq
import cv2
import threading
import numpy as np
from settings_1_0 import RASEPBERRY_PI_IP, PORT, FPS
from publisher_camera_1_0 import Publisher


img_row, img_col = 320, 240

cap = cv2.VideoCapture(0)
ret, frame1 = cap.read()

frame1 = cv2.resize(frame1, (img_row, img_col))
prvs = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)

class Subscriber:
    def __init__(self, host, port):
        self.host = host
        self.port = port

        self.create_sub_socket()

        self.thread = threading.Thread(target=self.threaded, args=())
        self.thread.daemon = True
        self.thread.start()

    def create_sub_socket(self):
        """Creates sub socket"""
        ctx = zmq.Context()

        self.socket = ctx.socket(zmq.SUB)
        self.socket.connect(f'tcp://{self.host}:{self.port}')
        self.socket.setsockopt_string(zmq.SUBSCRIBE, np.unicode(''))

    def main(self):
        """Main function. Starts all other functions"""
        self.show_frame()
        self.optical_flow()

    def threaded(self):
        """Get an image from PUBLISHER"""
        while True:
            self.frame = self.socket.recv()
            self.npimg = np.frombuffer(self.frame, dtype=np.uint8)
            self.source = cv2.imdecode(self.npimg, flags=1)

    def show_frame(self):
        """Shows frame"""
        try:
            cv2.imshow('frame', self.source)

            if cv2.waitKey(FPS) == ord('q'):
                cv2.destroyAllWindows()
                exit(1)

        except AttributeError:
            return

    def optical_flow(self):
        """Creates optical flow"""
        try:
            next_frame = cv2.cvtColor(self.source, cv2.COLOR_BGR2GRAY)

            flow = cv2.calcOpticalFlowFarneback(prvs, next_frame, None, 0.5, 1, 15, 1, 5, 1.2, 0)

            dvx = -np.ma.average(flow[..., 0])
            dvy = -np.ma.average(flow[..., 1])

            print(f'dvx: {dvx}')
            print(f'dvy: {dvy}')

        except Exception:
            return
