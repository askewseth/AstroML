import os
import pyfits
os.chdir('/home/seth/Desktop/AstroML/Programs/AstroML/')
import SimbadSearch as ss


def get_files_dic(path='/home/seth/Desktop/Entire_BeSS/'):
    files = [path + x for x in os.listdir(path) if '.fits' in x]
    dic = {}
    for f in files:
        try:
            fits = pyfits.open(f)
            name = fits[0].header['OBJNAME']
            sim_name = ss.get_name(name)
            fits.close()
            dic[f] = [f, sim_name]
        except:
            pass
    return dic

def get_unique(dic):
    values = dic.values()
    names = [x[1] for x in values]
    unique_names = []
    for x in names:
        if x not in unique_names:
            unique_names.append(x)
    return unique_names


def make_dirs(unique_names):
    os.chdir('/home/seth/Desktop/Entire_BeSS/dirs/')
    stripped = map(lambda x: ('').join(x.strip(' ')), unique_names)
    for x in stripped:
        os.mkdir(x)
    print 'DONE'


if __name__ == '__main__':
    dic = get_files_dic()
    unique_names = get_unique(dic)
    make_dirs(unique_names)
