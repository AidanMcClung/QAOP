import os
import numpy as np
from astropy.table import Table
from astropy.io import fits
from astropy.wcs import WCS
from astropy.coordinates import SkyCoord
from photutils.detection import DAOStarFinder
from astropy.stats import sigma_clipped_stats

from photutils.detection import find_peaks
from photutils.profiles import RadialProfile
from photutils.centroids import centroid_quadratic

class starIDInstance:
    
    def __init__(self,target_coord,working_dir='ident'):
        self.target_coord = target_coord
        self.target_ra = target_coord[0]
        self.target_dec = target_coord[1]
        self.target_sc = 
        
        if not os.listdir().count(working_dir): os.mkdir(working_dir)
        self.working_dir = working_dir
        
    def createNameloc(self):
        self.namelocTab = Table(names=['name','RA','DEC'])
        self.namelocTab.add_row({'name':'Target','RA':self.target_ra,'DEC':self.target_dec})
        return self.namelocTab
    
    def openImage(self,imgpath):
        with fits.open(imgpath) as hdul:
            self.image = hdul[0].data
            self.wcs = WCS(hdul[0].header)
    
    def findTargetPeak(self):
        
        