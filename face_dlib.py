#   Contains Graphics for to draw faces (Idle, Excited, Sad, OWO, Blush, Cry, Etc...) 
#   face_effect.py has color things like Blush, Tears, Anime Angry thing, etc that render over everything

#   +++++First+++++
#       0: Idle
#       1: Tired
#       2: Annoyed
#       3: Sad
#       4: OWO
#       5: The Rock
#       6: XD
#       7: 

#   +++++Second+++++
#       0: Mouth
#       1: Eye
#       2: Nose
#       3: Puiple

#   +++++Third+++++
#       0: Right
#       1: Left

#   +++++Forth+++++
#       0: X
#       1: Y

#   +++++Fith+++++
#       0 - 15: landmark




from re import S
from sqlite3 import DatabaseError
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
    tired = read_face('faces/tired_m.svg')
    annoyed = read_face('faces/annoyed_m.svg')
    sad = read_face('faces/sad_m.svg')
    owo = read_face('faces/owo_m.svg')
    rock = read_face('faces/rock_m.svg')
    xd = read_face('faces/xd_m.svg')
    faces = (
        idle, 
        tired, 
        annoyed, 
        sad, 
        owo, 
        rock,
        xd
        )
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
        #print(str(faces))
        face = faces[0][0][0]   #   Idle, Mouth, Right
        #                   |Feature|l/r
        #print(faces)
        ctx.move_to(face[0][0], face[1][0] - (mouth_y[3] * y_scale))
        ctx.line_to(face[0][1] - (mouth_x[3] * x_scale), face[1][1] - (mouth_y[3] * y_scale))
        ctx.line_to(face[0][2] - (mouth_x[2] * x_scale), face[1][2] - (mouth_y[2] * y_scale))
        ctx.line_to(face[0][3] - (mouth_x[1] * x_scale), face[1][3] - (mouth_y[1] * y_scale))
        ctx.line_to(face[0][4] - (mouth_x[0] * x_scale), face[1][4] - (mouth_y[0] * y_scale))
        ctx.line_to(face[0][5] - (mouth_x[0] * x_scale), face[1][5] - (mouth_y[0] * y_scale))
        ctx.line_to(face[0][6] - (mouth_x[0] * x_scale), face[1][6] - (mouth_y[0] * y_scale))
        ctx.line_to(face[0][7] - (mouth_x[11] * x_scale), face[1][7] - (mouth_y[11] * y_scale))
        ctx.line_to(face[0][8] - (mouth_x[10] * x_scale), face[1][8] - (mouth_y[10] * y_scale))
        ctx.line_to(face[0][9] - (mouth_x[9] * x_scale), face[1][9] - (mouth_y[9] * y_scale))
        ctx.line_to(face[0][10], face[1][10] - (mouth_y[9] * y_scale))

        face = faces[0][0][1]   #   Idle, Mouth, Left
        ctx.move_to(face[0][0], face[1][0] - (mouth_y[3] * y_scale))
        ctx.line_to(face[0][1] - (mouth_x[3] * x_scale), face[1][1] - (mouth_y[3] * y_scale))
        ctx.line_to(face[0][2] - (mouth_x[4] * x_scale), face[1][2] - (mouth_y[4] * y_scale))
        ctx.line_to(face[0][3] - (mouth_x[5] * x_scale), face[1][3] - (mouth_y[5] * y_scale))
        ctx.line_to(face[0][4] - (mouth_x[6] * x_scale), face[1][4] - (mouth_y[6] * y_scale))
        ctx.line_to(face[0][5] - (mouth_x[6] * x_scale), face[1][5] - (mouth_y[6] * y_scale))
        ctx.line_to(face[0][6] - (mouth_x[6] * x_scale), face[1][6] - (mouth_y[6] * y_scale))
        ctx.line_to(face[0][7] - (mouth_x[7] * x_scale), face[1][7] - (mouth_y[7] * y_scale))
        ctx.line_to(face[0][8] - (mouth_x[8] * x_scale), face[1][8] - (mouth_y[8] * y_scale))
        ctx.line_to(face[0][9] - (mouth_x[9] * x_scale), face[1][9] - (mouth_y[9] * y_scale))
        ctx.line_to(face[0][10], face[1][10] - (mouth_y[9] * y_scale))
        ctx.fill()

    def eye(ctx, eye_r_y, eye_l_y, faces):
        ctx.set_source_rgb(1, 1, 1)
        x_scale = .5
        y_scale = -.3
        face = faces[0][1][0]   #   Idle, Eye, Right
        ctx.move_to(face[0][0], face[1][0])
        ctx.line_to(face[0][1], face[1][1])
        ctx.line_to(face[0][2], face[1][2])
        ctx.line_to(face[0][3], face[1][3])
        ctx.line_to(face[0][4], face[1][4])
        ctx.line_to(face[0][5], face[1][5])
        ctx.line_to(face[0][6], face[1][6])
        ctx.line_to(face[0][7], face[1][7])
        ctx.line_to(face[0][8], face[1][8])
        ctx.line_to(face[0][9], face[1][9])
        ctx.line_to(face[0][10], face[1][10])
        face = faces[0][1][1]   #   Idle, Eye, Left
        ctx.move_to(face[0][0], face[1][0])
        ctx.line_to(face[0][1], face[1][1])
        ctx.line_to(face[0][2], face[1][2])
        ctx.line_to(face[0][3], face[1][3])
        ctx.line_to(face[0][4], face[1][4])
        ctx.line_to(face[0][5], face[1][5])
        ctx.line_to(face[0][6], face[1][6])
        ctx.line_to(face[0][7], face[1][7])
        ctx.line_to(face[0][8], face[1][8])
        ctx.line_to(face[0][9], face[1][9])
        ctx.line_to(face[0][10], face[1][10])
        ctx.fill()
    
    def nose(ctx, faces):
        ctx.set_source_rgb(1, 1, 1)
        face = faces[0][2][0]   #   Idle, Nose, Right
        ctx.move_to(face[0][0], face[1][0])
        ctx.line_to(face[0][1], face[1][1])
        ctx.line_to(face[0][2], face[1][2])
        ctx.line_to(face[0][3], face[1][3])
        ctx.line_to(face[0][4], face[1][4])
        face = faces[0][2][1]   #   Idle, Nose, Left
        ctx.move_to(face[0][0], face[1][0])
        ctx.line_to(face[0][1], face[1][1])
        ctx.line_to(face[0][2], face[1][2])
        ctx.line_to(face[0][3], face[1][3])
        ctx.line_to(face[0][4], face[1][4])
        ctx.fill()

    def puiple(ctx, eye_r_y, eye_l_y, faces):
        ctx.set_source_rgb(0, 0, 0)
        x_scale = .5
        y_scale = -.3
        face = faces[0][3][0]   #   Idle, Puiple, Right
        ctx.move_to(face[0][0], face[1][0])
        ctx.line_to(face[0][1], face[1][1])
        ctx.line_to(face[0][2], face[1][2])
        ctx.line_to(face[0][3], face[1][3])
        ctx.line_to(face[0][4], face[1][4])
        ctx.line_to(face[0][5], face[1][5])
        ctx.line_to(face[0][6], face[1][6])
        ctx.line_to(face[0][7], face[1][7])
        ctx.line_to(face[0][8], face[1][8])
        face = faces[0][3][1]   #   Idle, Puiple, Left
        ctx.move_to(face[0][0], face[1][0])
        ctx.line_to(face[0][1], face[1][1])
        ctx.line_to(face[0][2], face[1][2])
        ctx.line_to(face[0][3], face[1][3])
        ctx.line_to(face[0][4], face[1][4])
        ctx.line_to(face[0][5], face[1][5])
        ctx.line_to(face[0][6], face[1][6])
        ctx.line_to(face[0][7], face[1][7])
        ctx.line_to(face[0][8], face[1][8])
        ctx.fill()

