#!/usr/bin/env python3

import numpy as np
from PIL import Image, ImageOps
from rgbmatrix import RGBMatrix, RGBMatrixOptions

#vars
matrix = None

FRAME_WIDTH = 64
FRAME_HEIGHT = 16
col = [255, 0, 0] #Color of pixels

eyearray = [
                [0x00, 0x00, 0x7C, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x83, 0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x02, 0x00, 0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x04, 0x00, 0x40, 0x00, 0x00, 0x00, 0x00, 0x00, 0x04, 0x00, 0x40, 0x00, 0x00, 0x00, 0x00, 0x00, 0x08, 0x00, 0x20, 0x00, 0x00, 0x00, 0x00, 0x00, 0x08, 0x00, 0x20, 0x00, 0x00, 0x00, 0x00, 0x00, 0x08, 0x00, 0x20, 0x00, 0x00, 0x00, 0x00, 0x00, 0x08, 0x00, 0x20, 0x00, 0x00, 0x00, 0x00, 0x00, 0x08, 0x00, 0x20, 0x00, 0x00, 0x00, 0x00, 0x00, 0x04, 0x00, 0x40, 0x00, 0x00, 0x00, 0x00, 0x00, 0x04, 0x00, 0x40, 0x00, 0x00, 0x00, 0x00, 0x00, 0x02, 0x00, 0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x83, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x7C, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],  #  1
           ]
moutharray = [
                [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x01, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00, 0x80, 0x02, 0x80, 0x02, 0x00, 0x00, 0x00, 0x00, 0x80, 0x04, 0x40, 0x02, 0x00, 0x00, 0x00, 0x00, 0x40, 0x08, 0x20, 0x04, 0x00, 0x00, 0x00, 0x00, 0x40, 0x10, 0x10, 0x08, 0x00, 0x00, 0x00, 0x00, 0x20, 0x20, 0x10, 0x10, 0x00, 0x00, 0x00, 0x00, 0x10, 0x40, 0x08, 0x10, 0x00, 0x00, 0x00, 0x00, 0x10, 0x80, 0x04, 0x20, 0x00, 0x00, 0x00, 0x00, 0x09, 0x00, 0x02, 0x40, 0x00, 0x00, 0x00, 0x00, 0x0A, 0x00, 0x01, 0x40, 0x00, 0x00, 0x00, 0x00, 0x04, 0x00, 0x00, 0x80],  #  1
             ]

#Functions down here

#Split a frame into its rows
def frame_to_rows(frame):
  size = int(FRAME_WIDTH/8)
  rows = []
  for i in range(0, len(frame), size):
    rows.append(frame[i:i+size])
  return rows

#Turn a row with single-bit pixels into a row with RGB pixels
def row_to_rgb(row, col_on, col_off):
  new_row = []
  for byte in row:
    for i in range(8):
      bit = byte >> 7-i & 1
      if bit == 1:
        new_row.append(col_on)
      else:
        new_row.append(col_off)
  return new_row

#Take pixel arrays and turn them into an image
def array_to_img(arr, on_col):
  arr2 = []
  for row in arr:
    arr2.append(row_to_rgb(row, on_col, [0,0,0]))
  return Image.fromarray(np.uint8(arr2)).convert("RGB")

#Take the current frame states and turn them into a image to send to the panels
def frames_to_img(eyeframe, mouthframe):
  eye = frame_to_rows(eyearray[eyeframe])
  mouth = frame_to_rows(moutharray[mouthframe])
  img = array_to_img(eye+mouth, col) #Generate base image
  
  img_out = Image.new('RGB', (img.width*2, img.height)) #Create image with size of both panels
  img_out.paste(ImageOps.mirror(img), (img.width,0)) #Gotta mirror one to make them face the right way
  img_out.paste(img, (0, 0))
  
  return img_out

def init():
  global matrix
  
  options = RGBMatrixOptions()
  options.rows = 32
  options.cols = 64
  options.chain_length = 2
  options.parallel = 1
  options.gpio_slowdown = 2
  options.hardware_mapping = 'adafruit-hat'
  matrix = RGBMatrix(options=options)
    
if __name__ == "__main__":
  init()
  img = frames_to_img(0, 0) #Generate image from states
  matrix.SetImage(img) #Show em
  print(img)
  while True:
    pass