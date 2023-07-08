
# This is client code to send imu data over UDP
import cv2, socket
from icm20948 import ICM20948
import numpy as np
import time
import base64
import threading
import pickle


class IMUBlaster():

    def __init__(self, client_ip):
        BUFF_SIZE = 128 
        self.server_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,BUFF_SIZE)
        host_ip = '192.168.1.236'#  socket.gethostbyname(host_name)
        self.client_ip = '192.168.1.128'
        print(host_ip)
        self.port = 7170
        socket_address = (host_ip,self.port)
        self.server_socket.bind(socket_address)
        print('Listening at:',socket_address)
        self.imu = ICM20948()
        self.imu_data = {}
        self.thread = threading.Thread(target=self.main, args=())
        self.thread.daemon = True
        self.thread.start()

    def main(self):
        while True:
            x, y, z = self.imu.read_magnetometer_data()
            ax, ay, az, gx, gy, gz = self.imu.read_accelerometer_gyro_data()
            self.imu_data = {
                "acc": [ax, ay, az],
                "gy": [gx, gy, gz],
                "mag": [x, y, z]
                }
            #print(self.imu_data)
            message = pickle.dumps(self.imu_data)
            self.server_socket.sendto(message,(self.client_ip, self.port))
            time.sleep(0.016)

    def get_imu(self):
        return self.imu_data






