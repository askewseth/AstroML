import os
import pyfits


def getNewName(filename):
    """private."""
    fi = pyfits.open(filename)
    head = fi[0].header
    date = head["DATE-OBS"][0:10]
    datearr = date.split('-')
    datefinal = ''.join(datearr)
    finalfilename = datefinal + '.fits'
#    print finalfilename
    return finalfilename


def fileArray(path):
    """private."""
    os.chdir(path)
    arr = []
    for f in os.listdir(os.getcwd()):
            if '.fits' in f:
                tmp = path + f
                arr.append(tmp)
    return arr


path = '/home/seth/Desktop/AstroML/Drive/Astro/BeSS/'
