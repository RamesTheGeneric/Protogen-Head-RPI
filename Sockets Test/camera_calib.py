from chessboard import calibrate_chessboard
from utils import load_coefficients, save_coefficients

# Parameters
IMAGES_DIR = 'Sockets Test'
IMAGES_FORMAT = '.jpg'
SQUARE_SIZE = 1.6
WIDTH = 6
HEIGHT = 9

# Calibrate 
ret, mtx, dist, rvecs, tvecs = calibrate_chessboard(
    IMAGES_DIR, 
    IMAGES_FORMAT, 
    SQUARE_SIZE, 
    WIDTH, 
    HEIGHT
)
# Save coefficients into a file
save_coefficients(mtx, dist, "calibration_chessboard.yml")