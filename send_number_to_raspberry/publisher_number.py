import zmq
import time
import random


class Publiher_number:
    """All functionality will be called in the main function"""
    def __init__(self, port):
        self.port = port

    def main(self):

        context = zmq.Context()
        socket = context.socket(zmq.PUB)
        socket.bind(f"tcp://*:{self.port}")

        while True:
            topic = random.randrange(9999,10005)
            messagedata = random.randrange(1,215) - 80

            socket.send_string(f"{topic} {messagedata}")

            # time.sleep(1)

Publiher_number(5556).main()