class Tired():
    def mouth(ctx, mouth_x, mouth_y, eye_r_y, eye_l_y, surface, faces):  ## To-do: Move faces to xml file
        ctx.set_source_rgb(1, 1, 1)
        # Mouth coord driven face
        x_scale = .5
        y_scale = -.3
        #print(str(faces))
        face = faces[1][0][0]   #   Idle, Mouth, Right
        ctx.move_to(face[0][0], face[1][0] - (mouth_y[3] * y_scale))
        ctx.line_to(face[0][1] - (mouth_x[3] * x_scale), face[1][1] - (mouth_y[3] * y_scale))
        ctx.line_to(face[0][2] - (mouth_x[2] * x_scale), face[1][2] - (mouth_y[2] * y_scale))
        ctx.line_to(face[0][3] - (mouth_x[1] * x_scale), face[1][3] - (mouth_y[1] * y_scale))
        ctx.line_to(face[0][4] - (mouth_x[0] * x_scale), face[1][4] - (mouth_y[0] * y_scale))
        ctx.line_to(face[0][5] - (mouth_x[0] * x_scale), face[1][5] - (mouth_y[0] * y_scale))
        ctx.line_to(face[0][6] - (mouth_x[0] * x_scale), face[1][6] - (mouth_y[0] * y_scale))
        ctx.line_to(face[0][7] - (mouth_x[11] * x_scale), face[1][7] - (mouth_y[11] * y_scale))
        ctx.line_to(face[0][8] - (mouth_x[10] * x_scale), face[1][8] - (mouth_y[10] * y_scale))
        ctx.line_to(face[0][9] - (mouth_x[9] * x_scale), face[1][9] - (mouth_y[9] * y_scale))
        ctx.line_to(face[0][10], face[1][10] - (mouth_y[9] * y_scale))

        face = faces[1][0][1]   #   Idle, Mouth, Left
        ctx.move_to(face[0][0], face[1][0] - (mouth_y[3] * y_scale))
        ctx.line_to(face[0][1] - (mouth_x[3] * x_scale), face[1][1] - (mouth_y[3] * y_scale))
        ctx.line_to(face[0][2] - (mouth_x[4] * x_scale), face[1][2] - (mouth_y[4] * y_scale))
        ctx.line_to(face[0][3] - (mouth_x[5] * x_scale), face[1][3] - (mouth_y[5] * y_scale))
        ctx.line_to(face[0][4] - (mouth_x[6] * x_scale), face[1][4] - (mouth_y[6] * y_scale))
        ctx.line_to(face[0][5] - (mouth_x[6] * x_scale), face[1][5] - (mouth_y[6] * y_scale))
        ctx.line_to(face[0][6] - (mouth_x[6] * x_scale), face[1][6] - (mouth_y[6] * y_scale))
        ctx.line_to(face[0][7] - (mouth_x[7] * x_scale), face[1][7] - (mouth_y[7] * y_scale))
        ctx.line_to(face[0][8] - (mouth_x[8] * x_scale), face[1][8] - (mouth_y[8] * y_scale))
        ctx.line_to(face[0][9] - (mouth_x[9] * x_scale), face[1][9] - (mouth_y[9] * y_scale))
        ctx.line_to(face[0][10], face[1][10] - (mouth_y[9] * y_scale))
        ctx.fill()

    def eye(ctx, eye_r_y, eye_l_y, faces):
        ctx.set_source_rgb(1, 1, 1)
        x_scale = .5
        y_scale = -.3
        face = faces[1][1][0]   #   Idle, Eye, Right
        ctx.move_to(face[0][0], face[1][0])
        ctx.line_to(face[0][1], face[1][1])
        ctx.line_to(face[0][2], face[1][2])
        ctx.line_to(face[0][3], face[1][3])
        ctx.line_to(face[0][4], face[1][4])
        ctx.line_to(face[0][5], face[1][5])
        ctx.line_to(face[0][6], face[1][6])
        ctx.line_to(face[0][7], face[1][7])
        ctx.line_to(face[0][8], face[1][8])
        ctx.line_to(face[0][9], face[1][9])
        ctx.line_to(face[0][10], face[1][10])
        face = faces[1][1][1]   #   Idle, Eye, Left
        ctx.move_to(face[0][0], face[1][0])
        ctx.line_to(face[0][1], face[1][1])
        ctx.line_to(face[0][2], face[1][2])
        ctx.line_to(face[0][3], face[1][3])
        ctx.line_to(face[0][4], face[1][4])
        ctx.line_to(face[0][5], face[1][5])
        ctx.line_to(face[0][6], face[1][6])
        ctx.line_to(face[0][7], face[1][7])
        ctx.line_to(face[0][8], face[1][8])
        ctx.line_to(face[0][9], face[1][9])
        ctx.line_to(face[0][10], face[1][10])
        ctx.fill()
    
    def nose(ctx, faces):
        ctx.set_source_rgb(1, 1, 1)
        face = faces[1][2][0]   #   Idle, Nose, Right
        ctx.move_to(face[0][0], face[1][0])
        ctx.line_to(face[0][1], face[1][1])
        ctx.line_to(face[0][2], face[1][2])
        ctx.line_to(face[0][3], face[1][3])
        ctx.line_to(face[0][4], face[1][4])
        face = faces[1][2][1]   #   Idle, Nose, Left
        ctx.move_to(face[0][0], face[1][0])
        ctx.line_to(face[0][1], face[1][1])
        ctx.line_to(face[0][2], face[1][2])
        ctx.line_to(face[0][3], face[1][3])
        ctx.line_to(face[0][4], face[1][4])
        ctx.fill()

    def puiple(ctx, eye_r_y, eye_l_y, faces):
        ctx.set_source_rgb(0, 0, 0)
        x_scale = .5
        y_scale = -.3
        face = faces[1][3][0]   #   Idle, Puiple, Right
        ctx.move_to(face[0][0], face[1][0])
        ctx.line_to(face[0][1], face[1][1])
        ctx.line_to(face[0][2], face[1][2])
        ctx.line_to(face[0][3], face[1][3])
        ctx.line_to(face[0][4], face[1][4])
        ctx.line_to(face[0][5], face[1][5])
        ctx.line_to(face[0][6], face[1][6])
        ctx.line_to(face[0][7], face[1][7])
        ctx.line_to(face[0][8], face[1][8])
        face = faces[1][3][1]   #   Idle, Puiple, Left
        ctx.move_to(face[0][0], face[1][0])
        ctx.line_to(face[0][1], face[1][1])
        ctx.line_to(face[0][2], face[1][2])
        ctx.line_to(face[0][3], face[1][3])
        ctx.line_to(face[0][4], face[1][4])
        ctx.line_to(face[0][5], face[1][5])
        ctx.line_to(face[0][6], face[1][6])
        ctx.line_to(face[0][7], face[1][7])
        ctx.line_to(face[0][8], face[1][8])
        ctx.fill()

