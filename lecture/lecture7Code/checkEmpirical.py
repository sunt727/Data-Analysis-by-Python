# -*- coding: utf-8 -*-
"""
Created on Mon Nov  6 07:28:10 2017

@author: WELG
"""

def gaussian(x, mu, sigma):
    factor1 = (1.0/(sigma*((2*pylab.pi)**0.5)))
    factor2 = pylab.e**-(((x-mu)**2)/(2*sigma**2))
    return factor1*factor2
    
#xVals, yVals = [], []
#mu, sigma = 0, 1
#x = -6
#step = 0.05
#while x < 6:
#    xVals.append(x)
#    yVals.append(gaussian(x, mu, sigma))
#    x += step
#pylab.plot(xVals, yVals)
#pylab.title('Normal Distribution, mu = ' + str(mu)\
#            + ', sigma = ' + str(sigma))

import scipy.integrate

def checkEmpirical(numTrials):
    for t in range(numTrials):
        mu = random.randint(-100, 100)
        sigma = random.randint(1, 100)
        print('For mu =', mu, 'and sigma =', sigma)
        for numStd in (1, 1.96, 3):
            area = scipy.integrate.quad(gaussian,
                                        mu-numStd*sigma,
                                        mu+numStd*sigma,
                                        (mu, sigma))[0]
            print(' Fraction within', numStd, 
                  'std =', round(area, 4))