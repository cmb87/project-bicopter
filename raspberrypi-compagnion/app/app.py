"""Simple example showing how to get gamepad events."""
import time
import logging
import socketio
import config

from camera.camera import Camera
from control.ppm import PPM
from msp.msp import MSP

# =============================================
# Set logging formats
logging.basicConfig(
    level=config.server["logginglevel"],
    format=("[%(filename)8s] [%(levelname)4s] :  %(funcName)s - %(message)s"),
)

# Initialize camera object
camera = Camera()

# PPM Class
ppm = PPMDummy(gpio=config.drone["ppmgpio"], frame_ms=20)

# MSP Class
msp = MSPDummy(serialPort=config.drone["mspserialdev"])

# standard Python
sio = socketio.Client()

# =============================================

def getData():

    # Get Attitude
    attitude = msp.getAttitude()

    # Get camera frame
    try:
        frameBase64, _, _ = next(camera.processFrame())
    except:
        logging.error("Couldnt send frame")
        frameBase64 = ""
        pass

    return frameBase64, attitude


# =============================================
@sio.on('sendNextData')
def sendData(msg):

    frameBase64, attitude = getData()

    print("message received")

    # Tansmit data
    sio.emit('inferenceresults', {
        'frame': frameBase64,
        'attitude': attitude,
        }, namespace=config.server["namespace"]
    )
    time.sleep(config.analytic["sleeptime"])

# =============================================
@sio.on('control')
def setControl(msg):
    logging.info(msg)
    ppm.update_channels(msg)

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

    # Start data Tansmission
    sio.emit('starttransmission', "start", namespace=config.server["namespace"])


if __name__ == "__main__":
    main()