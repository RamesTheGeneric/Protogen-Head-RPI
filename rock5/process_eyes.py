import cv2
import AHSF
from one_euro_filter import OneEuroFilter
import numpy as np

class EyeTracker():
    def __init__(self):
        min_cutoff = 0.0004 #you need to adjust
        beta = 0.9 #you need to adjust
        noisy_point = np.array([2])
        self.filter = OneEuroFilter(
            noisy_point,
            min_cutoff=min_cutoff,
            beta=beta
        )
        self.gaze = [0,0]
        self.recal = 0.0
        self.center = [0,0]

    def Func(self, img):
        img = cv2.resize(img, (256, 256), interpolation = cv2.INTER_AREA)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        frame_gray, frame_clear_resize, x_center, y_center, thing = AHSF.External_Run_AHSF(img)
        gaze = (int(x_center), int(y_center))
        gaze = self.calibrate(gaze)
        self.gaze = self.filter(np.array(gaze))
    
    def calibrate(self, gaze):
        #print(self.recal)
        if self.recal == 1.0:
            #print("recal")
            self.center = gaze
            self.recal = 0.0
        gaze = np.array(gaze)-np.array(self.center)
        gaze = gaze.tolist()
        #range_xmin = -45
        #range_ymin = 60

        x_min, x_max = -100, 90
        y_min, y_max = -50,50
        x_range = x_max - x_min
        y_range = y_max - y_min 
        normalized_x = ((gaze[0] - 0) / x_range) * 2
        normalized_y = ((gaze[1] - 0) / y_range) * 2
        #x = (gaze[0] - x_min)/(x_max-x_min)
        #y = (gaze[1] - y_min)/(y_max-y_min)
        gaze = [normalized_x,normalized_y]
        #print(f"Gaze: {gaze}")
        return gaze
        

    def recalibrate_eyes(self, calibrate):
        self.recal = calibrate

    def get_gaze(self):
        return self.gaze
    
