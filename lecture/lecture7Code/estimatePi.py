import random

def throwNeedles(numNeedles):
    inCircle = 0
    for Needles in range(1, numNeedles + 1, 1):
        x = random.random()
        y = random.random()
        if (x*x + y*y)**0.5 <= 1.0:
            inCircle += 1
    return 4*(inCircle/float(numNeedles))

import pylab

def getEst(numNeedles, numTrials):
    estimates = []
    for t in range(numTrials):
        piGuess = throwNeedles(numNeedles)
        estimates.append(piGuess)
    sDev = pylab.std(estimates)
    curEst = sum(estimates)/len(estimates)
    print('Est. = ' + str(round(curEst,6)) +\
          ', Std. dev. = ' + str(round(sDev, 6))\
          + ', Needles = ' + str(numNeedles))
    return (curEst, sDev)

#def estPi(precision, numTrials):
#    numNeedles = 1000
#    sDev = precision
#    while sDev >= precision/1.96:
#        curEst, sDev = getEst(numNeedles,
#                              numTrials)
#        numNeedles *= 2
#    return curEst
#
#estPi(0.005, 100)

import pylab

#set line width
pylab.rcParams['lines.linewidth'] = 4
#set font size for titles 
pylab.rcParams['axes.titlesize'] = 20
#set font size for labels on axes
pylab.rcParams['axes.labelsize'] = 20
#set size of numbers on x-axis
pylab.rcParams['xtick.labelsize'] = 16
#set size of numbers on y-axis
pylab.rcParams['ytick.labelsize'] = 16
#set size of ticks on x-axis
pylab.rcParams['xtick.major.size'] = 7
#set size of ticks on y-axis
pylab.rcParams['ytick.major.size'] = 7
#set size of markers
pylab.rcParams['lines.markersize'] = 10
#set number of examples shown in legends
pylab.rcParams['legend.numpoints'] = 1


def estPiNew(precision, numTrials):
    numNeedles = 125
    sDev = precision
    trackSDev = []
    trackNeedles = []
    while sDev >= precision/1.96:
        curEst, sDev = getEst(numNeedles,
                              numTrials)
        trackSDev.append(sDev)
        trackNeedles.append(numNeedles)
        numNeedles *= 2
    pylab.plot(trackNeedles, trackSDev)
    pylab.semilogx()
    pylab.title('Variance in estimating pi')
    pylab.ylabel('Standard deviation')
    pylab.xlabel('Number of needles')
    return trackSDev

data = estPiNew(0.005, 100)