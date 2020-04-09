# Lecture 1

[TOC]

## Computational Models

* Optimization models
* Statistical models
* Simulation models

### Optimization Models

* An objective function that is to be maximized or minimized, e.g.,
    * Minimize time spent traveling from New York to Boston
* A set of constraints (possibly empty) that must be honored, e.g.,
    * Cannot spend more than $100
    * Must be in Boston before `5:00PM`

### Knapsack Problem

* You have limited strength, so there is a maximum weight knapsack that you can carry
* You would like to take more stuff than you can carry
* How do you choose which stuff to take and which to leave behind?
* Two variants
    * 0/1 knapsack problem
    * Continuous or fractional knapsack problem

### 0/1 Knapsack Problem, Formalized

* Each item is represented by a pair, `<value, weight>`
* The knapsack can accommodate items with a total weight of no more than `w`
* A vector, `L`, of length n, represents the set of available items. Each element of the vector is an item
* A vector, `V`, of length n, is used to indicate whether or not items are taken. If **V[i] = 1**, item **I[i]** is taken. If **V[i] = 0**, item **I[i]** is not taken
* Find a `V` that Maximizes:
    * \\(\displaystyle\sum_{i=0}^{n-1}V[i]*I[i].\text{value}\\) 
    * Subject to the constraint that:
        * \\(\displaystyle\sum_{i=0}^{n-1}V[i]*I[i].\text{weight} \le w\\) 

## Brute Force Algorithm

* Procedure:
    * 1. Enumerate all possible combinations of items. That is to say, generate all subsets of the set of subjects. This is called the **power set**.
    * 2. Remove all of the combinations whose total units exceeds the allowed weight.
    * 3. From the remaining combinations choose any one whose value is the largest.
* Dark Side:
    * Will take a considerable time to get the power set.
    * There will lots of `V`s to indicate whether or not items are taken.

## Greedy Algorithm

* Put “**best**” available item in knapsack
* Procedure:
    * Define what the best means.
    * Sort the items.
    * Take the items from the best to the worst, stop when it hit the maximum.
* Dark Side:
    * Sequence of locally “optimal” choices don’t always yield a globally optimal solution

