import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad

''' 
This module implements the limb darkening model of exoplanets transits 
for use in a project by students taking PHYS 315 at Queen's University. 

The functions are implementations of that described by Mandel & Agol (ApJ 580, 2001).
    https://iopscience.iop.org/article/10.1086/345520/pdf

The model takes 4 parameters to characterize it, determined by the star.
Values can be found at:
https://vizier.cds.unistra.fr/viz-bin/VizieR-3?-source=J/A%2bA/363/1081/atlasco

(For PHYS 315 students are using the V band)
'''


#For log[M/H]= -1.0, v = 2.0 kms, log g = 4.5
a1, a2, a3, a4 = 0.2621,0.6838,-0.0214,-0.1504 #Teff = 5250K
aa1, aa2, aa3, aa4 = 0.1551,1.2391,-0.8769,0.2287 #Teff = 5500K
a0 = 1 - a1 - a2 - a3 -a4
aa0 = 1 - aa1 - aa2 - aa3 - aa4

c = {'0':a0,'1':a1,'2':a2,'3':a3,'4':a4}
cc = {'0':aa0,'1':aa1,'2':aa2,'3':aa3,'4':aa4}

def omega(C=c):
    O = 0
    for n in [0,1,2,3,4]:
        O += C[str(n)]/(n+4)
    return O#thats a capital O not zero\

def a(z,p=0.1):
    return (z-p)**2

def b(z,p=0.1):
    return (z+p)**2

# P = Rp/Rs = sqrt delF
def kap1(z,p=0.1):
    k1 = np.arccos( (1-(p**2)+(z**2)) / (2*z) )
    return k1

def kap0(z,p=0.1):
    k0 = np.arccos( ((p**2)+(z**2)-1) / (2*z*p) )
    return k0

def mu(r):
    #mu = cos(theta)
    return (1-(r**2))**(1/2)

def transFlux(z,p=0.1,C=c):
    if z > 1+p:
        return 1
    if z < 1-p:
        def Istar(z):
            def I(r,C):
                result = 1
                for k in [1,2,3,4]:
                    term = 1 - (mu(r)**(k/2))
                    result = result - C[str(k)]*term
                return result
            def integrand(r,C):
                return I(r,C=C)*2*r
            return (1/(4*z*p))*( quad(integrand,z-p,z+p,args=(C))[0])
        return 1 - ( (p**2) * Istar(z) / (4*omega()) )
    else:
        def Istar(z):
            def I(r,C):
                result = 1
                for k in [1,2,3,4]:
                    term = 1 - (mu(r)**(k/2))
                    result = result - C[str(k)]*term
                return result
            def integrand(r,C):
                return I(r,C=C)*2*r
            return (quad(integrand,z-p,1,args=(C))[0])/(1-a(z=z,p=p))
        return 1 - (Istar(z)/(4*np.pi*omega()))*(((p**2)*np.arccos((z-1)/p) - (z-1)*np.sqrt((p**2)-((z-1)**2))))
    
def transFluxArr(zarr,p=0.1,C=c):
    result = []
    for i in range(len(zarr)):
        result.append(transFlux(zarr[i],p=p,C=C))
    return result

def twohalftransit(z,p=0.1,C=c):
    #this function will expect to get a z that ranges from a negative value to a positive one
    neg = np.take(z,np.where(z<0))[0]
    pos = np.take(z,np.where(z>0))[0]
    leftflux = transFluxArr(-neg,p=p,C=C)
    rightflux = transFluxArr(pos,p=p,C=C)
    midflux = []
    while (len(leftflux)+len(rightflux)+len(midflux) != len(z)):
        midflux.append((leftflux[-1]+rightflux[0])/2)
    return np.hstack((leftflux,midflux,rightflux))

def timesToProgress(times,duration,tstart=0):
    timesdelta = times - tstart
    progress = timesdelta/duration
    return progress
def ProgToTime(progress,duration,tstart=0):
    timesdelta = progress*duration
    times = timesdelta + tstart
    return times

def getTransitForTime(times,duration,tstart=0,p=0.1,C=c,both=False):
    progress = timesToProgress(times,duration,tstart=tstart) #progress is like z
    if both:
        return (ProgToTime(progress,duration, tstart=tstart),getTransitForProg(progress,p=p,C=C))
    return getTransitForProg(progress,p=p,C=C)
    
def getTransitForProg(prog,p=0.1,C=c):
    flux = twohalftransit(prog,p=p,C=C)
    return flux

def FluxForTime(times,duration,tstart,p):
    return getTransitForTime(times,duration,tstart=tstart,p=p)