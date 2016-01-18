from Spectrum import spectrum
import os

#get directory of files to be fixed
# path = raw_input('Path to the directory containing the files to be changed: \n')
#
# ans =  raw_input('you sure?')

path = '/home/oort/Downloads/BeSSSpectra/'

# if ans == 'n' or ans == 2:
#     path = raw_input('Path to the directory containing the files to be changed: \n')

os.chdir(path)
file_paths = [path + x for x in os.listdir(path) if '.fits' in x]

ans = raw_input('wanna check? y/n')
if ans == 'y':
    for x in file_paths:
        print x

specs = []
nots = []

for f in file_paths:
    try:
        specs.append(spectrum(f))
    except:
        nots.append(f)

print ''
print 'Number that worked: ', len(specs)
print 'Number that didnt work: ', len(nots)
print ''

same = 0
fnames = []
for s in specs:
    name = ('').join(s.obj_name.split())
    fname = name + '_' + str(s.hjd).split('.')[0] + '_' + str(s.hjd).split('.')[1]
    if fname in fnames:
        same+=1
    fnames.append(fname)
    print fname
print 'same' , same
print 'total', len(fname)
