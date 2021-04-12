import socket, ctypes
import time
import RPi.GPIO as GPIO
from time import sleep as Sleep
from threading import Thread
import multiprocessing

def SetAngle(orientation):
	
	GPIO.setmode(GPIO.BOARD)
	GPIO.setwarnings(False)

	GPIO.setup(5, GPIO.OUT)
	pwm_v=GPIO.PWM(5, 50)
	pwm_v.start(0)

	GPIO.setup(3, GPIO.OUT)
	pwm_h=GPIO.PWM(3, 50)
	pwm_h.start(0)
	
	while True:
		print(((int(orientation[0]))), ((int(orientation[1]))))
		
		if orientation[1]>180.0 or orientation[1]<1.0:
			continue
				
		duty = (int(orientation[1])) / 18 + 2
		GPIO.output(5, True)
		pwm_v.ChangeDutyCycle(duty)
		Sleep(0.1)
		GPIO.output(5, False)
		pwm_v.ChangeDutyCycle(0)		
		
		if orientation[0]>180.0 or orientation[1]<1.0:
			continue
	
		duty = (int(orientation[0])) / 18 + 2
		GPIO.output(3, True)
		pwm_h.ChangeDutyCycle(duty)
		Sleep(0.1)
		GPIO.output(3, False)
		pwm_h.ChangeDutyCycle(0)
		
		
		

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
	
	
	orientation = multiprocessing.Array(ctypes.c_float, [90.00,90.00])
	recvda = multiprocessing.Value(ctypes.c_wchar_p, "")
	lock = multiprocessing.Lock()
	
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind(('192.168.1.30', 5000))
	s.listen(5)

	#thread = Thread(target = SetAngle)
	#thread.start()
	p1 = multiprocessing.Process(target = SetAngle, args = (orientation, ))
	p2 = multiprocessing.Process(target = host, args = (recvda, orientation, ))
	p1.start()
	p2.start()
	
	#thread.join()
	p1.join()
	p2.join()
	GPIO.cleanup

''' (In potrait mode)
first value: move to face mobile upward: +ve values, downwards: -ve values  (left, right for landscape)
second value: move to face mobile towards left: +ve values, rightwards: -ve values (down, up for landscape)
third values: rotate mobile anticlockwise: +ve, clockwise: -ve values
'''
