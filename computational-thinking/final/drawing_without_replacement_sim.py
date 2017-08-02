#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  8 10:23:28 2017

@author: eric
"""
import random

def drawing_without_replacement_sim(numTrials):
    '''
    Runs numTrials trials of a Monte Carlo simulation
    of drawing 3 balls out of a bucket containing
    4 red and 4 green balls. Balls are not replaced once
    drawn. Returns a float - the fraction of times 3 
    balls of the same color were drawn in the first 3 draws.
    '''
    sameNum = 0
    for numTrail in range(numTrials):    
        balls = [0,0,0,0,1,1,1,1]
        out = []
        for i in range(3):
            index = random.randint(0, len(balls)-1)
            out.append(balls.pop(index))
        if out[0] == out[1] and out[1] == out[2]:
            sameNum += 1
    return sameNum/numTrials

f = drawing_without_replacement_sim(10000)
print(f)
f = drawing_without_replacement_sim(100000)
print(f)
f = drawing_without_replacement_sim(1000000)
print(f)