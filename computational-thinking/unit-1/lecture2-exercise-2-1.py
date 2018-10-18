#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  9 16:16:33 2017

@author: eric
"""

from itertools import chain

def powerset_generator(sets):
    for subset in chain.from_iterable(myCombinations(sets, r) for r in range(len(sets)+1)):
        yield subset

def combinations(iterable, r):
    # combinations('ABCD', 2) --> AB AC AD BC BD CD
    # combinations(range(4), 3) --> 012 013 023 123
    pool = tuple(iterable)
    n = len(pool)
    if r > n:
        return
    indices = list(range(r))
    yield tuple(pool[i] for i in indices)

    while True:
        for i in reversed(range(r)):
            if indices[i] != i + n - r:
                break
        else:
            return

        indices[i] += 1

        for j in range(i+1, r):
            indices[j] = indices[j-1] + 1

        yield tuple(pool[i] for i in indices)
        
 
        
# the logic of this function is 
#   set a new array with length r
#   loop the last element's index from i to i+n-r(n is the length of pool, r is the length of subsequence). 
#   when hit the maximum which should be n-1, increase the last-1 element's index.
#   loop until the first element's index hit the maximum, 
#   then increase the previous index, and set the last index to previous index + 1, 
#   then back to the loop until all of the indices hit the maximum
#   (1, 2, 3)
#   (1, 2, 4)
#   (1, 2, 5) <-- the last index hit the maximum
#   (1, 3, 4) <-- increase the previous index, and set every one after to previous index + 1,
#   (1, 3, 5) 
#   (1, 4, 5) <-- the (last-1) index hit the maximum
#   (2, 3, 4)
#   (2, 3, 5)
#   (2, 4, 5)
#   (3, 4, 5) <-- the (last-2) index hit the maximum
def myCombinations(iterable, r):
    
    pool = tuple(iterable)
    
    n = len(pool)
    
    if r > n:
        return
    indices = list(range(r))
 
    # In the "while" circle, we will start to change the indices by adding 1 consistently.
    # So yield the first permutation before the while start.
    yield tuple(pool[x] for x in indices)
    
    while True:

        # This 'for' loop is checking whether the index has hit the maximum from the last one to the first one.
        # if it indices[i] >= its maximum, 
        #   set i = i-1, check the previous one
        # if all of the indices has hit the maximum, 
        #   stop the `while` loop
        for i in reversed(range(r)):
            
            # let's take an example to explain why using i + n - r
            # pool indices: [0,1,2,3,4]
            # subsequence indices: [0,1,2]
            # so
            #   indices[2] can be one of [2,3,4],
            #   indices[1] can be one of [1,2,3],
            #   indices[0] can be one of [0,1,2],
            # and the gap of every index is n-r, like here is 5-3=2
            # then
            #   indices[2] < 2+2 = i+2 = i+n-r,
            #   indices[1] < 1+2 = i+2 = i+n-r,
            #   indices[0] < 0+2 = i+2 = i+n-r,
            if indices[i] < i + n - r:
                break
        else:
            # loop finished, return
            return
        
        # Add one for current indices[i], 
        # (we already yield the first permutation before the loop)
        indices[i] += 1
        # this for loop increases every indices which is after indices[i].
        # cause, current index has increased, and we need to confirm every one behind is initialized again.
        # For example: current we got i = 2, indices[i]+1 will be 3, 
        # so the next loop should start with [1, 3, 4], not [1, 3, 3]
        for j in range(i+1, r):
            indices[j] = indices[j-1] + 1
            
        yield tuple(pool[x] for x in indices) 



#for i in powerset_generator(sets):
#    print("output:  ", i)
#    print("==============o=========\n")


def anotherCombinations(iterable, distLen):

    pool = tuple(iterable)
    
    poolLen = len(pool)
    
    if poolLen < distLen or distLen < 1:
        return
    
    indices = list(range(distLen))
    
    yield tuple([pool[x]] for x in indices)

    i = distLen - 1    
    while indices[0] <= poolLen - distLen and i < distLen and i >= 0:

        if indices[i] < poolLen - distLen + i:
            indices[i] += 1
            for j in range(i+1, distLen):
                indices[j] = indices[j-1] + 1
            i += distLen - i - 1
            yield tuple([pool[x]] for x in indices)
        else:
            i -= 1

    return

sets1 = [1, 2, 3, 4, 5]
sets2 = [1]

for subset in chain.from_iterable(anotherCombinations(sets1, n) for n in range(len(sets1)+1)):
    print("output:  ", subset)
print("------")
for subset in anotherCombinations(sets2, 1):
    print("output:  ", subset)