class Annoyed():
    def mouth(ctx, mouth_x, mouth_y, eye_r_y, eye_l_y, surface, faces):  ## To-do: Move faces to xml file
        ctx.set_source_rgb(1, 1, 1)
        # Mouth coord driven face
        x_scale = .5
        y_scale = -.3
        #print(str(faces))
        face = faces[2][0][0]   #   Idle, Mouth, Right
        ctx.move_to(face[0][0], face[1][0] - (mouth_y[3] * y_scale))
        ctx.line_to(face[0][1] - (mouth_x[3] * x_scale), face[1][1] - (mouth_y[3] * y_scale))
        ctx.line_to(face[0][2] - (mouth_x[2] * x_scale), face[1][2] - (mouth_y[2] * y_scale))
        ctx.line_to(face[0][3] - (mouth_x[1] * x_scale), face[1][3] - (mouth_y[1] * y_scale))
        ctx.line_to(face[0][4] - (mouth_x[0] * x_scale), face[1][4] - (mouth_y[0] * y_scale))
        ctx.line_to(face[0][5] - (mouth_x[0] * x_scale), face[1][5] - (mouth_y[0] * y_scale))
        ctx.line_to(face[0][6] - (mouth_x[0] * x_scale), face[1][6] - (mouth_y[0] * y_scale))
        ctx.line_to(face[0][7] - (mouth_x[11] * x_scale), face[1][7] - (mouth_y[11] * y_scale))
        ctx.line_to(face[0][8] - (mouth_x[10] * x_scale), face[1][8] - (mouth_y[10] * y_scale))
        ctx.line_to(face[0][9] - (mouth_x[9] * x_scale), face[1][9] - (mouth_y[9] * y_scale))
        ctx.line_to(face[0][10], face[1][10] - (mouth_y[9] * y_scale))

        face = faces[2][0][1]   #   Idle, Mouth, Left
        ctx.move_to(face[0][0], face[1][0] - (mouth_y[3] * y_scale))
        ctx.line_to(face[0][1] - (mouth_x[3] * x_scale), face[1][1] - (mouth_y[3] * y_scale))
        ctx.line_to(face[0][2] - (mouth_x[4] * x_scale), face[1][2] - (mouth_y[4] * y_scale))
        ctx.line_to(face[0][3] - (mouth_x[5] * x_scale), face[1][3] - (mouth_y[5] * y_scale))
        ctx.line_to(face[0][4] - (mouth_x[6] * x_scale), face[1][4] - (mouth_y[6] * y_scale))
        ctx.line_to(face[0][5] - (mouth_x[6] * x_scale), face[1][5] - (mouth_y[6] * y_scale))
        ctx.line_to(face[0][6] - (mouth_x[6] * x_scale), face[1][6] - (mouth_y[6] * y_scale))
        ctx.line_to(face[0][7] - (mouth_x[7] * x_scale), face[1][7] - (mouth_y[7] * y_scale))
        ctx.line_to(face[0][8] - (mouth_x[8] * x_scale), face[1][8] - (mouth_y[8] * y_scale))
        ctx.line_to(face[0][9] - (mouth_x[9] * x_scale), face[1][9] - (mouth_y[9] * y_scale))
        ctx.line_to(face[0][10], face[1][10] - (mouth_y[9] * y_scale))
        ctx.fill()

    def eye(ctx, eye_r_y, eye_l_y, faces):
        ctx.set_source_rgb(1, 1, 1)
        x_scale = .5
        y_scale = -.3
        face = faces[2][1][0]   #   Idle, Eye, Right
        ctx.move_to(face[0][0], face[1][0])
        ctx.line_to(face[0][1], face[1][1])
        ctx.line_to(face[0][2], face[1][2])
        ctx.line_to(face[0][3], face[1][3])
        ctx.line_to(face[0][4], face[1][4])
        ctx.line_to(face[0][5], face[1][5])
        ctx.line_to(face[0][6], face[1][6])
        ctx.line_to(face[0][7], face[1][7])
        ctx.line_to(face[0][8], face[1][8])
        ctx.line_to(face[0][9], face[1][9])
        ctx.line_to(face[0][10], face[1][10])
        face = faces[2][1][1]   #   Idle, Eye, Left
        ctx.move_to(face[0][0], face[1][0])
        ctx.line_to(face[0][1], face[1][1])
        ctx.line_to(face[0][2], face[1][2])
        ctx.line_to(face[0][3], face[1][3])
        ctx.line_to(face[0][4], face[1][4])
        ctx.line_to(face[0][5], face[1][5])
        ctx.line_to(face[0][6], face[1][6])
        ctx.line_to(face[0][7], face[1][7])
        ctx.line_to(face[0][8], face[1][8])
        ctx.line_to(face[0][9], face[1][9])
        ctx.line_to(face[0][10], face[1][10])
        ctx.fill()
    
    def nose(ctx, faces):
        ctx.set_source_rgb(1, 1, 1)
        face = faces[2][2][0]   #   Idle, Nose, Right
        ctx.move_to(face[0][0], face[1][0])
        ctx.line_to(face[0][1], face[1][1])
        ctx.line_to(face[0][2], face[1][2])
        ctx.line_to(face[0][3], face[1][3])
        ctx.line_to(face[0][4], face[1][4])
        face = faces[2][2][1]   #   Idle, Nose, Left
        ctx.move_to(face[0][0], face[1][0])
        ctx.line_to(face[0][1], face[1][1])
        ctx.line_to(face[0][2], face[1][2])
        ctx.line_to(face[0][3], face[1][3])
        ctx.line_to(face[0][4], face[1][4])
        ctx.fill()

    def puiple(ctx, eye_r_y, eye_l_y, faces):
        ctx.set_source_rgb(0, 0, 0)
        x_scale = .5
        y_scale = -.3
        face = faces[2][3][0]   #   Idle, Puiple, Right
        ctx.move_to(face[0][0], face[1][0])
        ctx.line_to(face[0][1], face[1][1])
        ctx.line_to(face[0][2], face[1][2])
        ctx.line_to(face[0][3], face[1][3])
        ctx.line_to(face[0][4], face[1][4])
        ctx.line_to(face[0][5], face[1][5])
        ctx.line_to(face[0][6], face[1][6])
        ctx.line_to(face[0][7], face[1][7])
        ctx.line_to(face[0][8], face[1][8])
        face = faces[2][3][1]   #   Idle, Puiple, Left
        ctx.move_to(face[0][0], face[1][0])
        ctx.line_to(face[0][1], face[1][1])
        ctx.line_to(face[0][2], face[1][2])
        ctx.line_to(face[0][3], face[1][3])
        ctx.line_to(face[0][4], face[1][4])
        ctx.line_to(face[0][5], face[1][5])
        ctx.line_to(face[0][6], face[1][6])
        ctx.line_to(face[0][7], face[1][7])
        ctx.line_to(face[0][8], face[1][8])
        ctx.fill()

