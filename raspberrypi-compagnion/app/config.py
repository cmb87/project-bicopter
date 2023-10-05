import os
import logging

_loggingLevels = {
    "INFO": logging.INFO, "DEBUG": logging.DEBUG,
    "CRITICAL": logging.CRITICAL, "ERROR": logging.ERROR,
}

drone = {
    "ppmgpio": int(os.getenv('PPMGPIO', '26')), # Pin 37 on PiZero
    "mspserialdev" : os.getenv('SERIALMSPDEV', "/dev/ttyS0"),
    "pwmpin1": int(os.getenv('pwmpin1', 5)),
    "pwmpin2": int(os.getenv('pwmpin2', 6)),
    "pwmpin3": int(os.getenv('pwmpin3', 13)),
    "pwmpin4": int(os.getenv('pwmpin4', 19)),
    "pwmpin5": int(os.getenv('pwmpin5', 26)),
    "pwmpin6": int(os.getenv('pwmpin6', 16)),
    "pwmpin7": int(os.getenv('pwmpin7', 20)),
    "pwmpin8": int(os.getenv('pwmpin8', 21)),
}

analytic = {
    "flip": os.getenv('INFERENCEFLIP', '0'),
    "send_width": int(os.getenv('SENDWIDTH', '100')),
    "send_height": int(os.getenv('SENDHEIGHT', '100')),
    "source": int(os.getenv('CAMERADEV', '0')),
    "sleeptime": float(os.getenv('INFERENCESLEEPTIME', '0.1')),
    "graysend": os.getenv('INFERENCEGRAY', '1'),
}

server = {
    "appname": os.getenv('ENV_APPNAME', 'joystick'),
    "logginglevel": _loggingLevels[os.getenv('LOGGING', 'CRITICAL').upper()],
    "hostname": os.getenv('ENV_SOCKETIOSERVER', '192.168.2.109'),
    "port": int(os.getenv('ENV_SOCKETIOPORT', 5000)),
    "namespace": os.getenv('ENV_NAMESPACE', "/control"),
}