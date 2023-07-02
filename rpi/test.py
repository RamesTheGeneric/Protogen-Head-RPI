import requests
import numpy as np
import cv2
from PIL import Image
import rgbmatrix
import time

'''
class FrameReciever():
    def __init__(self, url):
        self.url = url
        self.img = Image.fromarray(np.random.randint(255, size=(128,32,3),dtype=np.uint8))
        self.thread = Thread(target=self.update, args=())
        self.thread.daemon = True
        self.thread.start()

    def update(self):
        stream = requests.get(self.url, stream=True)
        chunk_size = 8192
        frame_buffer = b''
        frame_start = -1
        frame_end = -1

        for chunk in stream.iter_content(chunk_size=chunk_size):
            frame_buffer += chunk
            while True:
                frame_start = frame_buffer.find(b'\xff\xd8')
                frame_end = frame_buffer.find(b'\xff\xd9', frame_start)
                if frame_start != -1 and frame_end != -1:
                    jpg_data = frame_buffer[frame_start:frame_end+2]
                    frame_buffer = frame_buffer[frame_end+2:]
                    try:
                        # Convert the JPEG data to an OpenCV image
                        img = cv2.imdecode(np.frombuffer(jpg_data, dtype=np.uint8), cv2.IMREAD_COLOR)
                        self.img = Image.fromarray(img)
                        #dp.frame(img)

                    except cv2.error as e:
                        print(f"Error decoding image: {e}")
                else:
                    break

    def get_frame(self):
        return self.img

'''

def init():
  global matrix
  options = rgbmatrix.RGBMatrixOptions()
  options.rows = 32
  options.cols = 64
  options.chain_length = 2
  options.parallel = 1
  options.gpio_slowdown = 2
  options.hardware_mapping = 'adafruit-hat'
  #options.limit_refresh_rate_hz = 30
  matrix = rgbmatrix.RGBMatrix(options=options)
def main(url):
    cap = cv2.VideoCapture(url)
    while True:
        check, frame = cap.read()
        frame = Image.fromarray(frame)
        matrix.SetImage(frame)


    '''
    stream = requests.get(url, stream=True)
    chunk_size = 8192
    frame_buffer = b''
    frame_start = -1
    frame_end = -1

    
    for chunk in stream.iter_content(chunk_size=chunk_size):
        frame_buffer += chunk
        while True:
            frame_start = frame_buffer.find(b'\xff\xd8')
            frame_end = frame_buffer.find(b'\xff\xd9', frame_start)
            if frame_start != -1 and frame_end != -1:
                jpg_data = frame_buffer[frame_start:frame_end+2]
                frame_buffer = frame_buffer[frame_end+2:]
                try:
                    # Convert the JPEG data to an OpenCV image
                    img = cv2.imdecode(np.frombuffer(jpg_data, dtype=np.uint8), cv2.IMREAD_COLOR)
                    img = Image.fromarray(img)
                    matrix.SetImage(img)

                except cv2.error as e:
                    print(f"Error decoding image: {e}")
            else:
                break
            '''
'''

# Example usage
if __name__ == '__main__':
    global matrix
    img = Image.fromarray(np.random.randint(255, size=(128,32,3),dtype=np.uint8))
    options = rgbmatrix.RGBMatrixOptions()
    options.rows = 32
    options.cols = 64
    options.chain_length = 2
    options.parallel = 1
    options.gpio_slowdown = 0
    options.hardware_mapping = 'adafruit-hat'
    matrix = rgbmatrix.RGBMatrix(options=options)
    #options.limit_refresh_rate_hz = 30
'''
    #fr = FrameReciever('192.168.1.167:8000/stream.mjpeg')
init()
main("http://192.168.1.236:8080/stream")
