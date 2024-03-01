import mediapipe as mp 
from mediapipe.tasks import python as mp_python 
MP_TASK_FILE = "face_landmarker_with_blendshapes.task" 
class FaceMeshDetector: 
  def __init__(self): 
    with open(MP_TASK_FILE, mode="rb") as f: 
      f_buffer = f.read() 
      base_options = mp_python.BaseOptions(model_asset_buffer=f_buffer) 
      options = mp_python.vision.FaceLandmarkerOptions( base_options=base_options, output_face_blendshapes=True, output_facial_transformation_matrixes=True, running_mode=mp.tasks.vision.RunningMode.LIVE_STREAM, num_faces=1, result_callback=self.mp_callback) 
      self.model = mp_python.vision.FaceLandmarker.create_from_options( options) 
      self.landmarks = None 
      self.blendshapes = None 
      self.latest_time_ms = 0 
      def mp_callback(self, mp_result, output_image, timestamp_ms: int): 
        if len(mp_result.face_landmarks) >= 1 and len( mp_result.face_blendshapes) >= 1: 
          self.landmarks = mp_result.face_landmarks[0] 
          self.blendshapes = [b.score for b in mp_result.face_blendshapes[0]] 
  def update(self, frame): 
    t_ms = int(time.time() * 1000) 
    if t_ms <= self.latest_time_ms: 
      return 
    frame_mp = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame) 
    self.model.detect_async(frame_mp, t_ms) 
    self.latest_time_ms = t_ms 
  def get_results(self): 
    return self.landmarks, self.blendshapes