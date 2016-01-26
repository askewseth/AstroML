import os
import pyfits
import math
import csv
import matplotlib.pyplot as plt
import numpy as np

class spectrum():

    def __init__(self, data, date):
        self.raw = data
        self.data = [x[1] for x in self.raw]
        self.path = None
        self.f = None
        self.head = None
        self.date = None
        self.hjd = date
        self.obj_name = None
        self.fname = None
        self.vhel = None
        self.wls = [x[0] for x in self.raw]


    def hasHA(self):
        wli = int(math.floor(self.wls[0]))
        wlf = int(math.ceil(self.wls[-1]))
        if 6562 in range(wli, wlf):
            return True
        else:
            return False

    def plot(self):
        plt.plot(self.wls ,self.data)
        title = self.date
        plt.title(title)
        plt.xlabel('Wavelength (Angstroms)')
        plt.ylabel('Intensity')
        plt.show()
