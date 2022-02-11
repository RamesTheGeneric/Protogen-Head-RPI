# For static images:
import math
import sys
import cv2
import mediapipe as mp
import numpy as np
#from lobe import ImageModel
from PIL import Image
from mediapipe.framework.formats import landmark_pb2
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_face_mesh = mp.solutions.face_mesh

#model = ImageModel.load('model/training_images TensorFlow')

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
  dist = math.sqrt(((x2 - x1) ** 2) + ((y2 - y1) ** 2))
  return dist


## Whole face 

"""
IMAGE_FILES = ["1.jpg", "2.jpg", "3.jpg", "4.jpg", "5.jpg", "6.jpg", "7.jpg", "8.jpg", "9.jpg", "10.jpg", "11.jpg", "12.jpg", "13.jpg", "14.jpg", '15.jpg', '16.jpg', '17.jpg', '18.jpg', '19.jpg', '20.jpg', '21.jpg', '22.jpg', "23.jpg", '24.jpg', '25.jpg', '26.jpg', '27.jpg', '28.jpg', '29.jpg']
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
    for face_landmarks in results.multi_face_landmarks:
      print('face_landmarks:', face_landmarks)
      mp_drawing.draw_landmarks(
          image=annotated_image,
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
    cv2.imwrite("training_images/New folder/" + 'test' + str(idx + 1) + '.png', annotated_image)
    cv2.imshow("Image", annotated_image)
    #cv2.waitKey(0)
    """

#IMAGE_FILES = ["1.jpg", "2.jpg", "3.jpg", "4.jpg", "5.jpg", "6.jpg", "7.jpg", "8.jpg", "9.jpg", "10.jpg", "11.jpg", "12.jpg", "13.jpg", "14.jpg", '15.jpg', '16.jpg', '17.jpg', '18.jpg', '19.jpg', '20.jpg', '21.jpg', '22.jpg', "23.jpg", '24.jpg', '25.jpg', '26.jpg', '27.jpg', '28.jpg', '29.jpg']
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
    for face_landmarks in results.multi_face_landmarks:
      #print('face_landmarks:', face_landmarks)
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
#    cv2.imwrite("training_images/New folder/" + 'test' + str(idx + 1) + '.png', annotated_image)

# Converts the specified mouth landmarks into a usable float to the nearest .001 and returns pixel coords
    
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

    sub_landmarks = np.asarray(face_landmarks.landmark[159])
    sub_landmarks = str(sub_landmarks)
    x = sub_landmarks.find("x:")
    x = float(sub_landmarks[x+3] + sub_landmarks[x+4] + sub_landmarks[x+5] + sub_landmarks[x+6] + sub_landmarks[x+7])
    x = int(x * width)
    y = sub_landmarks.find("y:")
    y = float(sub_landmarks[y+3] + sub_landmarks[y+4] + sub_landmarks[y+5] + sub_landmarks[y+6] + sub_landmarks[y+7])
    y = int(y * height)
    upper_eyeR = [x, y]

    sub_landmarks = np.asarray(face_landmarks.landmark[145])
    sub_landmarks = str(sub_landmarks)
    x = sub_landmarks.find("x:")
    x = float(sub_landmarks[x+3] + sub_landmarks[x+4] + sub_landmarks[x+5] + sub_landmarks[x+6] + sub_landmarks[x+7])
    x = int(x * width)
    y = sub_landmarks.find("y:")
    y = float(sub_landmarks[y+3] + sub_landmarks[y+4] + sub_landmarks[y+5] + sub_landmarks[y+6] + sub_landmarks[y+7])
    y = int(y * height)
    lower_eyeR = [x, y]

                # Calculate EyeL Gaze coordinates (0.0 - 1.0)
    distr_x = dist(outer_eyeR[0], inner_eyeR[0], outer_eyeR[1], inner_eyeR[1])
    distr_y = dist(lower_eyeR[0], upper_eyeR[0], lower_eyeR[1], upper_eyeR[1])
    puiple_distr_x = dist(outer_eyeR[0], puiple_R[0], outer_eyeR[1], puiple_R[1])
    puiple_distr_y = dist(lower_eyeR[0], puiple_R[0], lower_eyeR[1], puiple_R[1])
    gazeR_x = puiple_distr_x / distr_x
    gazeR_y = puiple_distr_y / distr_y
    print("GazeR X: " + str(gazeR_x))
    print("GazeR Y: " + str(gazeR_y))



    
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

    sub_landmarks = np.asarray(face_landmarks.landmark[163])
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

    sub_landmarks = np.asarray(face_landmarks.landmark[386])
    sub_landmarks = str(sub_landmarks)
    x = sub_landmarks.find("x:")
    x = float(sub_landmarks[x+3] + sub_landmarks[x+4] + sub_landmarks[x+5] + sub_landmarks[x+6] + sub_landmarks[x+7])
    x = int(x * width)
    y = sub_landmarks.find("y:")
    y = float(sub_landmarks[y+3] + sub_landmarks[y+4] + sub_landmarks[y+5] + sub_landmarks[y+6] + sub_landmarks[y+7])
    y = int(y * height)
    upper_eyeL = [x, y]

    sub_landmarks = np.asarray(face_landmarks.landmark[374])
    sub_landmarks = str(sub_landmarks)
    x = sub_landmarks.find("x:")
    x = float(sub_landmarks[x+3] + sub_landmarks[x+4] + sub_landmarks[x+5] + sub_landmarks[x+6] + sub_landmarks[x+7])
    x = int(x * width)
    y = sub_landmarks.find("y:")
    y = float(sub_landmarks[y+3] + sub_landmarks[y+4] + sub_landmarks[y+5] + sub_landmarks[y+6] + sub_landmarks[y+7])
    y = int(y * height)
    lower_eyeL = [x, y]





    #annotated_image = cv2.circle(annotated_image, (lm475[0], lm475[1]), 10, (0, 255, 0), 1)

    # Crop the frame to the mouth with the given coords
    percentage = 2.5
    x = int(width * percentage / 100)
    y = int(height * percentage / 100)
    buffer = [x, y]     # Expands crop region by percentage of canvas

    p1y = min(lm0[1], lm61[1], lm291[1])
    p2y = max(lm17[1], lm61[1], lm291[1])

    crop = annotated_image[p1y - buffer[1]:p2y + buffer[1], lm61[0] - buffer[0]:lm291[0] + buffer[0]]
    print("x: " + str(width) + " y: " + str(height))
    print("x: " + str(lm61[0]) + " y: " + str(lm0[1]))
    print("x: " + str(lm291[0]) + " y: " + str(lm17[1]))
    print("dist X: " + str(distr_x))
    print("dis Y: " + str(distr_y))
    print("buffer: " + str(buffer))
    
    scale_percent = 50 # percent of original size
    width = int(annotated_image.shape[1] * scale_percent / 100)
    height = int(annotated_image.shape[0] * scale_percent / 100)
    dim = (width, height)
 
    # resize image
    resized = cv2.resize(annotated_image, dim, interpolation = cv2.INTER_AREA)
    
    cv2.imshow("Image", resized)
    #cv2.imwrite("yeah.png", crop)
    cv2.waitKey(0)


'''

drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
#cap = cv2.VideoCapture(0)
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
width = 1920
height = 1080
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
    image.flags.writeable = True
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
        cv2.imwrite('yeah.png', image)
        result = model.predict_from_file(image)
        print(result)
    # Flip the image horizontally for a selfie-view display.
    cv2.imshow('MediaPipe Face Mesh', cv2.flip(image, 1))
    if cv2.waitKey(5) & 0xFF == 27:
      break
'''