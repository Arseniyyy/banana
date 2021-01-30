import socket
from settings import PORT, HOST

class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def define(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen()

    def main(self):
        while True:
            sock, address = self.server.accept()
            sock.send('You are connected'.encode('utf-8'))

            print('Sending...')

if __name__ == '__main__':
    server = Server(HOST, PORT)

    server.define()
    server.main()
