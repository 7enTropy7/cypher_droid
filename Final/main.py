from stream import VideoCamera
from flask import Flask, render_template, Response, request
import logging
from pygame import *
import RPi.GPIO as GPIO
from time import sleep as Sleep


log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

pi_camera = VideoCamera(flip=True) 

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


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route("/moveservos", methods=["POST"])
def moveServos():
    v_angle = int(float(request.form["updown"]))
    h_angle = int(float(request.form["leftright"]))
    
    if v_angle < 0:
        v_angle += 180
    h_angle = h_angle % 180
    
    print('Horizontal: ' + str(h_angle) + "        Vertical: " + str(v_angle))
    
    SetAngle(v_angle,vertical)
    SetAngle(h_angle,horizontal)
    Sleep(0.2)

    return Response(gen(pi_camera),mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    
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


    app.run(host='0.0.0.0', debug=False)

GPIO.cleanup()
