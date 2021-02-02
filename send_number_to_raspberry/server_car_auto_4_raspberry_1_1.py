#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
# for raspberry
# TODO: -c 17
import argparse
import time
import os
from server_echo_4_raspberry_1_1 import Server
from settings_1_1 import EMPTY_HOST, PORT_2


def setup_gpio():
    os.system("sudo pigpiod")  # Launching GPIO library
    # As i said it is too impatient and so if this delay is removed you will get an error
    time.sleep(1)
    import pigpio
    ESC = 17
    # STEER = 18
    pi = pigpio.pi()
    pi.set_servo_pulsewidth(ESC, 0)
    time.sleep(1)

    return pi, ESC

def calibrate(pi, ESC):   # Стандартная процедура автокалибровки для esc регулятора
    max_value = 1700  # Максимальное значение шим
    min_value = 1500  # Минимальное значение шим
    pi.set_servo_pulsewidth(ESC, 0)
    print("Отключите питание (батарею) и нажмите Enter")
    inp = input()
    if inp == '':
        pi.set_servo_pulsewidth(ESC, max_value)
        print("Подключите батарею прямо сейчас. Вы должны услышать 2 звуквых сигнала. Затем дождитесь окончания сигнала и нажмите Enter")
        inp = input()
        if inp == '':
            pi.set_servo_pulsewidth(ESC, min_value)
            print("Специальный сигнал скоро будет")
            time.sleep(7)
            print("Ждите ....")
            time.sleep(5)
            print("Не беспокойтесь, просто ждите.....")
            pi.set_servo_pulsewidth(ESC, 0)
            time.sleep(2)
            print("Остановите ESC сейчас...")
            pi.set_servo_pulsewidth(ESC, min_value)
            time.sleep(1)
            print("Калибровка завершена")
            # control() # You can change this to any other function you want
            pi.set_servo_pulsewidth(ESC, 1500)


def control(pi, ESC, speed):
    pi.set_servo_pulsewidth(ESC, int(speed))
    # pi.set_servo_pulsewidth(STEER,int(angle))


# This will stop every action your Pi is performing for ESC ofcourse.
def stop(pi, ESC, connection):
    pi.set_servo_pulsewidth(ESC, 0)
    pi.stop()
    connection.close()


def main():
    # Ввод порта для передачи данных и флага калибровка. По умполчанию порт 1080, калибровка отключена

    # изменить порт можно командой:
    # -p <номер порта> пример: -p 1081

    # включить калибровку можно командой:
    # -с 1

    # socket configuration
    server = Server(EMPTY_HOST, PORT_2)
    server.define_server_socket()

    ap = argparse.ArgumentParser()
    ap.add_argument("-p", "--port", required=False,
                    help="choose port: 1080 as default")
    ap.add_argument("-c", "--calibrate", required=True,
                    help="car motor calibration")
    args = vars(ap.parse_args())

    # port = 50008
    # if args["port"] is not None:
    #     if int(args["port"]):
    #         port = (int(args["port"]))

    pi, ESC = setup_gpio()
    if args["calibrate"] is not None:
        if int(args["calibrate"]) == 1:
            calibrate(pi, ESC)
        if int(args["calibrate"]) == 0:
            pass

    while True:
        # speed, angle, stop_key, connection = get_parameters(sock)

        speed = server.main()

        speed = int(speed)

        print(type(speed))

        control(pi, ESC, speed)


if __name__ == '__main__':
    main()
