#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  9 16:14:49 2017

@author: eric
"""


def yieldAllCombos(items):
    """
        Generates all combinations of N items into two bags, whereby each
        item is in one or zero bags.

        Yields a tuple, (bag1, bag2), where each bag is represented as a list
        of which item(s) are in each bag.
    """
    # Your code here
    N = len(items)
    # enumerate the 2**N possible combinations
    for i in range(2**N):
        combo = []
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
                combo.append(items[j])
        M = len(combo)
        for k in range(2**M):
            bag1 = []
            bag2 = []
            for l in range(M):
                if(k >> l) % 2 == 1:
                    bag1.append(combo[l])
                else:
                    bag2.append(combo[l])
            yield bag1, bag2


for bag1, bag2 in yieldAllCombos([1, 2, 3, 4, 5]):
    print(bag1, bag2)
