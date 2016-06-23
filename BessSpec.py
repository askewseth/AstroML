"""Spectrum object for filesdownloaded from the BESS database."""
import os
import pyfits
import math
import csv
import matplotlib.pyplot as plt
import gc


class spectrum():
    """Spectrum object initialized with file path."""

    def __init__(self, path):
        """initalize the spectrum."""
        self.path = path
        self.f = pyfits.open(path)
        self.head = self.f[0].header
        self.data = self.f[0].data
        self.date = self.head['DATE-OBS']
        self.obj_name = (' ').join(self.head['OBJNAME'].split()).lower()
        try:
            self.hjd = self.head['HJD-MID']
        except:
            self.hjd = self.head['MID-HJD']
        self.fname = self.getFName()
        self.vhel = self.head['BSS_VHEL']
        self.wls = self.getWLARR()
        self.f.close()
        gc.collect()

    def getFName(self):
        """private."""
        name = ('').join(self.obj_name.split())
        fname = name + '_' + str(self.hjd).split('.')[0] +\
            '_' + str(self.hjd).split('.')[1]
        return fname

    def getWLARR(self):
        """private."""
        wli = self.head['CRVAL1']
        step = self.head['CDELT1']
        wls = []
        for x in range(len(self.data)):
            tmp = wli + (x * step)
            wls.append(tmp)
        return wls

    def getWLRange(self):
        """private."""
        ini = str(math.floor(self.wls[0]))
        fin = str(math.ceil(self.wls[-1]))
        ret = ini + " - " + fin
        return ret

    def hasHA(self):
        """return true if spectrum contains ha line."""
        wls = self.getWLARR()
        wli = int(math.floor(wls[1]))
        wlf = int(math.ceil(wls[-1]))
        if 6562 in range(wli, wlf):
            return True
        else:
            return False

    def convertCSV(self):
        """convert .fits file to .csv file."""
        newname = self.path[:-5] + '.csv'
        data = []
        wls = self.wls
        d = self.data
        for x in range(len(self.data)):
            tmp = [wls[x], d[x]]
            data.append(tmp)
        with open(newname, 'w') as f:
            writer = csv.writer(f, delimiter=',')
            writer.writerows(data)

    def convertCSVNew(self):
        """convert csv with new naming convention."""
        newname = self.fname + '.csv'
        data = []
        wls = self.wls
        d = self.data
        for x in range(len(self.data)):
            tmp = [wls[x], d[x]]
            data.append(tmp)
        filepath_arr = self.path.split('/')
        dirpath = ('/').join(filepath_arr[:-1])
        os.chdir(dirpath)
        with open(newname, 'w') as f:
            writer = csv.writer(f, delimiter=',')
            writer.writerows(data)

    def plot(self):
        """plot the spectra."""
        plt.plot(self.wls, self.data)
        title = self.date
        plt.title(title)
        plt.xlabel('Wavelength (Angstroms)')
        plt.ylabel('Intensity')
        plt.show()
