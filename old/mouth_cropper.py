

import math
import sys
import cv2
import mediapipe as mp
import numpy as np
from os import listdir
from os.path import isfile, join
from lobe import ImageModel
from PIL import Image
from mediapipe.framework.formats import landmark_pb2
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_face_mesh = mp.solutions.face_mesh

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



'''
onlyfiles = [f for f in listdir("idle_training") if isfile(join("idle_training", f))]
onlyfiles = [f for f in listdir("idle_training")]
list = onlyfiles
str = 'idle_training/'
onlyfiles = prepend(list, str)
#for len(onlyfiles)


#IMAGE_FILES = ["1.jpg", "2.jpg", "3.jpg", "4.jpg", "5.jpg", "6.jpg", "7.jpg", "8.jpg", "9.jpg", "10.jpg", "11.jpg", "12.jpg", "13.jpg", "14.jpg", '15.jpg', '16.jpg', '17.jpg', '18.jpg', '19.jpg', '20.jpg', '21.jpg', '22.jpg', "23.jpg", '24.jpg', '25.jpg', '26.jpg', '27.jpg', '28.jpg', '29.jpg']
#IMAGE_FILES = onlyfiles
IMAGE_FILES = ["1.jpg"]
drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
with mp_face_mesh.FaceMesh(
    static_image_mode=True,
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5) as face_mesh:
  for idx, file in enumerate(IMAGE_FILES):
    image = cv2.imread(file)
    # Convert the BGR image to RGB before processing.
    results = face_mesh.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

    # Print and draw face mesh landmarks on the image.
    if not results.multi_face_landmarks:
      continue
    
    height, width, channels = image.shape

    #annotated_image = image.copy()
    annotated_image = create_blank(width, height, rgb_color = color) #Makes blank bg image
            image=annotated_image
            landmark_list=face_landmarks,
            connections=mp_face_mesh.FACEMESH_TESSELATION,
            landmark_drawing_spec=None,
            connection_drawing_spec=mp_drawing_styles
            .get_default_face_mesh_tesselation_style())
        mp_drawing.draw_landmarks(
            image=annotated_image,
            landmark_list=face_landmarks,
            connections=mp_face_mesh.FACEMESH_CONTOURS,
            landmark_drawing_spec=None,
            connection_drawing_spec=mp_drawing_styles
            .get_default_face_mesh_contours_style())
        mp_drawing.draw_landmarks(
            image=annotated_image,
            landmark_list=face_landmarks,
            connections=mp_face_mesh.FACEMESH_IRISES,
            landmark_drawing_spec=None,
            connection_drawing_spec=mp_drawing_styles
            .get_default_face_mesh_iris_connections_style())

    sub_landmarks = np.asarray(face_landmarks.landmark[61])
    sub_landmarks = str(sub_landmarks)
    x = sub_landmarks.find("x:")
    x = float(sub_landmarks[x+3] + sub_landmarks[x+4] + sub_landmarks[x+5] + sub_landmarks[x+6] + sub_landmarks[x+7])
    x = int(x * width)
    y = sub_landmarks.find("y:")
    y = float(sub_landmarks[y+3] + sub_landmarks[y+4] + sub_landmarks[y+5] + sub_landmarks[y+6] + sub_landmarks[y+7])
    y = int(y * height)
    lm61 = [x, y]

    sub_landmarks = np.asarray(face_landmarks.landmark[0])
    sub_landmarks = str(sub_landmarks)
    x = sub_landmarks.find("x:")
    x = float(sub_landmarks[x+3] + sub_landmarks[x+4] + sub_landmarks[x+5] + sub_landmarks[x+6] + sub_landmarks[x+7])
    x = int(x * width)
    y = sub_landmarks.find("y:")
    y = float(sub_landmarks[y+3] + sub_landmarks[y+4] + sub_landmarks[y+5] + sub_landmarks[y+6] + sub_landmarks[y+7])
    y = int(y * height)
    lm0 = [x, y]

    sub_landmarks = np.asarray(face_landmarks.landmark[17])
    sub_landmarks = str(sub_landmarks)
    x = sub_landmarks.find("x:")
    x = float(sub_landmarks[x+3] + sub_landmarks[x+4] + sub_landmarks[x+5] + sub_landmarks[x+6] + sub_landmarks[x+7])
    x = int(x * width)
    y = sub_landmarks.find("y:")
    y = float(sub_landmarks[y+3] + sub_landmarks[y+4] + sub_landmarks[y+5] + sub_landmarks[y+6] + sub_landmarks[y+7])
    y = int(y * height)
    lm17 = [x, y]

    sub_landmarks = np.asarray(face_landmarks.landmark[291])
    sub_landmarks = str(sub_landmarks)
    x = sub_landmarks.find("x:")
    x = float(sub_landmarks[x+3] + sub_landmarks[x+4] + sub_landmarks[x+5] + sub_landmarks[x+6] + sub_landmarks[x+7])
    x = int(x * width)
    y = sub_landmarks.find("y:")
    y = float(sub_landmarks[y+3] + sub_landmarks[y+4] + sub_landmarks[y+5] + sub_landmarks[y+6] + sub_landmarks[y+7])
    y = int(y * height)
    lm291 = [x, y]


    #eyes R

    sub_landmarks = np.asarray(face_landmarks.landmark[468])
    sub_landmarks = str(sub_landmarks)
    x = sub_landmarks.find("x:")
    x = float(sub_landmarks[x+3] + sub_landmarks[x+4] + sub_landmarks[x+5] + sub_landmarks[x+6] + sub_landmarks[x+7])
    x = int(x * width)
    y = sub_landmarks.find("y:")
    y = float(sub_landmarks[y+3] + sub_landmarks[y+4] + sub_landmarks[y+5] + sub_landmarks[y+6] + sub_landmarks[y+7])
    y = int(y * height)
    puiple_R = [x, y]

    sub_landmarks = np.asarray(face_landmarks.landmark[33])
    sub_landmarks = str(sub_landmarks)
    x = sub_landmarks.find("x:")
    x = float(sub_landmarks[x+3] + sub_landmarks[x+4] + sub_landmarks[x+5] + sub_landmarks[x+6] + sub_landmarks[x+7])
    x = int(x * width)
    y = sub_landmarks.find("y:")
    y = float(sub_landmarks[y+3] + sub_landmarks[y+4] + sub_landmarks[y+5] + sub_landmarks[y+6] + sub_landmarks[y+7])
    y = int(y * height)
    outer_eyeR = [x, y]

    sub_landmarks = np.asarray(face_landmarks.landmark[133])
    sub_landmarks = str(sub_landmarks)
    x = sub_landmarks.find("x:")
    x = float(sub_landmarks[x+3] + sub_landmarks[x+4] + sub_landmarks[x+5] + sub_landmarks[x+6] + sub_landmarks[x+7])
    x = int(x * width)
    y = sub_landmarks.find("y:")
    y = float(sub_landmarks[y+3] + sub_landmarks[y+4] + sub_landmarks[y+5] + sub_landmarks[y+6] + sub_landmarks[y+7])
    y = int(y * height)
    inner_eyeR = [x, y]

    sub_landmarks = np.asarray(face_landmarks.landmark[27])
    sub_landmarks = str(sub_landmarks)
    x = sub_landmarks.find("x:")
    x = float(sub_landmarks[x+3] + sub_landmarks[x+4] + sub_landmarks[x+5] + sub_landmarks[x+6] + sub_landmarks[x+7])
    x = int(x * width)
    y = sub_landmarks.find("y:")
    y = float(sub_landmarks[y+3] + sub_landmarks[y+4] + sub_landmarks[y+5] + sub_landmarks[y+6] + sub_landmarks[y+7])
    y = int(y * height)
    upper_eyeR = [x, y]

    sub_landmarks = np.asarray(face_landmarks.landmark[23])
    sub_landmarks = str(sub_landmarks)
    x = sub_landmarks.find("x:")
    x = float(sub_landmarks[x+3] + sub_landmarks[x+4] + sub_landmarks[x+5] + sub_landmarks[x+6] + sub_landmarks[x+7])
    x = int(x * width)
    y = sub_landmarks.find("y:")
    y = float(sub_landmarks[y+3] + sub_landmarks[y+4] + sub_landmarks[y+5] + sub_landmarks[y+6] + sub_landmarks[y+7])
    y = int(y * height)
    lower_eyeR = [x, y]

  

    
    # eyes R

    sub_landmarks = np.asarray(face_landmarks.landmark[473])
    sub_landmarks = str(sub_landmarks)
    x = sub_landmarks.find("x:")
    x = float(sub_landmarks[x+3] + sub_landmarks[x+4] + sub_landmarks[x+5] + sub_landmarks[x+6] + sub_landmarks[x+7])
    x = int(x * width)
    y = sub_landmarks.find("y:")
    y = float(sub_landmarks[y+3] + sub_landmarks[y+4] + sub_landmarks[y+5] + sub_landmarks[y+6] + sub_landmarks[y+7])
    y = int(y * height)
    puiple_L = [x, y]

    sub_landmarks = np.asarray(face_landmarks.landmark[263])
    sub_landmarks = str(sub_landmarks)
    x = sub_landmarks.find("x:")
    x = float(sub_landmarks[x+3] + sub_landmarks[x+4] + sub_landmarks[x+5] + sub_landmarks[x+6] + sub_landmarks[x+7])
    x = int(x * width)
    y = sub_landmarks.find("y:")
    y = float(sub_landmarks[y+3] + sub_landmarks[y+4] + sub_landmarks[y+5] + sub_landmarks[y+6] + sub_landmarks[y+7])
    y = int(y * height)
    outer_eyeL = [x, y]

    sub_landmarks = np.asarray(face_landmarks.landmark[362])
    sub_landmarks = str(sub_landmarks)
    x = sub_landmarks.find("x:")
    x = float(sub_landmarks[x+3] + sub_landmarks[x+4] + sub_landmarks[x+5] + sub_landmarks[x+6] + sub_landmarks[x+7])
    x = int(x * width)
    y = sub_landmarks.find("y:")
    y = float(sub_landmarks[y+3] + sub_landmarks[y+4] + sub_landmarks[y+5] + sub_landmarks[y+6] + sub_landmarks[y+7])
    y = int(y * height)
    inner_eyeL = [x, y]

    sub_landmarks = np.asarray(face_landmarks.landmark[257])
    sub_landmarks = str(sub_landmarks)
    x = sub_landmarks.find("x:")
    x = float(sub_landmarks[x+3] + sub_landmarks[x+4] + sub_landmarks[x+5] + sub_landmarks[x+6] + sub_landmarks[x+7])
    x = int(x * width)
    y = sub_landmarks.find("y:")
    y = float(sub_landmarks[y+3] + sub_landmarks[y+4] + sub_landmarks[y+5] + sub_landmarks[y+6] + sub_landmarks[y+7])
    y = int(y * height)
    upper_eyeL = [x, y]

    sub_landmarks = np.asarray(face_landmarks.landmark[253])
    sub_landmarks = str(sub_landmarks)
    x = sub_landmarks.find("x:")
    x = float(sub_landmarks[x+3] + sub_landmarks[x+4] + sub_landmarks[x+5] + sub_landmarks[x+6] + sub_landmarks[x+7])
    x = int(x * width)
    y = sub_landmarks.find("y:")
    y = float(sub_landmarks[y+3] + sub_landmarks[y+4] + sub_landmarks[y+5] + sub_landmarks[y+6] + sub_landmarks[y+7])
    y = int(y * height)
    lower_eyeL = [x, y]

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
    #print(str(distr_x) + "   " + str(distl_x))
    print("GazeR X: " + str(gazeR_x[1]) + " GazeR Y: " + str(gazeR_y[1]) + " GazeL X: " + str(gazeL_x[1]) + " GazeL Y: " + str(gazeL_y[1]))

    # Crop the frame to the mouth with the given coords
    percentage = 2.5
    x = int(width * percentage / 100)
    y = int(height * percentage / 100)
    buffer = [x, y]     # Expands crop region by percentage of canvas
    p1y = min(lm0[1], lm61[1], lm291[1])
    p2y = max(lm17[1], lm61[1], lm291[1])

    crop = image[p1y - buffer[1]:p2y + buffer[1], lm61[0] - buffer[0]:lm291[0] + buffer[0]]
    cv2.imwrite("training_images/idle/" + 'test' + str(idx + 1) + '.png', crop)
    '''

