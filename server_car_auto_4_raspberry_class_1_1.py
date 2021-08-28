import argparse
import time
import os
from server_echo_4_raspberry_1_1 import Server
from settings_1_1 import EMPTY_HOST, PORT_2
from settings_1_1 import FPS
from threading import Thread
import cv2


class Raspberry_pi:
    def __init__(self, ESC, max_value, min_value):
        # ESC - порт разберри, на котором подулючен регулятор скорости
        self.ESC = ESC
        self.max_value = max_value
        self.min_value = min_value
        # self.thread = Thread(target=self.main, args=(), daemon=True)
        # self.thread.start()

    def setup_gpio(self):
        os.system("sudo pigpiod")  # Launching GPIO library
        # As i said it is too impatient and so if this delay is removed you will get an error
        time.sleep(1)
        import pigpio
        # STEER = 18
        pi = pigpio.pi()
        pi.set_servo_pulsewidth(self.ESC, 0)
        time.sleep(1)

        return pi, self.ESC

    def calibrate(self, pi, ESC):   # Стандартная процедура автокалибровки для esc регулятора
        pi.set_servo_pulsewidth(ESC, 0)
        print("Отключите питание (батарею) и нажмите Enter")
        inp = input()
        if inp == '':
            pi.set_servo_pulsewidth(ESC, self.max_value)
            print("Подключите батарею прямо сейчас. Вы должны услышать 2 звуквых сигнала. Затем дождитесь окончания сигнала и нажмите Enter")
            inp = input()
            if inp == '':
                pi.set_servo_pulsewidth(ESC, self.min_value)
                print("Специальный сигнал скоро будет")
                time.sleep(7)
                print("Ждите ....")
                time.sleep(5)
                print("Не беспокойтесь, просто ждите.....")
                pi.set_servo_pulsewidth(ESC, 0)
                time.sleep(2)
                print("Остановите ESC сейчас...")
                pi.set_servo_pulsewidth(ESC, self.min_value)
                time.sleep(1)
                print("Калибровка завершена")
                # control() # You can change this to any other function you want
                pi.set_servo_pulsewidth(ESC, 1500)

    def control(self, pi, ESC, speed):
        pi.set_servo_pulsewidth(ESC, int(speed))
        # pi.set_servo_pulsewidth(STEER,int(angle))

    # This will stop every action your Pi is performing for ESC ofcourse.

    def stop(self, pi, ESC, connection):
        pi.set_servo_pulsewidth(ESC, 0)
        pi.stop()
        connection.close()

    def config(self):
        # speed, angle, stop_key, connection = get_parameters(sock)
        # socket configuration
        self.server = Server(EMPTY_HOST, PORT_2)
        self.server.define_server_socket()

        ap = argparse.ArgumentParser()
        ap.add_argument("-c", "--calibrate", required=False,
                        help="car motor calibration")
        args = vars(ap.parse_args())

        self.pi, self.ESC = self.setup_gpio()
        if args["calibrate"] is not None:
            if int(args["calibrate"]) == 1:
                calibrate(self.pi, self.ESC)
            if int(args["calibrate"]) == 0:
                pass
        
        self.control(self.pi, self.ESC, 1500)
        time.sleep(1)
        self.control(self.pi, self.ESC, 1620)
        time.sleep(1)
        self.control(self.pi, self.ESC, 1670)
        time.sleep(1)

    def main(self):
        pwm: str = self.server.main()

        if pwm.startswith('0') or pwm.startswith('1'):
            try:
                pwm = int(pwm[:4])
                pwm = '1695'
                print(pwm)
                self.control(self.pi, self.ESC, pwm) # тут было pwm вместо строки

                if cv2.waitKey(1) == ord('q'):
                    pwm = '1500'
                    self.control(self.pi, self.ESC, pwm)
                    print(pwm)

            except ValueError:
                return
