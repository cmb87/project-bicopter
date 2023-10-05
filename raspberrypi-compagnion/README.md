# Robotic SocketIO Control Stack
Computer Vision enhanced custom analytics

# Setup


## WiP

    scp -rv * pi@raspberrypi:/home/pi/projects/06_servoTest/.


## Start pigpio on start up



    sudo systemctl enable pigpiod

will enable it to auto-start on boot.

    
   

will start it immediately (just a posh way of doing

    sudo pigpiod

:)

If you change your mind,

    sudo systemctl disable pigpiod

will undo the start-up behaviour. Similarly,

    sudo systemctl stop pigpiod

will have an immediate effect.


## PWM Connection PiZero <-> FC

    Throttle D2 - GPIO 5
    Roll     D4 - GPIO 6
    Pitch    D5 - GPIO 13
    Yaw      D6 - GPIO 19
    Aux1     D7 - GPIO 26
    Aux1     D7 - GPIO 16
    Aux1     D7 - GPIO 20
    Aux1     D7 - GPIO 21
    G        GND
    
## Run Python script on every startup
Head over to /etc/profile, add command to start the Python script

    ...
    python3 /home/pi/..../app.py


## Issues

### RPI Slow Wifi network connection


Source (https://raspberrypi.stackexchange.com/questions/52066/pi3-wifi-extremely-slow)
Make sure power management is off on Pi.

    iwconfig

You should see something like this

    Power Management:off

If not, you can switch it to off by using

    sudo iwconfig wlan0 power off

If you want to make this permanent you should add the following line to /etc/rc.local (explanation here):

    iwconfig wlan0 power off






## Based on WiiProxy

https://github.com/engineer-99b/WiiProxy