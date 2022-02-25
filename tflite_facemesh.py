from fdlite import FaceDetection, FaceLandmark, face_detection_to_roi
from fdlite.render import Colors, landmarks_to_render_data, render_to_image
from PIL import Image, ImageOps
import PIL
import cv2
import numpy as np
import cairo
import rgbmatrix
import os
from threading import Thread
import math
#import keyboard


idle_x = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
idle_y = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

calibrated = False

matrix = None

DISPLAY_WIDTH = 64     # L_DISPLAY 0-64, R_DISPLAY = 65-128
DISPLAY_HEIGHT = 32
IM_SCALE = 4

color = (255, 0 , 0)

def init():
  global matrix
  isolcpus=3
  options = rgbmatrix.RGBMatrixOptions()
  options.rows = 32
  options.cols = 64
  options.chain_length = 2
  options.parallel = 1
  options.gpio_slowdown = 2
  options.hardware_mapping = 'adafruit-hat'
  matrix = rgbmatrix.RGBMatrix(options=options)

def create_blank(width, height, rgb_color=(0, 0, 0)):
    image = np.zeros((height, width, 3), np.uint8)
    color = tuple(reversed(rgb_color))
    image[:] = color

    return image




def coord_value(mplm, width, height):
  sub_landmarks = str(mplm)
  #sub_landmarks = str(sub_landmarks)
  x = sub_landmarks.find("x=")
  s = sub_landmarks[x+3] + sub_landmarks[x+4] + sub_landmarks[x+5] + sub_landmarks[x+6] + sub_landmarks[x+7]
  s = s.replace(',', '')
  x = float(s)
  x = int(x * width)
  y = sub_landmarks.find("y=")
  s = sub_landmarks[y+3] + sub_landmarks[y+4] + sub_landmarks[y+5] + sub_landmarks[y+6] + sub_landmarks[y+7]
  s = s.replace(',', '')
  y = float(s)
  y = int(y * height)
  return [x, y]
  
def average(lst):
  return sum(lst) / len(lst)

def dist(x2, x1, y2, y1):
  return math.sqrt(((x2 - x1) ** 2) + ((y2 - y1) ** 2))
  
def calc_ref(x_coord, slope, offset):
  return (-slope * x_coord) + offset

def NormalizeData(data):
  return (data - np.min(data)) / (np.max(data) - np.min(data))
  
