
"""Simple example showing how to get gamepad events."""
import time
import logging
import socketio
import config
import pigpio

from multiwii.multiwii import MultiWii
from camera.camera import Camera



def push8(buf, val):
    buf.append(0xFF & val)


def push16(buf, val):
    # low byte
    push8(buf, val)

    # high byte
    push8(buf, val >> 8)

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
board = MultiWii(serPort=config.drone["mspserialdev"])

# =============================================
def getData():

    attitude = {} #board.read_attitude()

    # Get camera frame
    try:
        frameBase64, _, _ = "" #next(cam.processFrame())
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
    time.sleep(4)
    print("calibration done")

# =============================================
@sio.on('control')
def setControl(msg):

    #
    buf = []
    push16(buf, msg[0])
    push16(buf, msg[1])
    push16(buf, msg[2])
    push16(buf, msg[3])
    push16(buf, msg[4])
    push16(buf, msg[5])
    push16(buf, msg[6])
    push16(buf, msg[7])


    board.sendCMD(MultiWii.SET_RAW_RC, buf)
    time.sleep(0.025)
    # msg = [1500,1500,1000,1500,0,0,0,0]
    #
    # for i in range(len(msg)):
    #   binary = '{0:016b}'.format(msg[i])
    #   msg.append(int(binary[8:], 2))
    #   msg.append(int(binary[:8], 2))
    #
    # print(msg)
    # board.sendCMD(16,MultiWii.SET_RAW_RC,msg,'16B')

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