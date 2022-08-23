import socket
import struct
import pickle
import cv2
import imutils
import dlib
from timeit import default_timer as timer

'''
HEADERSIZE = 10

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), 1243))
s.listen(5)
while True:
    clientsocket, address = s.accept()
    print(f"Connection from {address} has been established!")
    img = cv2.imread("E:\Pictures\bals.jpg")
    d = {1: "Hey", 2: "There", 3: img}
    msg = pickle.dumps(d)
    msg = bytes(f'{len(msg):<{HEADERSIZE}}', 'utf-8') + msg
    clientsocket.send(msg)
'''

# Socket Create
mode = input("Select Mode (view, data)")
server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host_name  = socket.gethostname()
print(host_name)
host_ip = socket.gethostbyname(host_name)
host_ip = "192.168.137.130"
print('HOST IP:',host_ip)
port = 9999
socket_address = (host_ip,port)

# Socket Bind
server_socket.bind(socket_address)

# Socket Listen
server_socket.listen(5)
print("LISTENING AT:",socket_address)

# Socket Accept
while True:
    client_socket,addr = server_socket.accept()
    print('GOT CONNECTION FROM:',addr)
    if client_socket:
        vid = cv2.VideoCapture(0)
        vid.set(cv2.CAP_PROP_FPS, 60)
        vid.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
        vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

        detector = dlib.simple_object_detector("detector.svm")
        predictor = dlib.shape_predictor("predictor.dat")

        #vid = cv2.VideoCapture("E:\Videos\Love.And.Monsters.2020.720p.mp4")
        while(vid.isOpened()):
            img,frame = vid.read()
            #frame = imutils.resize(frame,width=640)
            frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = detector(gray)
            if (mode == "view"):
                for face in faces:
                    print(face)
                    x1 = face.left()
                    y1 = face.top()
                    x2 = face.right()
                    y2 = face.bottom()
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 3)
                    start = timer()
                    landmarks = predictor(gray, face)
                    end = timer()
                    print(end - start)
                    lms = []
                    
                    for n in range(0, 12):
                        x = landmarks.part(n).x
                        y = landmarks.part(n).y
                        lm = (x, y)
                        lms.append(lm)
                        print("x: " + str(x) + "y: " + str(y))
                        if not n == 0:
                            color = 255 / n 
                        else: 
                            color = 0
                        font = cv2.FONT_HERSHEY_SIMPLEX
    
                        # org
                        org = (x, y)
                        
                        # fontScale
                        fontScale = .3
                        
                        # Blue color in BGR
                        color = (255, 0, 0)
                        
                        # Line thickness of 2 px
                        thickness = 1
                        
                        # Using cv2.putText() method
                        cv2.putText(frame, str(n), org, font, 
                                        fontScale, color, thickness, cv2.LINE_AA)

                        #cv2.circle(frame, (x, y), 4, (int(color), 0, 0), -1)
                    print(lms)
                
                

            #debug shit






            a = pickle.dumps(frame)
            message = struct.pack("Q",len(a))+a
            client_socket.sendall(message)
            
            #cv2.imshow('TRANSMITTING VIDEO',frame)
            key = cv2.waitKey(1) & 0xFF
            if key ==ord('q'):
                client_socket.close()
                