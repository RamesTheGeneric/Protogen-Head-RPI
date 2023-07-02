import numpy as np
import socket
from threading import Thread
from PIL import Image
import cv2
import base64
import numpy as np

class FrameReciever():

    def __init__(self, url):
        print('UDP Server Started!')
        self.img = Image.fromarray(np.random.randint(255, size=(128,32,3),dtype=np.uint8))
        self.ip = url
        self.port = 7171
        self.BUFF_SIZE = 13000
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,self.BUFF_SIZE)
        print(str(self.ip) + str(self.port))
        socket_address = (self.ip,self.port)
        self.sock.bind(socket_address)
        #print(f'Hostname: {self.hostname}')
        print(f'Start listening to {self.ip}:{self.port}')
        self.thread = Thread(target=self.listen, args=())
        self.thread.daemon = True
        self.thread.start()

    def listen(self):
        self.data = None
        while True:
            self.data, self.addr = self.sock.recvfrom(self.BUFF_SIZE)
            self.data = base64.b64decode(self.data,' /')
            self.npdata = np.fromstring(self.data,dtype=np.uint8)
            self.npdata = cv2.imdecode(self.npdata,1)
            self.img = Image.fromarray(self.npdata)

    def get_frame(self):
        return self.img

'''
    def main():
        BUFF_SIZE = 13000
        client_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        client_socket.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,BUFF_SIZE)
        host_name = socket.gethostname()
        host_ip = '192.168.1.167'#  socket.gethostbyname(host_name)
        print(host_ip)
        port = 9999
        message = b'Hello'

        client_socket.sendto(message,(host_ip,port))
        fps,st,frames_to_count,cnt = (0,0,20,0)

        while True:
            packet,_ = client_socket.recvfrom(BUFF_SIZE)
            data = base64.b64decode(packet,' /')
            npdata = np.fromstring(data,dtype=np.uint8)
            img = cv2.imdecode(npdata,1)
            img = Image.fromarray(img)
            matrix.SetImage(img)
'''