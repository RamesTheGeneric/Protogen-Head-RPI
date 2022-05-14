from xml.dom import minidom
from timeit import default_timer as timer
import ring
storage = {}
@ring.dict(storage, expire=1)       # Cache the loaded files into ram for the next call
def read_face(filename):

    mydoc = minidom.parse(filename)
    features = []
    feature = mydoc.getElementsByTagName('polygon')
    for i in range(1, (len(feature)), 2):
        x_r = []
        y_r = []
        x_l = []
        y_l = []
        points = feature[i - 1].attributes['points'].value
        points = points.split()
        for n in range(len(points)):
            if (n % 2) == 0:
                x_r.append(float(points[n]))
            else:
                y_r.append(float(points[n]))
        points = feature[(i)].attributes['points'].value
        points = points.split()
        for n in range(len(points)):
            if (n % 2) == 0:
                x_l.append(float(points[n]))
            else:
                y_l.append(float(points[n]))

        features.append(((x_r, y_r), (x_l, y_l)))
    return features






#          =====Face List=====

def load_faces():
    idle = read_face('faces/idle_m.svg')
    faces = (idle)
    return faces

#           =====Blank=====

#          =====Idle=====

#          -----Mouth-----
class Blush():
    def draw(ctx faces):  ## To-do: Move faces to xml file
        ctx.set_source_rgb(1, 1, 1)


    #def pupil():



def main(ctx, mouth_x, mouth_y, eye_r_y, eye_l_y, surface, button):
    
    faces = (load_faces(), "test")
    Blush.draw(ctx, faces)

    
    buf = surface.get_data()

    return buf
    
    #Blank.draw(ctx)
