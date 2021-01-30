import socket
from settings import PORT, HOST


class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def define(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((HOST, PORT))
    
    def main(self):
        while True:
            data = self.client.recv(2048)
            print(data.decode('utf-8'))

if __name__ == '__main__':
    client = Client(HOST, PORT)

    client.define()
    client.main()
