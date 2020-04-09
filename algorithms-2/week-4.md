# Week 4 - Tries & Substring Search

[TOC]

## Tries 

* Store characters in nodes (not keys).
* Each node has **R** children, one for each possible character.
    * `int R = 256; // extended ASCII`
* <img src="media/15450063487090.jpg" style="width:600px" />

### Ternary search tries

* Store characters and values in nodes (not keys).
* Each node has **3** children: smaller (left), equal (middle), larger (right).
* <img src="media/15450069948192.jpg" style="width:550px" />

#### TST with R^2 branching at root

* Hybrid of R-way trie and TST.
    * Do R^2 -way branching at root.
    * Each of R^2 root nodes points to a TST.
* <img src="media/15450072105593.jpg" style="width:550px" />

### Character-based Operations

* Prefix match. 
    * Find all keys in a symbol table starting with a given prefix.
    * <img src="media/15450074670385.jpg" style="width:600px" />

* Longest prefix.
    * Find longest key in symbol table that is a prefix of query string.
    * <img src="media/15450076011107.jpg" style="width:600px" />

* Wildcard match.
    * // TODO

## Substring Search

### Brute-force substring search

* Check for pattern starting at each text position.
* <img src="media/15450077666182.jpg" style="width:400px" />
* Brute-force algorithm needs **backup** for every mismatch.
    * <img src="media/15450078113176.jpg" style="width:400px" />
    * <img src="media/15450078456229.jpg" style="width:500px" />

### Knuth-Morris-Pratt (KMP)

#### Deterministic ﬁnite state automaton (DFA)

* DFA is abstract string-searching machine.
    * Finite number of states (including start and halt). 
    * Exactly one transition for each char in alphabet. 
    * Accept if sequence of transitions leads to halt state.
* <img src="media/15450079972578.jpg" style="width:550px" />
* State = number of characters in pattern that have been matched.
* <img src="media/15450081515164.jpg" style="width:550px" />

#### How to build DFA from pattern?

* <img src="media/15450184526200.jpg" style="width:600px" />

* <img src="media/15450148108106.jpg" style="width:600px" />
    * Every mismatch, is to re-simulate the the pattern without first character, and end with the new mismatch character. So we can simulate the process, and copy the result to the new column.
* Java implementation
    * <img src="media/15450148564532.jpg" style="width:500px" />
        * copy mismatch: 
            * <img src="media/15450201509853.jpg" style="width:200px" />



### Boyer-Moore

* **Intuition**.
    * Scan characters in pattern from right to left.
    * Can skip as many as M text chars when finding one not in the pattern.
    * <img src="media/15450094103139.jpg" style="width:600px" />
* How much to skip?
    * if the pattern doesn't have repeat letter, we can only check the rightmost letter, and perform full check when we hit the rightmost match.
    * But if the pattern has repeat letter, like the example: NEEDLE. We will need to move the pointer carefully:
        * <img src="media/15450145710882.jpg" style="width:400px" />
        * The ultimate solution:
            * <img src="media/15450146025670.jpg" style="width:600px" />
            * every time we occurred an `E` mismatch, backup 5 positions.
* Java implementation
    * <img src="media/15450146913445.jpg" style="width:500px" />



### Rabin-Karp

#### Basic idea = modular hashing

* Compute a hash of pattern characters `0` to `M - 1`.
* For each `i`, compute a hash of text characters `i` to `M + i - 1`. 
* If pattern hash = text substring hash, check for a match.
* <img src="media/15450086180197.jpg" style="width:400px" />

#### Modular hash function

* Using the notation `t_i` for `txt.charAt(i)`, we wish to compute
    * <img src="media/15450089079063.jpg" style="width:320px" />
* **Horner's method**. Linear-time method to evaluate degree-M polynomial.
    * <img src="media/15450089623754.jpg" style="width:600px" />
* **Efficiently computing the hash function**
    * Can update hash function in constant time!
    * <img src="media/15450090056983.jpg" style="width:450px" />

#### How to handle hash collision?

1. **Monte Carlo version**. Return match if hash match.
    * It is possible return the wrong answer.
2. **Las Vegas version**. Check for substring match if hash match; continue search if false collision.
    * Confidence about the answer, but also cost more time to verify.

### Summary

* Cost of searching for an M-character pattern in an N-character text.
* <img src="media/15450084388469.jpg" style="width:600px" />
