#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file presents an interface for interacting with the Playstation 4 Controller
# in Python. Simply plug your PS4 controller into your computer using USB and run this
# script!
#
# NOTE: I assume in this script that the only joystick plugged in is the PS4 controller.
#       if this is not the case, you will need to change the class accordingly.
#
# Copyright © 2015 Clay L. McLeod <clay.l.mcleod@gmail.com>
#
# Distributed under terms of the MIT license.

import os
import pprint
import pygame
import pickle
import time
import cv2 as cv
import multiprocessing
from multiprocessing import Pool
import socket
import numpy as np
import math


oldmin = -1
oldmax = 1
newmin = 1250
newmax = 1700
oldrange = oldmax-oldmin
newrange = newmax-newmin

oldmins = -2
oldmaxs = 2
newmins = 1300
newmaxs = 1700
oldranges = oldmaxs-oldmins
newranges = newmaxs-newmins
T_f = 0.1
dt = 0.0
d_f = 0.0
dgas = 0
s_f = False
flag = False
angle = 0.0
speed = 0.0
def send_cmd(cmd):
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Connect the socket to the port where the CarControl is listening
    #server_address = ('localhost', 1081)
    server_address = ('192.168.4.1', 50008)
    sock.connect(server_address)
    try:
        # Send data
        message = cmd.encode()

        sock.sendall(message)
    finally:

        sock.close()

class PS4Controller(object):
    """Class representing the PS4 controller. Pretty straightforward functionality."""

    controller = None
    axis_data = None
    button_data = None
    hat_data = None

    def init(self):
        """Initialize the joystick components"""

        pygame.init()
        pygame.joystick.init()
        self.controller = pygame.joystick.Joystick(0)
        self.controller.init()
        self.axis_data = {}
        self.button_data = {}
        self.hat_data = {}

        """Listen for events to happen"""





if __name__ == "__main__":
    ps4 = PS4Controller()
    ps4.init()
    ps4.axis_data = {0:0.0, 1:0.0, 2:0.0, 3:0.0, 4:0.0, 5:0.0}
    ps4.button_data = {0:False, 1:False, 2:False, 3:False, 4:False, 5:False, 6:False, 7:False, 8:False, 9:False, 10:False, 11:False, 12:False, 13:False}
    ps4.hat_data = {}

    first_gas = 0

    while True:
        for event in pygame.event.get():
            st = time.time()
            if event.type == pygame.JOYAXISMOTION:
                ps4.axis_data[event.axis] = round(event.value, 2)
            elif event.type == pygame.JOYBUTTONDOWN:
                ps4.button_data[event.button] = True
            elif event.type == pygame.JOYBUTTONUP:
                ps4.button_data[event.button] = False
            elif event.type == pygame.JOYHATMOTION:
                ps4.hat_data[event.hat] = event.value
            if ps4.button_data[0] == True:
                if s_f == False:
                    send_cmd('00/' + str(1500) + '/' + str(angle))
                    time.sleep(1)
                    s_f = True
            else:
                # Insert your code on what you would like to happen for each event here!
                # In the current setup, I have the state simply printing out to the screen.
                s_f = False
                #  os.system('clear')
                #pprint.pprint(ps4.button_data)
                # pprint.pprint(self.axis_data)
                #             pprint.pprint(self.hat_data)
                angle_rad = - ps4.axis_data[0]
                #second_gas = ps4.axis_data[4]
                #if dgas>=0:
                #    d_f = ((second_gas - d_f) * 1 / T_f * dt) + d_f
                #else:
                #    if second_gas>d_f:
                #        pass
                #    else:
                #        d_f = second_gas

                #dgas = second_gas - first_gas
                #first_gas = second_gas
                speed_rad = ps4.axis_data[4]-ps4.axis_data[5]

                # angle = (((U - oldmin) * newrange) / oldrange) + newmin
                angle = (((angle_rad - oldmin) * newrange) / oldrange) + newmin
                speed = (((speed_rad - oldmins) * newranges) / oldranges) + newmins
                # speed = (((Uf - oldminf) * newrangef) / oldrangef) + newminf
                if speed<1490:
                    if flag == False:
                        send_cmd('00/' + str(1400) + '/' + str(angle))
                        time.sleep(0.05)
                        send_cmd('00/' + str(1500) + '/' + str(angle))
                        time.sleep(0.05)
                        flag = True

                if speed >= 1500:
                    if flag == True:
                        flag = False
                        pass
                if speed >= 1640:
                    speed =1640
                send_cmd('00/' + str(speed) + '/' + str(angle))
                # print(dvy_f, dt, speed_ref_max, speed_ref)
                print(angle_rad, angle,speed_rad, speed)

                if not ps4.axis_data:
                    ps4.axis_data = {}

                if not ps4.button_data:

                    for i in range(ps4.controller.get_numbuttons()):
                        ps4.button_data[i] = False

                if not ps4.hat_data:

                    for i in range(ps4.controller.get_numhats()):
                        ps4.hat_data[i] = (0, 0)
                dt = time.time() - st
        if  ps4.button_data[2] == True:
            break