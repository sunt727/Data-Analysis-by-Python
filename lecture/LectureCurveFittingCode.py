# -*- coding: utf-8 -*-
"""
Created on Mon Sep 19 11:45:20 2016

@author: johnguttag, ericgrimson
"""

import pylab, numpy

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

def getData(fileName):
    dataFile = open(fileName, 'r')
    distances = []
    masses = []
    dataFile.readline() #discard header
    for line in dataFile:
        d, m = line.split()
        distances.append(float(d))
        masses.append(float(m))
    dataFile.close()
    return (masses, distances)
    
def labelPlot():
    pylab.title('Measured Displacement of Spring')
    pylab.xlabel('|Force| (Newtons)')
    pylab.ylabel('Distance (meters)')

def plotData(fileName):
    xVals, yVals = getData(fileName)
    xVals = pylab.array(xVals)
    yVals = pylab.array(yVals)
    xVals = xVals*9.81  #acc. due to gravity
    pylab.plot(xVals, yVals, 'bo',
               label = 'Measured displacements')
    labelPlot()
    
## for slide 14
#plotData('springData.txt')
    
def fitData(fileName):
    xVals, yVals = getData(fileName)
    xVals = pylab.array(xVals)
    yVals = pylab.array(yVals)
    xVals = xVals*9.81 #get force
    pylab.plot(xVals, yVals, 'bo',
               label = 'Measured points')
    labelPlot()                 
    a,b = pylab.polyfit(xVals, yVals, 1)
    estYVals = a*pylab.array(xVals) + b
    print('a =', a, 'b =', b)
    pylab.plot(xVals, estYVals, 'r',
               label = 'Linear fit, k = '
               + str(round(1/a, 5)))
    pylab.legend(loc = 'best')
 

#for Slide 27 
#fitData('springData.txt')

   
def fitData1(fileName):
    xVals, yVals = getData(fileName)
    xVals = pylab.array(xVals)
    yVals = pylab.array(yVals)
    xVals = xVals*9.81 #get force
    pylab.plot(xVals, yVals, 'bo',
               label = 'Measured points')
    labelPlot()                 
    model = pylab.polyfit(xVals, yVals, 1)
    estYVals = pylab.polyval(model, xVals)
    pylab.plot(xVals, estYVals, 'r',
               label = 'Linear fit, k = '
               + str(round(1/model[0], 5)))
    pylab.legend(loc = 'best')
    ## added
    print(rSquared(yVals, estYVals))

#for Slide 28
#fitData1('springData.txt')


##for Slide 30, 31, 33 

#xVals, yVals = getData('mysteryData.txt')
#pylab.plot(xVals, yVals, 'o', label = 'Data Points')
#pylab.title('Mystery Data')
#
##Try linear model
#model1 = pylab.polyfit(xVals, yVals, 1)
#pylab.plot(xVals, pylab.polyval(model1, xVals),
#           label = 'Linear Model')
#
##Try a quadratic model
#model2 = pylab.polyfit(xVals, yVals, 2)
#pylab.plot(xVals, pylab.polyval(model2, xVals),
#           'r--', label = 'Quadratic Model')
#pylab.legend()

##Compare models
def aveMeanSquareError(data, predicted):
    error = 0.0
    for i in range(len(data)):
        error += (data[i] - predicted[i])**2
    return error/len(data)

##for Slide 36
#estYVals = pylab.polyval(model1, xVals)  
#print('Ave. mean square error for linear model =',
#      aveMeanSquareError(yVals, estYVals))
#estYVals = pylab.polyval(model2, xVals)
#print('Ave. mean square error for quadratic model =',
#      aveMeanSquareError(yVals, estYVals))

def rSquared(observed, predicted):
    error = ((predicted - observed)**2).sum()
    meanError = error/len(observed)
    return 1 - (meanError/numpy.var(observed))

def genFits(xVals, yVals, degrees):
    models = []
    for d in degrees:
        model = pylab.polyfit(xVals, yVals, d)
        models.append(model)
    return models

