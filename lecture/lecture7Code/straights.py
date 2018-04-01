# -*- coding: utf-8 -*-
"""
Created on Mon Nov  6 08:25:59 2017

@author: WELG
"""


import random 

def straights(n, rolls):
    count = 0
    for r in range(rolls):
        seq = ''
        for roll in range(n):
            seq += str(random.choice([1,2,3,4,5,6]))
        if seq == '1'*n or seq == '2'*n or seq == '3'*n\
            or seq == '4'*n or seq == '5'*n or seq == '6'*n:
            count += 1
    return count
    
#print(straights(3, 100))
        
def straightsStats(n, rolls, trials):
    record = []
    for t in range(trials):
        count = straights(n, rolls)
        record.append(count)
    mean = sum(record)/len(record)
    tot = 0.0
    for r in record:
        tot += (r - mean)**2
    return mean, (tot/len(record))**0.5
    
#print(straightsStats(3, 100, 100))

for numTrials in (100, 1000, 10000):
    print('')
    print('Gathering stats using', numTrials, 'trials')
    for rolls in (100, 1000, 10000):
        print('Data using ', rolls, 'rolls, over ', numTrials, 'trials')
        mean, sd = straightsStats(3, rolls, numTrials)
        cv = sd/mean
#        print('Number hits', mean, 'deviation', sd)
        print('Number hits', mean, 'deviation', round(sd, 3), 'CV', 
              round(cv, 3))
    
    
        