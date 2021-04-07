import socket
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('192.168.1.30', 5000))
s.listen(5)

recvdata = ''
orientation = [90.00,90.00] #degrees
start = time.time()

try:
	while True:
		clientsocket, address = s.accept()
		print(f"Connection from {address} has been established!")
		clientsocket.send(bytes("Welcome, User","utf-8"))
		data = clientsocket.recv(1024)
		while data:
			stri = data.decode("utf-8")
			recvdata += stri
			if stri[-1] == ';':
				#print(recvdata)			
				a,b = [float(i) for i in (recvdata[:-1].split(','))]
				a_degrees = (a*0.1)*(180/3.1415)
				b_degrees = (b*0.1)*(180/3.1415)
				tempa = round(orientation[0]+a_degrees,2)
				tempb = round(orientation[1]+b_degrees,2)
				if tempa<=180 and tempa>=0: orientation[0] = tempa
				if tempb<=180 and tempb>=0: orientation[1] = tempb 
				print(orientation)
				
				recvdata = ''
			data = clientsocket.recv(1024)
			
except KeyboardInterrupt:
	s.close()
	
	
''' (In potrait mode)
first value: move to face mobile upward: +ve values, downwards: -ve values  (left, right for landscape)
second value: move to face mobile towards left: +ve values, rightwards: -ve values (down, up for landscape)
third values: rotate mobile anticlockwise: +ve, clockwise: -ve values
'''