class Sad():
    def mouth(ctx, mouth_x, mouth_y, eye_r_y, eye_l_y, surface, faces):  ## To-do: Move faces to xml file
        ctx.set_source_rgb(1, 1, 1)
        # Mouth coord driven face
        x_scale = .5
        y_scale = -.3
        #print(str(faces))
        face = faces[3][0][0]   #   Idle, Mouth, Right
        ctx.move_to(face[0][0], face[1][0] - (mouth_y[3] * y_scale))
        ctx.line_to(face[0][1] - (mouth_x[3] * x_scale), face[1][1] - (mouth_y[3] * y_scale))
        ctx.line_to(face[0][2] - (mouth_x[2] * x_scale), face[1][2] - (mouth_y[2] * y_scale))
        ctx.line_to(face[0][3] - (mouth_x[1] * x_scale), face[1][3] - (mouth_y[1] * y_scale))
        ctx.line_to(face[0][4] - (mouth_x[0] * x_scale), face[1][4] - (mouth_y[0] * y_scale))
        ctx.line_to(face[0][5] - (mouth_x[0] * x_scale), face[1][5] - (mouth_y[0] * y_scale))
        ctx.line_to(face[0][6] - (mouth_x[0] * x_scale), face[1][6] - (mouth_y[0] * y_scale))
        ctx.line_to(face[0][7] - (mouth_x[11] * x_scale), face[1][7] - (mouth_y[11] * y_scale))
        ctx.line_to(face[0][8] - (mouth_x[10] * x_scale), face[1][8] - (mouth_y[10] * y_scale))
        ctx.line_to(face[0][9] - (mouth_x[9] * x_scale), face[1][9] - (mouth_y[9] * y_scale))
        ctx.line_to(face[0][10], face[1][10] - (mouth_y[9] * y_scale))

        face = faces[3][0][1]   #   Idle, Mouth, Left
        ctx.move_to(face[0][0], face[1][0] - (mouth_y[3] * y_scale))
        ctx.line_to(face[0][1] - (mouth_x[3] * x_scale), face[1][1] - (mouth_y[3] * y_scale))
        ctx.line_to(face[0][2] - (mouth_x[4] * x_scale), face[1][2] - (mouth_y[4] * y_scale))
        ctx.line_to(face[0][3] - (mouth_x[5] * x_scale), face[1][3] - (mouth_y[5] * y_scale))
        ctx.line_to(face[0][4] - (mouth_x[6] * x_scale), face[1][4] - (mouth_y[6] * y_scale))
        ctx.line_to(face[0][5] - (mouth_x[6] * x_scale), face[1][5] - (mouth_y[6] * y_scale))
        ctx.line_to(face[0][6] - (mouth_x[6] * x_scale), face[1][6] - (mouth_y[6] * y_scale))
        ctx.line_to(face[0][7] - (mouth_x[7] * x_scale), face[1][7] - (mouth_y[7] * y_scale))
        ctx.line_to(face[0][8] - (mouth_x[8] * x_scale), face[1][8] - (mouth_y[8] * y_scale))
        ctx.line_to(face[0][9] - (mouth_x[9] * x_scale), face[1][9] - (mouth_y[9] * y_scale))
        ctx.line_to(face[0][10], face[1][10] - (mouth_y[9] * y_scale))
        ctx.fill()

    def eye(ctx, eye_r_y, eye_l_y, faces):
        ctx.set_source_rgb(1, 1, 1)
        x_scale = .5
        y_scale = -.3
        face = faces[3][1][0]   #   Idle, Eye, Right
        ctx.move_to(face[0][0], face[1][0])
        ctx.line_to(face[0][1], face[1][1])
        ctx.line_to(face[0][2], face[1][2])
        ctx.line_to(face[0][3], face[1][3])
        ctx.line_to(face[0][4], face[1][4])
        ctx.line_to(face[0][5], face[1][5])
        ctx.line_to(face[0][6], face[1][6])
        ctx.line_to(face[0][7], face[1][7])
        ctx.line_to(face[0][8], face[1][8])
        ctx.line_to(face[0][9], face[1][9])
        ctx.line_to(face[0][10], face[1][10])
        face = faces[3][1][1]   #   Idle, Eye, Left
        ctx.move_to(face[0][0], face[1][0])
        ctx.line_to(face[0][1], face[1][1])
        ctx.line_to(face[0][2], face[1][2])
        ctx.line_to(face[0][3], face[1][3])
        ctx.line_to(face[0][4], face[1][4])
        ctx.line_to(face[0][5], face[1][5])
        ctx.line_to(face[0][6], face[1][6])
        ctx.line_to(face[0][7], face[1][7])
        ctx.line_to(face[0][8], face[1][8])
        ctx.line_to(face[0][9], face[1][9])
        ctx.line_to(face[0][10], face[1][10])
        ctx.fill()
    
    def nose(ctx, faces):
        ctx.set_source_rgb(1, 1, 1)
        face = faces[3][2][0]   #   Idle, Nose, Right
        ctx.move_to(face[0][0], face[1][0])
        ctx.line_to(face[0][1], face[1][1])
        ctx.line_to(face[0][2], face[1][2])
        ctx.line_to(face[0][3], face[1][3])
        ctx.line_to(face[0][4], face[1][4])
        face = faces[3][2][1]   #   Idle, Nose, Left
        ctx.move_to(face[0][0], face[1][0])
        ctx.line_to(face[0][1], face[1][1])
        ctx.line_to(face[0][2], face[1][2])
        ctx.line_to(face[0][3], face[1][3])
        ctx.line_to(face[0][4], face[1][4])
        ctx.fill()

    def puiple(ctx, eye_r_y, eye_l_y, faces):
        ctx.set_source_rgb(0, 0, 0)
        x_scale = .5
        y_scale = -.3
        face = faces[3][3][0]   #   Idle, Puiple, Right
        ctx.move_to(face[0][0], face[1][0])
        ctx.line_to(face[0][1], face[1][1])
        ctx.line_to(face[0][2], face[1][2])
        ctx.line_to(face[0][3], face[1][3])
        ctx.line_to(face[0][4], face[1][4])
        ctx.line_to(face[0][5], face[1][5])
        ctx.line_to(face[0][6], face[1][6])
        ctx.line_to(face[0][7], face[1][7])
        ctx.line_to(face[0][8], face[1][8])
        face = faces[3][3][1]   #   Idle, Puiple, Left
        ctx.move_to(face[0][0], face[1][0])
        ctx.line_to(face[0][1], face[1][1])
        ctx.line_to(face[0][2], face[1][2])
        ctx.line_to(face[0][3], face[1][3])
        ctx.line_to(face[0][4], face[1][4])
        ctx.line_to(face[0][5], face[1][5])
        ctx.line_to(face[0][6], face[1][6])
        ctx.line_to(face[0][7], face[1][7])
        ctx.line_to(face[0][8], face[1][8])
        ctx.fill()

