from cv2 import CALIB_FIX_ASPECT_RATIO


def average(lst):
	return sum(lst) / len(lst)

  

def process_landmarks(face_landmarks, eye_r, eye_l, width, height, button, calibrated, center_mouth, idle_x, idle_y):
	x = []
	y = []
	for i in range (len(face_landmarks)):
		lm = face_landmarks[i]
		x.append(lm[0])
		y.append(lm[1])

	
	if calibrated == False:
		idle_x = []
		idle_y = []
		center_mouth = (int(average(x)), int(average(y)))
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

	mouth_x = []
	for i in range(12):
		mouth_x.append(idle_x[i] - (x[i] - center_mouth[0]))

	mouth_y = []
	for i in range(len(y)):
		mouth_y.append(idle_y[i] - (y[i] - center_mouth[1]))

	eye_r_x = []


	eye_r_y = []
		
	return mouth_x, mouth_y, eye_r_x, eye_r_y, calibrated, center_mouth, idle_x, idle_y