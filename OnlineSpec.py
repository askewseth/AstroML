import os
import math
import matplotlib.pyplot as plt
from PyAstronomy import pyasl

class spectrum():
    """Creates spectrum object from online file."""

    def __init__(self, data, date):
        """Initialize spectrum with 2darray data and date."""
        self.raw = data
        self.data = [x[1] for x in self.raw]
        self.path = None
        self.f = None
        self.head = None
        self.hjd = date
        self.date = self.get_date()
        self.obj_name = None
        self.fname = None
        self.vhel = None
        self.wls = [x[0] for x in self.raw]

    def hasHA(self):
        """Return true if spectrum contains halpha line."""
        wli = int(math.floor(self.wls[0]))
        wlf = int(math.ceil(self.wls[-1]))
        if 6562 in range(wli, wlf):
            return True
        else:
            return False

    def get_date(self):
        """private method to get date in normal format."""
        date_arr = map(str, pyasl.daycnv(self.hjd))
        date_str = date_arr[1] + '-' + date_arr[2] + '-' + date_arr[0]
        return date_str

    def plot(self):
        """Plot the spectrum."""
        plt.plot(self.wls, self.data)
        title = self.date
        plt.title(title)
        plt.xlabel('Wavelength (Angstroms)')
        plt.ylabel('Intensity')
        plt.show()
