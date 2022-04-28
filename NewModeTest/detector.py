'''
https://pysource.com/2019/03/12/face-landmarks-detection-opencv-with-python/

'''



import cv2
from cv2 import ROTATE_90_COUNTERCLOCKWISE
import numpy as np
import dlib

width = 320
height = 240


cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
model = "mouth_landmark.dat"
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(model)
#predictor = dlib.shape_predictor("predictor.dat")
print("Loaded Model: " + model)
while True:
    _, frame = cap.read()
    frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = detector(gray)
    for face in faces:
        x1 = face.left()
        y1 = face.top()
        x2 = face.right()
        y2 = face.bottom()
        #cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 3)

        landmarks = predictor(gray, face)

        for n in range(0, 20):
            x = landmarks.part(n).x
            y = landmarks.part(n).y
            cv2.circle(frame, (x, y), 4, (255, 0, 0), -1)


    cv2.imshow("Frame", frame)

    key = cv2.waitKey(1)
    if key == 27:
        break