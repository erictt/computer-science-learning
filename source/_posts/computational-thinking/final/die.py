#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  8 10:37:14 2017

@author: eric
"""

import random, pylab

# You are given this function
def getMeanAndStd(X):
    mean = sum(X)/float(len(X))
    tot = 0.0
    for x in X:
        tot += (x - mean)**2
    std = (tot/len(X))**0.5
    return mean, std

# You are given this class
class Die(object):
    def __init__(self, valList):
        """ valList is not empty """
        self.possibleVals = valList[:]
    def roll(self):
        return random.choice(self.possibleVals)

# Implement this -- Coding Part 1 of 2
def makeHistogram(values, numBins, xLabel, yLabel, title=None):
    """
      - values, a sequence of numbers
      - numBins, a positive int
      - xLabel, yLabel, title, are strings
      - Produces a histogram of values with numBins bins and the indicated labels
        for the x and y axis
      - If title is provided by caller, puts that title on the figure and otherwise
        does not title the figure
    """
    pylab.hist(values, bins = numBins)
    pylab.xlabel(xLabel)
    pylab.ylabel(yLabel)
    if title is not None:
        pylab.title(title)
    pylab.show()
                    
# Implement this -- Coding Part 2 of 2
def getAverage(die, numRolls, numTrials):
    """
      - die, a Die
      - numRolls, numTrials, are positive ints
      - Calculates the expected mean value of the longest run of a number
        over numTrials runs of numRolls rolls.
      - Calls makeHistogram to produce a histogram of the longest runs for all
        the trials. There should be 10 bins in the histogram
      - Choose appropriate labels for the x and y axes.
      - Returns the mean calculated
    """
    results = []
    for numTrail in range(numTrials):
        longestVal = None
        longestLen = 0
        lastVal = None
        lastLen = 0
        for numRoll in range(numRolls):
            curVal = die.roll()
            if lastVal == None:
                lastVal = curVal
                lastLen = 0
                
            if lastVal == curVal:
                lastLen += 1
            
            if longestLen == 0 or longestLen < lastLen:
                longestVal = lastVal
                longestLen = lastLen
            
            if lastVal != curVal:
                lastVal = curVal
                lastLen = 1
        results.append(longestLen)
    makeHistogram(results, 10, "Longest run of a number", "Number of trials",\
                  "The longest run of a number over " + str(numTrials) + " runs of "\
                  + str(numRolls) + " rolls")
    mean, std = getMeanAndStd(results)
    return round(mean, 3)

# One test case
print(getAverage(Die([1]), 10, 1000))
#print(getAverage(Die([1,1]), 10, 1000))
print(getAverage(Die([1,2,3,4,5,6]), 50, 1000))
#print(getAverage(Die([1,2,3,4,5,6,6,6,7]), 500, 10000))