import os
import pyfits
import math
import csv
import matplotlib.pyplot as plt
import numpy as np

class spectrum():
    """
    Spectrum object initialized with file path.
    """
    def __init__(self, path):
        self.path = path
        self.f = pyfits.open(path)
        self.head = self.f[0].header
        self.data = self.f[0].data
        self.date = self.head['DATE-OBS']
        self.obj_name = (' ').join(self.head['OBJNAME'].split()).lower()
        try:
            self.hjd = self.head['HJD-MID']
        except Exception, e:
            self.hjd = self.head['MID-HJD']
        self.fname = self.getFName()
        self.vhel = self.head['BSS_VHEL']
        self.wls = self.getWLARR()

    def getFName(self):
        name = ('').join(self.obj_name.split())
        fname = name + '_' + str(self.hjd).split('.')[0] + '_' + str(self.hjd).split('.')[1]
        return fname

    def getWLARR(self):
        wli = self.head['CRVAL1']
        step = self.head['CDELT1']
        wls = []
        for x in range(len(self.data)):
            tmp = wli + ( x * step )
            wls.append(tmp)
        return wls

    def getWLRange(self):
        ini = str(math.floor(self.wls[0]))
        fin = str(math.ceil(self.wls[-1]))
        ret = ini + " - " + fin
        return ret

    def hasHA(self):
        wls = self.getWLARR()
        wli = int(math.floor(wls[1]))
        wlf = int(math.ceil(wls[-1]))
        if 6562 in range(wli, wlf):
            return True
        else:
            return False

    def convertCSV(self):
        newname = self.path[:-5] + '.csv'
        data = []
        wls = self.wls
        d = self.data
        for x in range(len(self.data)):
            tmp = [ wls[x], d[x] ]
            data.append(tmp)
        with open(newname, 'w') as f:
            writer = csv.writer(f, delimiter = ',')
            writer.writerows(data)

    def convertCSVNew(self):
        newname = self.fname + '.csv'
        data = []
        wls = self.wls
        d = self.data
        for x in range(len(self.data)):
            tmp = [ wls[x], d[x] ]
            data.append(tmp)
        filepath_arr = self.path.split('/')
        dirpath = ('/').join(filepath_arr[:-1])
        os.chdir(dirpath)
        with open(newname, 'w') as f:
            writer = csv.writer(f, delimiter = ',')
            writer.writerows(data)

    def plot(self):
        plt.plot(self.wls ,self.data)
        title = self.date
        plt.title(title)
        plt.xlabel('Wavelength (Angstroms)')
        plt.ylabel('Intensity')
        plt.show()


def makeList(path):
    try:
        fileNames = [path + x for x in os.listdir(path)]
    except:
        return 'try again'
    specs = []
    specsnoha = []
    nospecs = []
    for f in fileNames:
        try:
            s = spectrum(f)
            if s.hasHA():
                specs.append(s)
            else:
                specsnoha.append(s)
        except:
            nospecs.append(f)
    return specs, specsnoha, nospecs

def test(dirpath = '/home/seth/Desktop/AstroML/Drive/Astro/BeSS/'):
    files = []
    for f in os.listdir(dirpath):
        if '.fits' in f:
            files.append(dirpath + f)
    specs = []
    for f in sorted(files):
        try:
            specs.append(spectrum(f))
        except Exception, e:
            print 'ERROR FILE', f
    return specs

def main():
    specs = test()
    for s in specs:
        try:
            s.plotHA()
        except Exception, e:
            print(s.date)


##specs = test()
##has = []
##nots = []
##for s in specs:
##    if s.hasHA():
##        has.append(s)
##    else:
##        nots.append(s)
