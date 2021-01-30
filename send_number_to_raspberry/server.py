import socket
import threading
from settings_1_0 import PORT_2


# Самые используемые протоколы: я tcp, ip, udp
# AF - address family. SOCK_STREAM - протокол

# class Socket_server:
#     def __init__(self, host, port):
#         self.host = host
#         self.port = port
    
#     def socket_bind(self):
#         self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         self.server.bind((self.host, self.port))

#         # server.listen() говорит, что можно принимать входящие сообщения
#         self.server.listen()

#     def main(self):
#             # Принимает входящие сообщения
#         sock, address = self.server.accept()
#         sock.send('You are connected'.encode('utf-8'))

#         print('Sending...')

# if __name__ == '__main__':
#     socket_server = Socket_server('', PORT_2)
#     socket_server.socket_bind()

#     while True:
#         socket_server.main()







server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('', PORT_2))
server.listen()


while True:
    sock, address = server.accept()
    sock.send('You are connected'.encode('utf-8'))

    print('Sending...')