import BessSpec as be
import LocalSpec as lo
import pyfits
import numpy
import os

def gettype(path):
    f = pyfits.open(path)
    if type(f[0].data[0]) == numpy.float32:
        return 'BeSS'
    else:
        return 'Local'

def spectrum(path):
    '''
    Universal spectrum 'class', figures out type of spectrum then
    creates the necessary object for it
    '''
    if gettype(path) == 'BeSS':
        return be.spectrum(path)
    if gettype(path) == 'Local':
        return lo.spectrum(path)

def getCSV(dirpath):
    if dirpath[-1] != '/':
        dirpath = dirpath + '/'
    os.chdir(dirpath)
    fs= []
    for f in os.listdir(os.getcwd()):
        if '.fits' in f:
            tmp = dirpath + f
            fs.append(tmp)
    specs = []
    for f in fs:
        specs.append(spectrum(f))
    for s in specs:
        s.convertCSV()
    csvfiles = []
    for f in os.listdir(os.getcwd()):
        if '.csv' in f:
            csvfiles.append(f)
    try:
        os.mkdir('CSVFiles')
    except:
        pass
    csvpath = dirpath + 'CSVFiles/'
    




def test():
    bepath = '/home/seth/Desktop/AstroML/Drive/Astro/BeSS/PsiPer_19780911_ama.fits'
    lopath = '/home/seth/Desktop/AstroML/AllFiles/19950206.fits'

    locs = []
    lodir = '/home/seth/Desktop/AstroML/AllFiles/'
    for f in os.listdir(lodir):
        if '.fits' in f:
            tmp = '/home/seth/Desktop/AstroML/AllFiles/' + f
            try:
                locs.append(spectrum(tmp))
            except:
                print 'LOCAL: ', f

    bes = []
    bedir = '/home/seth/Desktop/AstroML/Drive/Astro/BeSS/'
    for f in os.listdir(bedir):
        if '.fits' in f:
            tmp = bedir + f
            try:
                bes.append(spectrum(tmp))
            except:
                print 'BESS: ', f


