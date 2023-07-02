import cv2
import time
from rknnpool import rknnPoolExecutor
# Image processing function
from func import myFunc

#cap = cv2.VideoCapture('./720p60hz.mp4')
cap = cv2.VideoCapture('http://192.168.1.236:8080/stream')
# cap = cv2.VideoCapture(0)
modelPath = "./models/mobileoneRKNNE32.rknn"
# NPU Cores
TPEs = 2
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
    frame, flag = pool.get()
    if flag == False:
        break
    '''
    cv2.imshow('test', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    '''
    if frames % 30 == 0:
        print("30 Average Frame Rate:\t", 30 / (time.time() - loopTime), "帧")
        loopTime = time.time()

print("Average Frame Rate\t", frames / (time.time() - initTime))
# Release capture and RKNN thread pool
cap.release()
#cv2.destroyAllWindows()
pool.release()
