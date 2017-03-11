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
        
def myCombinations(iterable, r):
    
    # first, we need to understand, this function is to record every possibility of indices
    # then return the elements with the indices
    
    pool = tuple(iterable)
    
    n = len(pool)
    
    if r > n:
        return
    indices = list(range(r))

    # yield the first permutation, 
    # cause in the "while" circle, we will start to change the indices by plus 1 consistently
    # for example: iterable is [1, 2, 3, 4, 5], and r = 3
    # this yield will return [1, 2, 3], but in the "while" loop, 
    # we will start to update last elements' index to 4, which will return [1, 2, 4]
    yield tuple(pool[i] for i in indices)
    
    while True:

        # in this for loop, we want to confirm whether indices[i] can be increased or not
        for i in reversed(range(r)):
            
            # after reversed, i will be r-1, r-2, r-3, ....,0
            # something we should know before we start the 'for' loop
            # the value of indices[r-1] should not greater than n-1
            # the value of indices[r-2] should not greater than n-2
            # and the maximum of indices[i] should be indices[r-1]
            # so the value of indices[r-1] should between r-1 and n-r + r-1, like this:
            #       r-1 <= indics[r-1] <= n-r + r-1
            # so, to r-2:
            #       r-2 <= indics[r-1] <= n-r + r-2
            # let's set i = r-1:
            #       i <= indices[i] <= n-r+i (n-1 is the maximum value)
            # since we will keep plusing the value of indices[i], let's ignore i <= indices[i]
            # and we just want to know if indices[i] can plus or not,
            # so indices[i] can be equal with n-r+i
            # then we got:
            #       indices[i] < i + n - r
            # the offical document give: indices[i] != i + n - r,
            # cause when indices[i] == i + n - r, it arrived the boundry, 
            # the "for" loop will get into indices[i-1], there will be no judgement for ">i+n-r"
            # so to use indices[i] != i + n - r is still a good way, 
            # but i prefer indices[i] < i + n - r, which is easier to understand for me.
            # so next question is "break" in here, 
            # it means the value of indices[i] doesn't reach the boundry still can plus one,
            # let break out to continue the iteration
            # when it hit the boundry, i will be r-2
            # So we can see the result:
            # 1, 2, 3
            # 1, 2, 4
            # 1, 2, 5
            # 1, 3, 4
            # always loop the last index, hit the boundry, check the last but one.
            if indices[i] < i + n - r:
                break
        else:
            # loop finished, return
            return
        
        # first of all, plus one for current indices[i], 
        # that's why we yield the first permutation, before the while loop
        # and increase every indices[i] by 1
        indices[i] = indices[i] + 1
        # this for loop is increase every indices which is after indices[i].
        # cause, current index increased, and we need to confirm every one behind is orderd
        # for example: current we got i = 2, indices[i]+1 will be 3, 
        # so the next loop will start with [1, 3, 4], not [1, 3, 3]
        for j in range(i+1, r):
            indices[j] = indices[j-1] + 1
            
        yield tuple(pool[i] for i in indices)  

sets = [1, 2, 3, 4, 5]

for i in myCombinations(sets, 3):
    print("output:  ", i)


#for i in powerset_generator(sets):
#    print("output:  ", i)
#    print("==============o=========\n")


