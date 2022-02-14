# For static images:
import math
import sys
import cv2
import mediapipe as mp
import numpy as np
import os
import PIL
#from lobe import ImageModel
from PIL import Image
from mediapipe.framework.formats import landmark_pb2
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_face_mesh = mp.solutions.face_mesh

#model = ImageModel.load('model/training_images TFLite')

color = (0, 0 ,0 )
def create_blank(width, height, rgb_color=(0, 0, 0)):
    """Create new image(numpy array) filled with certain color in RGB"""
    # Create black blank image
    image = np.zeros((height, width, 3), np.uint8)
    # Since OpenCV uses BGR, convert the color first
    color = tuple(reversed(rgb_color))
    # Fill image with color
    image[:] = color

    return image

def dist(x2, x1, y2, y1):
  return math.sqrt(((x2 - x1) ** 2) + ((y2 - y1) ** 2))

def NormalizeData(data):
  return (data - np.min(data)) / (np.max(data) - np.min(data))

def coord_value(mplm):
  sub_landmarks = np.asarray(mplm)
  sub_landmarks = str(sub_landmarks)
  x = sub_landmarks.find("x:")
  x = float(sub_landmarks[x+3] + sub_landmarks[x+4] + sub_landmarks[x+5] + sub_landmarks[x+6] + sub_landmarks[x+7])
  x = int(x * width)
  y = sub_landmarks.find("y:")
  y = float(sub_landmarks[y+3] + sub_landmarks[y+4] + sub_landmarks[y+5] + sub_landmarks[y+6] + sub_landmarks[y+7])
  y = int(y * height)
  return [x, y]




## Whole face 

drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
#cap = cv2.VideoCapture(0)
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
width = 640
height = 360
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
        '''
        mp_drawing.draw_landmarks(
            image=image,
            landmark_list=face_landmarks,
            connections=mp_face_mesh.FACEMESH_TESSELATION,
            landmark_drawing_spec=None,
            connection_drawing_spec=mp_drawing_styles
            .get_default_face_mesh_tesselation_style())
            '''
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

    # Mouth

    lm61 = coord_value(face_landmarks.landmark[61])
    lm0 = coord_value(face_landmarks.landmark[0])
    lm17 = coord_value(face_landmarks.landmark[17])
    lm291 = coord_value(face_landmarks.landmark[291])

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

              # Calculate EyeR Gaze coordinates (0.0 - 1.0)
              # x = 1.0 eye points towards face center
              # x = 0.0 eye points away face center
              # y = 1.0 eye points up
              # y = 0.0 eye points down

    distr_x = dist(outer_eyeR[0], inner_eyeR[0], outer_eyeR[1], inner_eyeR[1])
    distr_y = dist(lower_eyeR[0], upper_eyeR[0], lower_eyeR[1], upper_eyeR[1])
    x_refr = inner_eyeR[0] - int(distr_x / 2)
    y_refr = lower_eyeR[1] - int(distr_y / 2.4)
    puiple_distr_x = dist(outer_eyeR[0], puiple_R[0], outer_eyeR[1], puiple_R[1])
    puiple_distr_y = dist(lower_eyeR[0], puiple_R[0], lower_eyeR[1], puiple_R[1])
    image = cv2.circle(image, (x_refr, y_refr), 3, (0, 255, 0), 1)
    gazeR_x = puiple_distr_x / distr_x
    gazeR_x = NormalizeData([0.26, gazeR_x, 0.70])
    gazeR_y = puiple_distr_y / distr_y
    gazeR_y = NormalizeData([0.3225, gazeR_y, 0.6225])

    distl_x = dist(outer_eyeL[0], inner_eyeL[0], outer_eyeL[1], inner_eyeL[1])
    distl_y = dist(lower_eyeL[0], upper_eyeL[0], lower_eyeL[1], upper_eyeL[1])
    x_refl = (inner_eyeL[0] - int(distl_x / 2) * -1)
    y_refl = lower_eyeL[1] - int(distl_y / 2.4)
    puiple_distl_x = dist(outer_eyeL[0], puiple_L[0], outer_eyeL[1], puiple_L[1])
    puiple_distl_y = dist(lower_eyeL[0], puiple_L[0], lower_eyeL[1], puiple_L[1])
    image = cv2.circle(image, (x_refl, y_refl), 3, (0, 255, 0), 1)
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

    crop = image[p1y - buffer[1]:p2y + buffer[1], lm61[0] - buffer[0]:lm291[0] + buffer[0]]
    im_pil = Image.fromarray(crop)
    img_out = Image.new('RGB', (height, width))
    #result = model.predict(im_pil)
    cv2.imshow('MediaPipe Face Mesh', crop)
    cv2.imshow('camera', image)
    #print(result)
    if cv2.waitKey(5) & 0xFF == 27:
      break