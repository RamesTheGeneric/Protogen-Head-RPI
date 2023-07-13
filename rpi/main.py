# Main Render Thread
import rgbmatrix
from frame_receiver import FrameReciever
from PIL import Image
import time
import numpy as np
import os
import subprocess
import multiprocessing
from pythonosc import udp_client
import board
import adafruit_icm20x
from threading import Thread



class UStreamer():
  def __init__(self):
    self.thread = Thread(target=self.main, args=())
    self.thread.daemon = True
    self.thread.start()

  def main(self):
    subprocess.run(['bash start_ustreamer.sh'], shell=True)

class OSCReceiver():
  def __init__(self):
    self.client = udp_client.SimpleUDPClient('192.168.1.128', 7175)  # It's faster to have this in the main thread for some reason
    i2c = board.I2C()   # uses board.SCL and board.SDA
    self.imu = adafruit_icm20x.ICM20948(i2c, address=0x68)
    self.imu.accelerometer_data_rate = 1125
    self.imu.gyro_data_rate = 125
    self.process = multiprocessing.Process(target=self.main, args=())
    self.process.start()
    '''
    self.thread = Thread(target=self.main, args=())
    self.thread.daemon = True
    self.thread.start()
    '''

  def main(self):
    while True:
      start = time.time()
      x, y, z = self.imu.magnetic
      ax, ay, az = self.imu.acceleration
      gx, gy, gz = self.imu.gyro
      self.client.send_message("/accelerometer_x", ax)
      self.client.send_message("/accelerometer_y", ay)
      self.client.send_message("/accelerometer_z", az)
      self.client.send_message("/gyro_x", gx)
      self.client.send_message("/gyro_y", gy)
      self.client.send_message("/gyro_z", gz)
      self.client.send_message("/mag_x", x)
      self.client.send_message("/mag_y", y)
      self.client.send_message("/mag_z", z)
      end = time.time()
      print(1/(end-start))
      #time.sleep(0.0166)

def init():
  osc = OSCReceiver()
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
  pg = Pages()
  fr = FrameReciever('192.168.1.236') # PC Streamer for testing

  while True:
    start = time.time()

    page = 0
    if page == 0:
      frame = pg.frame_reciever(fr)

    if page == 1:
      frame = pg.noise()

    matrix.SetImage(frame)
    end = time.time()
    #print(1/(end-start))

if __name__ == '__main__':
  init()
  main()

