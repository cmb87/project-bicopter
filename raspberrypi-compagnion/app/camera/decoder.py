import logging
import base64
import cv2
import numpy as np

def decode(frame):
    # Send encoded frame back to browser
    retval, buf = cv2.imencode('.png', frame)
    png_as_text = base64.b64encode(buf).decode('utf-8')
    return f"data:image/png;base64,{png_as_text}"
