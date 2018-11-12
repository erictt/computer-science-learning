# Stacks and Queues & Elementary Sorts

[TOC]

## Stacks and Queues

### Stacks

* Stack of strings data type.
* <img src="media/15398926036988.jpg" style="width:500px" />
* Two ways to implement:
    * **Linked List**: Maintain pointer to first node in a linked list; insert/remove from front.
    * **Array**: Use array s[] to store N items on stack.
        * Defect: Stack overflows when N exceeds capacity. 
* Overflow and underflow.
    * Underflow: throw exception if pop from an empty stack.
    * Overflow: use resizing array for array implementation. 
* **Null items**. We allow null items to be inserted. 
* **Loitering**(Java). Holding a reference to an object when it is no longer needed. 
    * <img src="media/15398930391449.jpg" style="width:500px" />
    * Already pop up the N-th item, should set it null before return.

#### Resizing Array Stack

* push(): double size of array s[] when array is full.
* pop(): halve size of array s[] when array is one-quarter full.
* Array is between 25% and 100% full.

### Queues

* <img src="media/15398935073469.jpg" style="width:500px" />

* Two ways to implement:
    * **Linked List**: Maintain pointer to first and last nodes in a linked list;
    * **Array**: 
        * Use array q[] to store items in queue.
        * enqueue(): add new item at q[tail].
        * dequeue(): remove item from q[head].
        * Update head and tail modulo the capacity.
        * Add resizing array.
        * Q. How to resize?
            * create another array with double size of the original array and duplicate all of the nodes in the new array
            * create another array as the second array, and create a linkedlist to link the first queue and the second queue.

### Generics 

// ignore

### Iterators

* Has methods hasNext() and next().

### Applications(Dijkstra's two-stack algorithm)

* <img src="media/15398940938016.jpg" style="width:600px" />

## Elementary Sorts

### Selection Sort

* In iteration **i**, find index **min** of smallest remaining entry.
・Swap a[i] and a[min].

### Insertion sort 

* Assume left side is already sorted, then in iteration **i**, swap a[i] to the left if a[i] < a[i-1]

### Shellsort 

* Move entries more than one position at a time by **h-sorting** the array.
* <img src="media/15398957020735.jpg" style="width:600px" />
* Shellsort: which increment sequence to use?
    * 3x + 1. 1, 4, 13, 40, 121, 364, …
        * OK. Easy to compute.
    * Sedgewick. 1, 5, 19, 41, 109, 209, 505, 929, 2161, 3905, …
        * Good. Tough to beat in empirical studies.

### Shuffle

* One way is: Generate a random real number for each array entry, then sort the array.
    * Defect: sorting.
* Better way: **Knuth shuffle**
    * In iteration **i**, pick integer **r** between **0** and **i** uniformly at random.
    * Swap **a[i]** and **a[r]**.
    * <img src="media/15398971232285.jpg" style="width:500px" />
* <img src="media/15398971898786.jpg" style="width:600px" />

### Convex hull

* The convex hull of a set of N points is the smallest perimeter fence
enclosing the points.
    * <img src="media/15398973135529.jpg" style="width:400px" />

#### Convex hull application

* **Robot motion planning**. Find shortest path in the plane from **s** to **t** that avoids a polygonal obstacle.
    * <img src="media/15398974522939.jpg" style="width:400px" />

* **Farthest pair problem**. Given N points in the plane, find a pair of points with the largest Euclidean distance between them.
    * <img src="media/15398974766839.jpg" style="width:300px" />

* **Geometric properties**
    * Fact. Can traverse the convex hull by making only counterclockwise turns.
    * Fact. The vertices of convex hull appear in increasing order of polar angle with respect to point p with lowest y-coordinate.
    * <img src="media/15398974872043.jpg" style="width:300px" />

#### Graham scan demo

* Choose point p with smallest y-coordinate.
* Sort points by polar angle with p.
* Consider points in order; discard unless it create a counterclockwise turn.
* <img src="media/15399011032241.jpg" style="width:300px" />


* Given three points a, b, and c, is a → b→ c a counterclockwise turn?
    * <img src="media/15399012505804.jpg" style="width:600px" />
    * <img src="media/15399013148171.jpg" style="width:600px" />

