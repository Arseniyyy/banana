import socket
from settings_1_0 import PORT_2
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
        data = self.conn.recv(4)
        print(data.decode('utf-8'))

        sleep(1)

server = Server('', PORT_2)

server.define_server_socket()

if __name__ == '__main__':
    while True:
        server.main()
