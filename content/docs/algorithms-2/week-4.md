---
weight: 1
title: "Week 4 - Tries & Substring Search"
---

# Week 4 - Tries & Substring Search

## Tries 

* [from re**trie**val, but pronounced "try"]
* Store characters in nodes (not keys).
* Each node has **R** children, one for each possible character.
    * `int R = 256; // extended ASCII`
* <img src="https://i.imgur.com/jSIIGuR.jpg" style="width:600px" />

### Java implementation

```java
public class TrieST<Value> {

    private static final int R = 256; // extended ASCII
    private Node root = new Node();
    
    private static class Node { 
        private Object value; // use Object instead of Value since no generic array creation in Java
        private Node[] next = new Node[R]; // each node has an array of links and a value
    }
    
    public void put(String key, Value val) { root = put(root, key, val, 0); }
    
    private Node put(Node x, String key, Value val, int d) { 
        if (x == null) x = new Node(); 
        if (d == key.length()) { x.val = val; return x; } 
        char c = key.charAt(d); 
        x.next[c] = put(x.next[c], key, val, d+1); 
        return x; 
    }
    
    public boolean contains(String key) { return get(key) != null; }
    
    public Value get(String key) {
        Node x = get(root, key, 0);
        if (x == null) return null;
        return (Value) x.val;  // cast needed
    }
    
    private Node get(Node x, String key, int d) { 
        if (x == null) return null; 
        if (d == key.length()) return x; 
        char c = key.charAt(d); 
        return get(x.next[c], key, d+1); 
    }
}
```

* Performance: Fast search hit and even Trie representation faster search miss, but wastes space.

* Deletion in an R-way trie
    * Find the node corresponding to key and set value to null.
    * If node has null value and all null links, remove that node (and recur).
    * <img src="https://i.imgur.com/Dla0UOL.jpg" style="width:500px" />


### Ternary search tries(TST)

* To solve the problem that R-way tries took too much space.
* Store characters and values in nodes (not keys).
* Each node has **3** children: smaller (left), equal (middle), larger (right).
* <img src="https://i.imgur.com/oXo6XIl.jpg" style="width:600px" />
* Java implementation

    ```java
    public class TST<Value> { private Node root;
        private class Node {
            private Value val;
            private char c;
            private Node left, mid, right; 
        }
        
        public void put(String key, Value val) { root = put(root, key, val, 0); }
        
        private Node put(Node x, String key, Value val, int d) {
            char c = key.charAt(d); 
            if (x == null) { x = new Node(); x.c = c; } 
            if (c < x.c) x.left = put(x.left, key, val, d); 
            else if (c > x.c) x.right = put(x.right, key, val, d); 
            else if (d < key.length() - 1) x.mid = put(x.mid, key, val, d+1); 
            else x.val = val;
            return x;
        }
        
        public boolean contains(String key) { return get(key) != null; }
        
        public Value get(String key) {
            Node x = get(root, key, 0);
            if (x == null) return null;
            return x.val; 
        }
        
        private Node get(Node x, String key, int d) {
            if (x == null) return null; 
            char c = key.charAt(d); 
            if (c < x.c) return get(x.left, key, d); 
            else if (c > x.c) return get(x.right, key, d); 
            else if (d < key.length() - 1) return get(x.mid, key, d+1); 
            else return x;
        }
    
    }
    ```

#### TST with R^2 branching at root

* Hybrid of R-way trie and TST.
    * Do R^2 -way branching at root.
    * Each of R^2 root nodes points to a TST.
* <img src="https://i.imgur.com/pXgm3LU.jpg" style="width:600px" />

#### String symbol table implementation cost summary

<img src="https://i.imgur.com/cBcTtvv.jpg" style="width:500px" />

* TST vs. hashing
    * Hashing.
        * Need to examine entire key.
        * Search hits and misses cost about the same.
        * Performance relies on hash function.
        * Does not support ordered symbol table operations.
    * TSTs.
        * Works only for strings (or digital keys).
        * Only examines just enough key characters.
        * Search miss may involve only a few characters. 
        * Supports ordered symbol table operations (plus others!).
    * Bottom line. TSTs are:
        * Faster than hashing (especially for search misses). 
        * More flexible than red-black BSTs. 

### Character-based Operations

