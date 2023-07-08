import cv2



cap = cv2.VideoCapture("http://192.168.1.236:8080/stream")

while cap.isOpened():



    check, img = cap.read()
    #img = img[0:480, 160:640]
    img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
    img = cv2.resize(img, (256, 256), interpolation = cv2.INTER_AREA)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imshow('a',img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break