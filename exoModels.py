#This module has the few models that I want to be able to use to fit exoplanet transits.
#They are defined in three levels of complexity, although the third one is complex enough I haven't actually done it yet.

import numpy as np
import limbDark
from scipy.integrate import quad

#The first is a box fit.
def boxDip(x,delta,l,centre,base=1):
    #we assume that base is 1, and that we go down to delta*base.
    start = centre - (l/2)
    end = centre + (l/2)
    
    if x <= start: return base
    if x >= end: return base
    #otherwise we must be in between
    return delta*base

def trapDip(x,delta,l,w,centre,base=1):
    p1 = centre - (l/2) - (w/2)
    p2 = centre - (l/2) + (w/2)
    p3 = centre + (l/2) - (w/2)
    p4 = centre + (l/2) + (w/2)
    
    if x <= p1: return base
    if x >= p4: return base
    if x < p2: 
        t = x-p1
        return base - t*base*(1-delta)/w
    if x <= p3: return delta*base
    if x < p4: 
        t = p4-x
        return base - t*base*(1-delta)/w
    return 0

def boxDipArr(times,delta,l,centre,base=1):
    results = np.zeros(len(times))
    for i,t in enumerate(times):
        results[i] = boxDip(t,delta,l,centre,base)
    return results

def trapDipArr(times,delta,l,w,centre,base=1):
    results = np.zeros(len(times))
    for i,t in enumerate(times):
        results[i] = trapDip(t,delta,l,w,centre,base)
    return results

#l = duration, w = ingress time which doesn't matter anymore, delta = rp/rs = p
#def FluxForTime(times,duration,tstart,p):
def limbDarkArr(times,delta,l,centre,base=1):
    return limbDark.FluxForTime(times,duration=l/2,tstart=centre-(l/4),p=np.sqrt(delta))*base