* Prefix match. Find all keys in a symbol table starting with a given prefix.
    * <img src="https://i.imgur.com/P4cMOAB.jpg" style="width:600px" />

* Longest prefix. Find longest key in symbol table that is a prefix of query string.
    * <img src="https://i.imgur.com/L2406ZN.jpg" style="width:600px" />

* Wildcard match. Keys that match .he: she and the.



## Substring Search

* Goal. Find pattern of length M in a text of length N.
    * typically N >> M

### Brute-force substring search

* Check for pattern starting at each text position.
* <img src="https://i.imgur.com/1gp7R29.jpg" style="width:400px" />
    
    * worst case: ~M N char compares.
* Brute-force algorithm needs **backup** for every mismatch.
    * <img src="https://i.imgur.com/SbLNDHL.jpg" style="width:400px" />
* alternate implementaion for backup.
    * <img src="https://i.imgur.com/BiiApQ3.jpg" style="width:500px" />

### Knuth-Morris-Pratt (KMP)

Use DFA to match the pattern in string in linear time.

#### Deterministic ﬁnite state automaton (DFA)

* DFA is abstract string-searching machine.
    * <img src="https://i.imgur.com/iQbPA0S.jpg" style="width:550px" />

    * **State** = number of characters in pattern that have been matched.
        * e.g. 3 means 3 chars have been matcheed, aka `A B A`.
    * EXACTLY one state **transition** for each char to another in alphabet from left to right. 
    * When mismatch, the state will go back to the state that has the maximum matches so far.
        * e.g. state 5. if follow by B, the state will go to 4, because `ABABAB` still has the `ABAB` matches which is state 4.

    * Java code for search the pattern:
        * <img src="https://i.imgur.com/6vrBVW6.jpg" style="width:550px" />
        * In the loop, we only augment i, and keep updating j until either i = N or j = M.

#### How to build DFA from pattern?

* <img src="https://i.imgur.com/2UAcaAu.jpg" style="width:600px" />

* <img src="https://i.imgur.com/ZnczNtP.jpg" style="width:600px" />
    
    * State **X** is used for simulating when state **j** goes mismatch. Why?
        * For example, when j=5, we have matched pattern: `ABABA`. If the next char is not `C`, we have a mismatch. Then we need to match `BABA` (without the start A) in the existing previous pattern.
            * Why omit the first `A`? Think about how we do brute-force. after a mismatch, we restart the match with i+1. the same idea here.
        * The straightforward way is to run a loop to rematch BABA then deciding where the new mismatch char should go. But a genious way is to mark a state `X` in the previous path so every time we only need to check how the last char(j) goes in the `X` state for mismatching.
            * Take 5 as an example. we can simply tell where a mismatch goes by simulating `3` because `BABA` ends with matching 3 elements(As showed in the graph). We only need to check where the state will go for a mismatch and copy over the mismatch to state 5.
        * The next question is, how to find the state `X` without loop the whole [1,j-1] in the pattern?
            * Think about how to get X for state 5? We simulate `BABA` then check the mismatch of that state column. So what about X for state 4? we need to simulate `BAB`, right?
            * You can see to simulate `BABA`, we need to check the state for `BAB` and check where `A` goes on that state. Same as `BAB`, we need to find the state for `BA` at first, then check where the `B` goes. 
            * So if we reverse the process, simulating `B` can be used for checking mismatch of `AB_`, simulating `BA` can be used for checking mismatch of `ABA_`, simulating `BAB` can be used for checking mismatch of `ABAB_`. 
            * We don't actually need to loop every element for searching state **X** but record the state of the previous match, and check the new element in the state which will be our state **X** for the next state's mismatch. e.g.
                * [B][0] = 0, then the mismatch of `AB_` check the state `0`.
                * [A][0] = 1, then the mismatch of `ABA_` check the state `1`.
            * Why not calculate state for `A_`? because [i,j-1] is empty which means X = 0.
        * Let's loop from the beginning. 
            * when j = 0, nothing need to be done, the only match is A, and the others are 0. So we initialize X = 0.
            * When j = 1, we copy over the mismatches from state 0(X=0) to state 1. And mark X = dfa[B][0] = 0 meaning we finished the matching of [B], the next state can use the result as X.
            * When j = 2, we copy over the state 0 to state 2 as well. Notice that the mismatch is base on state 2, not 0. So for state 2, we only copy B, C, etc.., then set X = dfa[A][0] = 1 because after matching [BA] the state reached 1
            * When j = 3, we need to know what a match of [1, 2] looks like. [1, 2] = [BA] which already been set up in the last loop which X = 1. So we only need to copy over state 1 to 3, and then find the new X. X = state of [BAB] = dfa[B][1] = 2
            * When j = 4, same as last loop. Copy over, and set up X = state of [BABA] = dfa[A][2] = 3
            * Whey j = 5, copy over, and set up X = state of [BABAC] = dfa[C][3] = 0
                * <img src="https://i.imgur.com/KtVYneb.jpg" style="width:400px" />
