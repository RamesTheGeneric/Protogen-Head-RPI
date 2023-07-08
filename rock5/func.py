#以下代码改自https://github.com/rockchip-linux/rknn-toolkit2/tree/master/examples/onnx/yolov5
import cv2
import numpy as np
from pythonosc import udp_client

def myFunc(rknn_lite, img):
    img = img[0:480, 160:640]   # Crop lower mouth portion of the camera frame 
    img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
    #img = img[160:640, 0:480]
    img = cv2.resize(img, (256, 256), interpolation = cv2.INTER_AREA)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = img.astype('float32')
    img /= 255.0
    img = img.reshape(1, 1, 256, 256)
    outputs = rknn_lite.inference(inputs=[img])
    array = outputs[0][0]
    for i in range(len(array)):  # Clip values between 0 - 1
        array[i] = max(min(array[i], 1), 0)
    return array
