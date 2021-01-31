# Вызов всех сокетов (С raspberry присылается изображение и сразу же после этого ноутбук шлёт число на raspberry. Все описанные действия происходят в бесконечном цикле)
# Файл исполняется на ноутбуке, следовательно вызываются только
# такие сокеты, как subscriber_camera & server
# subscriber_camera - получает изображения с камеры, подключённой к raspberry
# server - сразу же после получения изображения посылает на raspberry число

from settings_1_0 import PORT, RASEPBERRY_PI_IP, PORT_2
from subscriber_camera_1_0 import Subscriber
from client_echo import Client

if __name__ == '__main__':
    subscriber = Subscriber(RASEPBERRY_PI_IP, PORT)
    client = Client(RASEPBERRY_PI_IP, PORT_2)

    client.define_client_socket()

    while True:
        subscriber.main()
        client.main()
 