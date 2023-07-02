# Main Render Thread
import rgbmatrix
from frame_receiver import FrameReciever
from PIL import Image
import time
import numpy as np
import os

def init():
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

