import re
import matplotlib.pyplot as plt
import numpy as np


pat = re.compile(r'(G.+)X\s*(\d+\.?\d+)\s*Y\s*(\d+\.?\d+)(.*)')

# ========================================================
def writeMergedFile(filename, contents):

    newfilename = f"{filename.split('.')[0]}_merged.gcode"

    header =  "G21"+"\n"
    header += "G90"+"\n"
    header += "G94"+"\n"
    header += "F40.00"+"\n"
    header += "G00 Z3.0000"+"\n"
    header += "M03 S1000"+"\n"
    header += "G4 P1"+"\n"

    footer = "G00 Z11.0000"+"\n"
    footer+= "M05"+"\n"    

    with open(newfilename, 'w') as f1:
        f1.write(header + ''.join(contents) + footer) 

def duplicateMerge(files, offsets):

    for f in files:
        # Initialize content
        contents = len(offsets)*['']
        # Read lines
        with open(f,'r') as f1:
            lines = f1.readlines()[8:-2]

        # Loop over content
        for line in lines:
            m = pat.match(line)
            if m:
                g = m.group(1)
                x = float(m.group(2))
                y = float(m.group(3))
                e = m.group(4)

                for n, off in enumerate(offsets):
                    contents[n] += f"{g}X{x+off[0]:.3f} Y{y+off[1]:.3f}{e}\n"
            else:
                for n, off in enumerate(offsets):     
                    contents[n] += line

        writeMergedFile(f, contents)
# ========================================================

offsetsTop = [[0,0], [15,0], [30,0], [45,0], [60,0], [0,13], [15,13], [30,13], [45,13], [60,13]]
filesTop = ["top1.gcode", "drill1.gcode",] #["drill1.gcode", "top1.gcode"]

offsetsBot = [[-o[0], o[1]] for o in offsetsTop]
filesBot = ["bottom1.gcode", "cutout1.gcode",] #["drill1.gcode", "top1.gcode"]

print(offsetsBot)
duplicateMerge(filesTop, offsetsTop)
duplicateMerge(filesBot, offsetsBot)