import random, pylab, numpy

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


def makeHist(data, title, xlabel, ylabel, bins = 20):
    pylab.hist(data, bins = bins)
    pylab.title(title)
    pylab.xlabel(xlabel)
    pylab.ylabel(ylabel)

def getHighs():
    inFile = open('temperatures.csv')
    population = []
    for l in inFile:
        try:
            tempC = float(l.split(',')[1])
            population.append(tempC)
        except:
            continue
    return population

def getMeansAndSDs(population, sample, verbose = False):
    popMean = sum(population)/len(population)
    sampleMean = sum(sample)/len(sample)
    if verbose:
        makeHist(population,
                 'Daily High 1961-2015, Population\n' +\
                 '(mean = '  + str(round(popMean, 2)) +\
                 ', std = ' +\
                 str(round(numpy.std(population), 2)) + ')',
                 'Degrees C', 'Number Days')
        pylab.figure()
        makeHist(sample, 'Daily High 1961-2015, Sample\n' +\
                 '(mean = ' + str(round(sampleMean, 2)) +\
                 ', std = ' +\
                 str(round(numpy.std(sample), 2)) + ')',
                 'Degrees C', 'Number Days')   
        print('Population mean =', popMean)
        print('Standard deviation of population =',
              numpy.std(population))
        print('Sample mean =', sampleMean)
        print('Standard deviation of sample =',
              numpy.std(sample))
    return popMean, sampleMean,\
           numpy.std(population), numpy.std(sample)

## code for Slides 10 and 12

#random.seed(0)         
#population = getHighs()
#sample = random.sample(population, 100)
#getMeansAndSDs(population, sample, True)

## code for Slides 14-17

#random.seed(0) 
#population = getHighs()
#sampleSize = 100
#numSamples = 1000
#sampleMeans = []
#for i in range(numSamples):
#    sample = random.sample(population, sampleSize)
#    popMean, sampleMean, popSD, sampleSD =\
#       getMeansAndSDs(population, sample, verbose = False)
#    sampleMeans.append(sampleMean)
#print('Mean of sample Means =',
#      round(sum(sampleMeans)/len(sampleMeans), 3))
#print('Standard deviation of sample means =',
#      round(numpy.std(sampleMeans), 3))
#makeHist(sampleMeans, 'Means of Samples', 'Mean', 'Frequency')
#pylab.axvline(x = popMean, color = 'r')

def showErrorBars(population, sizes, numTrials):
    xVals = []
    sizeMeans, sizeSDs = [], []
    for sampleSize in sizes:
        xVals.append(sampleSize)
        trialMeans = []
        for t in range(numTrials):
            sample = random.sample(population, sampleSize)
            popMean, sampleMean, popSD, sampleSD =\
               getMeansAndSDs(population, sample)
            trialMeans.append(sampleMean)
        sizeMeans.append(sum(trialMeans)/len(trialMeans))
        sizeSDs.append(numpy.std(trialMeans))
    pylab.errorbar(xVals, sizeMeans,
                   yerr = 1.96*pylab.array(sizeSDs),
                   fmt = 'o',
                   label = '95% Confidence Interval')
    pylab.title('Mean Temperature ('
                + str(numTrials) + ' trials)')
    pylab.xlabel('Sample Size')
    pylab.ylabel('Mean')
    pylab.axhline(y = popMean, color ='r', label = 'Population Mean')
    pylab.xlim(0, sizes[-1] + 10)
    pylab.legend()

## code for Slides 20-21

#random.seed(0)
#population = getHighs()   
#showErrorBars(population,
#              (50, 100, 200, 300, 400, 500, 600), 100)

## code for Slides 25-26

#dist, numSamples = [], 1000000
#
#for i in range(numSamples):
#    dist.append(random.gauss(0, 100))
#    
#pylab.hist(dist, bins = 100)
#pylab.xlabel('Value')
#pylab.ylabel('Frequency')

## code for Slides 28-29

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

