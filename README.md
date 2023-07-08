
Complete rewrite from V1 as it was initally used as a learning tool. 

# Protogen-Head-RPI
Software for interfacing with displays and sensors for RPI based Protogen Heads.
Made for 64x32x2 matricies
Tested on RPI 4 2GB

# Protogen-Head-ROCK5B
Software for processing the Babble model and display rendering. 


Runs a customized Babble mouth tracker model based on Mobileone. 
Project Babble repo: https://github.com/SummerSigh/ProjectBabble


https://user-images.githubusercontent.com/53163624/167325850-92f9755d-7d87-4397-bf45-9e34f66615f9.mp4



## How it works: ##

The rpi broadcasts an mjpeg stream of the internal cameras using ustreamer, udp packets containing imu data, and lisitens for udp packets for the main displays and osc messages for the minioled. 
The rock5 receives the mjpeg stream and imu data and renders the display using a mesh defined as a set of obj files and broadcasts the final frame. 

## Current state: ##

Babble model easily runs at a solid 60 fps on the npu. Blendshape predictions, customization shapekeys, and imutracking shapes are all smoothed using a oneeurofilter. 

## Implemented Models: ##
- [x] Customized Babble MouthTracker model.
- [ ] Protogen claw landmark/classifer model. (handtracking but for suit paws)






## To do (By Priority): ##

* Make socket input function without a router (p2p via bluetooth or WiFi Direct)
~~* Add Linear Transistion between faces~~
~~* Add filtering to the shapes~~
* Add controller input (hand tracker and maybe webui))
~~* Option to offload facemesh processing to another device (another SBC or an android phone)~~
* I forgor the rest











Idk what else to put, I wrote this in like 2 minutes 

## Contact ##

Discord: Rames The Generic#3540
