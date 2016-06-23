import os
import pyfits
import math
import csv
import matplotlib.pyplot as plt
import SimbadSearch as ss
import gc

class spectrum(object):
    """
    Creates spectrum object for local .fits file.

    Spectrum object initialized with file path.
    Contains get methods for
    """
    def __init__(self, path):
        """Initalized with path to .fits file."""
        self.path = path
        self.f = pyfits.open(path)
        self.head = self.f[0].header
        self.wlarr = self._getWLArr()
        self.data = self.f[0].data
        self.date = self.head['DATE-OBS']
        self.hjd = self.head['HJD']
        self.fullwl = self._getFullWL()
        # self._getWLArr()
        self.vhel = self.head['VHELIO']
        self.stararr = self._getStarArr()
        self.obj_name = self._get_obj_name()
        self.f.close()
        gc.collect()

    def __repr__(self):
        """Print Spectrum type along with star name and obs. date."""
        return "Local Spectrum: {0} , {1}".format(self.obj_name, self.date)

    def _get_obj_name(self):
        obj_name = (' ').join(self.head['OBJNAME'].split())
        ss_name = ss.get_name(obj_name)
        if ss_name is not None:
            return ss_name
        else:
            return obj_name

    def _getWLArr(self):
        wat2 = []
        for key in self.head.keys():
            if 'WAT2' in key:
                wat2.append(key)
        spec = []
        for w in wat2:
            spec.append(self.head[w])
        specstring = ''.join(spec)
        specend = specstring.split('spec')
        specend2 = []
        for x in range(len(specend)):
            if specend[x][0] in ['0', '1', '2', '3', '4', '5', '6', '7',
                                 '8', '9']:
                specend2.append(specend[x])
        final = []                    # Contains w.l. info as 2D array
        for x in range(len(specend2)):
            final.append(specend2[x].split(' '))
        for x in range(len(final)):
            if len(final[x][4]) > 1:
                final[x].insert(4, 0)
        # Corrections to be done to final
        # Correction for 6th order 2nd decimal
        if final[5][5].count('.') > 1:
            pos = final[5][5].rfind('.')
            tokeep = final[5][5][:pos]
            toapp = final[5][5][pos:]
            final[5][5] = tokeep
            final[5].insert(6, toapp)
        self.wltest = final
        order = []
        wli = []
        step = []
        end = []
        for o in final:
            order.append(int(float(o[0])))
            wli.append(float(o[5]))
            step.append(float(o[6]))
            end.append(float(o[7]))
        newLast = (1149 * step[-1]) + wli[-1]
        self.last = newLast
        nendnum = int(max(end))
        nend = [nendnum for x in range(len(order))]
        wlarr = [order, wli, step, nend]
        return wlarr

    def _getFullWL(self):
        larray = []
        for y in range(len(self.wlarr[0])):    # extra wl for end
            ls = []
            for x in range(self.wlarr[3][0]):
                ls.append(self.wlarr[1][y] + (x * self.wlarr[2][y]))
            larray.append(ls)
        # Correction for 6th order issues
        return larray

    def _getStarArr(self):
        d = self.date
        h = self.hjd
        v = self.vhel
        bint = None   # self.bintensity
        dint = None   # self.depintensity
        rint = None   # self.rintensity
        bwl = None    # self.bwavelength
        dwl = None    # self.depwavelength
        rwl = None    # self.rwavelength
        return [d, h, v, bint, dint, rint, bwl, dwl, rwl]

    def _findHA(self, ha=6562, show=False):
        """private."""
        haord = -1
        initialwl = [self.wlarr[1][x] for x in range(len(self.wlarr[1]))]
        initialwl.append(self.last)
        tmp = [str(x) for x in initialwl]
        initialwl = tmp
        for x in range(len(initialwl)-1):
            if show is True:
                print(initialwl[x][0:6], initialwl[x+1][0:6])
            start = int(math.ceil(float(initialwl[x][0:6])))
            end = int(math.ceil(float(initialwl[x+1][0:6])))
            if ha in range(start, end):
                haord = x
        return haord

    def plot(self, order=-1, ha=False):
        """Plot all orders of the spectrum file."""
        if order == -1:
            # print len(self.wlarr[1])
            for x in range(len(self.wlarr[1])):
                self.plotOrd(x)

    def plotOrd(self, i):
        """Plot a given order of the spectrum file."""
        plt.plot(self.fullwl[i], self.data[i])
        title = str(i) + "th order of the spectrum from " + self.date
        plt.title(title)
        plt.xlabel('Wavelength (Angstroms)')
        plt.ylabel('Intensity')
        plt.show()

    def plotHA(self):
        """Plot the H-Alpha line of the spectrum."""
        i = self._findHA()
        plt.plot(self.fullwl[i], self.data[i])
        halphalinex = [6562 for x in range(25000)]
        halphaliney = [x for x in range(25000)]
        plt.plot(halphalinex, halphaliney)
        title = str(i) + "th order of the spectrum from " + self.date
        plt.title(title)
        plt.xlabel('Wavelength (Angstroms)')
        plt.ylabel('Intensity')
        maxx = max(self.data[i]) + 100
        minn = min(self.data[i]) - 100
        plt.ylim(minn, maxx)
        plt.show()

    def convertCSV(self, order=-1, ha=True):
        """Converts to a CSV file."""
        if ha:
            self.convertCSV(order=self._findHA(), ha=False)
        csvdata = self.fullwl[order]
        sdata = self.data[order]
        newname = self.path[:-5] + '_ord' + str(order) + '_2' + '.csv'
        data = []
        for x in range(len(csvdata)):
            tmp = [csvdata[x], sdata[x]]
            data.append(tmp)
        with open(newname, 'w') as f:
            writer = csv.writer(f, delimiter=',')
            writer.writerows(data)

    def convertCSVNew(self, order=-1, ha=True):
        """Converts to a CSV file with the 'new' nameing convention."""
        if ha:
            self.convertCSVNew(order=self._findHA(), ha=False)
        csvdata = self.fullwl[order]
        sdata = self.data[order]
        name = ('').join(self.obj_name.split())
        fname = name + '_' + str(self.hjd).split('.')[0] +\
            '_' + str(self.hjd).split('.')[1]
        data = []
        print len(sdata), len(csvdata)
        for x in range(len(csvdata)):
            tmp = [csvdata[x], sdata[x]]
            data.append(tmp)
        with open(fname, 'w') as f:
            writer = csv.writer(f, delimiter=',')
            writer.writerows(data)

        # name = ('').join(self.obj_name.split())
        # fname = name + '_' + str(self.hjd).split('.')[0] +\
        #     '_' + str(self.hjd).split('.')[1]

        # """convert csv with new naming convention."""
        # newname = self.fname + '.csv'
        # data = []
        # wls = self.wls
        # d = self.data
        # for x in range(len(self.data)):
        #     tmp = [wls[x], d[x]]
        #     data.append(tmp)
        # filepath_arr = self.path.split('/')
        # dirpath = ('/').join(filepath_arr[:-1])
        # os.chdir(dirpath)
        # with open(newname, 'w') as f:
        #     writer = csv.writer(f, delimiter=',')
        #     writer.writerows(data)
