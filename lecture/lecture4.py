# -*- coding: utf-8 -*-
"""
Created on Sat Aug 20 11:09:36 2016

@author: guttag
"""
def rollDie():
    """returns an int between 1 and 6"""
    return 3
    
import random
 
def rollDie():
    """returns a random int between 1 and 6"""
    return random.choice([1,2,3,4,5,6])
 
def testRoll(n):
    result = ''
    for i in range(n):
        result = result + str(rollDie())
    print(result)

#testRoll(5)

random.seed(0)

def runSim(goal, numTrials):
    total = 0
    for i in range(numTrials):
        result = ''
        for j in range(len(goal)):
            result += str(rollDie())
        if result == goal:
            total += 1
    print('Actual probability of', goal, '=',
          round(1/(6**len(goal)), 8)) 
    estProbability = round(total/numTrials, 8)
    print('Estimated Probability of', goal, '=',
          round(estProbability, 8))
    
runSim('11111', 1000)

import pylab, numpy
   
def getBdays(toPlot = False):
    inFile = open('Births.csv')
    inFile.readline() #discard first line
    numBirths = []
    for l in inFile:
        line = l.split(',')
        numBirths.append(int(line[2][:-1]))
    possibleDates = []
    d = {}
    for i in range(len(numBirths)):
        possibleDates += [i]*(numBirths[i])
        d[i+1] = numBirths[i]
    if toPlot:
        for i in range(len(numBirths)):
            d[i+1] = numBirths[i]
        vals = []
        for k in d:
            vals.append(d[k])
        pylab.plot(vals, 'bo')
        pylab.xlim(-10, pylab.xlim()[1])
        pylab.xlabel('Day of Year')
        pylab.ylabel('Number of Births')
        mean = 'Mean = ' + str(int(sum(vals)/len(vals)))
        std = 'Std = ' + str(int(numpy.std(vals)))
        pylab.title('Frequency of Birthdates\n' +
                    mean + ', ' + std)
    return possibleDates
    
def sameDate(numPeople, numSame, possibleDates):
    birthdays = [0]*366
    for p in range(numPeople):
        birthDate = random.choice(possibleDates)
        birthdays[birthDate] += 1
    return max(birthdays) >= numSame

def birthdayProb(numPeople, numSame, numTrials,
                 possibleDates):
    numHits = 0
    for t in range(numTrials):
        if sameDate(numPeople, numSame, possibleDates):
            numHits += 1
    return numHits/numTrials

import math

def trueProb(numPeople):
    #assumes each birth date equally probable
    numerator = math.factorial(366)
    denom = (366**numPeople)*math.factorial(366-numPeople)
    return 1 - numerator/denom
    
#for numPeople in [10, 20, 40, 100]:
#    possibleDates = list(range(366))
#    possibleDates = getBdays(False)
#    print('For', numPeople,
#          'est. prob. of a shared birthday is',
#          birthdayProb(numPeople, 2, 10000, possibleDates))
#    print('Actual prob. (uniform distribution) =',
#          trueProb(numPeople))