class OWO():
    def mouth(ctx, mouth_x, mouth_y, eye_r_y, eye_l_y, surface, faces):  ## To-do: Move faces to xml file
        ctx.set_source_rgb(1, 1, 1)
        # Mouth coord driven face
        x_scale = 0
        y_scale = 0
        #print(str(faces))
        face = faces[4][0][0]   #   Idle, Mouth, Right
        ctx.move_to(face[0][0], face[1][0] - (mouth_y[3] * y_scale))
        ctx.line_to(face[0][1] - (mouth_x[3] * x_scale), face[1][1] - (mouth_y[3] * y_scale))
        ctx.line_to(face[0][2] - (mouth_x[2] * x_scale), face[1][2] - (mouth_y[2] * y_scale))
        ctx.line_to(face[0][3] - (mouth_x[1] * x_scale), face[1][3] - (mouth_y[1] * y_scale))
        ctx.line_to(face[0][4] - (mouth_x[0] * x_scale), face[1][4] - (mouth_y[0] * y_scale))
        ctx.line_to(face[0][5] - (mouth_x[0] * x_scale), face[1][5] - (mouth_y[0] * y_scale))
        ctx.line_to(face[0][6] - (mouth_x[0] * x_scale), face[1][6] - (mouth_y[0] * y_scale))
        ctx.line_to(face[0][7] - (mouth_x[11] * x_scale), face[1][7] - (mouth_y[11] * y_scale))
        ctx.line_to(face[0][8] - (mouth_x[10] * x_scale), face[1][8] - (mouth_y[10] * y_scale))
        ctx.line_to(face[0][9] - (mouth_x[9] * x_scale), face[1][9] - (mouth_y[9] * y_scale))
        ctx.line_to(face[0][10], face[1][10] - (mouth_y[9] * y_scale))

        face = faces[4][0][1]   #   Idle, Mouth, Left
        ctx.move_to(face[0][0], face[1][0] - (mouth_y[3] * y_scale))
        ctx.line_to(face[0][1] - (mouth_x[3] * x_scale), face[1][1] - (mouth_y[3] * y_scale))
        ctx.line_to(face[0][2] - (mouth_x[4] * x_scale), face[1][2] - (mouth_y[4] * y_scale))
        ctx.line_to(face[0][3] - (mouth_x[5] * x_scale), face[1][3] - (mouth_y[5] * y_scale))
        ctx.line_to(face[0][4] - (mouth_x[6] * x_scale), face[1][4] - (mouth_y[6] * y_scale))
        ctx.line_to(face[0][5] - (mouth_x[6] * x_scale), face[1][5] - (mouth_y[6] * y_scale))
        ctx.line_to(face[0][6] - (mouth_x[6] * x_scale), face[1][6] - (mouth_y[6] * y_scale))
        ctx.line_to(face[0][7] - (mouth_x[7] * x_scale), face[1][7] - (mouth_y[7] * y_scale))
        ctx.line_to(face[0][8] - (mouth_x[8] * x_scale), face[1][8] - (mouth_y[8] * y_scale))
        ctx.line_to(face[0][9] - (mouth_x[9] * x_scale), face[1][9] - (mouth_y[9] * y_scale))
        ctx.line_to(face[0][10], face[1][10] - (mouth_y[9] * y_scale))
        ctx.fill()

    def eye(ctx, eye_r_y, eye_l_y, faces):
        ctx.set_source_rgb(1, 1, 1)
        x_scale = .5
        y_scale = -.3
        face = faces[4][1][0]   #   Idle, Eye, Right
        ctx.move_to(face[0][0], face[1][0])
        ctx.line_to(face[0][1], face[1][1])
        ctx.line_to(face[0][2], face[1][2])
        ctx.line_to(face[0][3], face[1][3])
        ctx.line_to(face[0][4], face[1][4])
        ctx.line_to(face[0][5], face[1][5])
        ctx.line_to(face[0][6], face[1][6])
        ctx.line_to(face[0][7], face[1][7])
        ctx.line_to(face[0][8], face[1][8])
        ctx.line_to(face[0][9], face[1][9])
        ctx.line_to(face[0][10], face[1][10])
        face = faces[4][1][1]   #   Idle, Eye, Left
        ctx.move_to(face[0][0], face[1][0])
        ctx.line_to(face[0][1], face[1][1])
        ctx.line_to(face[0][2], face[1][2])
        ctx.line_to(face[0][3], face[1][3])
        ctx.line_to(face[0][4], face[1][4])
        ctx.line_to(face[0][5], face[1][5])
        ctx.line_to(face[0][6], face[1][6])
        ctx.line_to(face[0][7], face[1][7])
        ctx.line_to(face[0][8], face[1][8])
        ctx.line_to(face[0][9], face[1][9])
        ctx.line_to(face[0][10], face[1][10])
        ctx.fill()
    
    def nose(ctx, faces):
        ctx.set_source_rgb(1, 1, 1)
        face = faces[4][2][0]   #   Idle, Nose, Right
        ctx.move_to(face[0][0], face[1][0])
        ctx.line_to(face[0][1], face[1][1])
        ctx.line_to(face[0][2], face[1][2])
        ctx.line_to(face[0][3], face[1][3])
        ctx.line_to(face[0][4], face[1][4])
        face = faces[4][2][1]   #   Idle, Nose, Left
        ctx.move_to(face[0][0], face[1][0])
        ctx.line_to(face[0][1], face[1][1])
        ctx.line_to(face[0][2], face[1][2])
        ctx.line_to(face[0][3], face[1][3])
        ctx.line_to(face[0][4], face[1][4])
        ctx.fill()

    def puiple(ctx, eye_r_y, eye_l_y, faces):
        ctx.set_source_rgb(0, 0, 0)
        x_scale = .5
        y_scale = -.3
        face = faces[4][3][0]   #   Idle, Puiple, Right
        ctx.move_to(face[0][0], face[1][0])
        ctx.line_to(face[0][1], face[1][1])
        ctx.line_to(face[0][2], face[1][2])
        ctx.line_to(face[0][3], face[1][3])
        ctx.line_to(face[0][4], face[1][4])
        ctx.line_to(face[0][5], face[1][5])
        ctx.line_to(face[0][6], face[1][6])
        ctx.line_to(face[0][7], face[1][7])
        ctx.line_to(face[0][8], face[1][8])
        face = faces[4][3][1]   #   Idle, Puiple, Left
        ctx.move_to(face[0][0], face[1][0])
        ctx.line_to(face[0][1], face[1][1])
        ctx.line_to(face[0][2], face[1][2])
        ctx.line_to(face[0][3], face[1][3])
        ctx.line_to(face[0][4], face[1][4])
        ctx.line_to(face[0][5], face[1][5])
        ctx.line_to(face[0][6], face[1][6])
        ctx.line_to(face[0][7], face[1][7])
        ctx.line_to(face[0][8], face[1][8])
        ctx.fill()

