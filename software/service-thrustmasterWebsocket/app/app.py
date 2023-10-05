"""Simple example showing how to get gamepad events."""
import asyncio
import json
import logging
import websockets

import config
from joystick import Joystick

# =============================================
# Set logging formats
logging.basicConfig(
    level=config.server["logginglevel"],
    format=("[%(filename)8s] [%(levelname)4s] :  %(funcName)s - %(message)s"),
)

# Initialize Joystick
joystick = Joystick()

# Connect to websocket
async def listen():
    url = f"ws://{config.server['hostname']}:{config.server['port']}"

    async with websockets.connect(url, ping_interval=None) as ws:
        joystick.ws = ws
        await joystick.run()

if __name__ == "__main__":
    print("WS Client is about to start")
    asyncio.get_event_loop().run_until_complete(listen())
