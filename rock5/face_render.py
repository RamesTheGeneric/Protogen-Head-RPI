from obj_parser import load_obj
import cv2
import numpy as np
from one_euro_filter import OneEuroFilter

class Render():
    def __init__(self):
        path = "faces/rames/"
        self.HEIGHT = 32
        self.WIDTH = 128
        self.MULTI = 10  # polyFill requires int32 so we multiply our floats to be rendered with ints
        self.shape_index = ('Basis', 'jawOpen', 'jawLeft', 'jawRight', 'mouthFunnel', 'mouthPucker', 'mouthLeft', 'mouthRight', 'mouthShrugUpper', 'mouthShrugLower', 'mouthSmileLeft', 'mouthSmileRight', 
        'mouthFrownLeft', 'mouthFrownRight', 'mouthDimpleLeft', 'mouthDimpleRight', 'mouthUpperUpLeft', 'mouthUpperUpRight', 'mouthLowerDownLeft', 'mouthLowerDownRight', 'mouthStretchLeft', 'mouthStretchRight', 'tongueOut',
        'slideLeft', 'slideRight', 'slideUp', 'slideDown', 'rollUp', 'rollDown', 'rollLeft', 'rollRight',
        'eyes_Angry', 'eyes_Suprised', 'eyes_X', 'mouth_Fangs')
        self.shapes = dict(     # 29 tracked shapes 33 total
            Basis = load_obj(path + self.shape_index[0] + '.obj'),
            jawOpen = load_obj(path + self.shape_index[1] + '.obj'),
            jawLeft = load_obj(path + self.shape_index[2] + '.obj'),
            jawRight = load_obj(path + self.shape_index[3] + '.obj'),
            mouthFunnel = load_obj(path + self.shape_index[4] + '.obj'),
            mouthPucker = load_obj(path + self.shape_index[5] + '.obj'),
            mouthLeft = load_obj(path + self.shape_index[6] + '.obj'),
            mouthRight = load_obj(path + self.shape_index[7] + '.obj'),
            mouthShrugUpper = load_obj(path + self.shape_index[8] + '.obj'),
            mouthShrugLower = load_obj(path + self.shape_index[9] + '.obj'),
            mouthSmileLeft = load_obj(path + self.shape_index[10] + '.obj'),
            mouthSmileRight = load_obj(path + self.shape_index[11] + '.obj'),
            mouthFrownLeft = load_obj(path + self.shape_index[12] + '.obj'),
            mouthFrownRight = load_obj(path + self.shape_index[13] + '.obj'),
            mouthDimpleLeft = load_obj(path + self.shape_index[14] + '.obj'),
            mouthDimpleRight = load_obj(path + self.shape_index[15] + '.obj'),
            mouthUpperUpLeft = load_obj(path + self.shape_index[16] + '.obj'),
            mouthUpperUpRight = load_obj(path + self.shape_index[17] + '.obj'),
            mouthLowerDownLeft = load_obj(path + self.shape_index[18] + '.obj'),
            mouthLowerDownRight = load_obj(path + self.shape_index[19] + '.obj'),
            mouthStretchLeft = load_obj(path + self.shape_index[20] + '.obj'),
            mouthStretchRight = load_obj(path + self.shape_index[21] + '.obj'),
            tongueOut = load_obj(path + self.shape_index[22] + '.obj'),
            #   End Babble shapes. Start Tracking shapes
            slideLeft = load_obj(path + self.shape_index[23] + '.obj'),
            slideRight = load_obj(path + self.shape_index[24] + '.obj'),
            slideUp = load_obj(path + self.shape_index[25] + '.obj'),
            slideDown = load_obj(path + self.shape_index[26] + '.obj'),
            rollUp = load_obj(path + self.shape_index[27] + '.obj'),
            rollDown = load_obj(path + self.shape_index[28] + '.obj'),
            rollLeft = load_obj(path + self.shape_index[29] + '.obj'),
            rollRight = load_obj(path + self.shape_index[30] + '.obj'),
            #   End tracking shapes. Start emote shapes
            eyes_Angry = load_obj(path + self.shape_index[31] + '.obj'),
            eyes_Suprised = load_obj(path + self.shape_index[32] + '.obj'),
            eyes_X = load_obj(path + self.shape_index[33] + '.obj'),
            mouth_Fangs = load_obj(path + self.shape_index[34] + '.obj'),
        )
        self.shape_transforms = self.calculate_shape_transforms()
        # OneEuroFilter
        min_cutoff = 0.0004 #you need to adjust
        beta = 0.9 #you need to adjust
        noisy_point = np.array([33])
        self.filter = OneEuroFilter(
            noisy_point,
            min_cutoff=min_cutoff,
            beta=beta
        )

    def remap_shapes(self, w, t, e):
        #input 45 babble shapes
        shapes = [
            0,  # Basis
            w[4],
            w[6],
            w[7],
            w[10],
            w[11],
            w[12],
            w[13],
            w[16],
            w[17],
            w[19],
            w[20],
            w[21],
            w[22],
            w[23],
            w[24],
            w[25],
            w[26],
            w[27],
            w[28],
            w[31],
            w[32],
            w[33],

            np.clip(t["/gyro_z"] * .001, 0, 1),
            (np.clip(t["/gyro_z"] * .001, -1, 0) * -1),
            np.clip(t["/gyro_y"] * .001, 0, 1),
            (np.clip(t["/gyro_y"] * .001, -1, 0) * -1),
            np.clip(t["/gyro_y"] * .0025, 0, 1),
            (np.clip(t["/gyro_y"] * .0025, -1, 0) * -1),
            np.clip(t["/gyro_x"] * .0025, 0, 1),
            (np.clip(t["/gyro_x"] * .0025, -1, 0) * -1),
            e[0],
            e[1],
            e[2],
            e[3],
        ]
        output = self.filter(np.array(shapes))
        return output

    
    def process_mesh(self, weights): 
        out_array = []
        for i in range(len(self.shapes['Basis'][0])):       # Remove Y Vertecies
            out_array.append([(float(self.shapes['Basis'][0][i][0]) + (self.WIDTH / 2)) * self.MULTI, (float(self.shapes['Basis'][0][i][2]) + (self.HEIGHT / 2)) * self.MULTI])    # Vertex will always have 3 axis coords
        
        for out_item_idx, out_item in enumerate(out_array):
            for out_axis_idx, out_axis in enumerate(out_item):
                for tf_idx, tf in enumerate(self.shape_transforms):
                    out_array[out_item_idx][out_axis_idx] += (tf[out_item_idx][out_axis_idx] * weights[tf_idx])
        out_face = []
        for i in range(len(self.shapes['Basis'][3])):   
            face = [] 
            for f in self.shapes['Basis'][3][i]:    # Loop becuse face could be a tri or quad
                face.append(f[0])
            out_face.append(face)
        output = []
        for i in range(len(out_face)):  # Make face arrays using fixed vertices and face indecies as index
            face = []
            for v in out_face[i]:
                face.append(out_array[v])
            output.append(face)
        return output
    

    def calculate_shape_transforms(self): # Get the difference between the vertices in the shapes reletive to Basis
        vertex = []
        for shape in self.shape_index:
            out_array = []
            for i in range(len(self.shapes[shape][0])):       # Remove Y Vertecies
                out_array.append([(float(self.shapes[shape][0][i][0]) + (self.WIDTH / 2)) * self.MULTI, (float(self.shapes[shape][0][i][2]) + (self.HEIGHT / 2)) * self.MULTI])    # Vertex will always have 3 axis coords
            vertex.append(out_array)
        vertex_offsets = []
        for idx in range(len(vertex)):  
            shape = []
            for coord_idx, coord in enumerate(vertex[0]):
                coordinate = []
                for axis_idx, axis in enumerate(coord):
                    axis_offset = vertex[idx][coord_idx][axis_idx] - axis
                    coordinate.append(axis_offset)
                shape.append(coordinate)
            vertex_offsets.append(shape)
        return vertex_offsets
        
    def draw_face(self, array):
        image = np.zeros((self.HEIGHT * self.MULTI, self.WIDTH * self.MULTI))
        for face in array:
            contours = np.array(face, np.int32)
            image = cv2.fillPoly(image, pts = [contours], color =(255,255,255))
        image = cv2.resize(image, (self.WIDTH, self.HEIGHT), interpolation = cv2.INTER_AREA)
        return image.astype('float32')
