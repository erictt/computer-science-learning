#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug  4 11:11:56 2017

@author: eric
"""

import random

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
        
random.seed(0)
estPi(0.005, 100)
