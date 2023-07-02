#以下代码改自https://github.com/rockchip-linux/rknn-toolkit2/tree/master/examples/onnx/yolov5
import cv2
import numpy as np
from pythonosc import udp_client

def myFunc(rknn_lite, img):
    img = img[0:480, 160:640]
    img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
    #img = img[160:640, 0:480]
    img = cv2.resize(img, (256, 256), interpolation = cv2.INTER_AREA)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = img.astype('float32')
    img /= 255.0
    img = img.reshape(1, 1, 256, 256)
    outputs = rknn_lite.inference(inputs=[img])
    x = outputs[0]
    '''
    output = np.exp(x)/np.sum(np.exp(x))
    outputs = [output]
    clamped = []
    for i in range(len(outputs[0][0])):  # Clip values between 0 - 1
        #print(outputs[0])
        clamped.append(max(min(outputs[0][0][i], 0.032), 0.0215))
    #max(0, min(new_index, len(mylist)-1))
    #newmulti = []
    newmulti = (x-np.min(clamped))/(np.max(clamped)-np.min(clamped))
    array = np.clip(newmulti, a_min = 0, a_max = 100)
    array = array[0]
    '''
    array = x[0]
    #print(array)
    #print(newmulti)


    OSCip="192.168.1.167" 
    OSCport= 9000 #VR Chat OSC port
    client = udp_client.SimpleUDPClient(OSCip, OSCport)
    location = ""
    multi = 100
    #print(array[0])
    client.send_message(location + "/cheekPuffLeft", array[0] * multi)
    client.send_message(location + "/cheekPuffRight", array[1] * multi)
    client.send_message(location + "/cheekSuckLeft", array[2] * multi)
    client.send_message(location + "/cheekSuckRight", array[3] * multi)
    client.send_message(location + "/jawOpen", array[4] * multi)
    client.send_message(location + "/jawForward", array[5] * multi)
    client.send_message(location + "/jawLeft", array[6] * multi)
    client.send_message(location + "/jawRight", array[7] * multi)
    client.send_message(location + "/noseSneerLeft", array[8] * multi)
    client.send_message(location + "/noseSneerRight", array[9] * multi)
    client.send_message(location + "/mouthFunnel", array[10] * multi)
    client.send_message(location + "/mouthPucker", array[11] * multi)
    client.send_message(location + "/mouthLeft", array[12] * multi)
    client.send_message(location + "/mouthRight", array[13] * multi)
    client.send_message(location + "/mouthRollUpper", array[14] * multi)
    client.send_message(location + "/mouthRollLower", array[15] * multi)
    client.send_message(location + "/mouthShrugUpper", array[16] * multi)
    client.send_message(location + "/mouthShrugLower", array[17] * multi)
    client.send_message(location + "/mouthClose", array[18] * multi)
    client.send_message(location + "/mouthSmileLeft", array[19] * multi)
    client.send_message(location + "/mouthSmileRight", array[20] * multi)
    client.send_message(location + "/mouthFrownLeft", array[21] * multi)
    client.send_message(location + "/mouthFrownRight", array[22] * multi)
    client.send_message(location + "/mouthDimpleLeft", array[23] * multi)
    client.send_message(location + "/mouthDimpleRight", array[24] * multi)
    client.send_message(location + "/mouthUpperUpLeft", array[25] * multi)
    client.send_message(location + "/mouthUpperUpRight", array[26] * multi)
    client.send_message(location + "/mouthLowerDownLeft", array[27] * multi)
    client.send_message(location + "/mouthLowerDownRight", array[28] * multi)
    client.send_message(location + "/mouthPressLeft", array[29] * multi)
    client.send_message(location + "/mouthPressRight", array[30] * multi)
    client.send_message(location + "/mouthStretchLeft", array[31] * multi)
    client.send_message(location + "/mouthStretchRight", array[32] * multi)
    client.send_message(location + "/tongueOut", array[33] * multi)
    client.send_message(location + "/tongueUp", array[34] * multi)
    client.send_message(location + "/tongueDown", array[35] * multi)
    client.send_message(location + "/tongueLeft", array[36] * multi)
    client.send_message(location + "/tongueRight", array[37] * multi)
    client.send_message(location + "/tongueRoll", array[38] * multi)
    client.send_message(location + "/tongueBendDown", array[39] * multi)
    client.send_message(location + "/tongueCurlUp", array[40] * multi)
    client.send_message(location + "/tongueSquish", array[41] * multi)
    client.send_message(location + "/tongueFlat", array[42] * multi)
    client.send_message(location + "/tongueTwistLeft", array[43] * multi)
    client.send_message(location + "/tongueTwistRight", array[44] * multi)
    return array
