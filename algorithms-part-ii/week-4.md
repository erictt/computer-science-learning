# Week 4 - Tries & Substring Search

\[TOC\]

## Tries

* Store characters in nodes \(not keys\).
* Each node has **R** children, one for each possible character.
  * `int R = 256; // extended ASCII`
* ![](../.gitbook/assets/15450063487090.jpg)

### Ternary search tries

* Store characters and values in nodes \(not keys\).
* Each node has **3** children: smaller \(left\), equal \(middle\), larger \(right\).
* ![](../.gitbook/assets/15450069948192.jpg)

#### TST with R^2 branching at root

* Hybrid of R-way trie and TST.
  * Do R^2 -way branching at root.
  * Each of R^2 root nodes points to a TST.
* ![](../.gitbook/assets/15450072105593.jpg)

### Character-based Operations

* Prefix match.
  * Find all keys in a symbol table starting with a given prefix.
  * ![](../.gitbook/assets/15450074670385.jpg)
* Longest prefix.
  * Find longest key in symbol table that is a prefix of query string.
  * ![](../.gitbook/assets/15450076011107.jpg)
* Wildcard match.
  * // TODO

## Substring Search

### Brute-force substring search

* Check for pattern starting at each text position.
* ![](../.gitbook/assets/15450077666182.jpg)
* Brute-force algorithm needs **backup** for every mismatch.
  * ![](../.gitbook/assets/15450078113176.jpg)
  * ![](../.gitbook/assets/15450078456229.jpg)

### Knuth-Morris-Pratt \(KMP\)

#### Deterministic ﬁnite state automaton \(DFA\)

* DFA is abstract string-searching machine.
  * Finite number of states \(including start and halt\). 
  * Exactly one transition for each char in alphabet. 
  * Accept if sequence of transitions leads to halt state.
* ![](../.gitbook/assets/15450079972578.jpg)
* State = number of characters in pattern that have been matched.
* ![](../.gitbook/assets/15450081515164.jpg)

#### How to build DFA from pattern?

* ![](../.gitbook/assets/15450184526200.jpg)
* ![](../.gitbook/assets/15450148108106.jpg)
  * Every mismatch, is to re-simulate the the pattern without first character, and end with the new mismatch character. So we can simulate the process, and copy the result to the new column.
* Java implementation
  * ![](../.gitbook/assets/15450148564532.jpg)
    * copy mismatch: 
      * ![](../.gitbook/assets/15450201509853.jpg)

### Boyer-Moore

* **Intuition**.
  * Scan characters in pattern from right to left.
  * Can skip as many as M text chars when finding one not in the pattern.
  * ![](../.gitbook/assets/15450094103139.jpg)
* How much to skip?
  * if the pattern doesn't have repeat letter, we can only check the rightmost letter, and perform full check when we hit the rightmost match.
  * But if the pattern has repeat letter, like the example: NEEDLE. We will need to move the pointer carefully:
    * ![](../.gitbook/assets/15450145710882.jpg)
    * The ultimate solution:
      * ![](../.gitbook/assets/15450146025670.jpg)
      * every time we occurred an `E` mismatch, backup 5 positions.
* Java implementation
  * ![](../.gitbook/assets/15450146913445.jpg)

### Rabin-Karp

#### Basic idea = modular hashing

* Compute a hash of pattern characters `0` to `M - 1`.
* For each `i`, compute a hash of text characters `i` to `M + i - 1`. 
* If pattern hash = text substring hash, check for a match.
* ![](../.gitbook/assets/15450086180197.jpg)

#### Modular hash function

* Using the notation `t_i` for `txt.charAt(i)`, we wish to compute
  * ![](../.gitbook/assets/15450089079063.jpg)
* **Horner's method**. Linear-time method to evaluate degree-M polynomial.
  * ![](../.gitbook/assets/15450089623754.jpg)
* **Efficiently computing the hash function**
  * Can update hash function in constant time!
  * ![](../.gitbook/assets/15450090056983.jpg)

#### How to handle hash collision?

1. **Monte Carlo version**. Return match if hash match.
   * It is possible return the wrong answer.
2. **Las Vegas version**. Check for substring match if hash match; continue search if false collision.
   * Confidence about the answer, but also cost more time to verify.

### Summary

* Cost of searching for an M-character pattern in an N-character text.
* ![](../.gitbook/assets/15450084388469.jpg)

