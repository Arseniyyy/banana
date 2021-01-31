import socket
from settings_1_0 import PORT_2, LOCALHOST, RASEPBERRY_PI_IP


class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def define_client_socket(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((self.host, self.port))

    def main(self):
        self.s.sendall('1500'.encode('utf-8'))
