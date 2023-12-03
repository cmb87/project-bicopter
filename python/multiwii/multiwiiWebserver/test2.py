from os     import system
from shutil import copy2
from termios import CR2
from serial import Serial
from time   import sleep, time
import random

from multiwii.multiwii import MultiWii, Commands, Priority

# -----------------------------------------------------------

#    board = multiwii.Multiwii("/dev/ttyAMA0")
#   # board = multiwii.Multiwii("/dev/serial1")

# https://stackoverflow.com/questions/28343941/python-serialexception-device-reports-readiness-to-read-but-returned-no-data-d
serial = Serial("/dev/ttyUSB0", 115200)

for i in range(16):
  print("Start in ", 16-i)
  sleep(1)

Commands.seed()

fc = MultiWii(serial)

# -----------------------------------------------------------

def arm():
    command = Commands.SET_RAW_RC
 #   values  = (1500, 1500, 2000, 1000, 0, 0, 0, 0)
    values  = (1000, 1500, 1500, 2000, 0, 0, 0, 0)

   #"throttle roll pitch yaw aux1 aux2 aux3 aux4")

    start   = time()
    elapsed = 0

    while elapsed < 0.5:
        fc.execute(command, values)

        sleep(0.05)

        elapsed = time() - start


def disarm():

    command = Commands.SET_RAW_RC
    values  = (1500, 1500, 1000,1000, 0, 0, 0, 0)
    
    start   = time()
    elapsed = 0

    while elapsed < 0.5:
        fc.execute(command, values)

        sleep(0.05)

        elapsed = time() - start


# -----------------------------------------------------------

fc.start()

print("Arming...")

arm()

print("Armed.")

Commands.IDENT.priority = Priority.Low

t0 = 0

while True:
    ident       = fc.data[Commands.IDENT]
    status      = fc.data[Commands.STATUS]
    rc          = fc.data[Commands.RC]
    imu         = fc.data[Commands.RAW_IMU]
    attitude    = fc.data[Commands.ATTITUDE]

    print(imu.gyro, rc.throttle, rc.roll, rc.pitch, rc.yaw, rc.aux)


    if t0 > 16:
      c1 = random.randint(1000,2000) # Yaw
      c2 = random.randint(1000,2000)
      c3 = random.randint(1000,2000)
      c4 = random.randint(1000,2000) # Throttle

      print(c1,c2,c3,c4)
                                   #  Throttle
      fc.execute( Commands.SET_RAW_RC, (c1, c2, c3, c4, 0, 0, 0, 0))
       
      sleep(0.05)
      

      t0 = 0
    else:
       t0 +=1






    # print("RC                        ")
    # print("--------------------------")
    # print(f"roll      = {rc.roll}    ")
    # print(f"pitch     = {rc.pitch}   ")
    # print(f"yaw       = {rc.yaw}     ")
    # print(f"throttle  = {rc.throttle}")
    # print(f"aux       = {rc.aux}     ")

    # print()

    # print("IMU                ")
    # print("-------------------")
    # print(f"acc   = {imu.acc} ")
    # print(f"gyro  = {imu.gyro}")
    # print(f"mag   = {imu.mag} ")

    # print()

    # print("ATTITUDE                      ")
    # print("------------------------------")
    # print(f"angle    = {attitude.angle}  ")
    # print(f"heading  = {attitude.heading}")

    sleep(0.05)

#    sleep(0.1)

#    system("clear") # system("cls")

fc.stop()

print("Exiting...")
