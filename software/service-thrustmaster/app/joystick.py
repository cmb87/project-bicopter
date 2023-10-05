from inputs import get_gamepad
import logging
import config
import time

class Joystick:

    # =================================
    def __init__(self, socketIOClient):

        self.state = {
            "throttle": config.joystick["config"]["ABS_Z"]["lbm"],
            "pitch": 1500,
            "roll": 1500,
            "yaw": 1500,
            "aux1": 1000,
            "aux2": 1000,
            "aux3": 1000,
            "aux4": 1000
        }

        self.sio = socketIOClient

        logging.info("Joystick instance created!")

    # =================================
    def _send(self):
        self.sio.emit(
            'joystick',
            [self.state[k] for k in config.joystick["channelorder"]],
            namespace=config.server['namespace']
        )
    # =================================
    def start(self):
        """Just print out some event infomation when the gamepad is used."""

        timeLastEmit = 0.0
        timeLastTransmission = 0.0

        while True:

            events = get_gamepad()

            for event in events:

                if event.code in ["ABS_X", "ABS_Y", "ABS_Z", "ABS_HAT0X", "ABS_HAT0Y"]:

                    if config.joystick["config"][event.code]['invert']:
                        val = 1.0 - (event.state - config.joystick["config"][event.code]['lb']) / (
                                    config.joystick["config"][event.code]['ub'] - config.joystick["config"][event.code]['lb'])
                    else:
                        val = (event.state - config.joystick["config"][event.code]['lb']) / (
                                    config.joystick["config"][event.code]['ub'] - config.joystick["config"][event.code]['lb'])

                    val = int(config.joystick["config"][event.code]['lbm'] + val * (
                                config.joystick["config"][event.code]['ubm'] - config.joystick["config"][event.code]['lbm']))
                    self.state[config.joystick["config"][event.code]['description']] = val

                if event.code in ["BTN_THUMB", "BTN_TOP", "BTN_TRIGGER"]:
                    # Deactivate Button from activated state
                    if config.joystick["config"][event.code]['activated'] and event.state == 1:
                        self.state[config.joystick["config"][event.code]['description']] = config.joystick["config"][event.code]['lbm']
                        config.joystick["config"][event.code]['activated'] = False

                    # Activate Button
                    elif not config.joystick["config"][event.code]['activated'] and event.state == 1:
                        self.state[config.joystick["config"][event.code]['description']] = config.joystick["config"][event.code]['ubm']
                        config.joystick["config"][event.code]['activated'] = True

            # sio.emit('gamepad', [self.state[k] for k in ["pitch", "roll", "throttle", "yaw", "aux1", "aux2" ]])
            # sio.emit('gamepad', [self.state[k] for k in ["pitch", "yaw", "throttle", "roll", "aux1", "aux2", "aux3", "aux4" ]])

            # ["throttle", "roll", "pitch", "yaw", "aux1", "aux2", "aux3", "aux4"] for multiwii!
            # only emit every t timesteps
            if (time.time()-timeLastEmit) > config.joystick["timesleep"]:
                # Hello
                self._send()
                timeLastEmit = time.time()


