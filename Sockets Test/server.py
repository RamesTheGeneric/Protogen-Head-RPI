import socket
import struct
import pickle
import cv2
import imutils
import dlib

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
server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host_name  = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
host_ip = "192.168.1.187"
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
        #detector = dlib.get_frontal_face_detector()
        #predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

        #vid = cv2.VideoCapture("E:\Videos\Love.And.Monsters.2020.720p.mp4")
        while(vid.isOpened()):
            img,frame = vid.read()
            #frame = imutils.resize(frame,width=640)
            frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
            #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            #faces = detector(gray)
            #for face in faces:
            #    print(face)
            a = pickle.dumps(frame)
            message = struct.pack("Q",len(a))+a
            client_socket.sendall(message)
            
            #cv2.imshow('TRANSMITTING VIDEO',frame)
            key = cv2.waitKey(1) & 0xFF
            if key ==ord('q'):
                client_socket.close()
                