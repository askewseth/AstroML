import tests
from Spectrum import spectrum

print len(tests.file_paths)
print 'DONE'


def catch(func, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except Exception as e:
        print "EXCEPTION:"
        print '\t', e
        print '\t', ','.join(args)

specs = [catch(spectrum, f) for f in tests.file_paths]