## code for Slide 31

#checkEmpirical(5)

    
## code for slides 36-37
    
def getMeanAndStd(X):
    mean = sum(X)/float(len(X))
    tot = 0.0
    for x in X:
        tot += (x - mean)**2
    std = (tot/len(X))**0.5
    return mean, std

def plotMeans(numDice, numRolls, numBins, legend, color, style):
    means = []
    for i in range(numRolls//numDice):
        vals = 0
        for j in range(numDice):
            vals += 5*random.random() + 1
        means.append(vals/float(numDice))
    pylab.hist(means, numBins, color = color, label = legend,
               weights = [1/len(means)]*len(means),
               hatch = style)
    return getMeanAndStd(means)
    
mean, std = plotMeans(1, 1000000, 19, '1 die', 'b', '*')
print('Mean of rolling 1 die =', str(mean) + ',', 'Std =', std)
mean, std = plotMeans(50, 1000000, 19, 'Mean of 50 dice', 'r', '//')
print('Mean of rolling 50 dice =', str(mean) + ',', 'Std =', std)
pylab.title('Rolling Continuous Dice')
pylab.xlabel('Value')
pylab.ylabel('Probability')
pylab.legend()


## code for slides 38-39
class FairRoulette():
    def __init__(self):
        self.pockets = []
        for i in range(1,37):
            self.pockets.append(i)
        self.ball = None
        self.pocketOdds = len(self.pockets) - 1
    def spin(self):
        self.ball = random.choice(self.pockets)
    def betPocket(self, pocket, amt):
        if str(pocket) == str(self.ball):
            return amt*self.pocketOdds
        else: return -amt
    def __str__(self):
        return 'Fair Roulette'

def playRoulette(game, numSpins, pocket, bet, toPrint):
    totPocket = 0
    for i in range(numSpins):
        game.spin()
        totPocket += game.betPocket(pocket, bet)
    if toPrint:
        print(numSpins, 'spins of', game)
        print('Expected return betting', pocket, '=',\
              str(100*totPocket/numSpins) + '%\n')
    return (totPocket/numSpins)

      
def findPocketReturn(game, numTrials, trialSize, toPrint):
    pocketReturns = []
    for t in range(numTrials):
        trialVals = playRoulette(game, trialSize, 2, 1, toPrint)
        pocketReturns.append(trialVals)
    return pocketReturns
    
#numTrials = 1000000
#numSpins = 200
#game = FairRoulette()
#
#means = []
#for i in range(numTrials):
#    means.append(findPocketReturn(game, 1, numSpins,
#                                  False)[0])
#                                  
#pylab.hist(means, bins = 19, 
#           weights = [1/len(means)]*len(means))
#pylab.xlabel('Mean Return')
#pylab.ylabel('Probability')
#pylab.title('Expected Return Betting a Pocket 200 Times')
    
    
    
def sem(popSD, sampleSize):
    return popSD/sampleSize**0.5

## code for Slides 43-44

#sampleSizes = (25, 50, 100, 200, 300, 400, 500, 600)
#numTrials = 50
#population = getHighs()
#popSD = numpy.std(population)
#sems = []
#sampleSDs = []
#for size in sampleSizes:
#    sems.append(sem(popSD, size))
#    means = []
#    for t in range(numTrials):
#        sample = random.sample(population, size)
#        means.append(sum(sample)/len(sample))
#    sampleSDs.append(numpy.std(means))
#pylab.plot(sampleSizes, sampleSDs,
#           label = 'Std of ' + str(numTrials) + ' means')
#pylab.plot(sampleSizes, sems, 'r--', label = 'SEM')
#pylab.xlabel('Sample Size')
#pylab.ylabel('Std and SEM')
#pylab.title('SD for ' + str(numTrials) + ' Means and SEM')
#pylab.legend()

def plotDistributions():
    uniform, normal, exp = [], [], []
    for i in range(100000):
        uniform.append(random.random())
        normal.append(random.gauss(0, 1))
        exp.append(random.expovariate(0.5))
    makeHist(uniform,'Uniform','Value','Frequency')
    pylab.figure()
    makeHist(normal,'Gaussian','Value','Frequency')
    pylab.figure()
    makeHist(exp,'Exponential','Value','Frequency')

## code for Slide 45

#plotDistributions()

def getDiffs(population, sampleSizes):
    popStd = numpy.std(population)
    diffsFracs = []
    for sampleSize in sampleSizes:
        diffs = []
        for t in range(100):
            sample = random.sample(population, sampleSize)
            diffs.append(abs(popStd - numpy.std(sample)))
        diffMean = sum(diffs)/len(diffs)
        diffsFracs.append(diffMean/popStd)
    return pylab.array(diffsFracs)*100
    
def plotDiffs(sampleSizes, diffs, title, label, color = 'b'):
    pylab.plot(sampleSizes, diffs, label = label,
               color = color)
    pylab.xlabel('Sample Size')
    pylab.ylabel('% Difference in SD')
    pylab.title(title)
    pylab.legend()

## code for Slide 45

#sampleSizes = range(20, 600, 1)
#diffs = getDiffs(getHighs(), sampleSizes)
#plotDiffs(sampleSizes, diffs,
#          'Sample SD vs Population SD, Temperatures',
#          label = 'High temps')


def compareDists():
    uniform, normal, exp = [], [], []
    for i in range(100000):
        uniform.append(random.random())
        normal.append(random.gauss(0, 1))
        exp.append(random.expovariate(0.5))
    sampleSizes = range(20, 600, 1)
    udiffs = getDiffs(uniform, sampleSizes)
    ndiffs = getDiffs(normal, sampleSizes)
    ediffs = getDiffs(exp, sampleSizes)
    plotDiffs(sampleSizes, udiffs,
              'Sample SD vs Population SD',
              'Uniform population', 'm')
    plotDiffs(sampleSizes, ndiffs,
              'Sample SD vs Population SD',
              'Normal population', 'b')
    plotDiffs(sampleSizes, ediffs,
              'Sample SD vs Population SD',
              'Exponential population', 'r')

## code for Slide 49

#compareDists()  

## code for Slide 52

#popSizes = (10000, 100000, 1000000)
#sampleSizes = range(20, 600, 1)
#colors = ('b', 'g', 'r')
#for trial in range(3):
#    size = popSizes[trial]
#    color = colors[trial]
#    population = []
#    for i in range(size):
#        population.append(random.expovariate(0.5))
#    ediffs = getDiffs(population, sampleSizes)
#    plotDiffs(sampleSizes, ediffs,
#              'Sample SD vs Population SD, Uniform',
#              'Population size = ' + str(size),
#              color = color)




#temps = getHighs()
#popMean = sum(temps)/len(temps)
#sampleSize = 200
#numTrials = 10000
#
#random.seed(0)
#numBad = 0
#for t in range(numTrials):
#    posStartingPts = range(0, len(temps) - sampleSize)
#    start = random.choice(posStartingPts)
#    sample = temps[start:start+sampleSize]
#    sampleMean = sum(sample)/sampleSize
#    se = numpy.std(sample)/sampleSize**0.5
#    if abs(popMean - sampleMean) > 1.96*se:
#        numBad += 1
#print('Fraction outside 95% confidence interval =',
#      numBad/numTrials)

## code for Slide 54


#random.seed(0)
#temps = getHighs()
#sampleSize = 200
#numTrials = 10000
#popMean = sum(temps)/len(temps)    
#numBad = 0
#for t in range(numTrials):
#    sample = random.sample(temps, sampleSize)
#    sampleMean = sum(sample)/sampleSize
#    SEM = numpy.std(sample)/sampleSize**0.5
#    if abs(popMean - sampleMean) > 1.96*SEM:
#        numBad += 1
#print('Fraction outside 95% confidence interval =',
#      numBad/numTrials)