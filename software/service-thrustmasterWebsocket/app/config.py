import os
import logging

_loggingLevels = {
    "INFO": logging.INFO, "DEBUG": logging.DEBUG,
    "CRITICAL": logging.CRITICAL, "ERROR": logging.ERROR,
}

joystick = {
    "channelorder": os.getenv('ENV_CHANNELORDER', "throttle roll pitch yaw aux1 aux2 aux3 aux4").split(" "), # Default MultiWii
    "timesleep": float(os.getenv('ENV_TIMESLEEP', "0.1")),
    "lastTime": float(os.getenv('ENV_TIMESLEEP', "1.0")),
    "config": {
        "ABS_Z": {"lb": 127, "ub": -128, "iv": 0, "lbm": 1000, "ubm": 1550, "description": "throttle", "invert": False},
        "ABS_X": {"lb": -128, "ub": 127, "iv": 0, "lbm": 1300, "ubm": 1700, "description": "roll", "invert": False},
        "ABS_Y": {"lb": -128, "ub": 127, "iv": 0, "lbm": 1000, "ubm": 2000, "description": "pitch", "invert": True},
        "ABS_HAT0X": {"lb": -1, "ub": 1, "iv": 0, "lbm": 1100, "ubm": 1900, "description": "yaw", "invert": False},
        "ABS_HAT0Y": {"lb": -1, "ub": 1, "iv": 0, "lbm": 1100, "ubm": 1900, "description": "aux4", "invert": False},

        "BTN_THUMB": {"lb": 0, "ub": 1, "iv": 0, "lbm": 1100, "ubm": 1800, "description": "aux1", "activated": False},
        "BTN_TOP": {"lb": 0, "ub": 1, "iv": 0, "lbm": 1100, "ubm": 1800, "description": "aux2", "activated": False},
        "BTN_TRIGGER": {"lb": 0, "ub": 1, "iv": 0, "lbm": 1100, "ubm": 1800, "description": "aux3", "activated": False},
    }
}

server = {
    "appname": os.getenv('ENV_APPNAME', 'joystick'),
    "logginglevel": _loggingLevels[os.getenv('LOGGING', 'CRITICAL').upper()],
    "hostname": os.getenv('ENV_WEBSOCKETSERVER', '192.168.2.147'),
    "port": int(os.getenv('ENV_WEBSOCKETPORT', 81)),
    "namespace": os.getenv('ENV_NAMESPACE', "/control"),
}




