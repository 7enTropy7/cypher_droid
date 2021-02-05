from flask import Flask, render_template_string, request
from time import sleep
import pigpio

# This HTML page + JS will be served when the root path is requested with a GET
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

function handleRotation(event)
{
    updown = Math.round(event.gamma);
    leftright = Math.round(event.beta);
}

function requestPermission()
{
    if (typeof(DeviceMotionEvent) !== 'undefined' && typeof(DeviceMotionEvent.requestPermission) === 'function')
    {
        output.innerHTML = "iOS 13+ device";
        DeviceMotionEvent.requestPermission().
        then(response => {
            if (response === 'granted') {
                output.innerHTML = "iOS 13+ device (Permission granted)";
                window.addEventListener('deviceorientation', handleRotation);
            }
            else {
                output.innerHTML = "iOS 13+ device (Permission denied)";
            }
            finishRequest();
        }).catch(console.error);
    }
    else
    {
        output.innerHTML = "Non-iOS 13 device";
        window.addEventListener('deviceorientation', handleRotation);
        finishRequest();
    }
}

function finishRequest()
{
    setInterval(sendToFlask, 250);
}

  </script>
</html>
'''

# The servos are connected on these GPIO pins (BCM numbering)
HORIZ_SERVO_PORT = 13
VERT_SERVO_PORT= 12

# Servo Info
HORIZ_SERVO_CENTER = 1750
VERT_SERVO_CENTER = 1500

# Create Flask App
app = Flask(__name__)

# GPIO Info
gpio = pigpio.pi()

def setupGPIO():
    gpio.set_servo_pulsewidth(HORIZ_SERVO_PORT, 0)
    gpio.set_servo_pulsewidth(VERT_SERVO_PORT, 0)

def setServoDuty(servo, duty):
    gpio.set_servo_pulsewidth(servo, duty)

def clamp(num, minimum, maximum):
    return max(min(num, maximum), minimum)

# Serve the HTML file when the root path is requested
@app.route("/")
def serveRoot():
    return render_template_string(TPL)

# Expose an endpoint for sending the servo coordinates
# from the JS to the Flask Backend
@app.route("/moveservos", methods=["POST"])
def moveServos():
    # Get the values from the request
    horizontal = 25 * int(request.form["updown"])
    vertical = 25 * int(request.form["leftright"])
    print(str(horizontal) + ", " + str(vertical))

    # Move the Servos
    setServoDuty(HORIZ_SERVO_PORT, clamp(HORIZ_SERVO_CENTER - horizontal, 500, 2500))
    setServoDuty(VERT_SERVO_PORT, clamp(VERT_SERVO_CENTER - vertical, 500, 2500))

    # Wait for 0.2s so that the servos have time to move
    sleep(0.2)

    # Stop the servo motors to save energy and reduce noise
    gpio.set_servo_pulsewidth(HORIZ_SERVO_PORT, 0)
    gpio.set_servo_pulsewidth(VERT_SERVO_PORT, 0)

    # Return empty request (Should return a 200 OK with an empty body)
    return ""

# Run the app on the local development server
# Accept any IP address
# Create ad-hoc SSL encryption (needed for iOS 13 support)
if __name__ == "__main__":
    app.run(host="0.0.0.0")#, ssl_context='adhoc')


