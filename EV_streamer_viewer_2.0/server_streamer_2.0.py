from threading import Thread
import cv2, time
import zmq
import numpy as np
import pickle

# for example send three objects in three threads

class VideoStreamWidget(object):
    def __init__(self, src=0):
        self.capture = cv2.VideoCapture(src)
        self.capture.set(cv2.CAP_PROP_FPS, 60)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        # Start the thread to read frames from the video stream
        self.thread = Thread(target=self.update, args=())
        self.thread.daemon = True
        self.thread.start()

    def update(self):
        # Read the next frame from the stream in a different thread
        while True:
            if self.capture.isOpened():
                (self.status, self.frame) = self.capture.read()
            #time.sleep(.01)

    def show_frame(self):
        # Display frames in main program

        return self.frame



if __name__ == '__main__':
    # context = zmq.Context()
    # footage_socket = context.socket(zmq.PUB)
    # footage_socket.bind('tcp://*:5555')
    # video_stream_widget = VideoStreamWidget()


    # context2 = zmq.Context()
    # footage_socket2 = context.socket(zmq.SUB)
    # footage_socket2.connect('tcp://localhost:5556')
    # #footage_socket2.connect('tcp://192.168.4.240:5556')
    # footage_socket2.setsockopt_string(zmq.SUBSCRIBE, np.unicode(''))

    context3 = zmq.Context()
    footage_socket3 = context3.socket(zmq.PUB)
    footage_socket3.bind('tcp://*:5557')
    while True:
        try:
            buffer = pickle.dumps('hi new string')
            footage_socket3.send(buffer, flags=0)
            # start_time = time.time()

            # frame = video_stream_widget.show_frame()
            # #dt_recieving = time.time() - start_time
            # encoded, buffer = cv2.imencode('.jpg', frame)
            # #dt_recieving = time.time() - start_time
            # start_time = time.time()

            # footage_socket.send(buffer)
            # dt_recieving = time.time() - start_time
            # print(f'Data receiving: {dt_recieving}')


            # data = footage_socket2.recv()
            # num = pickle.loads(data)
            # print(num)
        except AttributeError:
            pass