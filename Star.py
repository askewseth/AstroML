from LocalSpec import spectrum
import os

class star():

    def __init__(self, name):
        self.name = name
        self.specarr = []
        self.wlarr = []

    def setRADec(self, ra, dec):
        self.ra = ra
        self.dec = dec

    def addSpec(self, spec):
        date = spec.hjd
        data = spec.fullwl[spec.findHA()]
        self.wlarr.append([date, data])
        self.specarr.append(spec)
    
    def dispSpecArr(self):
        for s in self.specarr:
            print(join(s.stararr, ' '))
            
    def getAnalysisData(self):
        ''' returns list of lists, first of hjd datesx then of b.i./r.i.'''
        hjd = []
        intrat = []
        for spec in self.specarr:
            hjd.append(spec.stararr[1])
            intrat.append(spec.stararr[3]/spec.stararr[5])
        zipped = [ [x,y] for x,y in zip(hjd,intrat)]
        return zipped
        

        
def join(li, dividor):
    s = ''
    for x in li:
        s = s + str(x) + dividor
    return s
        
def getPsiper():
    dirpath = '/home/seth/Desktop/AstroML/AllFiles/'
    files = []
    for f in os.listdir(dirpath):
        if '.fits' in f:
            files.append(dirpath + f)
    specs = []
    for f in files:
        specs.append(spectrum(f))
    s = specs[1]
    psiper = star('Psi Persei')
    for s in specs:
        psiper.addSpec(s)

    return psiper

psiper = getPsiper()
