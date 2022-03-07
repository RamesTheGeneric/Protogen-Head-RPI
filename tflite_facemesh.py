from fdlite import FaceDetection, FaceLandmark, face_detection_to_roi
#from fdlite.render import Colors, landmarks_to_render_data, render_to_image
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





matrix = None



def init():
  global matrix
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
  
def render(face_landmarks, width, height, idle_x, idle_y, calibrated):

	DISPLAY_WIDTH = 64     # L_DISPLAY 0-64, R_DISPLAY = 65-128
	DISPLAY_HEIGHT = 32
	IM_SCALE = 4

	brightness = 0.8

	color = (255 * brightness, 0 * brightness , 0 * brightness)
																			#FaceCoords

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
															#Right Eye
	lm130 = coord_value(face_landmarks[107], width, height)
	lm247 = coord_value(face_landmarks[66], width, height)
	lm30 = coord_value(face_landmarks[105], width, height)
	lm29 = coord_value(face_landmarks[63], width, height)
	lm27 = coord_value(face_landmarks[70], width, height)
	lm28 = coord_value(face_landmarks[28], width, height)
	lm56 = coord_value(face_landmarks[56], width, height)
	lm190 = coord_value(face_landmarks[190], width, height)
	lm243 = coord_value(face_landmarks[243], width, height)
	lm112 = coord_value(face_landmarks[112], width, height)
	lm26 = coord_value(face_landmarks[26], width, height)
	lm22 = coord_value(face_landmarks[22], width, height)
	lm23 = coord_value(face_landmarks[23], width, height)
	lm24 = coord_value(face_landmarks[24], width, height)
	lm110 = coord_value(face_landmarks[110], width, height)
	lm25 = coord_value(face_landmarks[25], width, height)
															#Right Eye Center
	lm33 = coord_value(face_landmarks[33], width, height)   #Outer Corner of Eye
	lm133 = coord_value(face_landmarks[133], width, height)   #Center Corner of eye
	x1, y1 = lm33
	x2, y2 = lm133
	center_eye_r = [int(average([x1, x2])), int(average([y1, y2]))]
															#Left Eye
	lm359 = coord_value(face_landmarks[130], width, height)
	lm467 = coord_value(face_landmarks[247], width, height)
	lm260 = coord_value(face_landmarks[30], width, height)
	lm259 = coord_value(face_landmarks[29], width, height)
	lm257 = coord_value(face_landmarks[27], width, height)
	lm258 = coord_value(face_landmarks[28], width, height)
	lm286 = coord_value(face_landmarks[56], width, height)
	lm414 = coord_value(face_landmarks[190], width, height)
	lm463 = coord_value(face_landmarks[243], width, height)
	lm341 = coord_value(face_landmarks[26], width, height)
	lm256 = coord_value(face_landmarks[22], width, height)
	lm252 = coord_value(face_landmarks[23], width, height)
	lm253 = coord_value(face_landmarks[24], width, height)
	lm254 = coord_value(face_landmarks[110], width, height)
	lm339 = coord_value(face_landmarks[25], width, height)
	lm255 = coord_value(face_landmarks[255], width, height)
															#Left Eye Center
	lm263 = coord_value(face_landmarks[263], width, height)   #Outer Corner of Eye
	lm362 = coord_value(face_landmarks[362], width, height)   #Center Corner of eye
	x1, y1 = lm263
	x2, y2 = lm362
	center_eye_l = [int(average([x1, x2])), int(average([y1, y2]))]
	lm164 = coord_value(face_landmarks[164], width, height)   #First top point connecting to lips
	lm18 = coord_value(face_landmarks[18], width, height)   #First bottom point connecitng to lips
	x1, y1 = lm164
	x2, y2 = lm18
	center_mouth = [int(average([x1, x2])), int(average([y1, y2]))]
	
	if calibrated == False:         #   REMOVE KEYBOARD CONDITION FOR RPI!
		print("BrUh")						#Mouth			(0-19)
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
												#Right Eye		(20-35)
		idle_x[20] = lm130[0] - center_eye_r[0]
		idle_y[20] = lm130[1] - center_eye_r[1]
		idle_x[21] = lm247[0] - center_eye_r[0]
		idle_y[21] = lm247[1] - center_eye_r[1]
		idle_x[22] = lm30[0] - center_eye_r[0]
		idle_y[22] = lm30[1] - center_eye_r[1]
		idle_x[23] = lm29[0] - center_eye_r[0]
		idle_y[23] = lm29[1] - center_eye_r[1]
		idle_x[24] = lm27[0] - center_eye_r[0]
		idle_y[24] = lm27[1] - center_eye_r[1]
		idle_x[25] = lm28[0] - center_eye_r[0]
		idle_y[25] = lm28[1] - center_eye_r[1]
		idle_x[26] = lm56[0] - center_eye_r[0]
		idle_y[26] = lm56[1] - center_eye_r[1]
		idle_x[27] = lm190[0] - center_eye_r[0]
		idle_y[27] = lm190[1] - center_eye_r[1]
		idle_x[28] = lm243[0] - center_eye_r[0]
		idle_y[28] = lm243[1] - center_eye_r[1]
		idle_x[29] = lm112[0] - center_eye_r[0]
		idle_y[29] = lm112[1] - center_eye_r[1]
		idle_x[30] = lm26[0] - center_eye_r[0]
		idle_y[30] = lm26[1] - center_eye_r[1]
		idle_x[31] = lm22[0] - center_eye_r[0]
		idle_y[31] = lm22[1] - center_eye_r[1]
		idle_x[32] = lm23[0] - center_eye_r[0]
		idle_y[32] = lm23[1] - center_eye_r[1]
		idle_x[33] = lm24[0] - center_eye_r[0]
		idle_y[33] = lm24[1] - center_eye_r[1]
		idle_x[34] = lm110[0] - center_eye_r[0]
		idle_y[34] = lm110[1] - center_eye_r[1]
		idle_x[35] = lm25[0] - center_eye_r[0]
		idle_y[35] = lm25[1] - center_eye_r[1]
		calibrated = True
		print("calib: " + str(idle_x))
		
	else:
		pass

			
	'''
      191 80  81  82  13  312 311 310 415
    78                                   308
      95  88  178 87  14  317 402 318 324
    '''
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

	eye_r_x = [
		idle_x[20] - (lm130[0] - center_eye_r[0]),
		idle_x[21] - (lm247[0] - center_eye_r[0]),
		idle_x[22] - (lm30[0] - center_eye_r[0]),
		idle_x[23] - (lm29[0] - center_eye_r[0]),
		idle_x[24] - (lm27[0] - center_eye_r[0]),
		idle_x[25] - (lm28[0] - center_eye_r[0]),
		idle_x[26] - (lm56[0] - center_eye_r[0]),
		idle_x[27] - (lm190[0] - center_eye_r[0]),
		idle_x[28] - (lm243[0] - center_eye_r[0]),
		idle_x[29] - (lm112[0] - center_eye_r[0]),
		idle_x[30] - (lm26[0] - center_eye_r[0]),
		idle_x[31] - (lm22[0] - center_eye_r[0]),
		idle_x[32] - (lm23[0] - center_eye_r[0]),
		idle_x[33] - (lm24[0] - center_eye_r[0]),
		idle_x[34] - (lm110[0] - center_eye_r[0]),
		idle_x[35] - (lm25[0] - center_eye_r[0])
	]

	eye_r_y = [
		idle_y[20] - (lm130[1] - center_eye_r[1]),
		idle_y[21] - (lm247[1] - center_eye_r[1]),
		idle_y[22] - (lm30[1] - center_eye_r[1]),
		idle_y[23] - (lm29[1] - center_eye_r[1]),
		idle_y[24] - (lm27[1] - center_eye_r[1]),
		idle_y[25] - (lm28[1] - center_eye_r[1]),
		idle_y[26] - (lm56[1] - center_eye_r[1]),
		idle_y[27] - (lm190[1] - center_eye_r[1]),
		idle_y[28] - (lm243[1] - center_eye_r[1]),
		idle_y[29] - (lm112[1] - center_eye_r[1]),
		idle_y[30] - (lm26[1] - center_eye_r[1]),
		idle_y[31] - (lm22[1] - center_eye_r[1]),
		idle_y[32] - (lm23[1] - center_eye_r[1]),
		idle_y[33] - (lm24[1] - center_eye_r[1]),
		idle_y[34] - (lm110[1] - center_eye_r[1]),
		idle_y[35] - (lm25[1] - center_eye_r[1])
	]
	
	w, h = DISPLAY_WIDTH, DISPLAY_HEIGHT
	surface = cairo.ImageSurface (cairo.FORMAT_ARGB32, w, h)
	ctx = cairo.Context (surface)

	# creating a cairo context object
	x_scale = 3
	y_scale = 1.3

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
	# making close path
	ctx.fill()


									# Eye
	'''								
	ctx.move_to(4, 0)
	ctx.line_to(26, 0)
	ctx.line_to(30, 4)
	ctx.line_to(24.5, 8)
	ctx.line_to(21, 8)
	ctx.line_to(4, 0)
	ctx.fill()
	'''
	x_scale = 3
	y_scale = 1.5
	ctx.move_to(19.4, 3.5 - (eye_r_y[0] * y_scale))
	ctx.line_to(23.9, 1.8 - (eye_r_y[1] * y_scale))
	ctx.line_to(29.5, 2 - (eye_r_y[2] * y_scale))
	ctx.line_to(32.8, 3.6 - (eye_r_y[3] * y_scale))
	ctx.line_to(34, 7.3 - (eye_r_y[4] * y_scale))
	ctx.line_to(34.2, 9.6)
	ctx.line_to(31.4, 9.3)
	ctx.line_to(24, 9)
	ctx.line_to(18.6, 8.6)
	ctx.line_to(16.9, 8.2)
	ctx.line_to(18.1, 7.8)
	ctx.fill()

	# getting fill extends
	buf = surface.get_data()
	array = np.ndarray (shape=(h,w,4), dtype=np.uint8, buffer=buf)
	array = array[:,:,:3]
	# cv2.imshow('array', array)

	# printing message when file is saved
	##  Draws Face Image from Mask

	image = create_blank(DISPLAY_WIDTH, DISPLAY_HEIGHT, rgb_color = color) #Makes blank bg image
	maskimage = array #Reads Mask image
	ret, maskimage = cv2.threshold(maskimage, 50, 255,cv2.THRESH_BINARY)    #Converts mask image to BW
	res = cv2.bitwise_and(image, maskimage)  #Mask the base image
	up_res = cv2.resize(res, (DISPLAY_WIDTH * IM_SCALE, DISPLAY_HEIGHT * IM_SCALE), 0, 0, interpolation = cv2.INTER_NEAREST)
	# cv2.imshow('up_res', up_res)  #Display Image


	#Convert the image from CV2 to PIL
	im_pil = Image.fromarray(res)
	img_out = Image.new('RGB', (DISPLAY_WIDTH*2, DISPLAY_HEIGHT)) #Create image with size of both panels
	img_out.paste(ImageOps.mirror(im_pil), (DISPLAY_WIDTH,0)) # Write mirrored image on R_Display
	img_out.paste(im_pil, (0, 0)) #Write image on L_Display

	# cv2.waitKey(1)

	matrix.SetImage(img_out) #Display on matricies
	return calibrated

