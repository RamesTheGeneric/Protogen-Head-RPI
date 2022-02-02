#!/usr/bin/env python3
import numpy as np
from PIL import Image, ImageOps
import time, math, random, threading, os
import rgbmatrix
import cv2


matrix = None

DISPLAY_WIDTH = 64     # L_DISPLAY 0-64, R_DISPLAY = 65-128
DISPLAY_HEIGHT = 32
IM_SCALE = 4

color = (50, 200 , 50)

def init():
  global matrix
  
  options = rgbmatrix.RGBMatrixOptions()
  options.rows = 32
  options.cols = 64
  options.chain_length = 2
  options.parallel = 1
  options.gpio_slowdown = 2
  options.hardware_mapping = 'adafruit-hat'
  matrix = rgbmatrix.RGBMatrix(options=options)

def create_blank(width, height, rgb_color=(0, 0, 0)):
    """Create new image(numpy array) filled with certain color in RGB"""
    # Create black blank image
    image = np.zeros((height, width, 3), np.uint8)
    # Since OpenCV uses BGR, convert the color first
    color = tuple(reversed(rgb_color))
    # Fill image with color
    image[:] = color

    return image

#Running Code

image = create_blank(DISPLAY_WIDTH, DISPLAY_HEIGHT, rgb_color = color) #Makes blank bg image

maskimage = cv2.imread('images/testmask.png')   #Reads Mask image
ret, mask = cv2.threshold(maskimage, 127, 255,cv2.THRESH_BINARY)    #Converts mask image to BW
res = cv2.bitwise_and(image, mask)  #Mask the base image
up_res = cv2.resize(res, (DISPLAY_WIDTH * IM_SCALE, DISPLAY_HEIGHT * IM_SCALE), 0, 0, interpolation = cv2.INTER_NEAREST)
cv2.imshow('up_res', up_res)  #Display Image


#Convert the image from CV2 to PIL
init()
im_pil = Image.fromarray(res)
img_out = Image.new('RGB', (DISPLAY_WIDTH*2, DISPLAY_HEIGHT)) #Create image with size of both panels
img_out.paste(ImageOps.mirror(im_pil), (DISPLAY_WIDTH,0)) # Write mirrored image on R_Display
img_out.paste(im_pil, (0, 0)) #Write image on L_Display
matrix.SetImage(img_out) #Display on matricies

cv2.imshow('img_out', np.asarray(img_out))
cv2.waitKey(0)
