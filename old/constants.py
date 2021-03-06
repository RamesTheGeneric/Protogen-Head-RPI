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

idle_x = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
idle_y = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

def process_landmarks(face_landmarks, eye_r, eye_l, width, height, button, calibrated):
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

	center_eye_l = [int(average([x1, x2])), int(average([y1, y2]))]
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

	return mouth_x, mouth_y, eye_r_x, eye_r_y, calibrated