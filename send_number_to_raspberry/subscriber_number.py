import zmq
import time


class Publisher_number:
    """All functionality will be called in the main function"""
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def define(self):
        port = "5556"
        context = zmq.Context()
        self.socket = context.socket(zmq.SUB)
        self.socket.connect (f"tcp://localhost:{self.port}" )

        topicfilter = "10001"
        self.socket.setsockopt_string(zmq.SUBSCRIBE, topicfilter)

    def receive(self):
        bytess = self.socket.recv()
        number = int.from_bytes(bytess, 'little')

        print(number)

if __name__ == '__main__':
    pub = Publisher_number('localhost', 5556)
    pub.define()

    while True:
        pub.receive()