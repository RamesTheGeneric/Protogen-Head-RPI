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
import helpers.defines as defines
from helpers.constants import process_landmarks
#import keyboard
matrix = None

def render(face_landmarks, width, height, idle_x, idle_y, calibrated):

	DISPLAY_WIDTH = 64     # L_DISPLAY 0-64, R_DISPLAY = 65-128
	DISPLAY_HEIGHT = 32
	IM_SCALE = 4

	brightness = 0.8

	color = (255 * brightness, 0 * brightness , 0 * brightness)
	button = 0
	mouth_x, mouth_y, eye_r_x, eye_r_y = process_landmarks(face_landmarks, width, height, button, calibrated)
																			#FaceCoords

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
	defines.init()
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
	main()


#sync in /mnt/x/Documents/GitHub/Protogen-Head-RPI: rsync -rP ./*.py pi@192.168.1.130:~/pc_sync
#powershell ssh: ssh pi@192.168.1.130

