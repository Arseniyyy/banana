import zmq
import cv2
import time
import threading
import numpy as np
from settings_1_1 import RASEPBERRY_PI_IP, PORT, FPS
from publisher_camera_4_raspberry_1_1 import Publisher
from PID_function_1_1 import PID
from decimal import Decimal


img_row, img_col = 320, 240

cap = cv2.VideoCapture(0)
ret, frame1 = cap.read()

frame1 = cv2.resize(frame1, (img_row, img_col))
prvs = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)

speed_ref = 0.3
speed_ref_max = 0.1
oldmin = -1.6
oldmax = 1.6
oldmaxf = 1
oldminf = 0
oldrangef = oldmaxf - oldminf
Ian = 0
newmin = 1250
newmax = 1700
newminf = 1500
newmaxf = 1700
newrange = newmax - newmin
newrangef = newmaxf - newminf
oldrange = oldmax - oldmin
dvy_f = 0.0
T_f = 0.1
If = 0


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
        pwm = self.optical_flow(dvy_f, If)

        return pwm

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

    def optical_flow(self, dvy_f, If):
        """Creates optical flow"""
        try:
            # start
            st = time.time()

            next_frame = cv2.cvtColor(self.source, cv2.COLOR_BGR2GRAY)

            # road lane detection
            hsv_image = cv2.cvtColor(self.source, cv2.COLOR_RGB2HSV)

            lower = np.array([0, 0, 150])
            upper = np.array([255, 255, 255])
            thresh = cv2.inRange(hsv_image, lower, upper)

            thresh = cv2.erode(thresh, None, iterations=1)
            thresh = cv2.dilate(thresh, None, iterations=3)

            canny = cv2.Canny(thresh, 280, 360, apertureSize=3)

            lines = cv2.HoughLinesP(canny,
                                    rho=2,
                                    theta=np.pi / 180,
                                    threshold=50,
                                    lines=np.array([]),
                                    minLineLength=40,
                                    maxLineGap=100)

            if lines is not None:
                for line in lines[0]:
                    pt1 = (line[0], line[1])
                    pt2 = (line[2], line[3])

                    cv2.line(self.source, pt1, pt2,
                            (0, 0, 255), 3)
                cv2.imshow('Output frame', self.source)

            cv2.waitKey(1)
            # 

            flow = cv2.calcOpticalFlowFarneback(
                prvs, next_frame, None, 0.5, 1, 15, 1, 5, 1.2, 0)

            dvx = -np.ma.average(flow[..., 0])
            dvy = -np.ma.average(flow[..., 1])

            # print(f'dvx: {dvx}')
            # print(f'dvy: {dvy}')

            # optical flow values
            dt = time.time() - st
            dvy_f = ((dvy - dvy_f) * 1 / T_f * dt) + dvy_f

            # f - филтр
            Uf, Pf, If, Df = PID(Input=speed_ref, Feedback=dvy_f, SatUp=1, SatDwn=0,
                                 Kp=10, Ti=0.1, Kd=0, Integral=If, dt=dt)

            # pwm - pulse width modulation
            pwm: float = (((Uf - oldminf) * newrangef) / oldrangef) + newminf
            # print(pwm)

            if pwm >= 1500 and pwm <= 1700:
                return pwm
            else:
                return 1500
            # ---

        except AttributeError:
            return
