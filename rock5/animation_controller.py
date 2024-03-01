import numpy as np
class Animation:
    def __init__(self, play=True):
        """Initialize the animation clips."""
        # The parameters.
        self.play = play
        self.cf: int = 0        # Current Frame
        #self.blink_shape: float = 0   # Animated Value
        # Previous values.
        print("Animation controller initalized.")
    def tick(self):
        if not self.cf == 1000:
            self.cf += 1
        else:
            self.cf = 0


    def blink(self):
        if self.play:
            """Compute the current frame."""
            current_frame = self.cf - (500)
            shape = np.clip((50/((10*current_frame**2) + 5)), 0, 1)
            return float(shape)
        else:
            return float(np.random.uniform(0,1))


