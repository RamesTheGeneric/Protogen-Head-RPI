from pythonosc import osc_server
from pythonosc.dispatcher import Dispatcher
import threading

class OSCReceiver():
    def __init__(self, hostip):
        self.hostip = hostip
        self.values = {
            "/accelerometer_x": 0,
            "/accelerometer_y": 0,
            "/accelerometer_z": 0,
            "/gyro_x": 0,
            "/gyro_y": 0,
            "/gyro_z": 0,
            "/mag_x": 0,
            "/mag_y": 0,
            "/mag_z": 0
            }
        self.thread = threading.Thread(target=self.main, args=())
        self.thread.daemon = True
        self.thread.start()

    def message_handler(self, address, *args):
        #print(f"Received message: {address} {args[0]}")
        self.values[address] = float(args[0])

    def get_values(self):
        return self.values

    def main(self):
        dispatcher = Dispatcher()
        dispatcher.map("/gyro_x", self.message_handler)
        dispatcher.map("/accelerometer_x", self.message_handler)
        dispatcher.map("/accelerometer_y", self.message_handler)
        dispatcher.map("/accelerometer_z", self.message_handler)
        dispatcher.map("/gyro_x", self.message_handler)
        dispatcher.map("/gyro_y", self.message_handler)
        dispatcher.map("/gyro_z", self.message_handler)
        dispatcher.map("/mag_x", self.message_handler)
        dispatcher.map("/mag_y", self.message_handler)
        dispatcher.map("/mag_z", self.message_handler)
        server = osc_server.ThreadingOSCUDPServer((self.hostip, 7175), dispatcher)
        print("OSC server is running...")
        server.serve_forever()