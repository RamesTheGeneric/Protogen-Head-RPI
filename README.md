# Protogen-Head-RPI
Software for RPI based Protogen Heads

Made for 64x32x2 matricies
Tested on RPI 4 4GB

Runs TFLite Implementation of Mediapipe. 

tflite_facemesh.py is the Main file for now. I'm still messing around. 

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

How it works: 

The sbc takes the camera feed and processes the frames with mediapipe facemesh to return landmarks. The user presses a button to "reset" the "reference coordinates" which are then used to calculate landmark offsets as a normalized value to the video frame. In another thread, The different faces are drawn based on the button input. Each face is defined as a vector graphic being drawn with cario. The anchors are then manually assigend to different offsets from the landmark detector and that moves the anchors to move the mouth and eyes to the user's face. 

Current state:

~~Renders the Idle face just fine with offsets. Landmark detector runs at ~19fps at 320x240 it's acceptable but could be better. ~~

Mediapipe doesn't track well with the face this close to the camera. Dlib fairs about the same but is much faster. I need to train a new dlib model with a dataset from the helmet cam. 



To do: 

* Finish drawing the other face
* Add controller input (Wii remote for now)
* Make the background image a separate function
* Option to offload facemesh processing to another device (another SBC or an android phone)
* I forgor the rest











Idk what else to put, I wrote this in like 2 minutes 
Discord: Rames The Generic#3540
