import cv2
import http.server
import socketserver
import threading
import time

class MJPEGStreamHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/stream.mjpeg':
            self.send_response(200)
            self.send_header('Content-type', 'multipart/x-mixed-replace; boundary=frame')
            self.end_headers()

            # Continuously send MJPEG frames
            while True:
                ret, frame = video_capture.read()
                #frame = frame[int(center[1] - 200):int(center[1] + 200), int(center[0] - 200):int(center[0] + 200)] 
                frame = cv2.resize(frame, (256, 256))
                frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
                cv2.imshow('frame', frame)
                if cv2.waitKey(25) & 0xFF == ord('q'):
                    break

                # Encode the frame to JPEG
                _, jpeg_frame = cv2.imencode('.jpg', frame)

                # Send the frame as MJPEG
                self.send_frame(jpeg_frame.tobytes())

                # Delay between frames (adjust as needed)
                # This ensures a smoother stream with reduced bandwidth
                self.wfile.write(b'\r\n')
                self.wfile.flush()
                #time.sleep(0.01)

        elif self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'<html><body><img src="/stream.mjpeg"></body></html>')

    def send_frame(self, frame_data):
        try:
            self.wfile.write(b'--frame\r\n')
            self.send_header('Content-type', 'image/jpeg')
            self.send_header('Content-length', len(frame_data))
            self.end_headers()
            self.wfile.write(frame_data)
        except: pass

def serve_stream():
    with socketserver.TCPServer(('', 8000), MJPEGStreamHandler) as httpd:
        print('Streaming server started at http://localhost:8000')
        httpd.serve_forever()

if __name__ == '__main__':
    video_capture = cv2.VideoCapture("http://192.168.1.149/")

    # Start the stream server in a separate thread
    stream_thread = threading.Thread(target=serve_stream)
    stream_thread.start()

    # Wait for user interruption
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass

    video_capture.release()
    cv2.destroyAllWindows()
