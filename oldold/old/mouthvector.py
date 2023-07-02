import cairo
import numpy
import cv2
import numpy as np
with open("mouth.svg", "r") as myfile:
    vector = myfile.readlines()
print(vector)

w, h = 64, 32
surface = cairo.ImageSurface (cairo.FORMAT_ARGB32, w, h)
ctx = cairo.Context (surface)

# creating a cairo context object
ctx = cairo.Context(surface)
ctx.set_source_rgb(1, 1, 1)
# creating a arc with using close path method
ctx.move_to(61, 23)
ctx.line_to(52, 26)
ctx.line_to(49, 22)
ctx.line_to(42, 24)
ctx.line_to(24, 16.8)
ctx.line_to(24, 17.8)
ctx.line_to(26, 18.5)
ctx.line_to(42, 25)
ctx.line_to(48.5, 23)
ctx.line_to(51.5, 27)
ctx.line_to(62, 23.5)

# making close path
ctx.fill()

# getting fill extends
buf = surface.get_data()
array = np.ndarray (shape=(h,w,4), dtype=np.uint8, buffer=buf)
 
# printing message when file is saved
cv2.imshow('img_out', np.asarray(array))
cv2.waitKey(0)