class Rock():
    def mouth(ctx, mouth_x, mouth_y, eye_r_y, eye_l_y, surface, faces):  ## To-do: Move faces to xml file
        ctx.set_source_rgb(1, 1, 1)
        # Mouth coord driven face
        x_scale = .5
        y_scale = -.3
        #print(str(faces))
        face = faces[5][0][0]   #   Idle, Mouth, Right
        ctx.move_to(face[0][0], face[1][0] - (mouth_y[3] * y_scale))
        ctx.line_to(face[0][1] - (mouth_x[3] * x_scale), face[1][1] - (mouth_y[3] * y_scale))
        ctx.line_to(face[0][2] - (mouth_x[2] * x_scale), face[1][2] - (mouth_y[2] * y_scale))
        ctx.line_to(face[0][3] - (mouth_x[1] * x_scale), face[1][3] - (mouth_y[1] * y_scale))
        ctx.line_to(face[0][4] - (mouth_x[0] * x_scale), face[1][4] - (mouth_y[0] * y_scale))
        ctx.line_to(face[0][5] - (mouth_x[0] * x_scale), face[1][5] - (mouth_y[0] * y_scale))
        ctx.line_to(face[0][6] - (mouth_x[0] * x_scale), face[1][6] - (mouth_y[0] * y_scale))
        ctx.line_to(face[0][7] - (mouth_x[11] * x_scale), face[1][7] - (mouth_y[11] * y_scale))
        ctx.line_to(face[0][8] - (mouth_x[10] * x_scale), face[1][8] - (mouth_y[10] * y_scale))
        ctx.line_to(face[0][9] - (mouth_x[9] * x_scale), face[1][9] - (mouth_y[9] * y_scale))
        ctx.line_to(face[0][10], face[1][10] - (mouth_y[9] * y_scale))

        face = faces[5][0][1]   #   Idle, Mouth, Left
        ctx.move_to(face[0][0], face[1][0] - (mouth_y[3] * y_scale))
        ctx.line_to(face[0][1] - (mouth_x[3] * x_scale), face[1][1] - (mouth_y[3] * y_scale))
        ctx.line_to(face[0][2] - (mouth_x[4] * x_scale), face[1][2] - (mouth_y[4] * y_scale))
        ctx.line_to(face[0][3] - (mouth_x[5] * x_scale), face[1][3] - (mouth_y[5] * y_scale))
        ctx.line_to(face[0][4] - (mouth_x[6] * x_scale), face[1][4] - (mouth_y[6] * y_scale))
        ctx.line_to(face[0][5] - (mouth_x[6] * x_scale), face[1][5] - (mouth_y[6] * y_scale))
        ctx.line_to(face[0][6] - (mouth_x[6] * x_scale), face[1][6] - (mouth_y[6] * y_scale))
        ctx.line_to(face[0][7] - (mouth_x[7] * x_scale), face[1][7] - (mouth_y[7] * y_scale))
        ctx.line_to(face[0][8] - (mouth_x[8] * x_scale), face[1][8] - (mouth_y[8] * y_scale))
        ctx.line_to(face[0][9] - (mouth_x[9] * x_scale), face[1][9] - (mouth_y[9] * y_scale))
        ctx.line_to(face[0][10], face[1][10] - (mouth_y[9] * y_scale))
        ctx.fill()

    def eye(ctx, eye_r_y, eye_l_y, faces):
        ctx.set_source_rgb(1, 1, 1)
        x_scale = .5
        y_scale = -.3
        face = faces[5][1][0]   #   Idle, Eye, Right
        ctx.move_to(face[0][0], face[1][0])
        ctx.line_to(face[0][1], face[1][1])
        ctx.line_to(face[0][2], face[1][2])
        ctx.line_to(face[0][3], face[1][3])
        ctx.line_to(face[0][4], face[1][4])
        ctx.line_to(face[0][5], face[1][5])
        ctx.line_to(face[0][6], face[1][6])
        ctx.line_to(face[0][7], face[1][7])
        ctx.line_to(face[0][8], face[1][8])
        ctx.line_to(face[0][9], face[1][9])
        ctx.line_to(face[0][10], face[1][10])
        face = faces[5][1][1]   #   Idle, Eye, Left
        ctx.move_to(face[0][0], face[1][0])
        ctx.line_to(face[0][1], face[1][1])
        ctx.line_to(face[0][2], face[1][2])
        ctx.line_to(face[0][3], face[1][3])
        ctx.line_to(face[0][4], face[1][4])
        ctx.line_to(face[0][5], face[1][5])
        ctx.line_to(face[0][6], face[1][6])
        ctx.line_to(face[0][7], face[1][7])
        ctx.line_to(face[0][8], face[1][8])
        ctx.line_to(face[0][9], face[1][9])
        ctx.line_to(face[0][10], face[1][10])
        ctx.fill()
    
    def nose(ctx, faces):
        ctx.set_source_rgb(1, 1, 1)
        face = faces[5][2][0]   #   Idle, Nose, Right
        ctx.move_to(face[0][0], face[1][0])
        ctx.line_to(face[0][1], face[1][1])
        ctx.line_to(face[0][2], face[1][2])
        ctx.line_to(face[0][3], face[1][3])
        ctx.line_to(face[0][4], face[1][4])
        face = faces[5][2][1]   #   Idle, Nose, Left
        ctx.move_to(face[0][0], face[1][0])
        ctx.line_to(face[0][1], face[1][1])
        ctx.line_to(face[0][2], face[1][2])
        ctx.line_to(face[0][3], face[1][3])
        ctx.line_to(face[0][4], face[1][4])
        ctx.fill()

    def puiple(ctx, eye_r_y, eye_l_y, faces):
        ctx.set_source_rgb(0, 0, 0)
        x_scale = .5
        y_scale = -.3
        face = faces[5][3][0]   #   Idle, Puiple, Right
        ctx.move_to(face[0][0], face[1][0])
        ctx.line_to(face[0][1], face[1][1])
        ctx.line_to(face[0][2], face[1][2])
        ctx.line_to(face[0][3], face[1][3])
        ctx.line_to(face[0][4], face[1][4])
        ctx.line_to(face[0][5], face[1][5])
        ctx.line_to(face[0][6], face[1][6])
        ctx.line_to(face[0][7], face[1][7])
        ctx.line_to(face[0][8], face[1][8])
        face = faces[5][3][1]   #   Idle, Puiple, Left
        ctx.move_to(face[0][0], face[1][0])
        ctx.line_to(face[0][1], face[1][1])
        ctx.line_to(face[0][2], face[1][2])
        ctx.line_to(face[0][3], face[1][3])
        ctx.line_to(face[0][4], face[1][4])
        ctx.line_to(face[0][5], face[1][5])
        ctx.line_to(face[0][6], face[1][6])
        ctx.line_to(face[0][7], face[1][7])
        ctx.line_to(face[0][8], face[1][8])
        ctx.fill()

