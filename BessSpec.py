"""Spectrum object for filesdownloaded from the BESS database."""
import os
import pyfits
import math
import csv
import matplotlib.pyplot as plt
import gc


class spectrum(object):
    """Spectrum object initialized with file path."""

    def __init__(self, path):
        """initalize the spectrum."""
        self.path = path
        self.f = pyfits.open(path)
        self.head = self.f[0].header
        self.data = self.f[0].data
        self.date = self._getDate()
        self.obj_name = (' ').join(self.head['OBJNAME'].split()).lower()
        try:
            self.hjd = self.head['HJD-MID']
        except:
            self.hjd = self.head['MID-HJD']
        self.fname = self._getFName()
        self.vhel = self.head['BSS_VHEL']
        self.wls = self._getWLARR()
        self.f.close()
        gc.collect()

    def __repr__(self):
        """Print Spectrum type along with object name and obs. date."""
        obj_name = self.obj_name.title().rjust(8)
        date = self.date.rjust(12)
        return "BeSS  Spectrum: {0}, {1} ".format(obj_name, date)

    def _getDate(self):
        raw_date = self.head['DATE-OBS'][:10]
        months_list = ['Jan', 'Feb', 'March', 'April', 'May', 'June',
                       'July', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec']
        months = {str(x+1).rjust(2, '0'): y for x, y in enumerate(months_list)}
        try:
            year, month, day = raw_date.split('-')
            date = '-'.join([months[str(month)], day, year])
        except:
            date = raw_date
        return date

    def _getFName(self):
        name = ('').join(self.obj_name.split())
        fname = name + '_' + str(self.hjd).split('.')[0] +\
            '_' + str(self.hjd).split('.')[1]
        return fname

    def _getWLARR(self):
        wli = self.head['CRVAL1']
        step = self.head['CDELT1']
        # wls = []
        # for x in range(len(self.data)):
        #     tmp = wli + (x * step)
        #     wls.append(tmp)
        wls = [wli + (x * step) for x, _ in enumerate(self.data)]
        return wls

    def getWLRange(self):
        """Return the range of wavelengths in file as a string."""
        ini = str(math.floor(self.wls[0]))
        fin = str(math.ceil(self.wls[-1]))
        ret = ini + " - " + fin
        return ret

    def hasHA(self):
        """return true if spectrum contains ha line."""
        wls = self._getWLARR()
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
        data = zip(self.wls, self.data)
        # wls = self.wls
        # d = self.data
        # for x in range(len(self.data)):
        #     tmp = [wls[x], d[x]]
        #     data.append(tmp)
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
