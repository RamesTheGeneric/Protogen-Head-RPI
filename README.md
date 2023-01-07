
Complete rewrite is in order as this current codebase has served as a testbed and a learning tool. The rewrite will take place in a new branch when I get around to it. It'll use a blendshape facetracker for shapekeys instead of dlib landmarks meaning obj files for blendshapes. It'll also have many of the features such as camera view, remote control, etc implemented from the start. Pretty sure I'm just writing this for myself but atleast i'll remember after mff.



# Protogen-Head-RPI
Software for RPI based Protogen Heads

Made for 64x32x2 matricies
Tested on RPI 4 4GB




~~Runs TFLite Implementation of Mediapipe~~

Runs custom Dlib shape predictor. 


dlib_facemesh.py is the Main file for now. I'm still messing around. 


https://user-images.githubusercontent.com/53163624/167325850-92f9755d-7d87-4397-bf45-9e34f66615f9.mp4



## How it works: ##

The sbc takes the camera feed and processes the frames with mediapipe facemesh to return landmarks. The user presses a button to "reset" the "reference coordinates" which are then used to calculate landmark offsets as a normalized value to the video frame. In another thread, The different faces are drawn based on the button input. Each face is defined as a vector graphic being drawn with cario. The anchors are then manually assigend to different offsets from the landmark detector and that moves the anchors to move the mouth and eyes to the user's face. 

## Current state: ##

New Dlib model tracks ok at ~100 fps. I need to improve the dataset and add filtering but it looks really promising.

## Implemented Models: ##
- [x] Custom Dlib HOG Face Detector for full bounding box
- [ ] Custom Dlib HOG Face Detector for detecting mouth presence (To-do)
- [x] Custom Dlib Shape Predictor for Mouth Landmarks






## To do (By Priority): ##

~~* Make socket input function without a router (p2p via bluetooth or WiFi Direct)~~
* Add Linear Transistion between faces
* Add filtering to the landmarks
* Add controller input (cheapo vr controller for now)
* Add Lucid Glove input (Custom lucid gloves in the shape of protogen claws)
* Option to offload facemesh processing to another device (another SBC or an android phone)
* I forgor the rest











Idk what else to put, I wrote this in like 2 minutes 

## Contact ##

Discord: Rames The Generic#3540
