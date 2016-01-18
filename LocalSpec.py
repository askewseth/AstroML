import os
import pyfits
import math
import csv
import matplotlib.pyplot as plt
import numpy as np

class spectrum():
    """
    Spectrum object initialized with file path.
    Contains get methods for 
    """
    def __init__(self, path):
        self.path = path
        self.f = pyfits.open(path)
        self.head = self.f[0].header
        self.wlarr = self.getWLArr()
        self.data = self.f[0].data
        self.date = self.head['DATE-OBS']
        self.hjd = self.head['HJD']
        self.fullwl = self.getFullWL()
        self.getWLArr()
        self.vhel = self.head['VHELIO']
        self.stararr = self.getStarArr()
        
    def getWLArr(self):
        wat2 = []
        for key in self.head.keys():
            if 'WAT2' in key:
                wat2.append(key)
        spec = []
        for w in wat2:
            spec.append(self.head[w])
        specstring = ''.join(spec)
        specend = specstring.split('spec')
        specend2 = []
        for x in range(len(specend)):
            if specend[x][0] in ['0','1','2','3','4','5', '6', '7'
                                 ,'8', '9']:  
                specend2.append(specend[x])
        final = [] #Contains w.l. info as 2D array
        for x in range(len(specend2)):
            final.append(specend2[x].split(' '))
        for x in range(len(final)):
            if len(final[x][4])>1:
            	final[x].insert(4,0)
        #Corrections to be done to final
        #Correction for 6th order 2nd decimal
        if final[5][5].count('.') > 1:
            pos = final[5][5].rfind('.')
            tokeep = final[5][5][:pos]
            toapp = final[5][5][pos:]
            final[5][5] = tokeep
            final[5].insert(6, toapp)        	
        self.wltest = final
        order = []
        wli = []
        step = []
        end = []
##        return final
        for o in final:
            order.append(int(float(o[0])))
            wli.append(float(o[5]))
            step.append(float(o[6]))
            end.append(float(o[7]))
        newLast = ( 1149 * step[-1] ) + wli[-1]
        self.last = newLast
        nendnum = int(max(end))
        nend = [nendnum for x in range(len(order))]
        wlarr = [order, wli, step, nend]
        return wlarr

    def getFullWL(self):
        larray = []
        for y in range(len(self.wlarr[0])): #extra wl for end
            ls= []
            for x in range(self.wlarr[3][0]):
                ls.append(self.wlarr[1][y] + ( x * self.wlarr[2][y] ) )
            larray.append(ls)
        #Correction for 6th order issues
        
        return larray

    def getStarArr(self):
        d = self.date
        h = self.hjd
        v = self.vhel
        bint = None   #self.bintensity
        dint = None   #self.depintensity
        rint = None   #self.rintensity
        bwl = None    #self.bwavelength
        dwl = None    #self.depwavelength
        rwl = None    #self.rwavelength
        return [d,h,v,bint,dint,rint,bwl,dwl,rwl]
    

    def findHA(self, ha = 6562, show = False):
        haord = -1
        initialwl =[self.wlarr[1][x] for x in range(len(self.wlarr[1]))]
        initialwl.append(self.last)
        tmp = [str(x) for x in initialwl]
        initialwl = tmp
        for x in range(len(initialwl)-1):
            if show == True:
                print(initialwl[x][0:6], initialwl[x+1][0:6])
            start = int(math.ceil(float(initialwl[x][0:6])))
            end  = int(math.ceil(float(initialwl[x+1][0:6])))
            if ha in range(start, end):
                haord = x
        return haord

    def plot(self, order = -1, ha = False):
        if order == -1:
##            print len(self.wlarr[1])
            for x in range(len(self.wlarr[1])):
                self.plotOrd(x)
    
    def plotOrd(self, i):
        plt.plot(self.fullwl[i], self.data[i])  
        title = str(i) + "th order of the spectrum from " + self.date
        plt.title(title)
        plt.xlabel('Wavelength (Angstroms)')
        plt.ylabel('Intensity')
        plt.show()
        
    def plotHA(self):
        i = self.findHA()
        plt.plot(self.fullwl[i], self.data[i])
        halphalinex = [6562 for x in range(25000)]
        halphaliney = [x for x in range(25000)]
        plt.plot(halphalinex, halphaliney)
        title = str(i) + "th order of the spectrum from " + self.date
        plt.title(title)
        plt.xlabel('Wavelength (Angstroms)')
        plt.ylabel('Intensity')
        maxx = max(self.data[i]) + 100
        minn = min(self.data[i])- 100
        plt.ylim(minn, maxx)
        plt.show()

    def convertCSV(self, order = -1, ha = True ):
        if ha:
            self.convertCSV(order = self.findHA(), ha = False)
        csvdata = self.fullwl[order]
        sdata = self.data[order]
        newname = self.path[:-5] + '_ord' + str(order)+ '_2' + '.csv'
        data = []
        for x in range(len(csvdata)):
            tmp = [ csvdata[x] , sdata[x] ]
            data.append(tmp)
        with open(newname, 'w') as f:
            writer = csv.writer(f, delimiter=',')
            writer.writerows(data)
            
def test(dirpath = '/home/seth/Desktop/AstroML/AllFiles/'):    
    files = []
    for f in os.listdir(dirpath):
        if '.fits' in f:
            files.append(dirpath + f)
    specs = []
    for f in sorted(files):
        specs.append(spectrum(f))
    return specs


def main():
    specs = test()
    for s in specs:
        try:
            s.plotHA()
        except Exception, e:
            print(s.date)

def do():
    os.chdir('/home/seth/Desktop/AstroML/Drive/Astro/TCO/')
    names = []
    for f in os.listdir(os.getcwd()):
        if '.fits' in f:
            tmp = '/home/seth/Desktop/AstroML/Drive/Astro/TCO/' + f
            names.append(tmp)
    specs = []
    for n in names:
        try:
            tmp = spectrum(n)
            specs.append(tmp)
            print 'no prob'
        except Exception, e:
            print 'ERROR: ', n
    return specs


##specs = test()





        