class XD():
    def mouth(ctx, mouth_x, mouth_y, eye_r_y, eye_l_y, surface, faces):  ## To-do: Move faces to xml file
        ctx.set_source_rgb(1, 1, 1)
        # Mouth coord driven face
        x_scale = .5
        y_scale = -.3
        #print(str(faces))
        face = faces[6][0][0]   #   Idle, Mouth, Right
        #                   |Feature|l/r
        #print(faces)
        ctx.move_to(face[0][0], face[1][0] - (mouth_y[3] * y_scale))
        ctx.line_to(face[0][1] - (mouth_x[3] * x_scale), face[1][1] - (mouth_y[3] * y_scale))
        ctx.line_to(face[0][2] - (mouth_x[2] * x_scale), face[1][2] - (mouth_y[2] * y_scale))
        ctx.line_to(face[0][3] - (mouth_x[1] * x_scale), face[1][3] - (mouth_y[1] * y_scale))
        ctx.line_to(face[0][4] - (mouth_x[0] * x_scale), face[1][4] - (mouth_y[0] * y_scale))
        ctx.line_to(face[0][5] - (mouth_x[0] * x_scale), face[1][5] - (mouth_y[0] * y_scale))
        ctx.line_to(face[0][6] - (mouth_x[0] * x_scale), face[1][6] - (mouth_y[0] * y_scale))
        ctx.line_to(face[0][7] - (mouth_x[11] * x_scale), face[1][7] - (mouth_y[11] * y_scale))
        ctx.line_to(face[0][8] - (mouth_x[10] * x_scale), face[1][8] - (mouth_y[10] * y_scale))
        ctx.line_to(face[0][9] - (mouth_x[9] * x_scale), face[1][9] - (mouth_y[9] * y_scale))
        ctx.line_to(face[0][10], face[1][10] - (mouth_y[9] * y_scale))

        face = faces[6][0][1]   #   Idle, Mouth, Left
        ctx.move_to(face[0][0], face[1][0] - (mouth_y[3] * y_scale))
        ctx.line_to(face[0][1] - (mouth_x[3] * x_scale), face[1][1] - (mouth_y[3] * y_scale))
        ctx.line_to(face[0][2] - (mouth_x[4] * x_scale), face[1][2] - (mouth_y[4] * y_scale))
        ctx.line_to(face[0][3] - (mouth_x[5] * x_scale), face[1][3] - (mouth_y[5] * y_scale))
        ctx.line_to(face[0][4] - (mouth_x[6] * x_scale), face[1][4] - (mouth_y[6] * y_scale))
        ctx.line_to(face[0][5] - (mouth_x[6] * x_scale), face[1][5] - (mouth_y[6] * y_scale))
        ctx.line_to(face[0][6] - (mouth_x[6] * x_scale), face[1][6] - (mouth_y[6] * y_scale))
        ctx.line_to(face[0][7] - (mouth_x[7] * x_scale), face[1][7] - (mouth_y[7] * y_scale))
        ctx.line_to(face[0][8] - (mouth_x[8] * x_scale), face[1][8] - (mouth_y[8] * y_scale))
        ctx.line_to(face[0][9] - (mouth_x[9] * x_scale), face[1][9] - (mouth_y[9] * y_scale))
        ctx.line_to(face[0][10], face[1][10] - (mouth_y[9] * y_scale))
        ctx.fill()

    def eye(ctx, eye_r_y, eye_l_y, faces):
        ctx.set_source_rgb(1, 1, 1)
        x_scale = .5
        y_scale = -.3
        face = faces[6][1][0]   #   Idle, Eye, Right
        ctx.move_to(face[0][0], face[1][0])
        ctx.line_to(face[0][1], face[1][1])
        ctx.line_to(face[0][2], face[1][2])
        ctx.line_to(face[0][3], face[1][3])
        ctx.line_to(face[0][4], face[1][4])
        ctx.line_to(face[0][5], face[1][5])
        ctx.line_to(face[0][6], face[1][6])
        ctx.line_to(face[0][7], face[1][7])
        ctx.line_to(face[0][8], face[1][8])
        ctx.line_to(face[0][9], face[1][9])
        ctx.line_to(face[0][10], face[1][10])
        face = faces[6][1][1]   #   Idle, Eye, Left
        ctx.move_to(face[0][0], face[1][0])
        ctx.line_to(face[0][1], face[1][1])
        ctx.line_to(face[0][2], face[1][2])
        ctx.line_to(face[0][3], face[1][3])
        ctx.line_to(face[0][4], face[1][4])
        ctx.line_to(face[0][5], face[1][5])
        ctx.line_to(face[0][6], face[1][6])
        ctx.line_to(face[0][7], face[1][7])
        ctx.line_to(face[0][8], face[1][8])
        ctx.line_to(face[0][9], face[1][9])
        ctx.line_to(face[0][10], face[1][10])
        ctx.fill()
    
    def nose(ctx, faces):
        ctx.set_source_rgb(1, 1, 1)
        face = faces[6][2][0]   #   Idle, Nose, Right
        ctx.move_to(face[0][0], face[1][0])
        ctx.line_to(face[0][1], face[1][1])
        ctx.line_to(face[0][2], face[1][2])
        ctx.line_to(face[0][3], face[1][3])
        ctx.line_to(face[0][4], face[1][4])
        face = faces[6][2][1]   #   Idle, Nose, Left
        ctx.move_to(face[0][0], face[1][0])
        ctx.line_to(face[0][1], face[1][1])
        ctx.line_to(face[0][2], face[1][2])
        ctx.line_to(face[0][3], face[1][3])
        ctx.line_to(face[0][4], face[1][4])
        ctx.fill()

    def puiple(ctx, eye_r_y, eye_l_y, faces):
        ctx.set_source_rgb(0, 0, 0)
        x_scale = .5
        y_scale = -.3
        face = faces[6][3][0]   #   Idle, Puiple, Right
        ctx.move_to(face[0][0], face[1][0])
        ctx.line_to(face[0][1], face[1][1])
        ctx.line_to(face[0][2], face[1][2])
        ctx.line_to(face[0][3], face[1][3])
        ctx.line_to(face[0][4], face[1][4])
        ctx.line_to(face[0][5], face[1][5])
        ctx.line_to(face[0][6], face[1][6])
        ctx.line_to(face[0][7], face[1][7])
        ctx.line_to(face[0][8], face[1][8])
        face = faces[6][3][1]   #   Idle, Puiple, Left
        ctx.move_to(face[0][0], face[1][0])
        ctx.line_to(face[0][1], face[1][1])
        ctx.line_to(face[0][2], face[1][2])
        ctx.line_to(face[0][3], face[1][3])
        ctx.line_to(face[0][4], face[1][4])
        ctx.line_to(face[0][5], face[1][5])
        ctx.line_to(face[0][6], face[1][6])
        ctx.line_to(face[0][7], face[1][7])
        ctx.line_to(face[0][8], face[1][8])
        ctx.fill()
