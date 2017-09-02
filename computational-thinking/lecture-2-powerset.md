# Power Set Functions

[TOC]

* Use the position of `1` in bites to calculate all the possibilities of combinations in a list.
    * like five bits `0 0 0 0 0` to indicate all the items' positions, and `1` can be every position in the bits. All the combinations should be the Powerset we want to, then use `>>` to check every combination's position whether it is 1 or not.

    ```python
    def powerSet(items):
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
            yield combo
    ```
    
    
* Use `itertools.combinations` to calculate r length subsequences of elements, then iterate with different length.

    * the function of `combinations` is a little complicated, added some notations to help me to understand.

    ```python
    from itertools import chain
    
    def powerset_generator(sets):
        for subset in chain.from_iterable(combinations(sets, r) for r in range(len(sets)+1)):
            yield subset
            
    # the logic of this function is 
    #   set a new array with length r
    #   loop the last element's index from i to i+n-r(n is the length of pool, r is the length of subsequence). 
    #   when hit the maximum which should be n-1, increase the last-1 element's index.
    #   loop until the first element's index hit the maximum, 
    #   then increase the previous index, and set the last index to previous index + 1, 
    #   then back to the loop until all of the indices hit the maximum
    # For example: iterable = [1,2,3,4,5], r = 3
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
    def combinations(iterable, r):
        
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
    ```




