'''
Motor                        Motor 
  L                            R

  forward                   forward
  33->HIGH                        37->HIGH
  31->LOW                       35->LOW

  backward                  backward
  33->LOW                        37->LOW
  31->HIGH                       35->HIGH
'''

import pygame
import RPi.GPIO as GPIO
import time

def translate(value, leftMin, leftMax, rightMin, rightMax):
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin
    valueScaled = float(value - leftMin) / float(leftSpan)
    return rightMin + (valueScaled * rightSpan)

def SetAngle(angle):
	duty = angle / 18 + 2
	GPIO.output(3, True)
	pwm.ChangeDutyCycle(duty)
	time.sleep(1)
	GPIO.output(3, False)
	pwm.ChangeDutyCycle(0)

GPIO.setwarnings(False)

GPIO.setmode(GPIO.BOARD)
GPIO.setup(37,GPIO.OUT)
GPIO.setup(35,GPIO.OUT)
GPIO.setup(33,GPIO.OUT)
GPIO.setup(31,GPIO.OUT)

GPIO.setup(3, GPIO.OUT)
pwm=GPIO.PWM(3, 50)
pwm.start(0)

pygame.display.init()
clock = pygame.time.Clock()
pygame.joystick.init()
pygame.joystick.Joystick(0).init()

while True:
    pygame.event.pump()
    if pygame.joystick.Joystick(0).get_axis(0)<-0.2:
        GPIO.output(37,GPIO.HIGH)
        GPIO.output(35,GPIO.LOW)
        GPIO.output(33,GPIO.LOW)
        GPIO.output(31,GPIO.HIGH)
        print('Left')
    elif pygame.joystick.Joystick(0).get_axis(0)>0.2:
        GPIO.output(37,GPIO.LOW)
        GPIO.output(35,GPIO.HIGH)
        GPIO.output(33,GPIO.HIGH)
        GPIO.output(31,GPIO.LOW)
        print('Right')
    elif pygame.joystick.Joystick(0).get_axis(1)<-0.2:
        GPIO.output(37,GPIO.HIGH)
        GPIO.output(35,GPIO.LOW)
        GPIO.output(33,GPIO.HIGH)
        GPIO.output(31,GPIO.LOW)
        print('Up')
    elif pygame.joystick.Joystick(0).get_axis(1)>0.2:
        GPIO.output(37,GPIO.LOW)
        GPIO.output(35,GPIO.HIGH)
        GPIO.output(33,GPIO.LOW)
        GPIO.output(31,GPIO.HIGH)
        print('Down')
    else:
        GPIO.output(37,GPIO.LOW)
        GPIO.output(35,GPIO.LOW)
        GPIO.output(33,GPIO.LOW)
        GPIO.output(31,GPIO.LOW)
        print('Stop')
    
    SetAngle(translate(pygame.joystick.Joystick(0).get_axis(3),-1,1,0,180))

    clock.tick(5)

pwm.stop()
GPIO.cleanup()