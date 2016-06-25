"""Module for testing Spectrum objects."""
import os
from .Spectrum import spectrum
from tests import file_paths

script_dir = os.path.dirname(__file__)
rel_path = 'files/'
abs_file_path = os.path.join(script_dir, rel_path)


def catch(func, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except Exception as e:
        print "EXCEPTION:"
        print '\t', e
        print '\t', ','.join(args)

specs = [catch(spectrum, x) for x in file_paths]
