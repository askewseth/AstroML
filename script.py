import os
os.chdir('/home/seth/Desktop/AstroML/Programs/AstroML/')
from Spectrum import spectrum
path = '/home/seth/Desktop/AstroFiles/'
os.chdir(path)

directories = [x for x in os.listdir(os.getcwd()) if '.py' not in x]

def get_specs(star_dir):
    os.chdir(path + star_dir)
    specs = []
    nots = []
    file_names = [path + star_dir + '/' + x for x in os.listdir(os.getcwd())]
    for f in file_names:
        try:
            s = spectrum(f)
            specs.append(s)
            # print "s:", type(s)
        except:
            nots.append(f)

    # for x,s in enumerate(specs):
        # print x, type(s)
    return specs, nots

def get_stats(star_dir):
    os.chdir(path + star_dir)
    specs = []
    nots = []
    file_names = [path + star_dir + '/' + x for x in os.listdir(os.getcwd())]
    for f in file_names:
        try:
            specs.append(spectrum(f))
        except:
            nots.append(f)
    return len(specs), len(nots)

def get_all_stats():
    stats = []
    for x in directories:
        stat = get_stats(x)
        print x , ': ' , stat[0] ,',' , stat[1]

def do():
    specs, nots = get_specs('PsiPer')
    for x in nots:
        print x

def get_all_specs():
    all_specs = []
    for x in directories:
        specs, nots = get_specs(x)
        print type(specs)
        all_specs.append(specs)
    print 'len all specs: ', len(all_specs)
    for specarr in all_specs:
        for s in specarr:
            try:
                s.convertCSV()
            except Exception as e:
                print 'ERROR: ',e
get_all_specs()