def testFits(models, degrees, xVals, yVals, title):
    pylab.plot(xVals, yVals, 'o', label = 'Data')
    for i in range(len(models)):
        estYVals = pylab.polyval(models[i], xVals)
        error = rSquared(yVals, estYVals)
        pylab.plot(xVals, estYVals,
                   label = 'Fit of degree '\
                   + str(degrees[i])\
                   + ', R2 = ' + str(round(error, 5)))
    pylab.legend(loc = 'best')
    pylab.title(title)



#for slide 41

#xVals, yVals = getData('mysteryData.txt')
#degrees = (1, 2)
#models = genFits(xVals, yVals, degrees)
#testFits(models, degrees, xVals, yVals, 'Mystery Data')

#for slide 43

##Compare higher-order fits
#xVals, yVals = getData('mysteryData.txt')
#degrees = (2, 4, 8, 16)
#models = genFits(xVals, yVals, degrees)
#testFits(models, degrees, xVals, yVals, 'Mystery Data')


def genNoisyParabolicData(a, b, c, xVals, fName):
    yVals = []
    for x in xVals:
        theoreticalVal = a*x**2 + b*x + c
        yVals.append(theoreticalVal + random.gauss(0, 35))
    f = open(fName,'w')
    f.write('x        y\n')
    for i in range(len(yVals)):
        f.write(str(yVals[i]) + ' ' + str(xVals[i]) + '\n')
    f.close()
 
 
# for slides 49, 50
 
#random.seed(0)
#
#xVals = range(-10, 11, 1)
#a, b, c = 3, 0, 0
#genNoisyParabolicData(a, b, c, xVals, 'parabola1.txt')
#genNoisyParabolicData(a, b, c, xVals, 'parabola2.txt')
#
#degrees = (1, 2, 16)
#xVals1, yVals1 = getData('parabola1.txt')
#models1 = genFits(xVals1, yVals1, degrees)
#testFits(models1, degrees, xVals1, yVals1, 'Parabola 1')
#
#pylab.figure()
#xVals2, yVals2 = getData('parabola2.txt')
#models2 = genFits(xVals2, yVals2, degrees)
#testFits(models2, degrees, xVals2, yVals2, 'Parabola 2')
#
 
## for Slide 51
 
#pylab.figure()
#testFits(models1, degrees, xVals2, yVals2,
#         'Apply Parabola 1 Model to Parabola 2')


#def genParabolicData(a, b, c, xVals, fracOutliers):
#    yVals = []
#    for x in xVals:
#        theoreticalVal = a*x**2 + b*x + c
#        if random.random() > fracOutliers:
#            yVals.append(theoreticalVal\
#            + random.gauss(0, 35))
#        else: #generate outlier
#            yVals.append(theoreticalVal\
#            + random.gauss(0, theoreticalVal*2))
#    f = open('mystery.txt','w')
#    f.write('x        y\n')
#    for i in range(len(yVals)):
#        f.write(str(yVals[i]) + ' ' + str(xVals[i]) + '\n')
#    f.close()
#    return yVals
#    
##parameters for generating data
#xVals = range(-10, 11, 1)
#a, b, c = 3.0, 0.0, 0.0
#fracOutlier = 0.00
#
##generate data
#random.seed(0)
#yVals = genParabolicData(a, b, c, xVals, fracOutlier)

