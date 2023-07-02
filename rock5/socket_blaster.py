
# This is server code to send video frames over UDP
import cv2, imutils, socket
import numpy as np
import time
import base64

while True:
	try:
		BUFF_SIZE = 13000
		server_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
		server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,BUFF_SIZE)
		host_ip = '192.168.1.167'#  socket.gethostbyname(host_name)
		print(host_ip)
		port = 7171
		socket_address = (host_ip,port)
		server_socket.bind(socket_address)
		print('Listening at:',socket_address)

		vid = cv2.VideoCapture("http://192.168.1.236:8080/stream") #  replace 'rocket.mp4' with 0 for webcam
		fps,st,frames_to_count,cnt = (0,0,20,0)

		while True:
			while(vid.isOpened()):
				_,frame = vid.read()
				frame = cv2.resize(frame,(128, 32))
				frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
				encoded,buffer = cv2.imencode('.jpg',frame,[cv2.IMWRITE_JPEG_QUALITY,80])
				message = base64.b64encode(buffer)
				server_socket.sendto(message,('192.168.1.236', port))
				#frame = cv2.putText(frame,'FPS: '+str(fps),(10,40),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)
				cv2.imshow('TRANSMITTING VIDEO',frame)
				key = cv2.waitKey(1) & 0xFF
				if key == ord('q'):
					server_socket.close()
					break
				if cnt == frames_to_count:
					try:
						fps = round(frames_to_count/(time.time()-st))
						st=time.time()
						cnt=0
					except:
						pass
				cnt+=1
	except: time.sleep(5)