def main(ctx, mouth_x, mouth_y, eye_r_y, eye_l_y, surface, button):
    faces = load_faces()
    try:
        if any("face_1" in s for s in button) or len(button) == 0:
            Idle.mouth(ctx, mouth_x, mouth_y, eye_r_y, eye_l_y, surface, faces)
            Idle.eye(ctx, eye_r_y, eye_l_y, faces)
            Idle.nose(ctx, faces)
            Idle.puiple(ctx, eye_r_y, eye_l_y, faces)

        if any("face_2" in s for s in button):
            Tired.mouth(ctx, mouth_x, mouth_y, eye_r_y, eye_l_y, surface, faces)
            Tired.eye(ctx, eye_r_y, eye_l_y, faces)
            Tired.nose(ctx, faces)
            Tired.puiple(ctx, eye_r_y, eye_l_y, faces)

        if any("face_3" in s for s in button):
            Annoyed.mouth(ctx, mouth_x, mouth_y, eye_r_y, eye_l_y, surface, faces)
            Annoyed.eye(ctx, eye_r_y, eye_l_y, faces)
            Annoyed.nose(ctx, faces)
            Annoyed.puiple(ctx, eye_r_y, eye_l_y, faces)
        
        if any("face_4" in s for s in button):
            Sad.mouth(ctx, mouth_x, mouth_y, eye_r_y, eye_l_y, surface, faces)
            Sad.eye(ctx, eye_r_y, eye_l_y, faces)
            Sad.nose(ctx, faces)
            Sad.puiple(ctx, eye_r_y, eye_l_y, faces)

        if any("face_5" in s for s in button):
            OWO.mouth(ctx, mouth_x, mouth_y, eye_r_y, eye_l_y, surface, faces)
            OWO.eye(ctx, eye_r_y, eye_l_y, faces)
            OWO.nose(ctx, faces)
            OWO.puiple(ctx, eye_r_y, eye_l_y, faces)

        if any("face_6" in s for s in button):
            Rock.mouth(ctx, mouth_x, mouth_y, eye_r_y, eye_l_y, surface, faces)
            Rock.eye(ctx, eye_r_y, eye_l_y, faces)
            Rock.nose(ctx, faces)
            Rock.puiple(ctx, eye_r_y, eye_l_y, faces)

        if any('face_7' in s for s in button):
            XD.mouth(ctx, mouth_x, mouth_y, eye_r_y, eye_l_y, surface, faces)
            XD.eye(ctx, eye_r_y, eye_l_y, faces)
            XD.nose(ctx, faces)
            XD.puiple(ctx, eye_r_y, eye_l_y, faces)
    except:
        print(f"face_dlib.py: List out of range")
        mouth_x = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        mouth_y = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        if any("face_1" in s for s in button) or len(button) == 0:
            Idle.mouth(ctx, mouth_x, mouth_y, eye_r_y, eye_l_y, surface, faces)
            Idle.eye(ctx, eye_r_y, eye_l_y, faces)
            Idle.nose(ctx, faces)
            Idle.puiple(ctx, eye_r_y, eye_l_y, faces)

        if any("face_2" in s for s in button):
            Tired.mouth(ctx, mouth_x, mouth_y, eye_r_y, eye_l_y, surface, faces)
            Tired.eye(ctx, eye_r_y, eye_l_y, faces)
            Tired.nose(ctx, faces)
            Tired.puiple(ctx, eye_r_y, eye_l_y, faces)

        if any("face_3" in s for s in button):
            Annoyed.mouth(ctx, mouth_x, mouth_y, eye_r_y, eye_l_y, surface, faces)
            Annoyed.eye(ctx, eye_r_y, eye_l_y, faces)
            Annoyed.nose(ctx, faces)
            Annoyed.puiple(ctx, eye_r_y, eye_l_y, faces)

        if any("face_4" in s for s in button):
            Sad.mouth(ctx, mouth_x, mouth_y, eye_r_y, eye_l_y, surface, faces)
            Sad.eye(ctx, eye_r_y, eye_l_y, faces)
            Sad.nose(ctx, faces)
            Sad.puiple(ctx, eye_r_y, eye_l_y, faces)

        if any("face_5" in s for s in button):
            OWO.mouth(ctx, mouth_x, mouth_y, eye_r_y, eye_l_y, surface, faces)
            OWO.eye(ctx, eye_r_y, eye_l_y, faces)
            OWO.nose(ctx, faces)
            OWO.puiple(ctx, eye_r_y, eye_l_y, faces)

        if any("face_6" in s for s in button):
            Rock.mouth(ctx, mouth_x, mouth_y, eye_r_y, eye_l_y, surface, faces)
            Rock.eye(ctx, eye_r_y, eye_l_y, faces)
            Rock.nose(ctx, faces)
            Rock.puiple(ctx, eye_r_y, eye_l_y, faces)
        
        if any('face_7' in s for s in button):
            XD.mouth(ctx, mouth_x, mouth_y, eye_r_y, eye_l_y, surface, faces)
            XD.eye(ctx, eye_r_y, eye_l_y, faces)
            XD.nose(ctx, faces)
            XD.puiple(ctx, eye_r_y, eye_l_y, faces)

    #print(mouth_y)
    
    buf = surface.get_data()
    #end = timer()
    #print('render_time: ' + str(end - start))
    return buf
    
    #Blank.draw(ctx)
