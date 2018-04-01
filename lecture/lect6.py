import random
    
def UlamConjecture(n, toPrint = False):
    """assumes n a positive int"""
    result = [n]
    while n != 1:
        if n%2 == 0:
            n = n//2
        else:
            n = 3*n + 1
        if toPrint:
            result.append(n)
    if toPrint:
        print(result)
        print('Maximum value =', max(result))

#UlamConjecture(27, True)  

  
#for i in range(10000):
#    UlamConjecture(random.randint(1, 1000000))
#print('So far, it seems to be true')

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

#random.seed(1)
#game = FairRoulette()
#for numSpins in (100, 1000000):
#    for i in range(3):
#        playRoulette(game, numSpins, 2, 1, True)

class EuRoulette(FairRoulette):
    def __init__(self):
        FairRoulette.__init__(self)
        self.pockets.append('0')
    def __str__(self):
        return 'European Roulette'

class AmRoulette(EuRoulette):
    def __init__(self):
        EuRoulette.__init__(self)
        self.pockets.append('00')
    def __str__(self):
        return 'American Roulette'
#        
def findPocketReturn(game, numTrials, trialSize, toPrint):
    pocketReturns = []
    for t in range(numTrials):
        trialVals = playRoulette(game, trialSize, 2, 1, toPrint)
        pocketReturns.append(trialVals)
    return pocketReturns

#random.seed(0)
#numTrials = 20
#resultDict = {}
#games = (FairRoulette, EuRoulette, AmRoulette)
#for G in games:
#    resultDict[G().__str__()] = []
#for numSpins in (1000, 10000, 100000, 1000000):
#    print('\nSimulate', numTrials, 'trials of',
#          numSpins, 'spins each')
#    for G in games:
#        pocketReturns = findPocketReturn(G(), numTrials,
#                                         numSpins, False)
#        expReturn = 100*sum(pocketReturns)/len(pocketReturns)
#        print('Exp. return for', G(), '=',
#             str(round(expReturn, 4)) + '%')
             
def getMeanAndStd(X):
    mean = sum(X)/len(X)
    tot = 0.0
    for x in X:
        tot += (x - mean)**2
    std = (tot/len(X))**0.5
    return mean, std

#random.seed(0)
#resultDict = {}
#games = (FairRoulette, EuRoulette, AmRoulette)
#for G in games:
#    resultDict[G().__str__()] = []
#numTrials = 20
#for numSpins in (1000, 10000, 100000):
#    print('\nSimulate betting a pocket for', numTrials,
#          'trials of', numSpins, 'spins each')
#    for G in games:
#        pocketReturns = findPocketReturn(G(), numTrials,
#                                         numSpins, False)
#        mean, std = getMeanAndStd(pocketReturns)
#        resultDict[G().__str__()].append((numSpins,
#                                          100*mean,
#                                          100*std))
#        print('Exp. return for', G(), '=',
#              str(round(100*mean, 3))
#              + '%,', '+/- ' + str(round(100*1.96*std, 3))
#              + '% with 95% confidence')

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
    print('Est. = ' + str(curEst) +\
          ', Std. dev. = ' + str(round(sDev, 6))\
          + ', Needles = ' + str(numNeedles))
    return (curEst, sDev)

def estPi(precision, numTrials):
    numNeedles = 1000
    sDev = precision
    while sDev >= precision/1.96:
        curEst, sDev = getEst(numNeedles,
                              numTrials)
        numNeedles *= 2
    return curEst

estPi(0.005, 100)