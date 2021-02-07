from pygame import *
import RPi.GPIO as GPIO
from time import sleep as Sleep

GPIO.setwarnings(False)

# Wheel Control
GPIO.setmode(GPIO.BOARD)
GPIO.setup(37,GPIO.OUT)
GPIO.setup(35,GPIO.OUT)
GPIO.setup(33,GPIO.OUT)
GPIO.setup(31,GPIO.OUT)

# Servo Control
horizontal = 3
vertical = 5

GPIO.setup(horizontal, GPIO.OUT)
pwm_h=GPIO.PWM(horizontal, 50)
GPIO.setup(vertical, GPIO.OUT)
pwm_v=GPIO.PWM(vertical, 50)
pwm_h.start(0)
pwm_v.start(0)


init()

#Setup and init joystick
j=joystick.Joystick(0)
j.init()

#Check init status
if j.get_init() == 1: 
    print("Joystick is initialized")

print("Joystick ID: ", j.get_id())
print("Joystick Name: ", j.get_name())
print("No. of axes: ", j.get_numaxes())
print("No. of trackballs: ", j.get_numballs())
print("No. of buttons: ", j.get_numbuttons())
print("No. of hat controls: ", j.get_numhats())

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

h = 90
v = 90
SetAngle(h,3)
SetAngle(v,5)
delta = 10

while 1:
    for e in event.get():
        if e.type != QUIT:

            if (e.dict['axis'] == 0 or e.dict['axis'] == 1) and e.dict['value'] < 0.5 and e.dict['value'] > -0.5:
                GPIO.output(37,GPIO.LOW)
                GPIO.output(35,GPIO.LOW)
                GPIO.output(33,GPIO.LOW)
                GPIO.output(31,GPIO.LOW)
                # print('##### Stop #####')
            elif e.dict['axis'] == 0 and e.dict['value'] >= 0.5:
                GPIO.output(37,GPIO.LOW)
                GPIO.output(35,GPIO.HIGH)
                GPIO.output(33,GPIO.HIGH)
                GPIO.output(31,GPIO.LOW)
                # print('Right')
            elif e.dict['axis'] == 0 and e.dict['value'] <= -0.5:
                GPIO.output(37,GPIO.HIGH)
                GPIO.output(35,GPIO.LOW)
                GPIO.output(33,GPIO.LOW)
                GPIO.output(31,GPIO.HIGH)
                # print('Left')
            elif e.dict['axis'] == 1 and e.dict['value'] >= 0.5:
                GPIO.output(37,GPIO.LOW)
                GPIO.output(35,GPIO.HIGH)
                GPIO.output(33,GPIO.LOW)
                GPIO.output(31,GPIO.HIGH)
                # print('Down')
            elif e.dict['axis'] == 1 and e.dict['value'] <= -0.5:
                GPIO.output(37,GPIO.HIGH)
                GPIO.output(35,GPIO.LOW)
                GPIO.output(33,GPIO.HIGH)
                GPIO.output(31,GPIO.LOW)
                # print('Up')

            if e.dict['axis'] == 3 and e.dict['value'] >= 0.5:
                if h >= 10:
                    h -= delta
                else:
                    h = 0
                SetAngle(h,3)
            elif e.dict['axis'] == 3 and e.dict['value'] <= -0.5:
                if h <= 170:
                    h += delta
                else:
                    h = 180
                SetAngle(h,3)
            if e.dict['axis'] == 4 and e.dict['value'] <= -0.5:
                if v >= 10:
                    v -= delta
                else:
                    v = 0
                SetAngle(v,5)
            elif e.dict['axis'] == 4 and e.dict['value'] >= 0.5:
                if v <= 170:
                    v += delta
                else:
                    v = 180
                SetAngle(v,5)


GPIO.cleanup()