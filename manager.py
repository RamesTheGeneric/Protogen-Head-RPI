from venv import create
import rgbmatrix
import cv2
import socket
import numpy as np
import subprocess
from threading import Thread
from PIL import Image
from time import sleep


def create_blank(width, height, rgb_color=(0, 0, 0)):
    image = np.zeros((height, width, 3), np.uint8)
    color = tuple(reversed(rgb_color))
    image[:] = color
    return image

def matrix_init():
  
  global matrix
  options = rgbmatrix.RGBMatrixOptions()
  options.rows = 32
  options.cols = 64
  options.chain_length = 2
  options.parallel = 1
  options.gpio_slowdown = 2
  options.hardware_mapping = 'adafruit-hat'
  matrix = rgbmatrix.RGBMatrix(options=options)

def render(res):                    # Takes a PIL image and writes it to the displays
    im_pil = Image.fromarray(res)
    img_out = Image.new('RGB', (64*2, 32))
    img_out.paste(im_pil, (0, 0))
    matrix.SetImage(img_out) #Display on matricies

def draw_text(res, org, fontScale, color, thickness, letters):              # Draws text 
    font = cv2.FONT_HERSHEY_SIMPLEX
    res = cv2.putText(res, letters, org, font, fontScale, color, thickness, cv2.LINE_AA)

class Tick():           # multithreaded counter going from 0-10 every minute
    def __init__(self):
        self.current_tick = 0
        self.thread = Thread(target=self.tick, args=())
        self.thread.daemon = True
        self.thread.start()
    def tick(self):
        while True:
            sleep(6)
            if self.current_tick >= 10:
                self.current_tick = 0
            else:
                self.current_tick += 1
            print(f'current thread tick: {self.current_tick}')
            
    def get_tick(self):
        return self.current_tick


class Info():
    def draw(res):
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        draw_text(res, (0, 30), 0.40, (255, 150, 0), 1, ip)
        draw_text(res, (0, 10), 0.40, (255, 150, 0), 1, "AP: ")
        if any('10.0.0.' in s for s in str(ip)):
            ap = 'protohead'
            draw_text(res, (25, 10), 0.40, (255, 150, 0), 1, ap)
        else:                                           # If host ip isn't one from the host AP, show the connected ssid
            ap = subprocess.check_output(['iwgetid', '-r']).decode('utf-8').split('\n')
            draw_text(res, (25, 10), 0.35, (255, 150, 0), 1, str(ap))




def main():
    matrix_init()
    tick_class = Tick()
    while True:

        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        res = create_blank(128, 32)
        Info.draw(res)
        tick = str(tick_class.get_tick())
        draw_text(res, (0, 20), 0.30, (0, 150, 0), 1, tick)
        render(res)
        #ip = '192.168.137.130'
    



main()






