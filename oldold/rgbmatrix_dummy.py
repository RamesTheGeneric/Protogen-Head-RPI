import cv2
import numpy as np

def SetImage(img):
    img = np.array(img) 
    cv2.imshow('displays', img)
    