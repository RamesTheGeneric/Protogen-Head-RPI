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


Face_detector_detector_Model = "detector.svm"
Landmark_Model = "predictor.dat"


#detector = dlib.get_frontal_face_detector()
detector = dlib.simple_object_detector(Face_detector_detector_Model)
predictor = dlib.shape_predictor(Landmark_Model)
#predictor = dlib.shape_predictor("predictor.dat")
while True:
    _, frame = cap.read()
    frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    scale_percent = 100
    width = int(gray.shape[1] * scale_percent / 100)
    height = int(gray.shape[0] * scale_percent / 100)
    dim = (width, height)
    gray = cv2.resize(gray, dim, interpolation = cv2.INTER_AREA)

    faces = detector(gray)
    for face in faces:
        x1 = face.left()
        y1 = face.top()
        x2 = face.right()
        y2 = face.bottom()
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 3)

        landmarks = predictor(gray, face)
        lms = []
        for n in range(0, 12):
            x = landmarks.part(n).x
            y = landmarks.part(n).y
            lm = (x, y)
            lms.append(lm)
            print("x: " + str(x) + "y: " + str(y))
            cv2.circle(frame, (x, y), 4, (255, 0, 0), -1)
        print(lms)


    cv2.imshow("Frame", frame)

    key = cv2.waitKey(1)
    if key == 27:
        break