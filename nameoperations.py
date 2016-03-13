# import pyfits
import os
try:
    os.chdir('/home/oort/AstroML')
except:
    os.chdir('/home/extra/AstroML/')
# os.chdir('/home/seth/Desktop/AstroML/Programs/AstroML/')
# import SimbadSearch as ss




def split_str(string):
    known = {
        'ewlac': 'EW Lac',
        'betcmi': 'Bet CMi'
    }
    if string.lower() in known.keys():
        return known[string.lower()]
    if string[:2] == 'HD' and string[2] != ' ':
        return string[:2] + ' ' + string[2:]
    if ' ' in string or len(filter(lambda x: x.isupper(), string)) < 2:
        return string
    capindexes = []
    for i, x in enumerate(string):
        if x.isupper():
            capindexes.append(i)
    if capindexes[1] - capindexes[0] == 1:
        return string
    return string[:capindexes[1]] + ' ' + string[capindexes[1]:]


# def sort_directory(directorypath):
#     dirfiles = os.listdir(directorypath)
#     fitsfiles = [x for x in dirfiles if '.fits' in x]
#     dic = []
#     if directorypath[-1] != '/':
#         directorypath += '/'
#     for x in fitsfiles:
#         try:
#             fits = pyfits.open(directorypath + x)
#             name = fits[0].header['OBJNAME']
#             name = split_str(name)
#             ssname = ss.get_name(name)
#             dic.append([x, ssname])
#         except:
#             pass
#     alldirs = []
#     for x in dic:
#         try:
#             alldirs.append(''.join(x[1].split()))
#         except:
#             pass
#     # alldirs = [''.join(x[1].split()) for x in dic]
#     uniquedirs = []
#     for x in alldirs:
#         if x not in uniquedirs:
#             uniquedirs.append(x)
#     #Make the directories
#     for x in uniquedirs:
#         os.mkdir(x)
#     #put each file in it's respective directorypath
#     errors = []
#     for x in dic:
#         try:
#             split = x[0].split("/")
#             split.insert(-1, ''.join(x[1].split()))
#             newpath = '/'.join(split)
#             oldpath = x[0]
#             os.rename(oldpath, newpath)
#         except Exception as e:
#             errors.append(e)
#     # return errors

# if __name__ == "__main__":
#     print sort_directory('/home/oort/Downloads/Relevant/')
