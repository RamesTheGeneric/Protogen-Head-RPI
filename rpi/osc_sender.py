from pythonosc import udp_client
from icm20948 import ICM20948
import threading 
from time import sleep



class OSCSender():
    def __init__(self, clientip):
        OSCip=clientip 
        OSCport= 7170 # GenericProtogen port
        self.client = udp_client.SimpleUDPClient(OSCip, OSCport)
        self.imu = ICM20948()
        self.thread = threading.Thread(target=self.main, args=())
        self.thread.daemon = True
        self.thread.start()

    def main(self):
        while True:
            try:
                x, y, z = self.imu.read_magnetometer_data()
                ax, ay, az, gx, gy, gz = self.imu.read_accelerometer_gyro_data()
                
                self.client.send_message("/accelerometer_x", ax)
                self.client.send_message("/accelerometer_y", ay)
                self.client.send_message("/accelerometer_z", az)
                self.client.send_message("/gyro_x", gx)
                self.client.send_message("/gyro_y", gy)
                self.client.send_message("/gyro_z", gz)
                self.client.send_message("/mag_x", x)
                self.client.send_message("/mag_y", y)
                self.client.send_message("/mag_z", z)
                sleep(0.0166)
            except: pass

