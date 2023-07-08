import requests
import numpy as np
import cv2
from PIL import Image
import rgbmatrix
import time
import socket
import base64
from os import nice
nice(10) # Raise priority

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

def main():
    BUFF_SIZE = 13000
    client_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    client_socket.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,BUFF_SIZE)
    host_name = socket.gethostname()
    host_ip = '192.168.1.167'#  socket.gethostbyname(host_name)
    print(host_ip)
    port = 9999
    message = b'Hello'

    client_socket.sendto(message,(host_ip,port))
    fps,st,frames_to_count,cnt = (0,0,20,0)

    while True:
        packet,_ = client_socket.recvfrom(BUFF_SIZE)
        data = base64.b64decode(packet,' /')
        npdata = np.fromstring(data,dtype=np.uint8)
        img = cv2.imdecode(npdata,1)
        img = Image.fromarray(img)
        matrix.SetImage(img)

init()

main()

