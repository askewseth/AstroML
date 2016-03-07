import os
from Spectrum import spectrum
import SimbadSearch as ss
import math
from threading import Thread


def getSpecs(path = '/home/oort/Downloads/AstroFilesRaw/AstroFiles/', nots=False):
    specs = []
    errors = []
    nots_arr = []
    filenames = [path + x for x in os.listdir(path) if '.fits' in x]
    print 'length filenames: ', len(filenames)
    for i, x in enumerate(filenames):
        print i, '\r',
        try:
            specs.append(spectrum(x))
        except Exception as e:
            errors.append(e)
            nots_arr.append(x)
    print 'length specs: ', len(specs), '\tlength errors: ', len(errors)
    if nots is True:
        return nots_arr
    return specs, errors


def getCors(path='/home/oort/Downloads/AstroFilesRaw/AstroFiles/'):
    specs = []
    errors = []
    nots_arr = []
    dic = {}
    filenames = [path + x for x in os.listdir(path) if '.fits' in x]
    length = len(filenames)
    print 'length filenames: ', length
    for i, x in enumerate(filenames):
        try:
            print i, '\r',
            s = spectrum(x)
            specs.append(s)
            name = x.split('/')[-1]
            s.convertCSVNew()
            dic[name] = s.csv_name
        except Exception as e:
            errors.append(e)
            nots_arr.append(x)
    print 'length specs: ', len(specs), '\tlength errors: ', len(errors)
    return dic, errors


def getThread(path='/home/oort/Downloads/AstroFilesRaw/AstroFiles/'):
    names = []
    def convert(x):
        try:
            s = spectrum(x)
            s.convertCSVNew()
            names.append(s.csv_name)
            s.delete()
        except Exception as e:
            print e
    threads = []
    filenames = [path + x for x in os.listdir(path) if '.fits' in x]
    for i, x in enumerate(filenames):
        try:
            t = Thread(target=convert, args=(x,))
            threads.append(t)
            t.start()
        except:
            print 'ERROR'
    # print 'length specs: ', len(specs), '\tlength errors: ', len(errors)
    # return dic, errors
    print 'DONE!'
    return names