* Java implementation
    
    ```java
    public class KMP {

        private String pat; 
        private int[][] dfa;
        
        public KMP(String pat) {
            // Build DFA from pattern.
            this.pat = pat;
            int M = pat.length();
            int R = 256; // ASCII, the graph only shows A, B and C, but it's actually 256 characters
            dfa = new int[R][M]; // initialized with zeros as default
            dfa[pat.charAt(0)][0] = 1; // only update the match case to 1
            
            // then we start j at 1 since j = 0 already been initialized above
            for (int X = 0, j = 1; j < M; j++) {
                // Compute dfa[][j].
                // Copy over all cases including mismatch cases.
                // when j = 1, the state X is dfa[1][0] = 0. so if there is a mismatch, it will return to state 0 which is A->1, B->0*, C->0.
                // notice we set up B to 0 in the loop, 
                // it's only for convenience, and will overwrite it later on.
                for (int c = 0; c < R; c++)
                    dfa[c][j] = dfa[c][X]; 
                dfa[pat.charAt(j)][j] = j+1; // Overwrite the match case.
                // j = 1, pat.charAt(j) = B, X = 0, dfa[pat.charAt(j)][X] = 0;
                // j = 2, pat.charAt(j) = A, X = 0, dfa[pat.charAt(j)][X] = 1;
                // j = 3, pat.charAt(j) = B, X = 1, dfa[pat.charAt(j)][X] = 2;
                // j = 4, pat.charAt(j) = A, X = 2, dfa[pat.charAt(j)][X] = 3;
                // j = 5, pat.charAt(j) = C, X = 3, dfa[pat.charAt(j)][X] = 0;
                // j = 6, pat.charAt(j) = _, X = 0, dfa[pat.charAt(j)][X] = _;
                // The goal is to mark the match state of `[1, j]` in the current loop, 
                // so we can fill out the mismatch for j+1 in the next loop,
                // because the mismatch of j+1 = the matching result of the state for [1-j].
                X = dfa[pat.charAt(j)][X]; // Update restart(X) state.
            }
        }
        
        public int search(String txt) { 
            // Simulate operation of DFA on txt.
            int i, j, N = txt.length(), M = pat.length();
            for (i = 0, j = 0; i < N && j < M; i++)
                j = dfa[txt.charAt(i)][j];
            if (j == M) return i - M; // found (hit end of pattern)
            else return N; // not found (hit end of text)
        }
    }
    ```

* Cost analysis
    * KMP substring search accesses no more than **M + N** chars to search for a pattern of length M in a text of length N.

### Boyer-Moore

* **Intuition**.
    * Scan characters in pattern from right to left.
    * Can skip as many as M text chars when finding one not in the pattern.
    * <img src="https://i.imgur.com/VjXkKod.jpg" style="width:600px" />
