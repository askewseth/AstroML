import os
import pyfits
import math
import csv
import matplotlib.pyplot as plt
import SimbadSearch as ss
import gc
import nameoperations as no

class spectrum():
    """Creates spectrum object for local .fits file.

    Spectrum object initialized with file path.
    Contains get methods for
    """
    def __init__(self, path):
        """Initalized with path to .fits file."""
        self.path = path
        self.filepath = ("/").join([x for x in path.split('/')[:-1]]) + '/'
        self.f = pyfits.open(path)
        self.head = self.f[0].header
        self.wlarr = self.getWLArr()
        self.data = self.f[0].data
        self.date = self.head['DATE-OBS']
        self.hjd = self.head['HJD']
        self.fullwl = self.getFullWL()
        self.getWLArr()
        self.vhel = self.head['VHELIO']
        self.stararr = self.getStarArr()
        self.obj_name = self.get_obj_name()
        self.csv_name = ('').join(self.obj_name.split())
        # self.obj_name = (' ').join(self.head['OBJNAME'].split()).lower()
        # self.f.close()
        # self.delete()
        # gc.collect()

    def close(self):
        """Delete all refrences and close file."""
        del self.head
        del self.wlarr
        del self.data
        del self.date
        del self.hjd
        del self.fullwl
        del self.vhel
        del self.stararr
        del self.obj_name
        self.f.close()
        gc.collect()


    def get_obj_name(self):
        obj_name = (' ').join(self.head['OBJNAME'].split())
        ss_name = ss.get_name(no.split_str(obj_name))
        if ss_name != None:
            return ss_name
        else:
            return obj_name

    def getWLArr_final(self):
        """Break apart header into pieces with info about wavelength."""
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
        return final

    def correctFinal(self):
        """Make necessary corrections ot getWLArr_final."""
        final = self.getWLArr_final()
        for x in final:
            if x[5].count('.') > 1:
                pos = x[5].rfind('.')
                tokeep = x[5][:pos]
                toapp = x[5][pos:]
                x[5] = tokeep
                x.insert(6, toapp)
                # print 'corrected'
            # if first element contains '='
            if '=' in x[0]:
                x[0] = x[0].split('=')[0]


        return final

    def getWLArr(self):
        """Set the wavelengths for the file given final from correctFinal."""
        final = self.correctFinal()
        order = []
        wli = []
        step = []
        end = []
        for o in final:
            try:
                order.append(int(float(o[0])))
                wli.append(float(o[5]))
                step.append(float(o[6]))
                end.append(float(o[7]))
            except Exception as e:
                print 'ERROR: ', e
                print o
        newLast = (1149 * step[-1]) + wli[-1]
        self.last = newLast
        nendnum = int(max(end))
        # nend = [nendnum for x in range(len(order))]
        # Should always be 1374
        nend = [1374 for x in range(len(order))]
        wlarr = [order, wli, step, nend]
        return wlarr

    def getFullWL(self):
        """private."""
        larray = []
        for y in range(len(self.wlarr[0])):    # extra wl for end
            ls = []
            for x in range(self.wlarr[3][0]):
                ls.append(self.wlarr[1][y] + (x * self.wlarr[2][y]))
            larray.append(ls)
        # Correction for 6th order issues
        return larray

# def getTest(self):
#     """private."""
#     larray = []
#     for y in range(len(self.wlarr[0])):    # extra wl for end
#         ls = []
#         for x in range(self.wlarr[3][0]):
#             ls.append(self.wlarr[1][y] + (x * self.wlarr[2][y]))
#         larray.append(ls)
#     # Correction for 6th order issues
#     return return

    def getStarArr(self):
        """private."""
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

    def findHA(self, ha=6562, show=False):
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

    def plot(self, order=-1, ha=True):
        """private."""
        if ha:
            self.plotHA()
            return
        if order == -1:
            # print len(self.wlarr[1])
            for x in range(len(self.wlarr[1])):
                self.plotOrd(x)
            return


    def plotOrd(self, i):
        """private for plot."""
        plt.plot(self.fullwl[i], self.data[i])
        title = str(i) + "th order of the spectrum from " + self.date
        plt.title(title)
        plt.xlabel('Wavelength (Angstroms)')
        plt.ylabel('Intensity')
        plt.show()

    def plotHA(self):
        """private for plot."""
        i = self.findHA()
        try:
            assert len(self.fullwl[i]) == len(self.data[i])
        except AssertionError:
            print '\ndate: ', self.hjd
            print 'wl: ', len(self.fullwl[i]), 'data', len(self.data[i])
        plt.plot(self.fullwl[i], self.data[i])
        halphalinex = [6562 for x in range(max(self.data[i]))]
        halphaliney = [x for x in range(max(self.data[i]))]
        plt.plot(halphalinex, halphaliney)
        title = str(i) + "th order of the spectrum from " + self.date
        title = ''.join([self.obj_name, '\n', title])
        plt.title(title)
        plt.xlabel('Wavelength (Angstroms)')
        plt.ylabel('Intensity')
        maxx = max(self.data[i]) + 100
        minn = min(self.data[i]) - 100
        plt.ylim(minn, maxx)
        plt.show()

