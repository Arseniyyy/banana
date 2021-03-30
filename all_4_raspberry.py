# "All" file for raspberry. This file contain Server and Publisher instances, which works in infinite loop. Files executes consistently in the loop


from publisher_camera_4_raspberry_1_1 import Publisher
from server_car_auto_4_raspberry_class_1_1 import Raspberry_pi
from settings_1_1 import PORT
from settings_1_1 import FPS
import cv2


if __name__ == '__main__':
    # receiving video
    pub_instance = Publisher(src=0)
    pub_socket = pub_instance.create_pub_socket(port=PORT)

    # creating raspberry pi instance
    raspberry_pi = Raspberry_pi(ESC=17, min_value=1500, max_value=1700)
    raspberry_pi.config()

    while True:
        frame = pub_instance.get_frame()

        if frame is not None:
            encoded, buffer = cv2.imencode('.jpg', pub_instance.frame)
            pub_instance.send_data(pub_socket, buffer)

            raspberry_pi.main()

            if cv2.waitKey(FPS) == ord('q'):
                print('breaking...')
                break
