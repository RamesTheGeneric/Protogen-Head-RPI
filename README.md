
Complete rewrite from V1 as it was initally used as a learning tool. 

# Protogen-Head-RPI
Software for interfacing with displays and sensors for RPI based Protogen Heads.
Made for 64x32x2 matricies
Tested on RPI 4 2GB but it should work on any multicore rpi.
NOTE: I'm only using a pi for the led matrix libs. Otherwise I'd probably only use the rock board. 

# Protogen-Head-ROCK5B
Software for processing the Babble model and display rendering. 
Tested on a Rock5B 16GB but I think it should be fine on any rk3588 or even rk3566 board.


Runs a customized Babble mouth tracker model based on [MobileOne](https://github.com/apple/ml-mobileone). 

Project Babble repo: https://github.com/SummerSigh/ProjectBabble




https://github.com/RamesTheGeneric/Protogen-Head-RPI/assets/53163624/e94f1c84-583c-49f9-831b-e6525cff7ee2



## How it works: ##

The rpi broadcasts an mjpeg stream of the internal cameras using ustreamer, udp packets containing imu data, and lisitens for udp packets for the main displays and osc messages for the minioled. 
The rock5 receives the mjpeg stream and imu data and renders the display using a mesh defined as a set of obj files and broadcasts the final frame. 

## Current state: ##

Babble model easily runs at a solid 60 fps on the npu. Blendshape predictions, customization shapekeys, and imutracking shapes are all smoothed using a oneeurofilter. 

## Implemented Models: ##
- [x] Customized Babble MouthTracker model.
- [ ] Protogen claw landmark/classifer model. (handtracking but for suit paws)






## To do (By Priority): ##

* Add controller input (hand tracker and maybe webui for phones))
* Make socket input function without a router (p2p via bluetooth or WiFi Direct)
* rpi standalone???
* I forgor the rest











Idk what else to put, I wrote this in like 2 minutes 

## Contact ##

* Discord: ramesthegeneric
* Idk how to run a discord server: https://discord.gg/w2ArxtrSjC

