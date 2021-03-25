from flask import Flask, render_template_string, request

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

app = Flask(__name__)

@app.route("/")
def serveRoot():
    return render_template_string(TPL)

@app.route("/moveservos", methods=["POST"])
def moveServos():
    vertical = request.form["updown"]
    horizontal = request.form["leftright"]
    print('Horizontal: ' + str(horizontal) + "        Vertical: " + str(vertical))
    return ""

if __name__ == "__main__":
    app.run(host="0.0.0.0")#, ssl_context='adhoc')