import math
import sys
import cv2
import mediapipe as mp
import numpy as np
from os import listdir
from os.path import isfile, join
#from lobe import ImageModel
from PIL import Image
from mediapipe.framework.formats import landmark_pb2
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_face_mesh = mp.solutions.face_mesh





onlyfiles = [f for f in listdir("idle") if isfile(join("idle", f))]
# For static images:
IMAGE_FILES = onlyfiles
print(onlyfiles)
drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
with mp_face_mesh.FaceMesh(
    static_image_mode=True,
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5) as face_mesh:
  for idx, file in enumerate(IMAGE_FILES):
    image = cv2.imread(file)
    # Convert the BGR image to RGB before processing.
    results = face_mesh.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

    # Print and draw face mesh landmarks on the image.
    if not results.multi_face_landmarks:
      continue
    height, width, channels = image.shape
    annotated_image = create_blank(width, height, rgb_color = color) #Makes blank bg image
    for face_landmarks in results.multi_face_landmarks:
      print('face_landmarks:', face_landmarks)
      '''
      mp_drawing.draw_landmarks(
          image=annotated_image,
          landmark_list=face_landmarks,
          connections=mp_face_mesh.FACEMESH_TESSELATION,
          landmark_drawing_spec=None,
          connection_drawing_spec=mp_drawing_styles
          .get_default_face_mesh_tesselation_style())
        '''
      mp_drawing.draw_landmarks(
          image=annotated_image,
          landmark_list=face_landmarks,
          connections=mp_face_mesh.FACEMESH_CONTOURS,
          landmark_drawing_spec=None,
          connection_drawing_spec=mp_drawing_styles
          .get_default_face_mesh_contours_style())
      mp_drawing.draw_landmarks(
          image=annotated_image,
          landmark_list=face_landmarks,
          connections=mp_face_mesh.FACEMESH_IRISES,
          landmark_drawing_spec=None,
          connection_drawing_spec=mp_drawing_styles
          .get_default_face_mesh_iris_connections_style())
    sub_landmarks = np.asarray(face_landmarks.landmark[61])
    sub_landmarks = str(sub_landmarks)
    x = sub_landmarks.find("x:")
    x = float(sub_landmarks[x+3] + sub_landmarks[x+4] + sub_landmarks[x+5] + sub_landmarks[x+6] + sub_landmarks[x+7])
    x = int(x * width)
    y = sub_landmarks.find("y:")
    y = float(sub_landmarks[y+3] + sub_landmarks[y+4] + sub_landmarks[y+5] + sub_landmarks[y+6] + sub_landmarks[y+7])
    y = int(y * height)
    lm61 = [x, y]

    sub_landmarks = np.asarray(face_landmarks.landmark[0])
    sub_landmarks = str(sub_landmarks)
    x = sub_landmarks.find("x:")
    x = float(sub_landmarks[x+3] + sub_landmarks[x+4] + sub_landmarks[x+5] + sub_landmarks[x+6] + sub_landmarks[x+7])
    x = int(x * width)
    y = sub_landmarks.find("y:")
    y = float(sub_landmarks[y+3] + sub_landmarks[y+4] + sub_landmarks[y+5] + sub_landmarks[y+6] + sub_landmarks[y+7])
    y = int(y * height)
    lm0 = [x, y]

    sub_landmarks = np.asarray(face_landmarks.landmark[17])
    sub_landmarks = str(sub_landmarks)
    x = sub_landmarks.find("x:")
    x = float(sub_landmarks[x+3] + sub_landmarks[x+4] + sub_landmarks[x+5] + sub_landmarks[x+6] + sub_landmarks[x+7])
    x = int(x * width)
    y = sub_landmarks.find("y:")
    y = float(sub_landmarks[y+3] + sub_landmarks[y+4] + sub_landmarks[y+5] + sub_landmarks[y+6] + sub_landmarks[y+7])
    y = int(y * height)
    lm17 = [x, y]

    sub_landmarks = np.asarray(face_landmarks.landmark[291])
    sub_landmarks = str(sub_landmarks)
    x = sub_landmarks.find("x:")
    x = float(sub_landmarks[x+3] + sub_landmarks[x+4] + sub_landmarks[x+5] + sub_landmarks[x+6] + sub_landmarks[x+7])
    x = int(x * width)
    y = sub_landmarks.find("y:")
    y = float(sub_landmarks[y+3] + sub_landmarks[y+4] + sub_landmarks[y+5] + sub_landmarks[y+6] + sub_landmarks[y+7])
    y = int(y * height)
    lm291 = [x, y]


    #eyes R

    sub_landmarks = np.asarray(face_landmarks.landmark[468])
    sub_landmarks = str(sub_landmarks)
    x = sub_landmarks.find("x:")
    x = float(sub_landmarks[x+3] + sub_landmarks[x+4] + sub_landmarks[x+5] + sub_landmarks[x+6] + sub_landmarks[x+7])
    x = int(x * width)
    y = sub_landmarks.find("y:")
    y = float(sub_landmarks[y+3] + sub_landmarks[y+4] + sub_landmarks[y+5] + sub_landmarks[y+6] + sub_landmarks[y+7])
    y = int(y * height)
    puiple_R = [x, y]

    sub_landmarks = np.asarray(face_landmarks.landmark[33])
    sub_landmarks = str(sub_landmarks)
    x = sub_landmarks.find("x:")
    x = float(sub_landmarks[x+3] + sub_landmarks[x+4] + sub_landmarks[x+5] + sub_landmarks[x+6] + sub_landmarks[x+7])
    x = int(x * width)
    y = sub_landmarks.find("y:")
    y = float(sub_landmarks[y+3] + sub_landmarks[y+4] + sub_landmarks[y+5] + sub_landmarks[y+6] + sub_landmarks[y+7])
    y = int(y * height)
    outer_eyeR = [x, y]

    sub_landmarks = np.asarray(face_landmarks.landmark[133])
    sub_landmarks = str(sub_landmarks)
    x = sub_landmarks.find("x:")
    x = float(sub_landmarks[x+3] + sub_landmarks[x+4] + sub_landmarks[x+5] + sub_landmarks[x+6] + sub_landmarks[x+7])
    x = int(x * width)
    y = sub_landmarks.find("y:")
    y = float(sub_landmarks[y+3] + sub_landmarks[y+4] + sub_landmarks[y+5] + sub_landmarks[y+6] + sub_landmarks[y+7])
    y = int(y * height)
    inner_eyeR = [x, y]

    sub_landmarks = np.asarray(face_landmarks.landmark[27])
    sub_landmarks = str(sub_landmarks)
    x = sub_landmarks.find("x:")
    x = float(sub_landmarks[x+3] + sub_landmarks[x+4] + sub_landmarks[x+5] + sub_landmarks[x+6] + sub_landmarks[x+7])
    x = int(x * width)
    y = sub_landmarks.find("y:")
    y = float(sub_landmarks[y+3] + sub_landmarks[y+4] + sub_landmarks[y+5] + sub_landmarks[y+6] + sub_landmarks[y+7])
    y = int(y * height)
    upper_eyeR = [x, y]

    sub_landmarks = np.asarray(face_landmarks.landmark[23])
    sub_landmarks = str(sub_landmarks)
    x = sub_landmarks.find("x:")
    x = float(sub_landmarks[x+3] + sub_landmarks[x+4] + sub_landmarks[x+5] + sub_landmarks[x+6] + sub_landmarks[x+7])
    x = int(x * width)
    y = sub_landmarks.find("y:")
    y = float(sub_landmarks[y+3] + sub_landmarks[y+4] + sub_landmarks[y+5] + sub_landmarks[y+6] + sub_landmarks[y+7])
    y = int(y * height)
    lower_eyeR = [x, y]

  

    
    # eyes R

    sub_landmarks = np.asarray(face_landmarks.landmark[473])
    sub_landmarks = str(sub_landmarks)
    x = sub_landmarks.find("x:")
    x = float(sub_landmarks[x+3] + sub_landmarks[x+4] + sub_landmarks[x+5] + sub_landmarks[x+6] + sub_landmarks[x+7])
    x = int(x * width)
    y = sub_landmarks.find("y:")
    y = float(sub_landmarks[y+3] + sub_landmarks[y+4] + sub_landmarks[y+5] + sub_landmarks[y+6] + sub_landmarks[y+7])
    y = int(y * height)
    puiple_L = [x, y]

    sub_landmarks = np.asarray(face_landmarks.landmark[263])
    sub_landmarks = str(sub_landmarks)
    x = sub_landmarks.find("x:")
    x = float(sub_landmarks[x+3] + sub_landmarks[x+4] + sub_landmarks[x+5] + sub_landmarks[x+6] + sub_landmarks[x+7])
    x = int(x * width)
    y = sub_landmarks.find("y:")
    y = float(sub_landmarks[y+3] + sub_landmarks[y+4] + sub_landmarks[y+5] + sub_landmarks[y+6] + sub_landmarks[y+7])
    y = int(y * height)
    outer_eyeL = [x, y]

    sub_landmarks = np.asarray(face_landmarks.landmark[362])
    sub_landmarks = str(sub_landmarks)
    x = sub_landmarks.find("x:")
    x = float(sub_landmarks[x+3] + sub_landmarks[x+4] + sub_landmarks[x+5] + sub_landmarks[x+6] + sub_landmarks[x+7])
    x = int(x * width)
    y = sub_landmarks.find("y:")
    y = float(sub_landmarks[y+3] + sub_landmarks[y+4] + sub_landmarks[y+5] + sub_landmarks[y+6] + sub_landmarks[y+7])
    y = int(y * height)
    inner_eyeL = [x, y]

    sub_landmarks = np.asarray(face_landmarks.landmark[257])
    sub_landmarks = str(sub_landmarks)
    x = sub_landmarks.find("x:")
    x = float(sub_landmarks[x+3] + sub_landmarks[x+4] + sub_landmarks[x+5] + sub_landmarks[x+6] + sub_landmarks[x+7])
    x = int(x * width)
    y = sub_landmarks.find("y:")
    y = float(sub_landmarks[y+3] + sub_landmarks[y+4] + sub_landmarks[y+5] + sub_landmarks[y+6] + sub_landmarks[y+7])
    y = int(y * height)
    upper_eyeL = [x, y]

    sub_landmarks = np.asarray(face_landmarks.landmark[253])
    sub_landmarks = str(sub_landmarks)
    x = sub_landmarks.find("x:")
    x = float(sub_landmarks[x+3] + sub_landmarks[x+4] + sub_landmarks[x+5] + sub_landmarks[x+6] + sub_landmarks[x+7])
    x = int(x * width)
    y = sub_landmarks.find("y:")
    y = float(sub_landmarks[y+3] + sub_landmarks[y+4] + sub_landmarks[y+5] + sub_landmarks[y+6] + sub_landmarks[y+7])
    y = int(y * height)
    lower_eyeL = [x, y]

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
    #print(str(distr_x) + "   " + str(distl_x))
    print("GazeR X: " + str(gazeR_x[1]) + " GazeR Y: " + str(gazeR_y[1]) + " GazeL X: " + str(gazeL_x[1]) + " GazeL Y: " + str(gazeL_y[1]))

    # Crop the frame to the mouth with the given coords
    percentage = 2.5
    x = int(width * percentage / 100)
    y = int(height * percentage / 100)
    buffer = [x, y]     # Expands crop region by percentage of canvas
    p1y = min(lm0[1], lm61[1], lm291[1])
    p2y = max(lm17[1], lm61[1], lm291[1])

    crop = annotated_image[p1y - buffer[1]:p2y + buffer[1], lm61[0] - buffer[0]:lm291[0] + buffer[0]]
    cv2.imwrite("training_images/open/" + str(idx) + ".png", crop)
    print(idx)

