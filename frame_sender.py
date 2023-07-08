#Standalone thread to receive frames

import socket
import pickle
import PIL
import struct
import cv2
import threading


def send_msg(sock, msg):                            
    # Prefix each message with a 4-byte length (network byte order)
    msg = struct.pack('>I', len(msg)) + msg
    sock.sendall(msg)

def recv_msg(sock):
    # Read message length and unpack it into an integer
    raw_msglen = recvall(sock, 4)
    if not raw_msglen:
        return None
    msglen = struct.unpack('>I', raw_msglen)[0]
    # Read the message data
    return recvall(sock, msglen)

def recvall(sock, n):
    # Helper function to recv n bytes or return None if EOF is hit
    data = bytearray()
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data.extend(packet)
    return data

                                # Establish a connection to the render server


image = cv2.cvtColor(cv2.imread('gradient.png'), cv2.COLOR_BGR2RGB)
#image = cv2.imread('gradient.png')
HOST = '192.168.1.191'
PORT = 50000
HEADERSIZE = 10
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
message = pickle.dumps(image)
send_msg(s, message)
