#Contains Graphics for to draw faces (Idle, Excited, Sad, OWO, Blush, Cry, Etc...) 

#       0: Mouth
#       1: Eye
#       2: Nose
#       3: Puiple




from xml.dom import minidom
from timeit import default_timer as timer
import ring
storage = {}
@ring.dict(storage, expire=1)
def read_face(filename):

    mydoc = minidom.parse(filename)
    features = []
    feature = mydoc.getElementsByTagName('polygon')
    for i in range(len(feature)):
        x = []
        y = []
        points = feature[i].attributes['points'].value
        points = points.split()
        for i in range(len(points)):
            if (i % 2) == 0:
                x.append(points[i])
            else:
                y.append(points[i])
        features.append((x, y))
    return features

#          =====Face List=====

def load_faces():
    idle = read_face('faces/idle.svg')
    faces = (idle)
    return faces

#           =====Blank=====
class Blank():
    def draw(ctx):
        ctx.set_source_rgb(1, 1, 1)
        ctx.rectangle(0, 0, 64, 32)
        ctx.fill()        

#          =====Idle=====

#          -----Mouth-----
class Idle():
    def mouth(ctx, mouth_x, mouth_y, eye_r_y, eye_l_y, surface, faces):  ## To-do: Move faces to xml file
        ctx.set_source_rgb(1, 1, 1)
        # Mouth coord driven face
        x_scale = .5
        y_scale = -.3
        face = faces[0][0]
        ctx.move_to(64, 23 - (mouth_y[3] * y_scale))
        ctx.line_to(52 - (mouth_x[3] * x_scale), 26 - (mouth_y[3] * y_scale))
        ctx.line_to(49 - (mouth_x[2] * x_scale), 22 - (mouth_y[2] * y_scale))
        ctx.line_to(42 - (mouth_x[1] * x_scale), 24 - (mouth_y[1] * y_scale))
        ctx.line_to(24 - (mouth_x[0] * x_scale), 17 - (mouth_y[0] * y_scale))
        ctx.line_to(24 - (mouth_x[0] * x_scale), 18 - (mouth_y[0] * y_scale))
        ctx.line_to(26 - (mouth_x[0] * x_scale), 19 - (mouth_y[0] * y_scale))
        ctx.line_to(42 - (mouth_x[11] * x_scale), 25 - (mouth_y[11] * y_scale))
        ctx.line_to(48 - (mouth_x[10] * x_scale), 23 - (mouth_y[10] * y_scale))
        ctx.line_to(51 - (mouth_x[9] * x_scale), 27 - (mouth_y[9] * y_scale))
        ctx.line_to(64, 24 - (mouth_y[9] * y_scale))

        ctx.fill()
    '''
    def mouth(ctx, mouth_x, mouth_y, eye_r_y, eye_l_y, surface, faces):  ## To-do: Move faces to xml file
        ctx.set_source_rgb(1, 1, 1)
        # Mouth coord driven face
        x_scale = .5
        y_scale = -.3
        
        
        ctx.move_to(64, 23 - (mouth_y[3] * y_scale))
        ctx.line_to(52 - (mouth_x[3] * x_scale), 26 - (mouth_y[3] * y_scale))
        ctx.line_to(49 - (mouth_x[2] * x_scale), 22 - (mouth_y[2] * y_scale))
        ctx.line_to(42 - (mouth_x[1] * x_scale), 24 - (mouth_y[1] * y_scale))
        ctx.line_to(24 - (mouth_x[0] * x_scale), 17 - (mouth_y[0] * y_scale))
        ctx.line_to(24 - (mouth_x[0] * x_scale), 18 - (mouth_y[0] * y_scale))
        ctx.line_to(26 - (mouth_x[0] * x_scale), 19 - (mouth_y[0] * y_scale))
        ctx.line_to(42 - (mouth_x[11] * x_scale), 25 - (mouth_y[11] * y_scale))
        ctx.line_to(48 - (mouth_x[10] * x_scale), 23 - (mouth_y[10] * y_scale))
        ctx.line_to(51 - (mouth_x[9] * x_scale), 27 - (mouth_y[9] * y_scale))
        ctx.line_to(64, 24 - (mouth_y[9] * y_scale))

        ctx.fill()
        '''

    def eye(ctx, eye_r_y, eye_l_y, faces):
        x_scale = .5
        y_scale = -.3
        ctx.move_to(19.4, 3.5)
        ctx.line_to(23.9, 1.8)
        ctx.line_to(29.5, 2)
        ctx.line_to(32.8, 3.6)
        ctx.line_to(34, 7.3)
        ctx.line_to(34.2, 9.6)
        ctx.line_to(31.4, 9.3)
        ctx.line_to(24, 9)
        ctx.line_to(18.6, 8.6)
        ctx.line_to(16.9, 8.2)
        ctx.line_to(18.1, 7.8)
        ctx.fill()
    
    #def pupil():



def main(ctx, mouth_x, mouth_y, eye_r_y, eye_l_y, surface, button):
    
    start = timer()
    faces = load_faces()
    end = timer()
    print('load_time: ' + str(end - start))
    print('memory: ' + str(storage))
    #print(faces)
    Idle.mouth(ctx, mouth_x, mouth_y, eye_r_y, eye_l_y, surface, faces)
    Idle.eye(ctx, eye_r_y, eye_l_y, faces)
    #print(mouth_y)
    
    buf = surface.get_data()
    return buf
    
    #Blank.draw(ctx)
