import os
from Spectrum import spectrum
import SimbadSearch as ss
import math
from threading import Thread


def getSpecs(path=None, nots=False):
    if path is None:
        try:
            path = '/home/oort/Downloads/AstroFilesRaw/AstroFiles/'
            os.chdir(path)
        except:
            path = '/home/extra/Desktop/AllHA/t1/'
    specs = []
    errors = []
    nots_arr = []
    filenames = [path + x for x in os.listdir(path) if '.fits' in x]
    print 'length filenames: ', len(filenames)
    for i, x in enumerate(filenames):
        print i, '\r',
        try:
            s = spectrum(x)
            specs.append(s)
            s.close()
        except Exception as e:
            errors.append(e)
            nots_arr.append(x)
    print '\nlength specs: ', len(specs), '\tlength errors: ', len(errors)
    if nots is True:
        return nots_arr
    return specs, errors


def getCors(path=None, nots=False):
    if path is None:
        try:
            path = '/home/oort/Downloads/AstroFilesRaw/AstroFiles/'
            os.chdir(path)
        except:
            # path = '/home/extra/AstroFiles/'
            path = '/home/extra/Desktop/AllHA/t12/'
    specs = []
    errors = []
    nots_arr = []
    dic = {}
    print path
    filenames = [path + x for x in os.listdir(path) if '.fits' in x]
    length = len(filenames)
    finished = 0
    print 'length filenames: ', length
    csvfiles = [x for x in os.listdir(path) if '.csv' in x]
    print 'Number of CSV files in directory originally: ', len(csvfiles)
    for i, x in enumerate(filenames):
        percent_done = float(i)/length * 100
        print 'File Num: {1} \t % Done: {0:.3}'.format(percent_done, i), '\r',
        try:
            # print i
            s = spectrum(x)
            specs.append(s)
            name = x.split('/')[-1]
            s.convertCSVNew()
            dic[name] = s.csv_name
            s.close()
            # print 'closed'
            finished += 1
        except Exception as e:
            errors.append([i, e])
            nots_arr.append(x)
    print '\nlength specs: ', len(specs), '\tlength finished: ', finished, \
        '\tlength errors: ', len(errors)
    if nots:
        return nots_arr
    print ''
    csvfiles = [x for x in os.listdir(path) if '.csv' in x]
    print 'Number of CSV files in directory: ', len(csvfiles)
    return dic, errors


# def getThread(path=None):
#     if path is None:
#         try:
#             path = '/home/oort/Downloads/AstroFilesRaw/AstroFiles/'
#             os.chdir(path)
#         except:
#             path = '/home/extra/AstroFiles/'
#     names = []
#     def convert(x):
#         try:
#             s = spectrum(x)
#             s.convertCSVNew()
#             names.append(s.csv_name)
#             s.close()
#         except Exception as e:
#             print e
#     threads = []
#     filenames = [path + x for x in os.listdir(path) if '.fits' in x]
#     for i, x in enumerate(filenames):
#         try:
#             t = Thread(target=convert, args=(x,))
#             threads.append(t)
#             t.start()
#         except:
#             print 'ERROR'
#     # print 'length specs: ', len(specs), '\tlength errors: ', len(errors)
#     # return dic, errors
#     print 'DONE!'
#     return names
