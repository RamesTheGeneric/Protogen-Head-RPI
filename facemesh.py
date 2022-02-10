# For static images:
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
#    cv2.imwrite("training_images/New folder/" + 'test' + str(idx + 1) + '.png', annotated_image)

# Converts the specified mouth landmarks into a usable float to the nearest .001
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


    # Crop the frame to the mouth with the given coords

    crop = annotated_image[height - lm0[1]:lm61[0], height - lm17[1]:lm291[0]]
    print("x: " + str(width) + " y: " + str(height))
    print("x: " + str(lm61[0]) + " y: " + str(lm0[1]))
    print("x: " + str(lm291[0]) + " y: " + str(lm17[1]))
    '''
    scale_percent = 50 # percent of original size
    width = int(crop.shape[1] * scale_percent / 100)
    height = int(crop.shape[0] * scale_percent / 100)
    dim = (width, height)
 
    # resize image
    resized = cv2.resize(crop, dim, interpolation = cv2.INTER_AREA)
    '''
    cv2.imshow("Image", crop)
    cv2.imwrite("yeah.png", crop)
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