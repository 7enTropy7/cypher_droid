from pygame import *
import RPi.GPIO as GPIO
from time import sleep as Sleep

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

# Servo Control Pins
horizontal = 3
vertical = 5

GPIO.setup(horizontal, GPIO.OUT)
pwm_h=GPIO.PWM(horizontal, 50)
GPIO.setup(vertical, GPIO.OUT)
pwm_v=GPIO.PWM(vertical, 50)
pwm_h.start(0)
pwm_v.start(0)


def translate(value, leftMin, leftMax, rightMin, rightMax):
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin
    valueScaled = float(value - leftMin) / float(leftSpan)
    return rightMin + (valueScaled * rightSpan)


def SetAngle(angle,target_pin):
    if target_pin == 3:
        duty = angle / 18 + 2
        GPIO.output(target_pin, True)
        pwm_h.ChangeDutyCycle(duty)
        Sleep(0.2)
        GPIO.output(target_pin, False)
        pwm_h.ChangeDutyCycle(0)
    elif target_pin == 5:
        duty = angle / 18 + 2
        GPIO.output(target_pin, True)
        pwm_v.ChangeDutyCycle(duty)
        Sleep(0.2)
        GPIO.output(target_pin, False)
        pwm_v.ChangeDutyCycle(0)


SetAngle(10,horizontal)
SetAngle(10,vertical)