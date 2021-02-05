from pygame import display, joystick, event
from pygame import QUIT, JOYAXISMOTION, JOYBALLMOTION, JOYHATMOTION, JOYBUTTONUP, JOYBUTTONDOWN
import RPi.GPIO as GPIO

GPIO.setwarnings(False)

GPIO.setmode(GPIO.BOARD)
GPIO.setup(37,GPIO.OUT)
GPIO.setup(35,GPIO.OUT)
GPIO.setup(33,GPIO.OUT)
GPIO.setup(31,GPIO.OUT)

GPIO.setup(3, GPIO.OUT)
pwm=GPIO.PWM(3, 50)
pwm.start(0)


h = {(0,0):  'c',(1,0):  'E', (1,1):   'NE', (0,1):  'N', (-1,1): 'NW',(-1,0): 'W', (-1,-1): 'SW', (0,-1): 'S', (1,-1): 'SE'}

P = 2 # precision


display.init()
joystick.init()

for i in range(joystick.get_count()):
	joystick.Joystick(i).init()

e = event.wait()
while e.type != QUIT:
	if e.type == JOYAXISMOTION:
		if e.value < 0.5 and e.value > -0.5:
			GPIO.output(37,GPIO.LOW)
			GPIO.output(35,GPIO.LOW)
			GPIO.output(33,GPIO.LOW)
			GPIO.output(31,GPIO.LOW)
			print('##### Stop #####')
		elif e.axis == 0 and e.value >= 0.5:
			GPIO.output(37,GPIO.LOW)
			GPIO.output(35,GPIO.HIGH)
			GPIO.output(33,GPIO.HIGH)
			GPIO.output(31,GPIO.LOW)
			print('Right')
		elif e.axis == 0 and e.value <= -0.5:
			GPIO.output(37,GPIO.HIGH)
			GPIO.output(35,GPIO.LOW)
			GPIO.output(33,GPIO.LOW)
			GPIO.output(31,GPIO.HIGH)
			print('Left')
		elif e.axis == 1 and e.value >= 0.5:
			GPIO.output(37,GPIO.LOW)
			GPIO.output(35,GPIO.HIGH)
			GPIO.output(33,GPIO.LOW)
			GPIO.output(31,GPIO.HIGH)
			print('Down')
		elif e.axis == 1 and e.value <= -0.5:
			GPIO.output(37,GPIO.HIGH)
			GPIO.output(35,GPIO.LOW)
			GPIO.output(33,GPIO.HIGH)
			GPIO.output(31,GPIO.LOW)
			print('Up')
	
	e = event.wait()

pwm.stop()
GPIO.cleanup()