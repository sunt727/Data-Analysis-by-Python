# -*- coding: utf-8 -*-
"""
Created on Sat Nov  4 16:33:42 2017

@author: WELG
"""

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
        
class EuRoulette(FairRoulette):
    def __init__(self):
        FairRoulette.__init__(self)
        self.pockets.append('0')
    def __str__(self):
        return 'European Roulette'
        
class AmRoulette(FairRoulette):
    def __init__(self):
        EuRoulette.__init__(self)
        self.pockets.append('00')
    def __str__(self):
        return 'American Roulette'

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
    
#game = FairRoulette()
#for numSpins in (100, 1000000):
#    for i in range(3):
#        playRoulette(game, numSpins, 2, 1, True)
        
#for spins in (1000, 10000, 100000, 1000000, 10000000):
#    game = FairRoulette()
#    print('Simulate 20 trials of ' + str(spins) + ' spins each')
#    vals = findPocketReturn(game, 20, spins, False)
#    print('Exp. return for Fair Roulette = ' +\
#           str(100*sum(vals)/len(vals)))
#    game = EuRoulette()
#    vals = findPocketReturn(game, 20, spins, False)
#    print('Exp. return for European Roulette = ' +\
#           str(100*sum(vals)/len(vals)))    
#    game = AmRoulette()
#    vals = findPocketReturn(game, 20, spins, False)
#    print('Exp. return for American Roulette = ' + \
#           str(100*sum(vals)/len(vals)) )   
#    print('')
    
def getMeansAndStd(X):
    mean = sum(X)/len(X)
    tot = 0.0
    for x in X:
        tot += (x - mean)**2
    std = (tot/len(X))**0.5
    CV = std/mean
    return mean, std, CV
    
resultDict = {}
games = (FairRoulette, EuRoulette, AmRoulette)
for G in games:
    resultDict[G().__str__()] = []
numTrials = 20
for numSpins in (1000, 100000, 1000000):
    print('\nSimulate betting a pocket for', numTrials, 
          'trials of', numSpins, 'spins each')
    for G in games:
        pocketReturns = findPocketReturn(G(), numTrials,
                                         numSpins, False)
        mean, std = getMeanAndStd(pocketReturns)
        resultDict[G().__str__()].append((numSpins,
                                          100*mean,
                                          100*std))
        print('Exp. return for', G(), '=',
              str(round(100*mean, 3))
              + '%', '+/- ' + str(round(100*1.96*std, 3))
              + '% with 95% confidence')
    