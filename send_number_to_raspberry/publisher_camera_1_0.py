import zmq
import time
import pickle
import cv2
import threading

fps = 60



class Send_data_from_camera():
    """Receive data from laptop's camera"""
    def __init__(self, src=0):
        """Iniitiates the class"""
        self.capture = cv2.VideoCapture(src)
        self.capture.set(cv2.CAP_PROP_FPS, 60)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.thread = threading.Thread(target=self.update, args=())
        self.thread.daemon = True
        self.thread.start()
        self.status, self.frame = self.capture.read()

    def create_pub_socket(self, socket_type, port):
        """Creates the socket, PUB set to default"""
        ctx = zmq.Context()
        socket = ctx.socket(socket_type)
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


if __name__ == "__main__":
    pub_instance = Send_data_from_camera(src=0)

    # socket creating
    pub_socket = pub_instance.create_pub_socket(zmq.PUB, 5555)
    
    while True:
        frame = pub_instance.get_frame()

        if frame is not None:
            encoded, buffer = cv2.imencode('.jpg', pub_instance.frame)

            pub_instance.send_data(pub_socket, buffer)
            print('sending data')


            # time.sleep(1)
    
         # cv2.waitKey(<не должно быть равно 0>)
        if cv2.waitKey(int(60)) == ord('q'):
            break