* How much to skip?
    * **Case 1.** Mismatch character not in pattern.
        * mismatch character 'T' not in pattern: increment i one character beyond 'T' which measn i = j+1, j = length of the pattern.
        * <img src="https://i.imgur.com/1VFgLt8.jpg" style="width:500px" />
    * **Case 2a.** Mismatch character in pattern.
        * mismatch character 'N' in pattern: align text 'N' with **rightmost** pattern 'N'. 
        * <img src="https://i.imgur.com/2VSMgxN.jpg" style="width:500px" />
        * In the example above, `i += 3`. The comparing loop start from the right where `j = 5`. When mismatch, `j = 3` and the mismatched element `N`'s index = 0. So `i += (3 - 0)`.
        * So how to get 3?
            * First of all, we match text from right to left, as `j` is the index in the loop from `pattern.length-1` to `0`.
            * When the rightmost element didn't match `text[i]`, but `text[i]` is still in the pattern, we will augment i by `j - (index of the matched element in the pattern)`.
            * If there are some repeated elements in the pattern, we will choose the rightmost one to avoid missing matches.
                * The refined equation becomes: `i += j - (index of the rightmost matched element in the pattern)`.
            * There is another special case which will be demonstrated below:
    * **Case 2b.** Mismatch character in pattern.
        * <img src="https://i.imgur.com/GfnPQTz.jpg" style="width:500px" />
        * You can see, if we align 'E' to the rightmost pattern 'E', the pattern will skip '-2' since j = 3 and the index of the rightmost E = 5.
        * So instead of skiping a nagative number, we increment i by 1.
        * Then the i-update becomes `i += Max(1, j - (index of the rightmost matched element in the pattern))`;
    * To make the computation easier, we create a `right[]` to record the `(index of the rightmost matched element in the pattern)`:
        * Precompute index of rightmost occurrence of character `c` in pattern (`-1` if character not in pattern, meaning we skip `j-(-1) = j+1`).
        * <img src="https://i.imgur.com/oaDW74R.jpg" style="width:600px" />
        * You can see `E` occured three times, but we choose the rightmost one's index as the one for calculation.
            * i.e. every time an `E` mismatch occurrs, backup `Max(1, 5-5) = 1` positions.
* Java implementation
    * <img src="https://i.imgur.com/5wbMyZN.jpg" style="width:500px" />
* Worst-case. Can be as bad as ~ M N.
    * <img src="https://i.imgur.com/yM0saDs.jpg" style="width:400px" />


### Rabin-Karp

#### Basic idea = modular hashing

* Compute a hash of pattern characters `0` to `M - 1`.
* For each `i`, compute a hash of text characters `i` to `M + i - 1`. 
* If pattern hash = text substring hash, check for a match.
* <img src="https://i.imgur.com/qaOndBe.jpg" style="width:400px" />

#### Modular hash function

* Using the notation `t_i` for `txt.charAt(i)`, we wish to compute
    * <img src="https://i.imgur.com/SoaS8eU.jpg" style="width:320px" />
* **Horner's method**. Linear-time method to evaluate degree-M polynomial.
    * <img src="https://i.imgur.com/xGWs0e2.jpg" style="width:600px" />
* **Efficiently computing the hash function**
    * Can update hash function in constant time!
    * <img src="https://i.imgur.com/dSHqctb.jpg" style="width:450px" />
    * <img src="https://i.imgur.com/ft4sFke.jpg" style="width:450px" />

* Java implementation

```java
public class RabinKarp {
    private long patHash; // pattern hash value
    private int M; // pattern length
    private long Q; // modulus
    private int R; // radix
    private long RM; // R^(M-1) % Q

    public RabinKarp(String pat) { 
        M = pat.length(); 
        R = 256; 
        Q = longRandomPrime(); // a large prime (but avoid overflow)

        RM = 1; 
        for (int i = 1; i <= M-1; i++) // precompute R M – 1 (mod Q)
            RM = (R * RM) % Q; 
        patHash = hash(pat, M);
    }
    
    // Compute hash for M-digit key
    private long hash(String key, int M) { 
        long h = 0;
        for (int j = 0; j < M; j++)
        h = (R * h + key.charAt(j)) % Q;
        return h;
    }

    // check for hash collision using rolling hash function
    public int search(String txt) {
        int N = txt.length(); 
        int txtHash = hash(txt, M); 
        if (patHash == txtHash) return 0; 
        for (int i = M; i < N; i++) {
            txtHash = (txtHash + Q - RM*txt.charAt(i-M) % Q) % Q;
            txtHash = (txtHash*R + txt.charAt(i)) % Q;
            //  handle hash collision
            // 1. **Monte Carlo version**. Return match if hash match. Runs in linear time.
            //    * It is possible return the wrong answer.
            // 2. **Las Vegas version**. Check for substring match if hash match; continue search if false collision.
            //    * Confidence about the answer, but worst case is **MN**.
            if (patHash == txtHash) return i - M + 1; 
        } 
        return N;
    }
}
```

### Summary

* Cost of searching for an M-character pattern in an N-character text.
* <img src="https://i.imgur.com/F7XoNuo.jpg" style="width:600px" />
