from threading import Thread
import cv2, time
import numpy as np
import zmq
import pickle

class recieveFrame(object):
    def __init__(self, src=0):
        # Start the thread to read frames from the video stream
        self.thread = Thread(target=self.update, args=())
        self.thread.daemon = True
        self.thread.start()

    def update(self):
        # Read the next frame from the stream in a different thread
        while True:
            start_time = time.time()
            self.frame = footage_socket.recv()
            self.npimg = np.frombuffer(self.frame, dtype=np.uint8)
            self.source = cv2.imdecode(self.npimg, 1)
            dt_recieving = time.time() - start_time
            #print(dt_recieving)
            #time.sleep(.01)

    def show_frame(self):
        # Display frames in main program
        cv2.imshow("Stream", self.source)
        key = cv2.waitKey(1)
        if key == ord('q'):
            cv2.destroyAllWindows()
            exit(1)


if __name__ == '__main__':
    # context = zmq.Context()
    # footage_socket = context.socket(zmq.SUB)
    # footage_socket.connect('tcp://localhost:5555')
    # #footage_socket.connect('tcp://192.168.4.1:5555')
    # footage_socket.setsockopt_string(zmq.SUBSCRIBE, np.unicode(''))
    # doStreamRead = recieveFrame()

    # context2 = zmq.Context()
    # footage_socket2 = context.socket(zmq.PUB)
    # footage_socket2.bind('tcp://*:5556')
    # data = 'Hello'
    # buffer = pickle.dumps(data)

    context3 = zmq.Context()
    footage_socket3 = context3.socket(zmq.SUB)
    footage_socket3.connect('tcp://localhost:5557')
    while True:
        try:
            buffer = footage_socket3.recv()
            data = pickle.loads(buffer)

            print(data)

            # doStreamRead.show_frame()

            # footage_socket2.send(buffer)
        except AttributeError:
            pass