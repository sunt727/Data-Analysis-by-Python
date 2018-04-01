#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 11 09:56:05 2017

@author: johnguttag
"""

# -*- coding: utf-8 -*-
"""
Created on Wed May 11 14:29:43 2016

@author: johnguttag
"""

import random, pylab

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

random.seed(0)

#Initialize constants
numCasesPerYear = 36000
numYears = 3
stateSize = 10000
communitySize = 10
numCommunities = stateSize//communitySize

def findProb(numTrials):
    numGreater = 0
    for t in range(numTrials):
        locs = [0]*numCommunities
        for i in range(numYears*numCasesPerYear):
            locs[random.choice(range(numCommunities))] += 1
        if locs[111] >= 143:
            numGreater += 1
    prob = round(numGreater/numTrials, 4)
    print('Est. prob. of region 111 having >= 143 cases =',
          prob)
    
#findProb(100)

def findProb1(numTrials):
    anyRegion = 0
    for t in range(numTrials):
        locs = [0]*numCommunities
        for i in range(numYears*numCasesPerYear):
            locs[random.choice(range(numCommunities))] += 1
        if max(locs) >= 143:
            anyRegion += 1
    prob = round(anyRegion/numTrials, 4)
    print('Est. prob. of some region having >= 143 cases =',
          prob)
    
#findProb1(100)
