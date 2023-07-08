import requests
import numpy as np
import cv2

def capture_mjpeg_stream(url):
    stream = requests.get(url, stream=True)
    chunk_size = 8192
    frame_buffer = b''
    frame_start = -1
    frame_end = -1

    for chunk in stream.iter_content(chunk_size=chunk_size):
        frame_buffer += chunk
        while True:
            frame_start = frame_buffer.find(b'\xff\xd8')
            frame_end = frame_buffer.find(b'\xff\xd9', frame_start)
            if frame_start != -1 and frame_end != -1:
                jpg_data = frame_buffer[frame_start:frame_end+2]
                frame_buffer = frame_buffer[frame_end+2:]

                try:
                    # Convert the JPEG data to an OpenCV image
                    img = cv2.imdecode(np.frombuffer(jpg_data, dtype=np.uint8), cv2.IMREAD_COLOR)

                    # Do something with the image (e.g., display or process it)
                    cv2.imshow('Stream', img)
                    cv2.waitKey(1)  # Adjust the waitKey delay if needed

                    # Return the image if desired
                    # return img

                except cv2.error as e:
                    print(f"Error decoding image: {e}")
            else:
                break

# Example usage
stream_url = 'http://192.168.1.149/'
while True:
    capture_mjpeg_stream(stream_url)
