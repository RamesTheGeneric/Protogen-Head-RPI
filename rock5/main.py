import cv2
import time
import sys, os
from threading import Thread
from rknnpool import rknnPoolExecutor
import traceback
# Image processing function
from osc_receiver import OSCReceiver
from func import myFunc
from face_render import Render
from socket_blaster_class import SocketBlaster
'''
class CamStream():
    def __init__(self, url):
        self.cap = cv2.VideoCapture(url)
        self.frame = None
        self.thread = Thread(target=self.update, args=())
        self.thread.daemon = True
        self.thread.start()

    def update(self):
        while True:
            try: self.ret, self.frame = self.cap.read()
            except: sleep(1)
    
    def get_frame(self):
        return self.ret, self.frame
        '''

class DisplayStreamer():
    def __init__(self, rd, sb):
        self.rd = rd
        self.sb = sb
        self.predictions = None
        self.tracking = None
        self.emotes = None
        self.thread = Thread(target=self.send_display, args=())
        self.thread.daemon = True
        self.thread.start()
    
    def send_display(self):
        while True:
            try:
                predictions = self.rd.remap_shapes(self.predictions, self.tracking, self.emotes)
                face = self.rd.process_mesh(predictions)
                image = self.rd.draw_face(face)
                self.sb.set_frame(image)
            except Exception as e: 
                print(traceback.format_exc())
                time.sleep(1)

    def render_face(self, predictions, tracking, emotes):
        self.predictions = predictions
        self.tracking = tracking
        self.emotes = emotes




def main():
    cap = cv2.VideoCapture('http://192.168.1.236:8080/stream')
    rd = Render()
    sb = SocketBlaster()
    ds = DisplayStreamer(rd, sb)
    osc = OSCReceiver('192.168.1.128')
    modelPath = "./models/mobileoneRKNNE32.rknn"
    # NPU Cores
    TPEs = 3
    pool = rknnPoolExecutor(
        rknnModel=modelPath,
        TPEs=TPEs,
        func=myFunc)
    if (cap.isOpened()):
        for i in range(TPEs + 1):
            ret, frame = cap.read()
            if not ret:
                cap.release()
                del pool
                exit(-1)
            pool.put(frame)

    frames, loopTime, initTime = 0, time.time(), time.time()
    while (cap.isOpened()):
        frames += 1
        ret, frame = cap.read()
        if not ret:
            break
        pool.put(frame)
        predictions, flag = pool.get()
        tracking = osc.get_values()
        #   Render and Display functions here
        emotes = [0,0,0,0]  # Replace with input system
        ds.render_face(predictions, tracking, emotes)
        if flag == False:
            break
        if frames % 30 == 0:
            print("30 frame average:\t", 30 / (time.time() - loopTime), "frames")
            loopTime = time.time()

    print("Average Frame Rate\t", frames / (time.time() - initTime))
    # Release capture and RKNN thread pool
    cap.release()
    pool.release()

if __name__ == '__main__':
    while True:
        main()

