import dlib
from PIL import Image, ImageOps
import cv2
import numpy as np
import cairo
import rgbmatrix
from threading import Thread
import math
import constants_dlib
import face_dlib
import socket
import pickle
import struct

                                                            #Todo: Figure out what the fuck is going on with the face landmarks
                                                            #Todo: Make the face landmarks consistant by using a fixed box instead of object detector
def create_blank(width, height, rgb_color=(0, 0, 0)):
    image = np.zeros((height, width, 3), np.uint8)
    color = tuple(reversed(rgb_color))
    image[:] = color

    return image




def coord_value(mplm, width, height):
  sub_landmarks = str(mplm)
  #sub_landmarks = str(sub_landmarks)
  x = sub_landmarks.find("x=")
  s = sub_landmarks[x+3] + sub_landmarks[x+4] + sub_landmarks[x+5] + sub_landmarks[x+6] + sub_landmarks[x+7]
  s = s.replace(',', '')
  x = float(s)
  x = int(x * width)
  y = sub_landmarks.find("y=")
  s = sub_landmarks[y+3] + sub_landmarks[y+4] + sub_landmarks[y+5] + sub_landmarks[y+6] + sub_landmarks[y+7]
  s = s.replace(',', '')
  y = float(s)
  y = int(y * height)
  return [x, y]
  
def average(lst):
  return sum(lst) / len(lst)

def dist(x2, x1, y2, y1):
  return math.sqrt(((x2 - x1) ** 2) + ((y2 - y1) ** 2))
  
def calc_ref(x_coord, slope, offset):
  return (-slope * x_coord) + offset

def NormalizeData(data):
  return (data - np.min(data)) / (np.max(data) - np.min(data))

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

  
matrix = None

def render(face_landmarks, eye_r, eye_l, width, height, idle_x, idle_y, calibrated, center_mouth):
    DISPLAY_WIDTH = 64     # L_DISPLAY 0-64, R_DISPLAY = 65-128
    DISPLAY_HEIGHT = 32
    IM_SCALE = 4

    brightness = 0.8

    color = (255 * brightness, 0 * brightness , 0 * brightness)
    button = [0]
    mouth_x, mouth_y, eye_r_x, eye_r_y, calibrated, center_mouth, idle_x, idle_y = constants_dlib.process_landmarks(face_landmarks, eye_r, eye_l, width, height, button, calibrated, center_mouth, idle_x, idle_y)
                                                                #FaceCoords
    w, h = DISPLAY_WIDTH, DISPLAY_HEIGHT
    surface = cairo.ImageSurface (cairo.FORMAT_ARGB32, w, h)
    ctx = cairo.Context (surface)
    # creating a cairo context object
    x_scale = .5
    y_scale = -.3

    ctx = cairo.Context(surface)
    ctx.set_source_rgb(0, 0, 0)
    ctx.rectangle(0,0, width, height)
    ctx.fill()
    eye_l_y = "placeholder"
                                    # RightFace
    buf = face_dlib.main(ctx, mouth_x, mouth_y, eye_r_y, eye_l_y, surface, x_scale, y_scale, button) 		#Face File

    array = np.ndarray (shape=(h,w,4), dtype=np.uint8, buffer=buf)
    array = array[:,:,:3]

    ##  Draws Face Image from Mask

    image = create_blank(DISPLAY_WIDTH, DISPLAY_HEIGHT, rgb_color = color) #Makes blank bg image
    maskimage = array #Reads Mask image
    ret, maskimage = cv2.threshold(maskimage, 50, 255,cv2.THRESH_BINARY)    #Converts mask image to BW
    res = cv2.bitwise_and(image, maskimage)  #Mask the base image
    up_res = cv2.resize(res, (DISPLAY_WIDTH * IM_SCALE, DISPLAY_HEIGHT * IM_SCALE), 0, 0, interpolation = cv2.INTER_NEAREST)
    # cv2.imshow('up_res', up_res)  #Display Image


    #Convert the image from CV2 to PIL
    im_pil = Image.fromarray(res)
    img_out = Image.new('RGB', (DISPLAY_WIDTH*2, DISPLAY_HEIGHT)) #Create image with size of both panels
    img_out.paste(ImageOps.mirror(im_pil), (DISPLAY_WIDTH,0)) # Write mirrored image on R_Display
    img_out.paste(im_pil, (0, 0)) #Write image on L_Display

    # cv2.waitKey(1)

    matrix.SetImage(img_out) #Display on matricies
    #print("rendered")
    return calibrated, center_mouth, idle_x, idle_y




class ThreadedFace(object):
    def __init__(self, width, height):
        #self.detect_faces = FaceDetection()

        Face_detector_model = "models/detector.svm"
        Landmark_model = "models/predictor.dat"


        self.detect_faces = dlib.simple_object_detector(Face_detector_model)
        self.detect_face_landmarks = dlib.shape_predictor(Landmark_model)

        self.cap = cv2.VideoCapture('/dev/video0')
        #self.cap = cv2.VideoCapture(0)
        #self.cap = cv2.VideoCapture('/base/soc.i2c0mux/i2c@1/ov5647@36', cv2.CAP_V4L) gst-launch-1.0
        #self.cap = cv2.VideoCapture('libcamerasrc ! video/x-raw, width=320, height=240, framerate=30/1 ! videoconvert ! videoscale ! autovideosink', cv2.CAP_GSTREAMER)
        #self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
        
        self.width = width
        self.height = height


        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)

        self.cap.set(cv2.CAP_PROP_FPS, 60)

        self.face_landmarks = []

        self.thread = Thread(target=self.update, args=())
        self.thread.daemon = True
        self.thread.start()
        

    def update(self):
        while self.cap.isOpened():
            success, img = self.cap.read()
            img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
            if not success:
                print("Ignoring empty camera frame.")
                continue
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            face_detections = self.detect_faces(gray)
            if len(face_detections):
                # get ROI for the first face found
                face_roi = face_detections[0]
                #print("got roi")
                # detect face landmarks
                #self.face_landmarks = self.detect_face_landmarks(img, face_roi)
                self.landmarks = self.detect_face_landmarks(gray, face_roi)
                self.face_landmarks = []
                for n in range(0, 12):
                    x = self.landmarks.part(n).x
                    y = self.landmarks.part(n).y
                    lm = (x, y)
                    self.face_landmarks.append(lm)

                self.eye_r = "yeah"
                self.eye_l = "yeah"
            else:
                print('no face detected :(') 
        print('Capture didn' + "'" + 't open')


    def get_landmarks(self):
        return self.face_landmarks, self.eye_r, self.eye_l


def main():
    init()
    width = 320
    height = 240
    
    


#detector = dlib.get_frontal_face_detector()

    
    idle_x = []
    idle_y = []
    




    threaded_face = ThreadedFace(width, height)

    calibrated = False
    center_mouth = 0

    while True:
    


        try:
            face_landmarks, eye_r, eye_l = threaded_face.get_landmarks()
            if len(face_landmarks) > 0:
                calibrated, center_mouth, idle_x, idle_y = render(face_landmarks, eye_r, eye_l, width, height, idle_x, idle_y, calibrated, center_mouth)
        except AttributeError:
            #print("failed to render")
            pass




if __name__ == '__main__':

    main()


#sync in /mnt/x/Documents/GitHub/Protogen-Head-RPI: rsync -rP ./*.py pi@192.168.1.130:~/pc_sync
#powershell ssh: ssh pi@192.168.1.130
