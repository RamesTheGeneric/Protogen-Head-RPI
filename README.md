# Protogen-Head-RPI
Software for RPI based Protogen Heads

Made for 64x32x2 matricies
Tested on RPI 4 4GB




~~Runs TFLite Implementation of Mediapipe. ~~

Runs custom Dlib shape predictor. 


dlib_facemesh.py is the Main file for now. I'm still messing around. 

Required Packages: 

fdlite
PIL
cv2
numpy
cairo
rgbmatrix
threading
math
constants
face
dlib

How it works: 

The sbc takes the camera feed and processes the frames with mediapipe facemesh to return landmarks. The user presses a button to "reset" the "reference coordinates" which are then used to calculate landmark offsets as a normalized value to the video frame. In another thread, The different faces are drawn based on the button input. Each face is defined as a vector graphic being drawn with cario. The anchors are then manually assigend to different offsets from the landmark detector and that moves the anchors to move the mouth and eyes to the user's face. 

Current state:

New Dlib model tracks ok at ~100 fps. I need to improve the dataset and add filtering but it looks really promising.



~~To do:~~

Add filtering to the landmarks

* Finish drawing the other face
* Add controller input (Wii remote for now)
* Make the background image a separate function
* Option to offload facemesh processing to another device (another SBC or an android phone)
* I forgor the rest











Idk what else to put, I wrote this in like 2 minutes 
Discord: Rames The Generic#3540
