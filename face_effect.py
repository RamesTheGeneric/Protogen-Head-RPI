#       Contains Raster graphics for overlays (Blush, tears, images, etc...)






from cv2 import imread, IMREAD_UNCHANGED
import cv2
import ring
from cvzone import overlayPNG
import numpy as np

storage = {}
@ring.dict(storage, expire=1)   
def loadimages():
    blush_1 = imread('overlays/blush.png', IMREAD_UNCHANGED)
    blush_2 = imread('overlays/tears.png', IMREAD_UNCHANGED)
    images = (blush_1, blush_2)
    return images

def create_blank(width, height, rgb_color=(0, 0, 0, 255)):
    image = np.zeros((height, width, 4), np.uint8)
    color = tuple(reversed(rgb_color))
    image[:] = color
    return image


         



def main(res, mouth_x, mouth_y, eye_r_y, eye_l_y, surface, button):
    (H , W) = 128, 32
    overlays = loadimages()
    if any('overlay' in s for s in button):
        if any('overlay_1' in s for s in button):
            res = overlayPNG(res, overlays[0])
        if any('overlay_2' in s for s in button):
            res = overlayPNG(res, overlays[1])
    
    else:  
        blank = create_blank(H, W)
        res = overlayPNG(res, blank)

    

    return res
    
    #Blank.draw(ctx)