def fitDataWithBreak(fileName):
    xValsBase, yValsBase = getData(fileName)
    bestFitSoFar = None
    bestFitBreak = None
    for br in range(3,len(xValsBase)-3):
        xValsLow = pylab.array(xValsBase[:br])
        xValsHigh = pylab.array(xValsBase[br:])
        yValsLow = pylab.array(yValsBase[:br])
        yValsHigh = pylab.array(yValsBase[br:])
        xValsLow = xValsLow*9.81
        xValsHigh = xValsHigh*9.81
        modelLow = pylab.polyfit(xValsLow, yValsLow, 1)
        modelHigh = pylab.polyfit(xValsHigh, yValsHigh, 1)
        estYValsLow = pylab.polyval(modelLow, xValsLow)
        estYValsHigh = pylab.polyval(modelHigh, xValsHigh)
        fit = aveMeanSquareError(yValsLow, estYValsLow) + \
              aveMeanSquareError(yValsHigh, estYValsHigh)
        if bestFitSoFar == None or bestFitSoFar > fit:
            bestFitSoFar = fit
            bestFitBreak = br
    pylab.figure()
    pylab.plot(xValsLow,yValsLow, 'bo',
               label = 'Measured points')
    pylab.plot(xValsHigh, yValsHigh, 'bo',
               label = 'Measured points')
    labelPlot()
    br = bestFitBreak
    xValsLow = pylab.array(xValsBase[:br])
    xValsHigh = pylab.array(xValsBase[br:])
    yValsLow = pylab.array(yValsBase[:br])
    yValsHigh = pylab.array(yValsBase[br:])
    xValsLow = xValsLow*9.81
    xValsHigh = xValsHigh*9.81
    modelLow = pylab.polyfit(xValsLow, yValsLow, 1)
    modelHigh = pylab.polyfit(xValsHigh, yValsHigh, 1)
    estYValsLow = pylab.polyval(modelLow, xValsLow)
    estYValsHigh = pylab.polyval(modelHigh, xValsHigh)
    pylab.plot(xValsLow, estYValsLow, 'g', 
               label = 'Linear fit, k = ' 
               + str(round(1/modelLow[0], 5)))
    pylab.plot(xValsHigh, estYValsHigh, 'g',
               label = 'Linear fit,, k = '
               + str(round(1/modelHigh[0], 5)))
    pylab.legend(loc = 'best')
    print('rSquared value, low = ', 
          rSquared(yValsLow, estYValsLow))
    print('rSquared value, high = ',
          rSquared(yValsHigh, estYValsHigh))


## for slide 56
#
#fitDataWithBreak('springData.txt')

def fitDataWithBreakFlat(fileName):
    xValsBase, yValsBase = getData(fileName)
    bestFitSoFar = None
    bestFitBreak = None
    for br in range(3,len(xValsBase)-3):
        xValsLow = pylab.array(xValsBase[:br])
        xValsHigh = pylab.array(xValsBase[br:])
        yValsLow = pylab.array(yValsBase[:br])
        yValsHigh = pylab.array(yValsBase[br:])
        xValsLow = xValsLow*9.81
        xValsHigh = xValsHigh*9.81
        modelLow = pylab.polyfit(xValsLow, yValsLow, 1)
        modelHigh = pylab.polyfit(xValsHigh, yValsHigh, 0)
        estYValsLow = pylab.polyval(modelLow, xValsLow)
        estYValsHigh = pylab.polyval(modelHigh, xValsHigh)
        fit = aveMeanSquareError(yValsLow, estYValsLow) + \
              aveMeanSquareError(yValsHigh, estYValsHigh)
        if bestFitSoFar == None or bestFitSoFar > fit:
            bestFitSoFar = fit
            bestFitBreak = br
    pylab.figure()
    pylab.plot(xValsLow,yValsLow, 'bo',
               label = 'Measured points')
    pylab.plot(xValsHigh, yValsHigh, 'bo',
               label = 'Measured points')
    labelPlot()
    br = bestFitBreak
    xValsLow = pylab.array(xValsBase[:br])
    xValsHigh = pylab.array(xValsBase[br:])
    yValsLow = pylab.array(yValsBase[:br])
    yValsHigh = pylab.array(yValsBase[br:])
    xValsLow = xValsLow*9.81
    xValsHigh = xValsHigh*9.81
    modelLow = pylab.polyfit(xValsLow, yValsLow, 1)
    modelHigh = pylab.polyfit(xValsHigh, yValsHigh, 0)
    estYValsLow = pylab.polyval(modelLow, xValsLow)
    estYValsHigh = pylab.polyval(modelHigh, xValsHigh)
    pylab.plot(xValsLow, estYValsLow, 'g', 
               label = 'Linear fit, k = ' 
               + str(round(1/modelLow[0], 5)))
    pylab.plot(xValsHigh, estYValsHigh, 'g',
               label = 'Linear fit,, k = '
               + str(round(1/modelHigh[0], 5)))
    pylab.legend(loc = 'best')
    print('rSquared value, low = ', 
          rSquared(yValsLow, estYValsLow))
    print('rSquared value, high = ',
          rSquared(yValsHigh, estYValsHigh))

## for slide 57
          
#fitDataWithBreakFlat('springData.txt')