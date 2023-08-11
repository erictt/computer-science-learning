---
weight: 1
title: "Reductions & Linear Programming & Intractability"
---

# Reductions & Linear Programming & Intractability

## Reductions

* **Def**. Problem X **reduces to** problem Y if you can use an algorithm that solves Y to help solve X.
    * <img src="https://i.imgur.com/2jwhrxt.jpg" style="width:400px" />
    * ex1. find the median of N items: sort N items and return the on in the middle.
        * The cost os soloving finding the median is $N\log{N} + 1$. *1 is the cost of reductions.*

### Design Algorithms

* Mentality.
    * Since I know how to solve Y, can I use that algorithm to solve X ?
    * Programmer’s version: I have code for Y. Can I use it for X?
* Examples:
    * Convex hull
        * Given N points in the plane, identify the extreme points of the convex hull (in counterclockwise order).
        * <img src="https://i.imgur.com/JTFiz4E.jpg" style="width:300px" />
        * Solution
            * Graham scan.
                * Choose point p with smallest (or largest) y-coordinate. 
                * Sort points by polar angle with p to get simple polygon. 
                * Consider points in order, and discard those that would create a clockwise turn.
                * <img src="https://i.imgur.com/mrD3N6g.jpg" style="width:600px" />
                * Cost: $N \log{N} + N$ <-- N is the cost of reduction

### Summary

* Reductions are important in theory to:
    * Design algorithms.
    * Establish lower bounds.
    * Classify problems according to their computational requirements.

* Reductions are important in practice to:
    * Design algorithms.
    * Design reusable software modules.
        * stacks, queues, priority queues, symbol tables, sets, graphs
        * sorting, regular expressions, Delaunay triangulation
        * MST, shortest path, maxflow, linear programming
    * Determine difficulty of your problem and choose the right tool.

## Linear Programming 

// SKIP

## Intractability

* Def. 
    * A problem is **intractable** if it can't be solved in polynomial time.
    * **Search problem**. 
        * Given an instance I of a problem, **find** a solution S. 
        * Must be able to efficiently check that S is a solution.
* Problems
    * <img src="https://i.imgur.com/n2sshFz.jpg" style="width:600px" />

### P vs NP

* Def.
    * **NP** is the class of all search problems.
    * **P** is the class of search problems solvable in poly-time.
    * **Nondeterministic** machine can guess the desired solution. 
        * In week 5, we built a NFA for regular expression.
* Does P = NP ?
    * <img src="https://i.imgur.com/mSgsnLt.jpg" style="width:400px" />
    * If P = NP… Poly-time algorithms for SAT, ILP, TSP, FACTOR, …
    * If P ≠ NP… Would learn something fundamental about our universe.
* NP-completeness
    * Def. An NP problem is **NP-complete** if every problem in NP poly-time reduce to it.
    * Implications of Cook-Levin Theorem
        * <img src="https://i.imgur.com/Pzpvnkk.jpg" style="width:600px" />