def saveplot(self, ret=False):
    """private for plot."""
    i = self.findHA()
    try:
        assert len(self.fullwl[i]) == len(self.data[i])
    except AssertionError:
        print '\ndate: ', self.hjd
        print 'wl: ', len(self.fullwl[i]), 'data', len(self.data[i])
    plt.plot(self.fullwl[i], self.data[i])
    halphalinex = [6562 for x in range(max(self.data[i]))]
    halphaliney = [x for x in range(max(self.data[i]))]
    plt.plot(halphalinex, halphaliney)
    title = str(i) + "th order of the spectrum from " + self.date
    title = ''.join([self.obj_name, '\n', title])
    plt.title(title)
    plt.xlabel('Wavelength (Angstroms)')
    plt.ylabel('Intensity')
    maxx = max(self.data[i]) + 100
    minn = min(self.data[i]) - 100
    plt.ylim(minn, maxx)
    name = self.obj_name + '_' + str(self.hjd).split('.')[0] +\
        '_' + str(self.hjd).split('.')[1] + '.png'
    plt.saveas(name)
    if ret:
        return name
    return


    def convertCSV(self, order=-1, ha=True):
        """Converts."""
        if ha:
            self.convertCSV(order=self.findHA(), ha=False)
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

    def convertCSVNew(self, order=None, ha=True):
            """Converts."""
            if ha:
                self.convertCSVNew(order=self.findHA(), ha=False)
                return
            csvdata = self.fullwl[order]
            sdata = self.data[order]
            name = self.csv_name
            fname = name + '_' + str(self.hjd).split('.')[0] +\
                '_' + str(self.hjd).split('.')[1] + '.csv'
            # print fname
            self.csv_name = fname
            data = []
            # print len(sdata) == len(csvdata), '\t', len(sdata), '\t', len(csvdata)
            for x in range(len(csvdata)):
                tmp = [csvdata[x], sdata[x]]
                data.append(tmp)
            with open(self.filepath + fname, 'w') as f:
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


def test(dirpath='/home/seth/Desktop/AstroML/AllFiles/'):
    """private."""
    files = []
    for f in os.listdir(dirpath):
        if '.fits' in f:
            files.append(dirpath + f)
    specs = []
    for f in sorted(files):
        specs.append(spectrum(f))
    return specs


def main():
    """private."""
    specs = test()
    for s in specs:
        try:
            s.plotHA()
        except:
            print(s.date)


def do():
    """private."""
    os.chdir('/home/seth/Desktop/AstroML/Drive/Astro/TCO/')
    names = []
    for f in os.listdir(os.getcwd()):
        if '.fits' in f:
            tmp = '/home/seth/Desktop/AstroML/Drive/Astro/TCO/' + f
            names.append(tmp)
    specs = []
    for n in names:
        try:
            tmp = spectrum(n)
            specs.append(tmp)
            print 'no prob'
        except:
            print 'ERROR: ', n
    return specs

# specs = test()



def toTest():
    path = '/home/oort/Downloads/AstroFilesRaw/AstroFiles/'
    filenames = [path + x for x in os.listdir(path) if '.fits' in x]
    print "the length of filenames: ", len(filenames)
    specs = []
    nots = []
    errors = []
    # print filenames[:10]
    for f in filenames:
        try:
            specs.append(spectrum(f))
        except Exception as e:
            nots.append(f)
            errors.append(e)
    print "Specs length: ", len(specs)
    print "Nots length: ", len(nots)
    print "Errors: \n"
    print errors


if __name__ == "__main__":
    toTest()
