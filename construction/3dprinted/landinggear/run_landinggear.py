import numpy as np
import os
import matplotlib.pyplot as plt
from spline import Spline



cnpts = [
    [0,0],
    [25,0],
    [30,0],
    [40,-5],
    [50,-25],
    
    [48.5,-25],
    [40,-10], 
    [30,-3],
    [0,-3],

]




spline = Spline(cnpts, name="LandingGear")
spline.generate()
spline.plot(mirror=False, plot=False)

plt.axis("equal")
plt.show()
filename = 'landingGear.scad'

spline.linearExtrude(filename, z=15)

with open(filename, 'a') as f1:
    f1.write("LandingGear();\n")
