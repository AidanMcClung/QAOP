#import os
import numpy as np
# from astropy.table import Table
# from astropy.io import fits
# from astropy.wcs import WCS
# from astropy.coordinates import SkyCoord
# from photutils.detection import DAOStarFinder
# from astropy.stats import sigma_clipped_stats

# from photutils.detection import find_peaks
# from photutils.profiles import RadialProfile
# from photutils.centroids import centroid_quadratic


#enable use of QAOP config file
#with open('config.txt','r') as config_file:
#    codeFilePath = config_file.readline()
#    dataFilePath = config_file.readline()
try:
    from QAOP_utils import readConfigFile
except ModuleNotFoundError:
    from QAOP.QAOP_utils import readConfigFile
codeFilePath,dataFilePath,errormsg = readConfigFile()


#Autonamer section ---------
class autonamer:
    def __init__(self,fmt=chr,startindex=64,capacity=26):
        self.counter = 0
        self.start = startindex
        self.outfmt = fmt
        self.capacity = capacity
    
    def nextName(self):
        self.counter += 1
        return self.name(self.counter)
    
    def name(self,nameInt):
        lastDigit = 0 + nameInt #we do 0 + a number to verify we have a new object that's a copy
        firstDigit = 0
        while lastDigit > self.capacity:
            firstDigit += 1
            lastDigit -= self.capacity
            #print("roll",firstDigit,lastDigit)
        if firstDigit > self.capacity: raise IndexError("Two Digit Naming Capacity Limit ("+str((self.capacity+1)*self.capacity) +") Exceeded: " + str(nameInt))
        name = 's'
        if firstDigit > 0:
            name = name + str(self.outfmt(self.start + firstDigit))
        name = name + str(self.outfmt(self.start + lastDigit))
        return name

def charnamer():
    return autonamer(fmt=chr,startindex=64,capacity=26)
def intnamer():
    return autonamer(fmt=int,startindex=-1,capacity=10)

#end autonamer section -------


# class starIDInstance:
    
#     def __init__(self,target_coord,working_dir='ident'):
#         self.target_coord = target_coord
#         self.target_ra = target_coord[0]
#         self.target_dec = target_coord[1]
#         self.target_sc = "potato"
        
#         if not os.listdir().count(working_dir): os.mkdir(working_dir)
#         self.working_dir = working_dir
        
#     def createNameloc(self):
#         self.namelocTab = Table(names=['name','RA','DEC'])
#         self.namelocTab.add_row({'name':'Target','RA':self.target_ra,'DEC':self.target_dec})
#         return self.namelocTab
    
#     def openImage(self,imgpath):
#         with fits.open(imgpath) as hdul:
#             self.image = hdul[0].data
#             self.wcs = WCS(hdul[0].header)
    
#     def findTargetPeak(self):
        
        