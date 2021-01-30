import socket
from settings_1_0 import PORT_2, RASEPBERRY_PI_IP

# class Socket_client:
#     def __init__(self, host, port):
#         self.host = host
#         self.port = port

#     def define_socket(self):
#         self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         self.client.connect((self.host, self.port))

#     def main(self):
#         while True:
#             data: bytes = self.client.recv(2048) # 2048 - кол-воданных, которое надо полуить за одно подключение
#             print(data.decode('utf-8'))

# if __name__ == '__main__':
#     socket_client = Socket_client(RASEPBERRY_PI_IP, PORT_2)
#     socket_client.define_socket()

#     while True:
#         socket_client.main()





client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((RASEPBERRY_PI_IP, PORT_2))

while True:
    data = client.recv(2048)
    print(data.decode('utf-8'))