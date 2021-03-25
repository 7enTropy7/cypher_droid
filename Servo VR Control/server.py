from flask import Flask, render_template_string, request
from pygame import *
import RPi.GPIO as GPIO
from time import sleep as Sleep


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


TPL = '''
<html>
    <body>
        <button id="connectbtn" onclick="requestPermission()">Connect</button>
        <div id="outputdiv"></div>
    </body>
    <script>
    var output = document.getElementById("outputdiv");
    var btn = document.getElementById("connectbtn");
    var socket = false;
    var updown = 0;
    var leftright = 0;

    function sendToFlask()
    {
        const xhr = new XMLHttpRequest();
        const data = new FormData();
        data.append("updown", updown);
        data.append("leftright", leftright);
        xhr.open("POST", "moveservos");
        xhr.send(data);
    }

    function requestPermission()
    {
        output.innerHTML = "Non-iOS 13 device";
        if(window.DeviceOrientationEvent) {
            window.addEventListener('deviceorientation', function(event) {updown = event.gamma;leftright = event.alpha;});
        }
        finishRequest();
    }

    function finishRequest()
    {
        setInterval(sendToFlask, 250);
    }

    </script>
</html>
'''
import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
app = Flask(__name__)

@app.route("/")
def serveRoot():
    return render_template_string(TPL)

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
    return ""

GPIO.cleanup()

if __name__ == "__main__":
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

    app.run(host="0.0.0.0")#, ssl_context='adhoc')

