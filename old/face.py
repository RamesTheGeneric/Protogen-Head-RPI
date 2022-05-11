#Contains Graphics for to draw faces (Idle, Excited, Sad, OWO, Blush, Cry, Etc...) 
#          -----Idle-----

#          -----Mouth-----
class Idle():
    def mouth(ctx, mouth_x, mouth_y, eye_r_y, eye_l_y, surface, x_scale, y_scale):
        ctx.set_source_rgb(1, 1, 1)
        # Mouth coord driven face
        ctx.move_to(64, 23 - (mouth_y[5] * y_scale))
        ctx.line_to(52 - (mouth_x[4] * x_scale), 26 - (mouth_y[4] * y_scale))
        ctx.line_to(49 - (mouth_x[3] * x_scale), 22 - (mouth_y[3] * y_scale))
        ctx.line_to(42 - (mouth_x[2] * x_scale), 24 - (mouth_y[2] * y_scale))
        ctx.line_to(24 - (mouth_x[0] * x_scale), 17 - (mouth_y[0] * y_scale))
        ctx.line_to(24 - (mouth_x[0] * x_scale), 18 - (mouth_y[0] * y_scale))
        ctx.line_to(26 - (mouth_x[0] * x_scale), 19 - (mouth_y[0] * y_scale))
        ctx.line_to(42 - (mouth_x[18] * x_scale), 25 - (mouth_y[18] * y_scale))
        ctx.line_to(48 - (mouth_x[17] * x_scale), 23 - (mouth_y[17] * y_scale))
        ctx.line_to(51 - (mouth_x[16] * x_scale), 27 - (mouth_y[16] * y_scale))
        ctx.line_to(64, 24 - (mouth_y[15] * y_scale))
        # making close path
        ctx.fill()

    def eye(ctx, eye_r_y, eye_l_y, x_scale, y_scale):
        ctx.move_to(19.4, 3.5 - (eye_r_y[0] * y_scale))
        ctx.line_to(23.9, 1.8 - (eye_r_y[1] * y_scale))
        ctx.line_to(29.5, 2 - (eye_r_y[2] * y_scale))
        ctx.line_to(32.8, 3.6 - (eye_r_y[3] * y_scale))
        ctx.line_to(34, 7.3 - (eye_r_y[4] * y_scale))
        ctx.line_to(34.2, 9.6)
        ctx.line_to(31.4, 9.3)
        ctx.line_to(24, 9)
        ctx.line_to(18.6, 8.6)
        ctx.line_to(16.9, 8.2)
        ctx.line_to(18.1, 7.8)
        ctx.fill()
    
    #def pupil():



def main(ctx, mouth_x, mouth_y, eye_r_y, eye_l_y, surface, x_scale, y_scale, button):
    Idle.mouth(ctx, mouth_x, mouth_y, eye_r_y, eye_l_y, surface, x_scale, y_scale)
    Idle.eye(ctx, eye_r_y, eye_l_y, x_scale, y_scale)
    
    buf = surface.get_data()
    return buf