#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  8 13:27:55 2017

@author: eric
"""

import numpy as np

def find_combination(choices, total):
    """
    choices: a non-empty list of ints
    total: a positive int
 
    Returns result, a numpy.array of length len(choices) 
    such that
        * each element of result is 0 or 1
        * sum(result*choices) == total
        * sum(result) is as small as possible
    In case of ties, returns any result that works.
    If there is no result that gives the exact total, 
    pick the one that gives sum(result*choices) closest 
    to total without going over.
    """

    N = len(choices)
    # enumerate the 2**N possible combinations
    bestCombo = []
    bestSumVal = 0
    for i in range(2**N):
        combo = []
        sumVal = 0
        for j in range(N):
            # test bit jth of integer i
            # >>j. move the bit we want to check to the end
            # %2. remove all the other bits execpt the last one
            # check the one we kept if it is 1 not 0,
            # which means we want to keep the item which on the position
            # example:  0 1 1 0 1
            # we want to check the third "1"
            # first move the second bit to the end(>>j), will be "0 0 0 1 1"
            # then remove all the other bits(%2), we got "0 0 0 0 1"
            # compare it with 1, which is true, 
            # so we take the item with the position, which will be item[2]
            if (i >> j) % 2 == 1:
                if sumVal + choices[j] > total:
                    continue
                else:
                    combo.append(j)
                    sumVal += choices[j]
#        print(combo, sumVal, bestCombo, bestSumVal)
        if sumVal > bestSumVal or (len(combo) < len(bestCombo) and sumVal == bestSumVal):
            bestSumVal = sumVal
            bestCombo = combo
#        print("--", bestCombo)
        
    result = np.zeros(len(choices), dtype=np.int)
    for index in bestCombo:
        result[index] = 1
    return result

choices = [1,2,2,3]
total = 4
print(find_combination(choices, total))
choices = [1,1,3,5,3]
total = 5
print(find_combination(choices, total))
choices = [1,1,1,9]
total = 4
print(find_combination(choices, total))