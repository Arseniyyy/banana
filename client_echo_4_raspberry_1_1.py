import socket
from settings_1_1 import PORT_2, LOCALHOST, RASEPBERRY_PI_IP
from settings_1_1 import PWM


class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def define_client_socket(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((self.host, self.port))

    def main(self, pwm):
        self.s.sendall(str(pwm).encode('utf-8'))