'''
class ThreadedCamera(object):
    def __init__(self, src=0):
        self.capture = cv2.VideoCapture(src)
        self.capture.set(cv2.CAP_PROP_BUFFERSIZE, 3)
        # Start frame retrieval thread
        self.thread = Thread(target=self.update, args=())
        self.thread.daemon = True
        self.thread.start()

    def update(self, img):
		face_detections = detect_faces(img)
		if len(face_detections):
			# get ROI for the first face found
			face_roi = face_detection_to_roi(face_detections[0], img.size)
			# detect face landmarks
			face_landmarks = detect_face_landmarks(img, face_roi)
			# convert detections to render data
			render_data = landmarks_to_render_data(face_landmarks, [], landmark_color=Colors.PINK, thickness=3)
			# render and display landmarks (points only)
				# Mouth Outer
       

    def show_frame(self):
        img = cv2.cvtColor(self.frame, cv2.COLOR_RGB2GRAY)
        img = cv2.resize(img, dsize=(config.X_RES, config.Y_RES))
        // DO YOUR PREDICTION HERE
        cv2.imshow('frame', img)
        cv2.waitKey(1)
  
'''	
	  
  
def render(face_landmarks, width, height):
	lm78 = coord_value(face_landmarks[78], width, height)					# fuck OWO
	lm191 = coord_value(face_landmarks[191], width, height)
	lm80 = coord_value(face_landmarks[80], width, height)
	lm81 = coord_value(face_landmarks[81], width, height)
	lm82 = coord_value(face_landmarks[82], width, height)
	lm13 = coord_value(face_landmarks[13], width, height)
	lm312 = coord_value(face_landmarks[312], width, height)
	lm311 = coord_value(face_landmarks[311], width, height)
	lm310 = coord_value(face_landmarks[310], width, height)
	lm415 = coord_value(face_landmarks[415], width, height)
	lm308 = coord_value(face_landmarks[308], width, height)
	lm324 = coord_value(face_landmarks[324], width, height)
	lm318 = coord_value(face_landmarks[318], width, height)
	lm402 = coord_value(face_landmarks[402], width, height)
	lm317 = coord_value(face_landmarks[317], width, height)
	lm14 = coord_value(face_landmarks[14], width, height)
	lm87 = coord_value(face_landmarks[87], width, height)
	lm178 = coord_value(face_landmarks[178], width, height)
	lm88 = coord_value(face_landmarks[88], width, height)
	lm95 = coord_value(face_landmarks[95], width, height)
	
	lm164 = coord_value(face_landmarks[164])   #First top point connecting to lips
	lm18 = coord_value(face_landmarks[18])   #First bottom point connecitng to lips
	x1, y1 = lm164
	x2, y2 = lm18
	center_mouth = [int(average([x1, x2])), int(average([y1, y2]))]
	
	if calibrated == False:         #   REMOVE KEYBOARD CONDITION FOR RPI!
		print("BrUh")
		idle_x[0] = lm78[0] - center_mouth[0]
		idle_y[0] = lm78[1] - center_mouth[1]
		idle_x[1] = lm191[0] - center_mouth[0]
		idle_y[1] = lm191[1] - center_mouth[1]
		idle_x[2] = lm80[0] - center_mouth[0]
		idle_y[2] = lm80[1] - center_mouth[1]
		idle_x[3] = lm81[0] - center_mouth[0]
		idle_y[3] = lm81[1] - center_mouth[1]
		idle_x[4] = lm82[0] - center_mouth[0]
		idle_y[4] = lm82[1] - center_mouth[1]
		idle_x[5] = lm13[0] - center_mouth[0]
		idle_y[5] = lm13[1] - center_mouth[1]
		idle_x[6] = lm312[0] - center_mouth[0]
		idle_y[6] = lm312[1] - center_mouth[1]
		idle_x[7] = lm311[0] - center_mouth[0]
		idle_y[7] = lm311[1] - center_mouth[1]
		idle_x[8] = lm310[0] - center_mouth[0]
		idle_y[8] = lm310[1] - center_mouth[1]
		idle_x[9] = lm415[0] - center_mouth[0]
		idle_y[9] = lm415[1] - center_mouth[1]
		idle_x[10] = lm308[0] - center_mouth[0]
		idle_y[10] = lm308[1] - center_mouth[1]
		idle_x[11] = lm324[0] - center_mouth[0]
		idle_y[11] = lm324[1] - center_mouth[1]
		idle_x[12] = lm318[0] - center_mouth[0]
		idle_y[12] = lm318[1] - center_mouth[1]
		idle_x[13] = lm402[0] - center_mouth[0]
		idle_y[13] = lm402[1] - center_mouth[1]
		idle_x[14] = lm317[0] - center_mouth[0]
		idle_y[14] = lm317[1] - center_mouth[1]
		idle_x[15] = lm14[0] - center_mouth[0]
		idle_y[15] = lm14[1] - center_mouth[1]
		idle_x[16] = lm87[0] - center_mouth[0]
		idle_y[16] = lm87[1] - center_mouth[1]
		idle_x[17] = lm178[0] - center_mouth[0]
		idle_y[17] = lm178[1] - center_mouth[1]
		idle_x[18] = lm88[0] - center_mouth[0]
		idle_y[18] = lm88[1] - center_mouth[1]
		idle_x[19] = lm95[0] - center_mouth[0]
		idle_y[19] = lm95[1] - center_mouth[1]
		calibrated = True
		print("calib: " + str(idle_x))
		
	else:
		pass
			
	mouth_x = [
		idle_x[0] - (lm78[0] - center_mouth[0]), 
		idle_x[1] - (lm191[0] - center_mouth[0]), 
		idle_x[2] - (lm80[0] - center_mouth[0]), 
		idle_x[3] - (lm81[0] - center_mouth[0]), 
		idle_x[4] - (lm82[0] - center_mouth[0]), 
		idle_x[5] - (lm13[0] - center_mouth[0]), 
		idle_x[6] - (lm312[0] - center_mouth[0]), 
		idle_x[7] - (lm311[0] - center_mouth[0]), 
		idle_x[8] - (lm310[0] - center_mouth[0]), 
		idle_x[9] - (lm415[0] - center_mouth[0]), 
		idle_x[10] - (lm308[0] - center_mouth[0]), 
		idle_x[11] - (lm324[0] - center_mouth[0]), 
		idle_x[12] - (lm318[0] - center_mouth[0]),
		idle_x[13] - (lm402[0] - center_mouth[0]),
		idle_x[14] - (lm317[0] - center_mouth[0]),
		idle_x[15] - (lm14[0] - center_mouth[0]),
		idle_x[16] - (lm87[0] - center_mouth[0]),
		idle_x[17] - (lm178[0] - center_mouth[0]),
		idle_x[18] - (lm88[0] - center_mouth[0]),
		idle_x[19] - (lm95[0] - center_mouth[0])
	]

	mouth_y = [
		idle_y[0] - (lm78[1] - center_mouth[1]), 
		idle_y[1] - (lm191[1] - center_mouth[1]), 
		idle_y[2] - (lm80[1] - center_mouth[1]), 
		idle_y[3] - (lm81[1] - center_mouth[1]), 
		idle_y[4] - (lm82[1] - center_mouth[1]), 
		idle_y[5] - (lm13[1] - center_mouth[1]), 
		idle_y[6] - (lm312[1] - center_mouth[1]), 
		idle_y[7] - (lm311[1] - center_mouth[1]), 
		idle_y[8] - (lm310[1] - center_mouth[1]), 
		idle_y[9] - (lm415[1] - center_mouth[1]), 
		idle_y[10] - (lm308[1] - center_mouth[1]), 
		idle_y[11] - (lm324[1] - center_mouth[1]), 
		idle_y[12] - (lm318[1] - center_mouth[1]),
		idle_y[13] - (lm402[1] - center_mouth[1]),
		idle_y[14] - (lm317[1] - center_mouth[1]),
		idle_y[15] - (lm14[1] - center_mouth[1]),
		idle_y[16] - (lm87[1] - center_mouth[1]),
		idle_y[17] - (lm178[1] - center_mouth[1]),
		idle_y[18] - (lm88[1] - center_mouth[1]),
		idle_y[19] - (lm95[1] - center_mouth[1])
	]
	
	w, h = DISPLAY_WIDTH, DISPLAY_HEIGHT
	surface = cairo.ImageSurface (cairo.FORMAT_ARGB32, w, h)
	ctx = cairo.Context (surface)

	# creating a cairo context object
	x_scale = 2
	y_scale = .8

	ctx = cairo.Context(surface)
	ctx.set_source_rgb(0, 0, 0)
	ctx.rectangle(0,0, width, height)
	ctx.fill()

									# RightFace
	ctx.set_source_rgb(1, 1, 1)
	# Mouth coord driven face
	ctx.move_to(64, 23 - (mouth_y[5] * y_scale))
	ctx.line_to(52 - (mouth_x[4] * x_scale), 26 - (mouth_y[4] * y_scale))
	ctx.line_to(49 - (mouth_x[3] * x_scale), 22 - (mouth_y[3] * y_scale))
	ctx.line_to(42 - (mouth_x[2] * x_scale), 24 - (mouth_y[2] * y_scale))
	ctx.line_to(24 - (mouth_x[0] * x_scale), 17 - (mouth_y[0] * y_scale))
	ctx.line_to(24 - (mouth_x[0] * x_scale), 18 - (mouth_y[0] * y_scale))
	ctx.line_to(26 - (mouth_x[0] * x_scale), 19 - (mouth_y[0] * y_scale))
	ctx.line_to(42 - (mouth_x[18] * x_scale), 25 - (mouth_y[18] * y_scale))
	ctx.line_to(48 - (mouth_x[17] * x_scale), 23 - (mouth_y[17] * y_scale))
	ctx.line_to(51 - (mouth_x[16] * x_scale), 27 - (mouth_y[16] * y_scale))
	ctx.line_to(64, 24 - (mouth_y[15] * y_scale))
	print(mouth_y)
	# making close path
	ctx.fill()


									# Eye
	ctx.move_to(1, 0)
	ctx.line_to(26, 0)
	ctx.line_to(30, 4)
	ctx.line_to(26, 8)
	ctx.line_to(20, 8)
	ctx.line_to(1, 0)
	ctx.fill()
	# getting fill extends
	buf = surface.get_data()
	array = np.ndarray (shape=(h,w,4), dtype=np.uint8, buffer=buf)
	array = array[:,:,:3]
	cv2.imshow('array', array)

	
	# printing message when file is saved



													##  Draws Face Image from Mask

	image = create_blank(DISPLAY_WIDTH, DISPLAY_HEIGHT, rgb_color = color) #Makes blank bg image
	maskimage = array #Reads Mask image
	ret, maskimage = cv2.threshold(maskimage, 50, 255,cv2.THRESH_BINARY)    #Converts mask image to BW
	res = cv2.bitwise_and(image, maskimage)  #Mask the base image
	up_res = cv2.resize(res, (DISPLAY_WIDTH * IM_SCALE, DISPLAY_HEIGHT * IM_SCALE), 0, 0, interpolation = cv2.INTER_NEAREST)
	cv2.imshow('up_res', up_res)  #Display Image


	#Convert the image from CV2 to PIL
	im_pil = Image.fromarray(res)
	img_out = Image.new('RGB', (DISPLAY_WIDTH*2, DISPLAY_HEIGHT)) #Create image with size of both panels
	img_out.paste(ImageOps.mirror(im_pil), (DISPLAY_WIDTH,0)) # Write mirrored image on R_Display
	img_out.paste(im_pil, (0, 0)) #Write image on L_Display

	#matrix.SetImage(img_out) #Display on matricies

