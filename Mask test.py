import numpy as np
from PIL import Image, ImageOps
import time, math, random, threading, os
import cv2

DISPLAY_WIDTH = 64
DISPLAY_HEIGHT = 32
color = (50, 200 , 50)

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
cv2.imshow('res', res)  #Display Image
cv2.waitKey(0)