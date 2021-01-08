import zmq
import pickle
import asyncio
import cv2

class Subscriber:
    def __init__(self, port=5555, socket_type=zmq.SUB):
        self.port, self.socket_type = port, socket_type

        ctx = zmq.Context()
        self.socket = ctx.socket(socket_type)
        self.socket.connect(f'tcp://localhost:{port}')

    async def receive_frame(self):
        frame = self.socket.recv_string()
        print(frame)
        return frame

class Publisher:
    def __init__(self, port=5555, socket_type=zmq.PUB):
        self.port, self.socket_type = port, socket_type

        ctx = zmq.Context()
        self.socket = ctx.socket(socket_type)
        self.socket.bind(f'tcp://*:{port}')
    
    async def send_frame(self, frame):
        tracker = self.socket.send(pickle.dumps(frame))
        while tracker is not None:
            await asyncio.sleep(.2)
    