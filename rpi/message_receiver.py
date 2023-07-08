#Standalone thread to receive frames
import socket
import pickle
from PIL import Image
import struct
from threading import Thread
import acapture

class MessageReciever():
    def __init__(self, HOST, PORT):
        self.frame = None
        self.HOST = HOST
        self.PORT = PORT
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((self.HOST, self.PORT))
        self.thread = Thread(target=self.listen, args=())
        self.thread.daemon = True
        self.thread.start()

    def listen(self):
        self.s.listen(5)
        while True:                            
            conn, (address, port) = self.s.accept()
            if conn:
                data = self.recv_msg(conn)
                print('recieved_data')   
                self.frame = Image.fromarray(pickle.loads(data))

    def send_msg(self, sock, msg):                            
        # Prefix each message with a 4-byte length (network byte order)
        msg = struct.pack('>I', len(msg)) + msg
        sock.sendall(msg)

    def recv_msg(self, sock):
        # Read message length and unpack it into an integer
        raw_msglen = self.recvall(sock, 4)
        if not raw_msglen:
            return None
        msglen = struct.unpack('>I', raw_msglen)[0]
        # Read the message data
        return self.recvall(sock, msglen)

    def recvall(self, sock, n):
        # Helper function to recv n bytes or return None if EOF is hit
        data = bytearray()
        while len(data) < n:
            packet = sock.recv(n - len(data))
            if not packet:
                return None
            data.extend(packet)
        return data

    def get_frame(self):
        if self.frame: return self.frame
        else: return None