class ThreadedFace(object):
	def __init__(self, width, height):
		self.detect_faces = FaceDetection()
		self.detect_face_landmarks = FaceLandmark()

		self.cap = cv2.VideoCapture('/dev/video0')
		#self.cap = cv2.VideoCapture('/base/soc.i2c0mux/i2c@1/ov5647@36', cv2.CAP_V4L) gst-launch-1.0
		#self.cap = cv2.VideoCapture('libcamerasrc ! video/x-raw, width=320, height=240, framerate=30/1 ! videoconvert ! videoscale ! autovideosink', cv2.CAP_GSTREAMER)
		#self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
		
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
		print('Done')


	def get_landmarks(self):
		return self.face_landmarks


def main():
	init()
	width = 320
	height = 240

	idle_x = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
	idle_y = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]




	threaded_face = ThreadedFace(width, height)
	calibrated = False

	while True:
		try:
			face_landmarks = threaded_face.get_landmarks()
			if len(face_landmarks) > 0:
				calibrated = render(face_landmarks, width, height, idle_x, idle_y, calibrated)
		except AttributeError:
			pass




if __name__ == '__main__':
	'''
	cProfile.run('main()', 'output.dat')
	from pstats import SortKey

	with open('output_time.txt', 'w') as f:
		p = pstats.Stats("output.dat", stream=f)
		p.sort_stats("time").print_stats()
	with open("output_calls.txt", "w") as f:
		p = pstats.Stats("output.dat", stream=f)
		p.sort_stats("calls").print_stats()
		'''
	main()


#sync in /mnt/x/Documents/GitHub/Protogen-Head-RPI: rsync -rP ./*.py pi@192.168.1.130:~/pc_sync
#powershell ssh: ssh pi@192.168.1.130

