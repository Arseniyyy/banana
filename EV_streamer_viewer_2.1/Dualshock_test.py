import pickle
import time
import cv2 as cv
import multiprocessing
from multiprocessing import Pool
import socket
import numpy as np

oldmin = -1.6
oldmax = 1.6
newmin = 1250
newmax = 1700
oldrange = oldmax-oldmin
newrange = newmax-newmin

def send_cmd(cmd):
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Connect the socket to the port where the CarControl is listening
    #server_address = ('localhost', 1081)
    server_address = ('192.168.4.1', 1090)
    sock.connect(server_address)
    try:
        # Send data
        message = cmd.encode()

        sock.sendall(message)
    finally:

        sock.close()


        #angle = (((U - oldmin) * newrange) / oldrange) + newmin
        angle = (((angle_rad - oldmin) * newrange) / oldrange) + newmin
        speed = (((Uf - oldminf) * newrangef) / oldrangef) + newminf

        send_cmd('00/' + str(speed) + '/' + str(angle))
        #print(dvy_f, dt, speed_ref_max, speed_ref)
        print(angle_rad, angle,dx)








        ##time_counter += 200*dt
        ##print(time_counter)
        ##my_line_dblue(rook_image, ((int(10000 * float(dvy))), int(1 * time_counter)), ((int(10000 * float(dvy)), int(1 * (time_counter + 1)) )))
        ##cv.imshow(rook_window, rook_image)
        ##my_line_dblue(rook_image, (int(1 * time_counter), int(W/2)-int(1000 * float(dvy))), (int(1 * (time_counter + 5)), int(W/2)-int(1000 * float(dvy))))
        ##my_line_cyan(rook_image, (int(1 * time_counter), int(W/2)-int(1000 * float(dvy_f))), (int(1 * (time_counter + 5)), int(W/2)-int(1000 * float(dvy_f))))
        ##if time_counter>1000:
        ##    rook_image = np.zeros(size, dtype=np.uint8)
        ##    cv.imshow(rook_window, rook_image)
        ##    passrook_image = np.zeros(size, dtype=np.uint8)
        ##    time_counter = 0
        ##cv.imshow(rook_window, rook_image)