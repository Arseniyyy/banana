import socket
from settings_1_1 import PORT_2
from time import sleep

class Server:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

    def define_server_socket(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.listen()
            self.conn, self.addr = s.accept()

    def main(self):    
        data = self.conn.recv(1024)

        return data.decode('utf-8')
