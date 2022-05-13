from cv2 import CALIB_FIX_ASPECT_RATIO


def average(lst):
	return sum(lst) / len(lst)

  

def process_landmarks(face_landmarks, eye_r, eye_l, width, height, button, calibrated, center_mouth, idle_x, idle_y):
	x = []
	y = []
	arrange = (0, 1, 4, 5 ,6, 7, 8, 9, 10 ,11, 2, 3)


	try:
		for i in range (len(arrange)):
			lm = face_landmarks[arrange[i]]
			x.append(lm[0])
			y.append(lm[1])
	except:
		print("X/Y Index out of range")

	center_mouth = (average((x[3], x[9])), average((y[0], y[6])))
	if calibrated == False:
		idle_x = []
		idle_y = []
		#center_mouth = (int(average(x)), int(average(y)))
		print("BrUh")		
						#Mouth			(0-19)
		for i in range(len(face_landmarks)):
			center_x = center_mouth[0]
			center_y = center_mouth[1]

			idle_x.append(x[i] - center_mouth[0])
			idle_y.append(y[i] - center_mouth[1])
		calibrated = True
		print("calib: " + str(idle_x))
		
	else:
		pass

	try:
		mouth_x = []
		for i in range(12):
			mouth_x.append(idle_x[i] - (x[i] - center_mouth[0]))
	except:
		print('X out of range')

	try: 
		mouth_y = []
		for i in range(12):
			mouth_y.append(idle_y[i] - (y[i] - center_mouth[1]))
	except:
		print("Y out of range")
	eye_r_x = []
	eye_r_y = []
	#print(center_mouth)
	'''
	print_array = (
		idle_y[0],
		idle_y[1],
		idle_y[2],
		idle_y[3],
		idle_y[4],
		idle_y[5],
		idle_y[6]

	)
	print(center_mouth[1])

	
	print_array = (
		mouth_y[0],
		mouth_y[1],
		mouth_y[2],
		mouth_y[3],
		mouth_y[4],
		mouth_y[5],
		mouth_y[6]
	)
	
	#print(print_array)
	'''
	return mouth_x, mouth_y, eye_r_x, eye_r_y, calibrated, center_mouth, idle_x, idle_y