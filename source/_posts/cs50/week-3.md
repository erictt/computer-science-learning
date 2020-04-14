# Week 3

## Computational Complexity

* worst-case scenario: \\(O\\)
* best-case scenario: \\(\Omega\\)
* theta, \\(\Theta\\), if the running time of an algorithm is the same in the worst-case (\\(\Omega\\)) and the best-case (\\(O\\)).
* We don't actually care about how complex the algorithm is precisely, only it's tendency, which dictated by the highest-order term.
    * for example, \\(n^3\\), \\(n^3+n^2\\), \\(n^3-8n^2+20n\\). when `n` is 1,000,000, the values will be \\(1.0*10^{18}\\), \\(1.000001*10^{18}\\) and \\(9.99992*10^{17}\\). The lower terms became really irrelevant. So we only take the highest-order term, which is \\(n^3\\) here.

### Common Classes 

* from fast to slow:
    * \\(O(1)\\) constant time
    * \\(O(\log{n})\\) logarithmic time
        * binary search
    * \\(O(n)\\) linear time
        * linear search
    * \\(O(n\log{n})\\) linearithmic time
        * merge sort 
    * \\(O(n^2)\\) quadratic time
        * bubble sort, selection sort, insert sort
    * \\(O(n^c)\\) polynomial time
    * \\(O(c^n)\\) exponential time 
    * \\(O(n!)\\) factorial time
    * \\(O(\infty)\\) infinite time
* \\(O(1)<O(\log_{2}{n})<O(n)<O(n\log_{2}{n})<O(n^2)<O(n^3)<…<O(2^n)<O(n!)\\)
* More comparisons: [https://en.wikipedia.org/wiki/Sorting_algorithm#Comparison_of_algorithms](https://en.wikipedia.org/wiki/Sorting_algorithm#Comparison_of_algorithms)

## Search

### Linear Search

```
for each element in array
    if element you're looking for
        return true
return false
```

### Binary Search

```
look at middle of array
if element you're looking for
    return true
else if element is to left
    search left half of array
else if element is to right
    search right half of array
else
    return false
```   

## Sorting

### Selection Sort

* find the smallest element, and move it to the front of the list and shift the other ones down, until hit the end.

```
for i from 0 to n-1
    find smallest element between i'th and n-1'th
    swap smallest with i'th element
```    
   
## Bubble Sort

* from left to right and compare each pair of numbers. If they are out of order, then swap them. 

```
repeat until no swaps
    for i from 0 to n-2
        if i'th and i+1'th elements out of order
            swap them
```  

## Insertion Sort

* Each time, we look at the next element and place it into our sorted portion of the list, even if we have to shift elements.

```
for i from 1 to n-1
    call 0'th through i-1'th elements the "sorted side"
    remove i'th element
    insert it into the sorted side in order
```    
## Merge Sort

* First divide the list into the smallest unit (1 element), then compare each element with the adjacent list to sort and merge the two adjacent lists. Finally all the elements are sorted and merged.

```
on input of n elements
    if n < 2
        return
    else
        sort left half of elements
        sort right half of elements
        merge sorted halves
```

* An example:

    ![week-3-2](https://i.imgur.com/GViydxe.gif)

* Calculate the complexity: \\(\Theta(n\log{n})\\):
    
    ![week-3-1](https://i.imgur.com/e59kMdy.png)
    
    * `c` is the single step takes. In this case, c = 1, cause we only need to put an element into memory. 
    * Then use formula: `T(n) = T(n/2) + T(n/2) + n`. 
        * `n` means every layer will take `n` steps. When the array has been separated as one by one, we will need `1 * n` steps to sort them all, then `2 * n/2` steps, then `4 * n/4` step. So every steps will take `n` steps to sort.
        * \\[\begin{aligned}
            T(n) &= 2 * T(\frac{n}{2}) + n \\
                &= 2^2 * T(\frac{n}{2^2}) + 2n \\
                &=\ ... \\
                &= 2^{\log_2{n}} * T(\frac{n}{2^{\log_2{n}}}) + \log_2{n} * n \\
                &= 2^{\log_2{n}} * 1 + n\log_2{n} \\
                &= n + n\log_2{n} \\
            \end{aligned}\\].
        * So the complexity will be : \\(O(n\log{n}+n) = O(n\log{n})\\).

* [Implement with C](https://gist.github.com/erictt/2c4387dba45586b967ae2efe7bb94bc7)
* [Implement with Python 3](https://gist.github.com/erictt/0438c9db11b3b25f0e24c212d8f3c3b9)

## Quick Sort

```
pick an element called a pivot from array
partition the array with pivot
   if element i > pivot
       move to right
in the end swap the pivot to middle()
recursively apply steps before to the left and the right sub-array without pivot
```   

![Sorting_quicksort_anim.gif](https://upload.wikimedia.org/wikipedia/commons/6/6a/Sorting_quicksort_anim.gif)

* [Implement with C](https://gist.github.com/erictt/daede65d8178a93a25a5e52ed07d69aa) 
* [Implement with Python 3](https://gist.github.com/erictt/0438c9db11b3b25f0e24c212d8f3c3b9)

## Refers
* [CS50/week 3](http://docs.cs50.net/2016/fall/notes/3/week3.html)
* [Sorting_algorithm - Wikipedia](https://en.wikipedia.org/wiki/Sorting_algorithm)
* [Merge_sort - Wikipedia](https://en.wikipedia.org/wiki/Merge_sort)
* [Quicksort - Wikipedia](https://en.wikipedia.org/wiki/Quicksort)
* [Comparison Sorting Visualization](https://www.cs.usfca.edu/~galles/visualization/ComparisonSort.html)