class ThreadedFace(object):
	def __init__(self, width, height):
		# load detection models
		# open image; by default, the "front camera"-model is used, which is smaller
		# and ideal for selfies, and close-up portraits

		self.detect_faces = FaceDetection()
		self.detect_face_landmarks = FaceLandmark()

		self.cap = cv2.VideoCapture(1)
		self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
		
		self.width = width
		self.height = height


		self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
		self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)

		self.face_landmarks = []

		self.thread = Thread(target=self.update, args=())
		self.thread.daemon = True
		self.thread.start()

	def update(self):
		while self.cap.isOpened():
			success, img = self.cap.read()
			img = PIL.Image.fromarray(img)
			if not success:
				print("Ignoring empty camera frame.")
				continue
			face_detections = self.detect_faces(img)
			if len(face_detections):
				# get ROI for the first face found
				face_roi = face_detection_to_roi(face_detections[0], img.size)
				# detect face landmarks
				self.face_landmarks = self.detect_face_landmarks(img, face_roi)
			else:
				print('no face detected :(') 


	def get_landmarks(self):
		return self.face_landmarks

def main():  
	init()
	width = 640
	height = 480

	threaded_face = ThreadedFace(width, height)
	while True:
		try:
			face_landmarks = threaded_face.get_landmarks()
			if len(face_landmarks) > 0:
				render(face_landmarks, width, height)
		except AttributeError:
			pass




if __name__ == '__main__':
	main()
