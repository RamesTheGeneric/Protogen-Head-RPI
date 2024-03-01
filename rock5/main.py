import cv2
import time
import sys, os
from threading import Thread
from rknnpool import rknnPoolExecutor
import traceback
import requests
import numpy as np
from osc_receiver import OSCReceiver
import process_mouth
import process_eyes
from face_render import Render
from socket_blaster_class import SocketBlaster



def rotate_image(image, angle):
    image_center = tuple(np.array(image.shape[1::-1]) / 2)
    rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
    result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], borderMode=cv2.BORDER_CONSTANT, flags=cv2.INTER_LINEAR)
    return result

class CamStream():
    def __init__(self, url):
        self.cap = cv2.VideoCapture(url)
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 2)
        self.cap.set(cv2.CAP_PROP_POS_AVI_RATIO, 1)
        self.frame = None
        self.thread = Thread(target=self.update, args=())
        self.thread.daemon = True
        self.thread.start()

    def update(self):
        while True:
            if self.cap.isOpened():
                try: 
                    self.ret, self.frame = self.cap.read()
                    #print("read frame")
                    time.sleep(0.016)
                except:
                    print('failed to read camera stream') 
                    time.sleep(1)
    
    def get_frame(self):
        return self.ret, self.frame
        

class DisplayStreamer():
    def __init__(self, rd, sb):
        self.rd = rd
        self.sb = sb
        self.predictions = None
        self.tracking = None
        self.emotes = None
        self.gazer = None
        self.thread = Thread(target=self.send_display, args=())
        self.thread.daemon = True
        self.thread.start()
    
    def send_display(self):
        while True:
            try:
                predictions = self.rd.remap_shapes(self.predictions, self.tracking, self.emotes, self.gazer)
                face = self.rd.process_mesh(predictions)
                image = self.rd.draw_face(face)
                self.sb.set_frame(image)
            except Exception as e: 
                print(traceback.format_exc())
                time.sleep(1)

    def render_face(self, predictions, tracking, emotes, gazer):
        self.predictions = predictions
        #print(predictions)
        self.tracking = tracking
        self.emotes = emotes
        self.gazer = gazer


def frame_transforms(frame):
    frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
    frame = rotate_image(frame, 14)
    m_frame = frame[140:320, 0 + 20:240 - 20] 
    l_frame = frame[20:140, 120:240] 
    r_frame = frame[90:120, 50:90]
    return m_frame, l_frame, r_frame

def main():
    #cap = cv2.VideoCapture('http://192.168.1.236:8080/stream')
    cam = CamStream('http://192.168.253.100:8080/stream')
    rd = Render()
    print('start SB')
    sb = SocketBlaster()
    ds = DisplayStreamer(rd, sb)
    osc = OSCReceiver('192.168.253.101')
    eye = process_eyes.EyeTracker()
    modelPath = "./models/mobileoneRKNNE32.rknn"
    # NPU Cores
    TPEs = 2
    mouth_pool = rknnPoolExecutor(rknnModel=modelPath,TPEs=TPEs,func=process_mouth.Func)
    #eye_l_pool = rknnPoolExecutor(rknnModel=modelPath,TPEs=TPEs,func=None)
    #eye_r_pool = rknnPoolExecutor(rknnModel=modelPath,TPEs=TPEs,func=None)
    if (cam.cap.isOpened()):
        for i in range(TPEs + 1):
            #ret, frame = cap.read()
            ret, frame = cam.get_frame()
            if not ret:
                cam.cap.release()
                del mouth_pool
                exit(-1)
            m_frame, l_frame, r_frame = frame_transforms(frame)
            mouth_pool.put(m_frame)


    frames, loopTime, initTime = 0, time.time(), time.time()
    print('start')
    while (cam.cap.isOpened()):
        frames += 1
        #print('ping')
        ret, frame = cam.get_frame()
        m_frame, l_frame, r_frame = frame_transforms(frame)
        if not ret:
            break
        mouth_pool.put(m_frame)
        predictions, flag = mouth_pool.get()
        tracking = osc.get_values()
        eye.Func(r_frame)
        eye.recalibrate_eyes(tracking["/recenter_eyes"])
        gaze_r = eye.get_gaze()

        #   Render and Display functions here
        #emotes = [0,0,0,1]   #  Drive with osc reciever
        emotes = [tracking["/eyes_angry"], tracking["/eyes_suprised"], tracking["/eyes_x"], tracking["/mouth_fangs"]]
        ds.render_face(predictions, tracking, emotes, gaze_r)
        if flag == False:
            break
        if frames % 30 == 0:
            #print("30 frame average:\t", 30 / (time.time() - loopTime), "frames")
            loopTime = time.time()

    print("Average Frame Rate\t", frames / (time.time() - initTime))
    # Release capture and RKNN thread pool
    cam.cap.release()
    mouth_pool.release()

if __name__ == '__main__':
    while True:
        try:
            main()
        except Exception as e: print(traceback.format_exc())

