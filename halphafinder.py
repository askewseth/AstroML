import os, pyfits, math
import matplotlib.pyplot as plt
import numpy as np

class spectrum():
    def __init__(self, path):
        self.f = pyfits.open(path)
        self.head = self.f[0].header
        self.wlarr = self.getHeader()
        self.order, self.initialwl, self.step, self.end, self.last =self.stuff()
        self.initialwl.append(str(self.last))
        self.data = self.f[0].data
##        self.fullwl = self.getFullWL()
        self.date = self.getObsDate()
        
    def getHeader(self):
        wat2 = []  #Keys that contain w.l. info
        for key in self.head.keys():
            if 'WAT2' in key:
                wat2.append(key)
        spec = []  #values from wat2 keys
        for w in wat2:
            spec.append(self.head[w])
        specstring = ''.join(spec)
        specend = specstring.split('spec')
##        for x in specend:
##        pops = 0
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
        return final

    def stuff(self):
        order = []
        initalwl = []
        step = []
        end = []
        for o in self.wlarr:
            order.append(o[0])
            initalwl.append(o[5])
            step.append(o[6])
            end.append(o[7])
        newLast = ( float(end[-1]) * float(step[-1]) ) + float(initalwl[-1])
        return order, initalwl, step, end, newLast

    def findHA(self, ha = 6562, show = False):
        haord = -1
##        ha = 6562
        for x in range(len(self.initialwl)-1):
            if show == True:
                print self.initialwl[x][0:6], self.initialwl[x+1][0:6]
            start = int(math.ceil(float(self.initialwl[x][0:6])))
            end  = int(math.ceil(float(self.initialwl[x+1][0:6])))
            if ha in range(start, end):
                haord = x
            if x == len(self.initialwl)-2 and ha != -1:
                ha = x
        return haord

    def getObsDate(self):
        return self.head['DATE-OBS']
    
    def getFullWL(self):
        larray = []
        for y in xrange(len(self.initialwl)-1): #extra wl for end
            ls= []
            for x in xrange(int(self.end[y])):
                ls.append(float(self.initialwl[y]) + ( x * float(self.step[y]) ) )
            larray.append(ls)
        return larray

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
        plt.show()

    def plotOrd(self,i):
        plt.plot(self.fullwl[i], self.data[i])  
        title = str(i) + "th order of the spectrum from " + self.date
        plt.title(title)
        plt.xlabel('Wavelength (Angstroms)')
        plt.ylabel('Intensity')
        plt.show()
       
##    def convertCSV(self, order, path):
        
def getDir():
    os.chdir('/home/seth/Desktop/AstroML/Drive/Astro/BeSS/')
    files = [x for x in os.listdir(os.getcwd()) if '.fits' in x]
    ords = []
    for f in files:
        path = '/home/seth/Desktop/AstroML/Drive/Astro/BeSS/' + f
##        print path
        s= spectrum(path)
        ords.append(s.findHA())
    ans = zip(files, ords)
    for x in ans:
        print x

def dirFile(inputName, outputName):
    os.chdir('/home/seth/Desktop/AstroML/Drive/Astro/BeSS')
    files = [x for x in os.listdir(os.getcwd()) if '.fits' in x]
    ords = []
    for f in files:
        path = '/home/seth/Desktop/AstroML/Drive/Astro/BeSS/' + f
##            print path
        s= spectrum(path)
        ords.append(s.findHA())
    ans = zip(files, ords)
    inputnames = ''
    for x in range(len(ans)):
        tmp = files[x][0:-5]  + '[*,' + str(ords[x]) + '].fits' + '\n'
        inputnames = inputnames + tmp
    inFile = open(inputName, 'w')
    inFile.write(inputnames)
    print 'dir:  ', os.getcwd()
    inFile.close()

    outputnames = ''
    for x in range(len(ans)):
        tmp = files[x] + '.asc' + '\n'
        outputnames = outputnames + tmp
    outFile = open(outputName, 'w')
    outFile.write(outputnames)
    outFile.close()


def getFull(i):
    s = spectrum('/home/seth/Desktop/AstroML/AllFiles/19931201.fits')
    ls = []
    for x in xrange(int(s.end[i])):
        ls.append(float(s.initialwl[i]) + ( x * float(s.step[i]) ) )
    return ls



def listSpecDir(dirpath):
    os.chdir(dirpath)
    files = []
    for f in os.listdir(os.getcwd()):
        if '.fits' in f:
            files.append(dirpath + f)
##    return files
    files.pop(0)
    specs = []
    for f in files:
        print f
        temp = spectrum(f)
        print temp.step
        print ''
        specs.append(temp)
    return specs




s = spectrum('/home/seth/Desktop/AstroML/AllFiles/19931201.fits')

	
