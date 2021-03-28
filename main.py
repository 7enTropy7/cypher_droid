from stream import VideoCamera
from flask import Flask, render_template_string, Response, request
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

TPL = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=0.5">
    <title>Video Stream</title>
</head>
<body>
    <center><h1>cYpher</h1></center>
    <div style="width:50%;Text-align:left;float:left;">
        <img  class="camera-bg" style="width: 90%; height:60%; background-attachment: fixed;" id="bg" class="center" src="{{ url_for('video_feed') }}">        
    </div>
    <div style="Text-align:right;Width:50%;float:right">
        <img  class="camera-bg" style="width: 90%; height:60%; background-attachment: fixed;" id="bg" class="center" src="{{ url_for('video_feed') }}">        
    </div>
        <button id="connectbtn" onclick="requestPermission()">Connect</button>
        <button id="calibratebtn" onclick="calibrate()">Calibrate</button>
    <div id="outputdiv"></div>
</body> 
<script>
    var output = document.getElementById("outputdiv");
    var btn = document.getElementById("connectbtn");
    var socket = false;
    var initPos_h = 0;
    var initPos_v = 0;
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
        output.innerHTML = "Android device";
        if(window.DeviceOrientationEvent) {
            window.addEventListener('deviceorientation', function(event) {
                updown = event.gamma;
                leftright = event.alpha-initPos_h+90;});
        }
        finishRequest();
    }
    function calibrate()
    {
        initPos_h = leftright;
        initPos_v = updown;
    }
    function finishRequest()
    {
        setInterval(sendToFlask, 500);
    }
</script>
</html>
'''

@app.route('/')
def index():
    return render_template_string(TPL)

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(pi_camera),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


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


    app.run(host='0.0.0.0')

GPIO.cleanup()
