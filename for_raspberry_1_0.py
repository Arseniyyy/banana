from threading import Thread
import cv2, time
import zmq

# for raspberry

class VideoStreamWidget(object):
    def __init__(self, src=0):
        self.capture = cv2.VideoCapture(src)
        self.capture.set(cv2.CAP_PROP_FPS, 60)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
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
    context = zmq.Context()
    footage_socket = context.socket(zmq.PUB)
    footage_socket.bind('tcp://*:5555')
    video_stream_widget = VideoStreamWidget()
    while True:
        try:
            #start_time = time.time()

            frame = video_stream_widget.show_frame()
            #dt_recieving = time.time() - start_time
            start_time = time.time()
            encoded, buffer = cv2.imencode('.jpg', frame)
            #dt_recieving = time.time() - start_time
            

            footage_socket.send(buffer)
            dt_recieving = time.time() - start_time
            print(dt_recieving)
        except AttributeError:
            pass
