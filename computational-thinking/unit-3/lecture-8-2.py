#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug  4 11:11:56 2017

@author: eric
"""

import random, math, pylab

def getMeanAndStd(data):
    mean = sum(data)/float(len(data))
    std = (sum([(d-mean)**2 for d in data])/len(data))**0.5
    return (mean, std)

def throwNeedls(numNeedles):
    inCircle = 0;
    for needle in range(numNeedles):
        if (random.random()**2 + random.random()**2)**0.5 <= 1.0:
            inCircle+=1
    return 4*inCircle/numNeedles

def getEst(numNeedles, numTrails):
    estPis = []
    for t in range(numTrails):
        estPis.append(throwNeedls(numNeedles))
    return getMeanAndStd(estPis)

def estPi(precision, numTrails):
    numNeedles = 1000
    std = precision
    while(std >= precision/1.96):
        mean, std = getEst(numNeedles, numTrails)
        print("Mean="+str(mean)+", Std="+str(round(std, 6))+", Needls="+str(numNeedles))
        numNeedles *= 2 

#random.seed(0)
#estPi(0.005, 100)

# estimate area of sinx
def throwNeedls(numNeedles):
    inSin = 0;
    for needle in range(numNeedles):
        if math.sin(random.random()*math.pi) >= random.random():
            inSin+=1
    return math.pi*inSin/numNeedles

#random.seed(0)
#estPi(0.005, 100)

def integrate(f, a, b, step):
    yVals, xVals = [], []
    xVal = a
    while xVal <= b:
        xVals.append(xVal)
        yVals.append(f(xVal))
        xVal += step
    pylab.plot(xVals, yVals)
    pylab.title('sin(x)')
    pylab.xlim(a, b)
    pylab.ylim(0, 1)
    xUnders, yUnders, xOvers, yOvers = [],[],[],[]
    for i in range(500):
        xVal = random.uniform(a, b)
        yVal = random.uniform(0, 1)
        if yVal < f(xVal):
            xUnders.append(xVal)
            yUnders.append(yVal)
        else:
            xOvers.append(xVal)
            yOvers.append(yVal)
    pylab.plot(xUnders, yUnders, 'ro')
    pylab.plot(xOvers, yOvers, 'ko')
    pylab.xlim(a, b)
    ratio = len(xUnders)/(len(xUnders) + len(yUnders))
    print(ratio)
    print(ratio*b)
    
def one(x):
    return math.sin(x)
    
#integrate(one, 0, math.pi, 0.001)