from socketserver import UDPServer
import rgbmatrix
import cv2
import socket
import numpy as np
import subprocess
import netifaces as ni
import pickle
from dlib_facemesh import main as facemesh_run
from threading import Thread, Event
import multiprocessing as mp
from PIL import Image
from time import sleep
from html.parser import HTMLParser


def get_ip_address():       #   Gets the current IP of the WLAN adapter
    ips = str(ni.ifaddresses('wlan0')[ni.AF_INET][0]['addr'])
    return ips

def create_blank(width, height, rgb_color=(0, 0, 0)):   #   Makes a black RGB numpy array
    image = np.zeros((height, width, 3), np.uint8)
    color = tuple(reversed(rgb_color))
    image[:] = color
    return image

def matrix_init():      #   Inital matrix setup
  
  global matrix
  options = rgbmatrix.RGBMatrixOptions()
  options.rows = 32
  options.cols = 64
  options.chain_length = 2
  options.parallel = 1
  options.gpio_slowdown = 2
  options.hardware_mapping = 'adafruit-hat'
  matrix = rgbmatrix.RGBMatrix(options=options)

def render(res):                    # Takes a PIL image and writes it to the displays
    im_pil = Image.fromarray(res)
    img_out = Image.new('RGB', (64*2, 32))
    img_out.paste(im_pil, (0, 0))
    matrix.SetImage(img_out) #Display on matricies

def draw_text(res, org, fontScale, color, thickness, letters):         # Draws text 
    font = cv2.FONT_HERSHEY_SIMPLEX
    res = cv2.putText(res, letters, org, font, fontScale, color, thickness, cv2.LINE_AA)

class Tick():           # threaded counter going from 0-10 every minute
    def __init__(self):
        self.current_tick = 0
        self.thread = Thread(target=self.tick, args=())
        self.thread.daemon = True
        self.thread.start()
    def tick(self):
        while True:
            sleep(6)
            if self.current_tick >= 10:
                self.current_tick = 0
            else:
                self.current_tick += 1
            print(f'current thread tick: {self.current_tick}')
            
    def get_tick(self):
        return self.current_tick

class CommandSender():


    def __init__(self):               #Implement BT server Code as TCP
        global port, sock

        
        #ip = "protohead"
        self.ip = socket.gethostbyname('localhost')
        print(f'control client ip: {ip}')
        self.port = 7171
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send(self, msg):
        data_string = pickle.dumps(msg)
        sock.sendto(data_string, (self.ip, self.port))





class UdpServer():
    def __init__(self):
        print('UDP Server Started!')
        #self.hostname = "192.168.1.187"            #       
        self.hostname = socket.gethostname()   # Setup Wifi Direct
        self.ip = get_ip_address()
        #self.ip = socket.gethostbyname('localhost')
        self.port = 7272
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.ip, self.port))
        print(f'Hostname: {self.hostname}')
        print(f'Start listening to {self.ip}:{self.port}')
        self.thread = Thread(target=self.listen, args=())
        self.thread.daemon = True
        self.thread.start()

    def listen(self):
        self.data = None
        while True:
            self.data, self.addr = self.sock.recvfrom(4096)
            try: 
                self.data = pickle.loads(self.data)
            except: 
                print('Pickle load function failed')


            print(f'got: {self.data} from: {self.addr}')

    def get_data(self):
        if self.data:
            return self.data
    def clear_data(self):
        if self.data:
            self.data = None


class NetworkInfo():
    def draw(res, ip):                  #   Gets IP and Access Point info and draws it on the displays
        hostname = socket.gethostname()
        draw_text(res, (0, 30), 0.40, (255, 150, 0), 1, ip)
        draw_text(res, (0, 10), 0.40, (255, 150, 0), 1, "AP: ")
        #if any('10.0.0' in s for s in ip):
        if '10.0.0' in ip:
            ap = 'protohead'
            draw_text(res, (25, 10), 0.40, (255, 150, 0), 1, ap)
        else:                                           # If host ip isn't one from the host AP, show the connected ssid
            ap = subprocess.check_output(['iwgetid', '-r']).decode('utf-8').split('\n')
            draw_text(res, (25, 10), 0.35, (255, 150, 0), 1, str(ap))



'''
async def gui(ip):
    print('started')
    ui.label('Hello NiceGUI!')
    ui.button('BUTTON', on_click=lambda: ui.notify('button was pressed'))
    print('about to run')
    ui.run(host = '192.168.137.82')
    '''
    

def main():
    global facemesh, camera, control_client, ip, data_hold     #   Initalizing variables
    facemesh = False
    camera = False
    control_client = False
    ip = get_ip_address()
    data_hold = [None, None]
    kill = False
    matrix_init()
    tick_class = Tick()
    udp_class = UdpServer()
    command_sender = CommandSender()
    event = Event()
    dlib = Thread(target=facemesh_run, args=(event,))
    dlib.daemon = True
    while True:

        data = udp_class.get_data()
        if data:
            data_hold = data
            print(f'if_data: {str(data)}')
            
        if data_hold[0]:
            if 'facemesh' in str(data_hold):
                if 'facemesh=True' in str(data_hold):
                    facemesh = True
                if 'facemesh=False' in str(data_hold):
                    facemesh = False



        if facemesh == False:
            if not event.is_set():
                print('killing dlib thread')
                res = create_blank(128, 32)
                render(res)
                print('setting event')
                event.set()
            res = create_blank(128, 32)
            NetworkInfo.draw(res, ip)
            tick = str(tick_class.get_tick())
            draw_text(res, (0, 20), 0.30, (0, 150, 0), 1, tick)
            render(res)
            sleep(0.016)
        
        else:
            print('facemesh running')
            if event.is_set():
                black = create_blank(128, 32)
                render(black)
                print('clearing event')
                event.clear()
            if not dlib.is_alive():
                res = create_blank(128, 32)
                render(res)
                print('starting dlib')
                dlib.start()
                
            if data:
                if data in data_hold:
                    if 'control' in str(data):
                        print('found control in data')
                        face = str(data).split('_')
                        face_value = f'face_{face[1]}'
                        overlay_value = f'overlay_{face[2]}'
                        command_string = (face_value, overlay_value)
                        #command_string = str(f'{face_value} {overlay_value}')
                        print(f'Sending command: {command_string}')
                        command_sender.send(command_string)

                    
        udp_class.clear_data()
        sleep(1)

if __name__ == '__main__':

    main()

            
    









