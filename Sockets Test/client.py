import socket
import pickle
import cv2
import struct
from time import sleep
'''
HEADERSIZE = 10

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostname(), 1243))

while True:
    full_msg = b''
    new_msg = True
    while True:
        msg = s.recv(16)
        if new_msg:
            print("new msg len:",msg[:HEADERSIZE])
            msglen = int(msg[:HEADERSIZE])
            new_msg = False

        print(f"full message length: {msglen}")

        full_msg += msg

        print(len(full_msg))

        if len(full_msg)-HEADERSIZE == msglen:
            print("full msg recvd")
            print(full_msg[HEADERSIZE:])
            print(pickle.loads(full_msg[HEADERSIZE:]))
            new_msg = True
            full_msg = b""
            '''


# create socket
mode = input('Select mode (view, data): ')
if (mode == 'data'):
    count = int(input('starting value for the counter: '))
    end = int(input('end value for the counter: '))
else: 
    count = 0
    end = 1

client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host_ip = 'protohead' # paste your server ip address here
port = 9999
client_socket.connect((host_ip,port)) # a tuple
data = b""
payload_size = struct.calcsize("Q")
while True:
    while len(data) < payload_size:
        packet = client_socket.recv(8*1024) # 4K
        if not packet: break
        data+=packet
    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack("Q",packed_msg_size)[0]
    
    while len(data) < msg_size:
        data += client_socket.recv(4*1024)
    frame_data = data[:msg_size]
    data  = data[msg_size:]
    frame = pickle.loads(frame_data)
    #frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
    cv2.imshow("RECEIVING VIDEO",frame)
    if mode == 'data':
        cv2.imwrite(str(count) + ".png", frame)
    count += 1
    key = cv2.waitKey(1) & 0xFF
    if key  == ord('q') or (count == end and mode == 'data'):
        break
client_socket.close()
    