# For static images:
import cairo
import math
import sys
import cv2
import mediapipe as mp
import numpy as np
import os
import PIL
from PIL import Image, ImageOps
import time, math, random, threading, os
#import rgbmatrix
#from lobe import ImageModel
from PIL import Image
from mediapipe.framework.formats import landmark_pb2
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_face_mesh = mp.solutions.face_mesh
import keyboard

#model = ImageModel.load('model/training_images TFLite')
calibrated = False

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
    image = np.zeros((height, width, 3), np.uint8)
    color = tuple(reversed(rgb_color))
    image[:] = color

    return image



def average(lst):
  return sum(lst) / len(lst)

def dist(x2, x1, y2, y1):
  return math.sqrt(((x2 - x1) ** 2) + ((y2 - y1) ** 2))

def slope(x2, x1, y2, y1):
  return -((y2 - y1) / max((x2 - x1), 0.001))

def calc_ref(x_coord, slope, offset):
  return (-slope * x_coord) + offset

def NormalizeData(data):
  return (data - np.min(data)) / (np.max(data) - np.min(data))

def coord_value(mplm):                        #Fucking Awful
  sub_landmarks = np.asarray(mplm)
  sub_landmarks = str(sub_landmarks)
  x = sub_landmarks.find("x:")
  x = float(sub_landmarks[x+3] + sub_landmarks[x+4] + sub_landmarks[x+5] + sub_landmarks[x+6] + sub_landmarks[x+7])
  x = int(x * width)
  y = sub_landmarks.find("y:")
  y = float(sub_landmarks[y+3] + sub_landmarks[y+4] + sub_landmarks[y+5] + sub_landmarks[y+6] + sub_landmarks[y+7])
  y = int(y * height)
  return [x, y]
  
idle_x = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
idle_y = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]




## Whole face 

drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
#cap = cv2.VideoCapture(0)
cap = cv2.VideoCapture(1)
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
width = 640
height = 480

cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

with mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as face_mesh:
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      # If loading a video, use 'break' instead of 'continue'.
      continue

    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(image)

    # Draw the face mesh annotations on the image.
    image.flags.writeable = False
    #image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    height, width, channels = image.shape
    image = create_blank(width, height, rgb_color = color) #Makes blank bg image
    if results.multi_face_landmarks:
      for face_landmarks in results.multi_face_landmarks:
        
        mp_drawing.draw_landmarks(
            image=image,
            landmark_list=face_landmarks,
            connections=mp_face_mesh.FACEMESH_TESSELATION,
            landmark_drawing_spec=None,
            connection_drawing_spec=mp_drawing_styles
            .get_default_face_mesh_tesselation_style())
            
        mp_drawing.draw_landmarks(
            image=image,
            landmark_list=face_landmarks,
            connections=mp_face_mesh.FACEMESH_CONTOURS,
            landmark_drawing_spec=None,
            connection_drawing_spec=mp_drawing_styles
            .get_default_face_mesh_contours_style())
        mp_drawing.draw_landmarks(
            image=image,
            landmark_list=face_landmarks,
            connections=mp_face_mesh.FACEMESH_IRISES,
            landmark_drawing_spec=None,
            connection_drawing_spec=mp_drawing_styles
            .get_default_face_mesh_iris_connections_style())

    # Mouth Outer

    lm61 = coord_value(face_landmarks.landmark[61])   #RightCorner
    lm0 = coord_value(face_landmarks.landmark[0])   #Top
    lm17 = coord_value(face_landmarks.landmark[17])   #Bottom 
    lm291 = coord_value(face_landmarks.landmark[291])   #LeftCorner

    
    
    # Mouth Inner
    
    # RightDisplay             # LeftDisplay
    '''
      191 80  81  82  13  312 311 310 415
    78                                   308
      95  88  178 87  14  317 402 318 324
    '''

      
    lm78 = coord_value(face_landmarks.landmark[78])                 #Fuck
    lm191 = coord_value(face_landmarks.landmark[191])
    lm80 = coord_value(face_landmarks.landmark[80])
    lm81 = coord_value(face_landmarks.landmark[81])
    lm82 = coord_value(face_landmarks.landmark[82])
    lm13 = coord_value(face_landmarks.landmark[13])
    lm312 = coord_value(face_landmarks.landmark[312])
    lm311 = coord_value(face_landmarks.landmark[311])
    lm310 = coord_value(face_landmarks.landmark[310])
    lm415 = coord_value(face_landmarks.landmark[415])
    lm308 = coord_value(face_landmarks.landmark[308])
    lm324 = coord_value(face_landmarks.landmark[324])
    lm318 = coord_value(face_landmarks.landmark[318])
    lm402 = coord_value(face_landmarks.landmark[402])
    lm317 = coord_value(face_landmarks.landmark[317])
    lm14 = coord_value(face_landmarks.landmark[14])
    lm87 = coord_value(face_landmarks.landmark[87])
    lm178 = coord_value(face_landmarks.landmark[178])
    lm88 = coord_value(face_landmarks.landmark[88])
    lm95 = coord_value(face_landmarks.landmark[95])

    # eyes R

    puiple_R = coord_value(face_landmarks.landmark[468])
    outer_eyeR = coord_value(face_landmarks.landmark[33])
    inner_eyeR = coord_value(face_landmarks.landmark[133])
    upper_eyeR = coord_value(face_landmarks.landmark[27])
    lower_eyeR = coord_value(face_landmarks.landmark[23])

    # eyes R

    puiple_L = coord_value(face_landmarks.landmark[473])
    outer_eyeL = coord_value(face_landmarks.landmark[263])
    inner_eyeL = coord_value(face_landmarks.landmark[362])
    upper_eyeL = coord_value(face_landmarks.landmark[257])
    lower_eyeL = coord_value(face_landmarks.landmark[253])

    # Ref Points
    
    lm164 = coord_value(face_landmarks.landmark[164])   #First top point connecting to lips
    lm18 = coord_value(face_landmarks.landmark[18])   #First bottom point connecitng to lips
    x1, y1 = lm164
    x2, y2 = lm18
    center_mouth = [int(average([x1, x2])), int(average([y1, y2]))]

    try: 
      if keyboard.is_pressed('1') or calibrated == False:         #   REMOVE KEYBOARD CONDITION FOR RPI!
        print("BrUh")
        idle_x[0] = lm78[0] - center_mouth[0]
        idle_y[0] = lm78[1] - center_mouth[1]
        idle_x[1] = lm191[0] - center_mouth[0]
        idle_y[1] = lm191[1] - center_mouth[1]
        idle_x[2] = lm80[0] - center_mouth[0]
        idle_y[2] = lm80[1] - center_mouth[1]
        idle_x[3] = lm81[0] - center_mouth[0]
        idle_y[3] = lm81[1] - center_mouth[1]
        idle_x[4] = lm82[0] - center_mouth[0]
        idle_y[4] = lm82[1] - center_mouth[1]
        idle_x[5] = lm13[0] - center_mouth[0]
        idle_y[5] = lm13[1] - center_mouth[1]
        idle_x[6] = lm312[0] - center_mouth[0]
        idle_y[6] = lm312[1] - center_mouth[1]
        idle_x[7] = lm311[0] - center_mouth[0]
        idle_y[7] = lm311[1] - center_mouth[1]
        idle_x[8] = lm310[0] - center_mouth[0]
        idle_y[8] = lm310[1] - center_mouth[1]
        idle_x[9] = lm415[0] - center_mouth[0]
        idle_y[9] = lm415[1] - center_mouth[1]
        idle_x[10] = lm308[0] - center_mouth[0]
        idle_y[10] = lm308[1] - center_mouth[1]
        idle_x[11] = lm324[0] - center_mouth[0]
        idle_y[11] = lm324[1] - center_mouth[1]
        idle_x[12] = lm318[0] - center_mouth[0]
        idle_y[12] = lm318[1] - center_mouth[1]
        idle_x[13] = lm402[0] - center_mouth[0]
        idle_y[13] = lm402[1] - center_mouth[1]
        idle_x[14] = lm317[0] - center_mouth[0]
        idle_y[14] = lm317[1] - center_mouth[1]
        idle_x[15] = lm14[0] - center_mouth[0]
        idle_y[15] = lm14[1] - center_mouth[1]
        idle_x[16] = lm87[0] - center_mouth[0]
        idle_y[16] = lm87[1] - center_mouth[1]
        idle_x[17] = lm178[0] - center_mouth[0]
        idle_y[17] = lm178[1] - center_mouth[1]
        idle_x[18] = lm88[0] - center_mouth[0]
        idle_y[18] = lm88[1] - center_mouth[1]
        idle_x[19] = lm95[0] - center_mouth[0]
        idle_y[19] = lm95[1] - center_mouth[1]
        calibrated = True
        print("calib: " + str(idle_x))
      else:
        pass
    except:
      break
    #else:
      #print("KeyNotPressed")
    #print("Idle_X: " + str(idle_x) + " Idle_Y: " + str(idle_y))

    mouth_x = [idle_x[0] - (lm78[0] - center_mouth[0]), 
    idle_x[1] - (lm191[0] - center_mouth[0]), 
    idle_x[2] - (lm80[0] - center_mouth[0]), 
    idle_x[3] - (lm81[0] - center_mouth[0]), 
    idle_x[4] - (lm82[0] - center_mouth[0]), 
    idle_x[5] - (lm13[0] - center_mouth[0]), 
    idle_x[6] - (lm312[0] - center_mouth[0]), 
    idle_x[7] - (lm311[0] - center_mouth[0]), 
    idle_x[8] - (lm310[0] - center_mouth[0]), 
    idle_x[9] - (lm415[0] - center_mouth[0]), 
    idle_x[10] - (lm308[0] - center_mouth[0]), 
    idle_x[11] - (lm324[0] - center_mouth[0]), 
    idle_x[12] - (lm318[0] - center_mouth[0]),
    idle_x[13] - (lm402[0] - center_mouth[0]),
    idle_x[14] - (lm317[0] - center_mouth[0]),
    idle_x[15] - (lm14[0] - center_mouth[0]),
    idle_x[16] - (lm87[0] - center_mouth[0]),
    idle_x[17] - (lm178[0] - center_mouth[0]),
    idle_x[18] - (lm88[0] - center_mouth[0]),
    idle_x[19] - (lm95[0] - center_mouth[0])
    ]

    mouth_y = [idle_y[0] - (lm78[1] - center_mouth[1]
    ), 
    idle_y[1] - (lm191[1] - center_mouth[1]), 
    idle_y[2] - (lm80[1] - center_mouth[1]), 
    idle_y[3] - (lm81[1] - center_mouth[1]), 
    idle_y[4] - (lm82[1] - center_mouth[1]), 
    idle_y[5] - (lm13[1] - center_mouth[1]), 
    idle_y[6] - (lm312[1] - center_mouth[1]), 
    idle_y[7] - (lm311[1] - center_mouth[1]), 
    idle_y[8] - (lm310[1] - center_mouth[1]), 
    idle_y[9] - (lm415[1] - center_mouth[1]), 
    idle_y[10] - (lm308[1] - center_mouth[1]), 
    idle_y[11] - (lm324[1] - center_mouth[1]), 
    idle_y[12] - (lm318[1] - center_mouth[1]),
    idle_y[13] - (lm402[1] - center_mouth[1]),
    idle_y[14] - (lm317[1] - center_mouth[1]),
    idle_y[15] - (lm14[1] - center_mouth[1]),
    idle_y[16] - (lm87[1] - center_mouth[1]),
    idle_y[17] - (lm178[1] - center_mouth[1]),
    idle_y[18] - (lm88[1] - center_mouth[1]),
    idle_y[19] - (lm95[1] - center_mouth[1])
    ]




    image = cv2.circle(image, (center_mouth[0], center_mouth[1]), 3, (0, 255, 0), 1)



              # Calculate Eye Gaze coordinates (0.0 - 1.0)
              # x = 1.0 eye points towards face center
              # x = 0.0 eye points away face center
              # y = 1.0 eye points up
              # y = 0.0 eye points down

    distr_x = dist(outer_eyeR[0], inner_eyeR[0], outer_eyeR[1], inner_eyeR[1])
    distr_y = dist(lower_eyeR[0], upper_eyeR[0], lower_eyeR[1], upper_eyeR[1])
    puiple_distr_x = dist(outer_eyeR[0], puiple_R[0], outer_eyeR[1], puiple_R[1])
    puiple_distr_y = dist(lower_eyeR[0], puiple_R[0], lower_eyeR[1], puiple_R[1])
    gazeR_x = puiple_distr_x / distr_x
    gazeR_x = NormalizeData([0.26, gazeR_x, 0.70])
    gazeR_y = puiple_distr_y / distr_y
    gazeR_y = NormalizeData([0.3225, gazeR_y, 0.6225])

    distl_x = dist(outer_eyeL[0], inner_eyeL[0], outer_eyeL[1], inner_eyeL[1])
    distl_y = dist(lower_eyeL[0], upper_eyeL[0], lower_eyeL[1], upper_eyeL[1])
    puiple_distl_x = dist(outer_eyeL[0], puiple_L[0], outer_eyeL[1], puiple_L[1])
    puiple_distl_y = dist(lower_eyeL[0], puiple_L[0], lower_eyeL[1], puiple_L[1])
    gazeL_x = puiple_distl_x / distl_x
    gazeL_x = NormalizeData([0.26, gazeL_x, 0.70])
    gazeL_y = puiple_distl_y / distl_y
    gazeL_y = NormalizeData([0.3225, gazeL_y, 0.6225])


    print("GazeR X: " + str(gazeR_x[1]) + " GazeR Y: " + str(gazeR_y[1]) + " GazeL X: " + str(gazeL_x[1]) + " GazeL Y: " + str(gazeL_y[1]))

    # Crop the frame to the mouth with the given coords
    percentage = 2.5
    x = int(width * percentage / 100)
    y = int(height * percentage / 100)
    buffer = [x, y]     # Expands crop region by percentage of canvas
    p1y = min(lm0[1], lm61[1], lm291[1])
    p2y = max(lm17[1], lm61[1], lm291[1])
    p1y = min(p1y, height - 25)
    p2y = min(p2y, height - 5)

    crop = image[p1y - buffer[1]:p2y + buffer[1], lm61[0] - buffer[0]:lm291[0] + buffer[0]]
    #im_pil = Image.fromarray(crop)
    img_out = Image.new('RGB', (height, width))
    #result = model.predict(im_pil)
    cv2.imshow('MediaPipe Face Mesh', crop)
    cv2.imshow('camera', image)

                                                ##  Draws Face Mask From Vectors
    
    
    w, h = DISPLAY_WIDTH, DISPLAY_HEIGHT
    surface = cairo.ImageSurface (cairo.FORMAT_ARGB32, w, h)
    ctx = cairo.Context (surface)

    # creating a cairo context object
    x_scale = 3
    y_scale = 0.5

    ctx = cairo.Context(surface)
    ctx.set_source_rgb(0, 0, 0)
    ctx.rectangle(0,0, width, height)
    ctx.fill()

                                      # RightFace
    ctx.set_source_rgb(1, 1, 1)
    # Mouth coord driven face
    ctx.move_to(64, 23 - (mouth_y[5] * y_scale))
    ctx.line_to(52 - (mouth_x[4] * x_scale), 26 - (mouth_y[4] * y_scale))
    ctx.line_to(49 - (mouth_x[3] * x_scale), 22 - (mouth_y[3] * y_scale))
    ctx.line_to(42 - (mouth_x[2] * x_scale), 24 - (mouth_y[2] * y_scale))
    ctx.line_to(24 - (mouth_x[0] * x_scale), 17 - (mouth_y[0] * y_scale))
    ctx.line_to(24 - (mouth_x[0] * x_scale), 18 - (mouth_y[0] * y_scale))
    ctx.line_to(26 - (mouth_x[0] * x_scale), 19 - (mouth_y[0] * y_scale))
    ctx.line_to(42 - (mouth_x[18] * x_scale), 25 - (mouth_y[18] * y_scale))
    ctx.line_to(48 - (mouth_x[17] * x_scale), 23 - (mouth_y[17] * y_scale))
    ctx.line_to(51 - (mouth_x[16] * x_scale), 27 - (mouth_y[16] * y_scale))
    ctx.line_to(64, 24 - (mouth_y[15] * y_scale))

    # making close path
    ctx.fill()


                                      # Eye
    ctx.move_to(1, 0)
    ctx.line_to(26, 0)
    ctx.line_to(30, 4)
    ctx.line_to(26, 8)
    ctx.line_to(20, 8)
    ctx.line_to(1, 2.5)
    ctx.fill()
    # getting fill extends
    buf = surface.get_data()
    array = np.ndarray (shape=(h,w,4), dtype=np.uint8, buffer=buf)
    array = array[:,:,:3]


    cv2.imshow("array", array)
    
    # printing message when file is saved



                                                    ##  Draws Face Image from Mask

    image = create_blank(DISPLAY_WIDTH, DISPLAY_HEIGHT, rgb_color = color) #Makes blank bg image
    maskimage = array #Reads Mask image
    ret, maskimage = cv2.threshold(maskimage, 50, 255,cv2.THRESH_BINARY)    #Converts mask image to BW
    cv2.imshow("yeah", maskimage)
    res = cv2.bitwise_and(image, maskimage)  #Mask the base image
    #up_res = cv2.resize(res, (DISPLAY_WIDTH * IM_SCALE, DISPLAY_HEIGHT * IM_SCALE), 0, 0, interpolation = cv2.INTER_NEAREST)
    #cv2.imshow('up_res', up_res)  #Display Image


    #Convert the image from CV2 to PIL
    #init()
    im_pil = Image.fromarray(res)
    img_out = Image.new('RGB', (DISPLAY_WIDTH*2, DISPLAY_HEIGHT)) #Create image with size of both panels
    img_out.paste(ImageOps.mirror(im_pil), (DISPLAY_WIDTH,0)) # Write mirrored image on R_Display
    img_out.paste(im_pil, (0, 0)) #Write image on L_Display
    #matrix.SetImage(img_out) #Display on matricies

    up_res = cv2.resize(res, (DISPLAY_WIDTH * IM_SCALE, DISPLAY_HEIGHT * IM_SCALE), 0, 0, interpolation = cv2.INTER_NEAREST)
    cv2.imshow('img_out', np.asarray(up_res))
    #print(p1y)
    #print(p2y)
    #print(result)
    
    if cv2.waitKey(5) & 0xFF == 27:
      break