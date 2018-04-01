# -*- coding: utf-8 -*-
"""
Created on Sun Nov  5 18:44:16 2017

@author: WELG
"""
import math

def choose(n,k):
    return math.factorial(n)/(math.factorial(k)*math.factorial(n-k))

def binomial(n,k,p):
    return choose(n,k)*(p**k)*((1-p)**(n-k))
    
def plotBinomial(n, p, title, xLabel, yLabel):
    xVals = []
    yVals = []
    for i in range(n+1):
        xVals.append(i)
        yVals.append(binomial(n,i,p))
    pylab.figure() 
    pylab.title(title) 
    pylab.xlabel(xLabel) 
    pylab.ylabel(yLabel) 
    pylab.plot(xVals, yVals) 

#plotBinomial(10, 0.5, 'Binomial Distribution, p = 1/2', 'Hits', 'Frequency')

#plotBinomial(100, 0.5, 'Binomial Distribution, p = 1/2', 'Hits', 'Frequency')


def checkEmpiricalBinomial(n, p):
    mu = n*p
    sigma = (n * p * (1-p))**0.5
    #print('For mu =', mu, 'and sigma =', sigma)
    for numStd in (1.0, 1.96, 3.0):
        #print('range is from', round(mu-numStd*sigma), 
        #     'to', round(mu+numStd*sigma))

        tot = 0
        for i in range(int(round(mu-numStd*sigma)), int(round(mu+numStd*sigma))+ 1):
            tot += binomial(n, i, p)
        print(' Fraction within', numStd, 'std =', round(tot, 4)) 
        
for n in (50, 200, 1000):
    print('For n =', n)
    checkEmpiricalBinomial(n, 0.5)
        
import pylab
        
def plotDeaths(n,p):
    runningSum = 0.0
    xVals = []
    yVals = []
    for k in range(n+1):
        new = binomial(n, k, p)
        runningSum += new
        xVals.append(k)
        yVals.append(1- runningSum)
    pylab.figure() 
    pylab.title('Probability of at least k deaths') 
    pylab.xlabel('Number of deaths') 
    pylab.ylabel('Probability')
    pylab.plot(xVals, yVals)
    pylab.semilogy()
    
#plotDeaths(5, .04)


    
