# Joystick

Microservice which reads the input of a connected Thrustmaster.
Commands are transferred via socketIO to a MultiWii or Betaflight compatible Device.

### Add Thrustmaster USB Joystick
Device wasnt showed as /dev/ttyUSB0. According to website (https://www.linuxquestions.org/questions/linux-server-73/ttyusb0-not-showing-up-in-dev-827416/):

        mknod /dev/ttyUSB0 c 188 0

# Docker

        docker build -t cmb87/skylink-thrustmaster:latest -f docker/Dockerfile .
        docker run --privileged -v /dev:/dev -e ENV_SOCKETIOSERVER="192.168.2.138"  joystick:latest
        docker push  cmb87/skylink-thrustmaster:latest