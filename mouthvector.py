import cairo
import cv2
with open("mouth.svg", "r") as myfile:
    vector = myfile.readlines()
print(vector)

with cairo.SVGSurface("geek1.svg", 640, 320) as surface:
 
    # creating a cairo context object
    ctx = cairo.Context(surface)
 
    # creating a arc with using close path method
    ctx.arc(300, 60, 40, 0, 1*22/7)
 
    # making close path
    ctx.close_path()
    ctx.fill()
 
    # getting fill extends
    a = ctx.fill_extents()
 
    # stroke the context to remove the moved pen
    ctx.stroke()
 
# printing message when file is saved

print(a)