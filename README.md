# cYpher_droid

This project was completed under the guidance of [**Dr. P. Mahalakshmi**](https://research.vit.ac.in/researcher/mahalakshmi-p).

## Introduction

Cypher is an autonomous robot capable of traversing alien environments and sending relevant data retrieved back to the user. It uses a VR based controller that allows the user to take control of the bot and use the real-time video feed from the bot to manipulate various aspects of the bot.

## How Stuff Works

The locomotion of the VR bot is manipulated by a bluetooth enabled gaming controller. We plan on using a dual joystick controller for experimentation of the concept. The signals transmitted by the controller to the raspberry pi across bluetooth will first be parsed at a satisfactory refresh rate to minimize lag. These joystick axis commands will then be parsed using pygame module and will be converted to the appropriate GPIO on-off signals on the raspberry pi which will then be sent to the motor driver circuit. 

The raspberry pi will have a picam attached onboard which will stream the live video. The picam will be placed on a servo bracket that allows 2 degrees of freedom. The video streamed by the picamera will be hosted on a flask server website on the raspberry pi itself. The website, when opened on a handheld device, will render the live feed in a 2-windowed VR format. 

The code hosted on the Flask server will additionally track the gyroscopic values of the client device. These x-y axis readings will be sent back to the flask server on the raspberry pi where they will be translated to the appropriate PWM based servo commands that will move the servo bracket to change the camera view in real time. 

![cypher](https://user-images.githubusercontent.com/36446402/114155223-dd9ce080-993e-11eb-98ac-7e8cd16f845f.png)


## Dependencies
```bash
$ pip3 install -r requirements.txt
```

## Instructions
```bash
$ python3 main.py
```

> **Note :** 
> - After running the main.py file, open the address: ***IP of raspberry pi:5000** on your smartphone webbrowser.
> - Preferably use ***Firefox browser*** on Android to avoid sensor data permission related issues
> - Make sure your smartphone and raspberry pi are connected to the same wifi network.
> - Press Connect button on webpage.
> - Hit Calibrate button after pointing phone in same direction as cYpher.

cYpher's now ready to go out for a spin!

## Demonstration

### VR Headset View

![ezgif com-gif-maker (7)](https://user-images.githubusercontent.com/36446402/114066930-dda6cd00-98b9-11eb-8a0f-457779c7e8b9.gif)

### Realtime Demo
![ezgif com-gif-maker (7)](https://user-images.githubusercontent.com/36446402/114071931-4fcde080-98bf-11eb-8c4c-67c4076cd932.gif)

## Creators
* [**Atharva Hudlikar**](https://github.com/Mastermind0100)
* [**Unnikrishnan Menon**](https://github.com/7enTropy7)