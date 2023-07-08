# Main Render Thread
import rgbmatrix
from frame_receiver import FrameReciever
from PIL import Image
import time
import numpy as np
import os
import subprocess
from pythonosc import udp_client
from icm20948 import ICM20948
from threading import Thread



class UStreamer():
  def __init__(self):
    self.thread = Thread(target=self.main, args=())
    self.thread.daemon = True
    self.thread.start()

  def main(self):
    subprocess.run(['bash start_ustreamer.sh'], shell=True)

def init():
  ustreamer = UStreamer()
  global matrix
  options = rgbmatrix.RGBMatrixOptions()
  options.rows = 32
  options.cols = 64
  options.chain_length = 2
  options.parallel = 1
  options.gpio_slowdown = 2
  options.hardware_mapping = 'adafruit-hat'
  #options.limit_refresh_rate_hz = 30
  matrix = rgbmatrix.RGBMatrix(options=options)

class Pages():
  def frame_reciever(self, fr):
    frame = fr.get_frame()
    return frame

  def noise(self):
    return Image.fromarray(np.random.randint(255, size=(128,32,3),dtype=np.uint8))

def main():
  imu = ICM20948()
  client = udp_client.SimpleUDPClient('192.168.1.128', 7175)  # It's faster to have this in the main thread for some reason
  pg = Pages()
  fr = FrameReciever('192.168.1.236') # PC Streamer for testing

  while True:
    start = time.time()

    page = 0
    if page == 0:
      frame = pg.frame_reciever(fr)

    if page == 1:
      frame = pg.noise()

    x, y, z = imu.read_magnetometer_data()
    ax, ay, az, gx, gy, gz = imu.read_accelerometer_gyro_data()
    client.send_message("/accelerometer_x", ax)
    client.send_message("/accelerometer_y", ay)
    client.send_message("/accelerometer_z", az)
    client.send_message("/gyro_x", gx)
    client.send_message("/gyro_y", gy)
    client.send_message("/gyro_z", gz)
    client.send_message("/mag_x", x)
    client.send_message("/mag_y", y)
    client.send_message("/mag_z", z)

    matrix.SetImage(frame)
    end = time.time()
    #print(1/(end-start))

if __name__ == '__main__':
  init()
  main()

