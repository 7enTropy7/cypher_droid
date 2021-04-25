import socket, ctypes
import time
from time import sleep as Sleep
import multiprocessing
import cv2
from piservo import Servo

def videostream():
	while True:
		ret, fr = cap.read()
		frame = cv2.flip(fr,0)
		cv2.imshow('frame',frame)
		if cv2.waitKey(1) & 0xff == 27:
			break
	cv2.destroyAllWindows()
	

def SetAngle(orientation):
	horizontal_servo = Servo(13)
	vertical_servo = Servo(12)
	while True:
		print(((int(orientation[0]))), ((int(orientation[1]))))
		
		if orientation[1]-50>170.0 or orientation[1]-50<1.0:
			continue

		vertical_servo.write(orientation[1]-50)
		Sleep(0.2)
		
		if orientation[0]>180.0 or orientation[1]<1.0:
			continue

		horizontal_servo.write(orientation[0])
		Sleep(0.2)
		

def host(recvda, orientation):
	recvdata = recvda.value
	try:
		while True:
			clientsocket, address = s.accept()
			print(f"Connection from {address} has been established!")
			clientsocket.send(bytes("Welcome, User","utf-8"))
			data = clientsocket.recv(8)
			while data:
				stri = data.decode("utf-8")
				recvdata += stri
				if stri[-1] == ';':
					#print(recvdata)
					index = recvdata.find(';')		
					a,b = [float(i) for i in (recvdata[:index].split(','))]
					a_degrees = (a*0.1)*(180/3.1415)
					b_degrees = (b*0.1)*(180/3.1415)
					orientation[0] = round(orientation[0]+a_degrees,2)
					orientation[1] = round(orientation[1]+b_degrees,2)
					
					#print(orientation)
									
					recvdata = ''
				data = clientsocket.recv(8)
				
	except KeyboardInterrupt:
		s.close()
		
if __name__ == "__main__":
	
	cap = cv2.VideoCapture(0)
	
	orientation = multiprocessing.Array(ctypes.c_float, [90.00,90.00])
	recvda = multiprocessing.Value(ctypes.c_wchar_p, "")
	lock = multiprocessing.Lock()
	
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind(('192.168.1.30', 5000))
	s.listen(5)

	p1 = multiprocessing.Process(target = SetAngle, args = (orientation, ))
	p2 = multiprocessing.Process(target = host, args = (recvda, orientation, ))
	p3 = multiprocessing.Process(target = videostream)
	p1.start()
	p2.start()
	p3.start()

	p1.join()
	p2.join()
	p3.join()
	GPIO.cleanup
	
	cap.release()

''' (In potrait mode)
first value: move to face mobile upward: +ve values, downwards: -ve values  (left, right for landscape)
second value: move to face mobile towards left: +ve values, rightwards: -ve values (down, up for landscape)
third values: rotate mobile anticlockwise: +ve, clockwise: -ve values
'''
