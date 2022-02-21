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

#### Deterministic ﬁnite state automaton (DFA)

* DFA is abstract string-searching machine.
    * Finite number of states (including start and halt). 
    * Exactly one transition for each char in alphabet. 
    * Accept if sequence of transitions leads to halt state.
* <img src="https://i.imgur.com/iQbPA0S.jpg" style="width:550px" />
* State = number of characters in pattern that have been matched.
* <img src="https://i.imgur.com/6vrBVW6.jpg" style="width:550px" />

#### How to build DFA from pattern?

* <img src="https://i.imgur.com/2UAcaAu.jpg" style="width:600px" />

* <img src="https://i.imgur.com/ZnczNtP.jpg" style="width:600px" />
    
    * Every mismatch, is to re-simulate the the pattern without first character, and end with the new mismatch character. So we can simulate the process, and copy the result to the new column.
* Java implementation
    * <img src="https://i.imgur.com/82lptvD.jpg" style="width:500px" />
        
        * copy mismatch: 
            * <img src="https://i.imgur.com/KtVYneb.jpg" style="width:200px" />



### Boyer-Moore

* **Intuition**.
    * Scan characters in pattern from right to left.
    * Can skip as many as M text chars when finding one not in the pattern.
    * <img src="https://i.imgur.com/VjXkKod.jpg" style="width:600px" />
* How much to skip?
    * if the pattern doesn't have repeat letter, we can only check the rightmost letter, and perform full check when we hit the rightmost match.
    * But if the pattern has repeat letter, like the example: NEEDLE. We will need to move the pointer carefully:
        * <img src="https://i.imgur.com/GfnPQTz.jpg" style="width:400px" />
        * The ultimate solution:
            * <img src="https://i.imgur.com/oaDW74R.jpg" style="width:600px" />
            * every time we occurred an `E` mismatch, backup 5 positions.
* Java implementation
    * <img src="https://i.imgur.com/5wbMyZN.jpg" style="width:500px" />

* KMP substring search analysis
    * KMP substring search accesses no more than **M + N** chars to search for a pattern of length M in a text of length N.

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
