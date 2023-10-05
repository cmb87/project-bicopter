"""Simple example showing how to get gamepad events."""
import time
import logging
import socketio
import config

from joystick import Joystick

# =============================================
# Set logging formats
logging.basicConfig(
    level=config.server["logginglevel"],
    format=("[%(filename)8s] [%(levelname)4s] :  %(funcName)s - %(message)s"),
)

# standard Python
sio = socketio.Client()

# Initialize Joystick
joystick = Joystick(socketIOClient=sio)

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
    joystick.start()

if __name__ == "__main__":
    main()
