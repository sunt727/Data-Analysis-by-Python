# -*- coding: utf-8 -*-
"""
Created on Sun Nov  5 16:09:37 2017

@author: WELG
"""

def mean(X):
    return sum(X)/len(X)
    
def variance(X):
    mean = sum(X)/len(X)
    tot = 0.0
    for x in X:
        tot += (x - mean)**2
    return tot/len(X)
    
def stdDev(X):
    return variance(X)**0.5
    
def CV(X):
    mean = sum(X)/len(X)
    try:
        return stdDev(X)/mean
    except ZeroDivisionError:
        return float('nan')
            
    
    
def makePlot(xVals, yVals, title, xLabel, yLabel, style, logX = False, logY = False):
     pylab.figure() 
     pylab.title(title) 
     pylab.xlabel(xLabel) 
     pylab.ylabel(yLabel) 
     pylab.plot(xVals, yVals, style) 
     if logX:
         pylab.semilogx() 
     if logY:
         pylab.semilogy()

def runTrial(numFlips): 
    numHeads = 0
    for n in range(numFlips):
        if random.choice(('H', 'T')) == 'H':
            numHeads += 1
    numTails = numFlips - numHeads
    return (numHeads, numTails)

def coinFlipPlot(minExp, maxExp, numTrials):
    """Assumes minExp, maxExp, numTrials ints >0; minExp < maxExp
    Plots summaries of results of numTrials trials of
    2**minExp to 2**maxExp coin flips"""
    ratiosMeans, diffsMeans, ratiosSDs, diffsSDs = [], [], [], []
    ratiosCVs, diffsCVs, xAxis = [], [], []
    for exp in range(minExp, maxExp + 1):
        xAxis.append(2**exp) 
    for numFlips in xAxis:
        ratios, diffs = [], []
        for t in range(numTrials):
            numHeads, numTails = runTrial(numFlips) 
            ratios.append(numHeads/numTails) 
            diffs.append(abs(numHeads - numTails))
        ratiosMeans.append(sum(ratios)/numTrials) 
        diffsMeans.append(sum(diffs)/numTrials) 
        ratiosSDs.append(stdDev(ratios)) 
        diffsSDs.append(stdDev(diffs))
        ratiosCVs.append(CV(ratios))
        diffsCVs.append(CV(diffs))
    numTrialsString = ' (' + str(numTrials) + ' Trials)' 
    title = 'Mean Heads/Tails Ratios' + numTrialsString 
    makePlot(xAxis, ratiosMeans, title, 'Number of flips',
             'Mean Heads/Tails', 'ko', logX = True)
    title = 'SD Heads/Tails Ratios' + numTrialsString 
    makePlot(xAxis, ratiosSDs, title, 'Number of Flips',
             'Standard Deviation', 'ko', logX = True, logY = True)
    
    title = 'Mean abs(#Heads - #Tails)' + numTrialsString 
    makePlot(xAxis, diffsMeans, title,
             'Number of Flips', 'Mean abs(#Heads - #Tails)', 'ko',
             logX = True, logY = True)
    title = 'SD abs(#Heads - #Tails)' + numTrialsString 
    makePlot(xAxis, diffsSDs, title,
             'Number of Flips', 'Standard Deviation', 'ko', 
             logX = True, logY = True)
    title = 'Coeff. of Var. abs(#Heads - #Tails)' + numTrialsString
    makePlot(xAxis, diffsCVs, title, 'Number of Flips',
             'Coeff. of Var.', 'ko', logX = True)
    title = 'Coeff. of Var. Heads/Tails Ratio' + numTrialsString
    makePlot(xAxis, ratiosCVs, title, 'Number of Flips',
             'Coeff. of Var.', 'ko', logX = True, logY = True)