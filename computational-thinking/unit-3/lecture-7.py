#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  2 12:08:14 2017

@author: eric
"""

import math, random, pylab

random.seed(0)

def mean(X):
    return float(sum(X)/len(X))

def stdDev(X):

    sumVal = 0
    mu = mean(X)
    for x in X:
        sumVal += (x-mu)**2
    return math.sqrt(sumVal / len(X))


def flipCoin(numTrials):
    heads = 0
    for i in range(numTrials):
        if random.random() > 0.5:
            heads = heads + 1
    return (heads, numTrials - heads)

def makePlot(xVals, yVals, title, xLabel, yLabel, style,
             logX = False, logY = False):
    """Plots xVals vs. yVals with supplied titles and labels."""
    pylab.figure()
    pylab.title(title)
    pylab.xlabel(xLabel)
    pylab.ylabel(yLabel)
    pylab.plot(xVals, yVals, style)
    if logX:
        pylab.semilogx()
    if logY:
        pylab.semilogy()

def simulateStdDev(minExp, maxExp, numTrials):
    
    ratiosMeans, diffsMeans, ratiosSDs, diffsSDs = [], [], [], []
    
    xVals = []
    for i in range(minExp, maxExp+1):
        xVals.append(2**i)
    for numFlips in xVals:
        ratios = []
        diffs = []
        for t in range(numTrials):
            heads, tails = flipCoin(numFlips)
            ratios.append(heads/float(tails))
            diffs.append(abs(heads - tails))
        ratiosMeans.append(mean(ratios))
        diffsMeans.append(mean(diffs))
        ratiosSDs.append(stdDev(ratios))
        diffsSDs.append(stdDev(diffs))
       
    numTrialsString = ' (' + str(numTrials) + ' Trials)'
    title = 'Mean Heads/Tails Ratios' + numTrialsString
    makePlot(xVals, ratiosMeans, title,
             'Number of flips', 'Mean Heads/Tails', 'bo', logX = True)
    title = 'SD Heads/Tails Ratios' + numTrialsString
    makePlot(xVals, ratiosSDs, title,
             'Number of Flips', 'Standard Deviation', 'bo',
             logX = True, logY = True)
    
    title = 'Mean abs(#Heads - #Tails)' + numTrialsString 
    makePlot(xVals, diffsMeans, title, 
             'Number of Flips', 'Mean abs(#Heads - #Tails)', 'bo', 
             logX = True, logY = True) 
    title = 'SD abs(#Heads - #Tails)' + numTrialsString 
    makePlot(xVals, diffsSDs, title,
             'Number of Flips', 'Standard Deviation', 'bo',
             logX = True, logY = True)



#simulateStdDev(4, 20, 20)

def CV(X):
    mean = sum(X)/float(len(X))
    try:
        return stdDev(X)/mean
    except ZeroDivisionError:
        return float('nan')

def simulateCV(minExp, maxExp, numTrials):
    
    ratiosMeans, diffsMeans, ratiosSDs, diffsSDs = [], [], [], []
    
    xVals = []
    for i in range(minExp, maxExp+1):
        xVals.append(2**i)
    for numFlips in xVals:
        ratios = []
        diffs = []
        for t in range(numTrials):
            heads, tails = flipCoin(numFlips)
            ratios.append(heads/float(tails))
            diffs.append(abs(heads - tails))
        ratiosMeans.append(mean(ratios))
        diffsMeans.append(mean(diffs))
        ratiosSDs.append(CV(ratios))
        diffsSDs.append(CV(diffs))
       
    numTrialsString = ' (' + str(numTrials) + ' Trials)'
    title = 'Mean Heads/Tails Ratios' + numTrialsString
    makePlot(xVals, ratiosMeans, title,
             'Number of flips', 'Mean Heads/Tails', 'bo', logX = True)
    title = 'SD Heads/Tails Ratios' + numTrialsString
    makePlot(xVals, ratiosSDs, title,
             'Number of Flips', 'Standard Deviation', 'bo',
             logX = True, logY = True)
    
    title = 'Mean abs(#Heads - #Tails)' + numTrialsString 
    makePlot(xVals, diffsMeans, title, 
             'Number of Flips', 'Mean abs(#Heads - #Tails)', 'bo', 
             logX = True, logY = True) 
    title = 'SD abs(#Heads - #Tails)' + numTrialsString 
    makePlot(xVals, diffsSDs, title,
             'Number of Flips', 'Standard Deviation', 'bo',
             logX = True, logY = True)

simulateCV(4, 20, 20)