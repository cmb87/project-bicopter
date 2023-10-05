import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate
import os

class Spline:

    def __init__(self, cnpts, closed=False, name="Spline"):
        self.cnpts = np.asarray(cnpts)
        self.name = name

    def generate(self, npts: int = 100, closed: bool=False, normalize: bool=False):
        le = self.cnpts.shape[0]
        t = np.linspace(0, 1, le - 2, endpoint=True)
        t = np.append([0, 0, 0], t)
        t = np.append(t, [1, 1, 1])

        tck = [t, [self.cnpts[:, 0], self.cnpts[:, 1]], 3]
        u3 = np.linspace(0, 1, (max(le * 2, npts)), endpoint=True)
        self.geom = np.asarray(interpolate.splev(u3, tck)).T

        if normalize:
            self.geom = self.geom/np.linalg.norm(self.geom[0,:]-self.geom[-1,:])

        if closed:
            self.geom = np.vstack((self.geom, self.geom[0,:]))

        return self.geom

    def plot(self,mirror=False, plot=True):

        plt.plot(self.cnpts[:,0], self.cnpts[:,1], 'o--', color="gray")
        plt.plot(self.geom[:,0], self.geom[:,1], 'r-')
        if mirror:
            plt.plot(-self.cnpts[:,0], self.cnpts[:,1], 'o--', color="gray")
            plt.plot(-self.geom[:,0], self.geom[:,1], 'r-')
        plt.axis("equal")
        plt.grid(True)
        if plot:
            plt.show()


    def _geom2pnts(self):
        _pnts = (
            ", ".join([str([pnt[0], pnt[1]]) for pnt in self.geom.tolist()])
            + ", "
        )
        return _pnts


    def linearExtrude(self, filename, z=10):
        
        with open(filename,'a') as f1:

            content = "module " + self.name + "(){\n"
            content += " rotate([-90,0,0])\n"
            content += " union() {\n"
            content += f"  linear_extrude(height = {z}, center = true, convexity = 10, twist = 0)polygon( points=[" + self._geom2pnts() + "] );\n"
            content += f"  linear_extrude(height = {z}, center = true, convexity = 10, twist = 0)mirror([1,0,0])polygon( points=[" + self._geom2pnts() + "] );\n"
            content += "};};\n\n"

            f1.write(content)

    def rotateExtrude(self, filename):

        with open(filename,'a') as f1:

            content = "module " + self.name + "(){\n"
            content += "  rotate(a=[0,90,0]) {\n"
            content += "    rotate_extrude($fn=200){\n"
            content += "      polygon( points=[" + self._geom2pnts() + "] );\n"
            content += "    };\n"
            content += "  };\n"
            content += "};\n\n"

            f1.write(content)
