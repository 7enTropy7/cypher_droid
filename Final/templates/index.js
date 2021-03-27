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
    output.innerHTML = "Android device";
    if(window.DeviceOrientationEvent) {
        window.addEventListener('deviceorientation', function(event) {updown = event.gamma;leftright = event.alpha;});
    }
    finishRequest();
}
function finishRequest()
{
    setInterval(sendToFlask, 250);
}
