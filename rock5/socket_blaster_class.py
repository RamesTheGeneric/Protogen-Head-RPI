
# This is server code to send video frames over UDP
import cv2, socket
import numpy as np
import time
import base64
import threading
import traceback


class SocketBlaster():

    def __init__(self):
        BUFF_SIZE = 13000
        self.server_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,BUFF_SIZE)
        host_ip = '192.168.253.101'#  socket.gethostbyname(host_name)
        self.client_ip = '192.168.253.100'
        print(host_ip)
        self.port = 7171
        socket_address = (host_ip,self.port)
        self.server_socket.bind(socket_address)
        print('Listening at:',socket_address)
        fps,st,frames_to_count,cnt = (0,0,20,0)
        self.frame = np.zeros((32,128,3), np.uint8)
        self.thread = threading.Thread(target=self.main, args=())
        self.thread.daemon = True
        self.thread.start()

    def set_frame(self, frame):
        self.frame = frame

    def main(self):
        while True:
            try:
                #while True:
                self.frame = cv2.resize(self.frame,(128, 32))
                self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
                encoded,buffer = cv2.imencode('.png',self.frame)
                message = base64.b64encode(buffer)
                self.server_socket.sendto(message,(self.client_ip, self.port))
                time.sleep(0.016)   # 60hz 0.016
            except Exception as error:
                print('closing Socket')
                self.server_socket.close()
                print(traceback.format_exc())


