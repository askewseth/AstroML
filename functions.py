import os
from Spectrum import spectrum
import SimbadSearch as ss


def getSpecs(path = '/home/oort/Downloads/AstroFilesRaw/AstroFiles/'):
    specs = []
    errors = []
    filenames = [path + x for x in os.listdir(path) if '.fits' in x]
    print 'length filenames: ', len(filenames)
    for x in filenames:
        try:
            specs.append(spectrum(x))
        except Exception as e:
            errors.append(e)
    print 'length specs: ', len(specs), '\tlength errors: ', len(errors)
    return specs, errors
