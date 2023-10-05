
"""Simple example showing how to get gamepad events."""
import time
import logging
import socketio
import config
import pigpio

from pymultiwii import MultiWii
from camera.camera import Camera

# =============================================
# Set logging formats
logging.basicConfig(
    level=config.server["logginglevel"],
    format=("[%(filename)8s] [%(levelname)4s] :  %(funcName)s - %(message)s"),
)

# standard Python
sio = socketio.Client()

# Start pigpio
pi = pigpio.pi()

# Start camera
cam = Camera()

# Connect to board
board = MultiWii(config.drone["mspserialdev"])

print("Calibrate")
board.sendCMD(0, MultiWii.ACC_CALIBRATION,[],'')
time.sleep(5)

# =============================================
def getData():

    attitude = board.getData(MultiWii.ATTITUDE)

    # Get camera frame
    try:
        frameBase64, _, _ = next(cam.processFrame())
    except:
        logging.error("Couldnt send frame")
        frameBase64 = ""
        pass

    print(attitude)
    return frameBase64, attitude

# =============================================
@sio.on('sendNextData')
def sendData(msg):

    frameBase64, attitude = getData()

    print("message received")
    time.sleep(config.analytic["sleeptime"])

    # Tansmit data
    sio.emit('inferenceresults', {
        'frame': frameBase64,
        'attitude': attitude,
        }, namespace=config.server["namespace"]
    )

# =============================================
@sio.on('calibrate')
def calibrate(msg):
    print("Starting calibration")
    time.sleep(4)
    board.sendCMD(0, MultiWii.ACC_CALIBRATION,[],'')
    time.sleep(4)
    print("calibration done")

# =============================================
@sio.on('control')
def setControl(msg):
    pi.set_servo_pulsewidth(config.drone["pwmpin1"], int(msg[0]))
    pi.set_servo_pulsewidth(config.drone["pwmpin2"], int(msg[1]))
    pi.set_servo_pulsewidth(config.drone["pwmpin3"], int(msg[2]))
    pi.set_servo_pulsewidth(config.drone["pwmpin4"], int(msg[3]))
    pi.set_servo_pulsewidth(config.drone["pwmpin5"], int(msg[4]))
    pi.set_servo_pulsewidth(config.drone["pwmpin6"], int(msg[5]))
    pi.set_servo_pulsewidth(config.drone["pwmpin7"], int(msg[6]))
    pi.set_servo_pulsewidth(config.drone["pwmpin8"], int(msg[7]))

# =============================================
@sio.on('toggleled')
def setArmed(msg):
    print("System armed")

# =============================================
@sio.event
def connect():
    logging.info('Successfully connected to server.')

# =============================================
@sio.event
def connect_error():
    logging.info('Failed to connect to server.')

# =============================================
@sio.event
def disconnect():
    logging.info('Disconnected from server.')


def main():
    while True:
        try:
            sio.connect(f"ws://{config.server['hostname']}:{config.server['port']}", namespaces=[config.server['namespace']])
            logging.info(f"Connected to ws://{config.server['hostname']}:{config.server['port']} under the namespace {config.server['namespace']}")
            break
        except:
            logging.warning(f"Could not connect to server ws://{config.server['hostname']}:{config.server['port']}")
            time.sleep(4)

    logging.info("Starting infinity loop")
    print("Server Online")

    # Start data Tansmission
    sio.emit('starttransmission', "start", namespace=config.server["namespace"])


if __name__ == "__main__":
    main()