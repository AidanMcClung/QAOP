#This module is designed to provide access to some general purpose functions that could be needed throughout the project
#Note that for now it will only contain things which I needed, and I don't have time to think of things that *may* be needed yet.
#Most of these will be things that are needed for plotting and stuff, that I have been copying and pasting at the start of 
# each new notebook.

import numpy as np

def readConfigFile(configPath='QAOP/'):
    try:
        with open(configPath+'config.txt','r') as config_file:
            codeFilePath = config_file.readline()
            dataFilePath = config_file.readline()
            #The lines are stored like dataFilePath='path/Demo/' but we dont want the info about what the line is
            codeFilePath = codeFilePath.split("'")[1]
            dataFilePath = dataFilePath.split("'")[1]
        return codeFilePath,dataFilePath,'no errors reading config file'
    except Exception as e:
        return '','', e


def getFilepath(number,folder='output/',ext='.fits'):
    dataFilePath = readConfigFile()[1]
    return dataFilePath + folder + "{:03d}".format(number) + ext


#Conversions
def hmstodays(h,m,s):
    return h/24 + m/(24*60) + s/(24*60*60)

def hmsToDeg(h,m,s):
    return 15*h + 15*m/60 + 15*s/3600

def dmsToDeg(d,m,s):
    return d + m/60 + s/3600

#astro functions
def diffMag(fluxV,fluxC):
    return -2.5 * np.log10(fluxV/fluxC)

def mag(flux):
    return -2.5 * np.log10(flux)


#iTelescope date conversions.
def getTimeFromDate(dateStr):
    #dateStr format: YYYY-MM-DD'T'HH:MM:SS.SSS
    split = dateStr.split(':')
    #print(split)
    hourStr = split[0][-2:]; minStr = split[1]; secStr = split[2]
    second = float(secStr); minute = float(minStr); hour = float(hourStr)
    #print(hour,minute,second)
    time = hour + (minute + (second/60))/60
    return time

#this is a useful method, idk where to put it
def genTimesFromTable(table,debug=False):
    times = np.zeros(len(table))
    for d,date in enumerate(table['time']):
        if debug: print(d,date)
        times[d] = getTimeFromDate(date)
    return times