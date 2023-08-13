---
weight: 1
title: "Week 5 - Regular Expressions & Data Compression"
---

# Week 5 - Regular Expressions & Data Compression

## Regular Expressions

### DFA vs NFA

- Deterministic finite state automata (DFA);
- Nondeterministic finite state automata (NFA).

- Basic plan:
    1. Build DFA/NFA from RE.
    2. Simulate DFA/NFA with text as input.

- refer to [week 4#knuth-morris-pratt-kmp](/algorithms-2/week-4/#knuth-morris-pratt-kmp) for the DFA implementation
  - Bad news with DFA is, it may have exponential # of states.
- NFA is widely used in modern languages.

### NFA

- Features:
  - RE enclosed in parentheses.
  - One state per Re character (start = 0, accept = M).
  - Red $\color{red}{\epsilon\text{-transition}}$ (change state, but don't scan text);
  - Black match transition (change state and scan to next text char).
  - Accept if **any** sequence of transitions ends in accept state.
- RE:
  - <img src="https://i.imgur.com/OZPphzB.jpg" style="width:600px" />
  - Red directions are $\epsilon$ transition which are stored in a **digraph** G.
    - 0→1, 1→2, 1→6, 2→3, 3→2, 3→4, 5→8, 8→9, 10→11
- The general steps are to find states reachableeither by either match transitions or $\color{red}{\epsilon\text{-transition}}$ alternatively.
- Take `A A B D` as an example to simulate the RE.
  - <img src="https://i.imgur.com/ezeRWid.jpg" style="width:600px" />

#### Java implementation

```java
public class NFA {

    private char[] re; // match transitions
    private Digraph G; // epsilon transition digraph 
    private int M; // number of states
    
    public NFA(String regexp) {
        M = regexp.length();
        re = regexp.toCharArray();
        G = buildEpsilonTransitionDigraph(); 
    }
    
    public boolean recognizes(String txt) {
        Bag<Integer> pc = new Bag<Integer>(); 
        DirectedDFS dfs = new DirectedDFS(G, 0); // states reachable from start by ε-transitions
        for (int v = 0; v < G.V(); v++) 
            if (dfs.marked(v)) pc.add(v);

        for (int i = 0; i < txt.length(); i++) {
            // states reachable after scanning past txt.charAt(i)
            Bag<Integer> match = new Bag<Integer>(); 
            for (int v : pc) {
                if (v == M) continue;
                if ((re[v] == txt.charAt(i)) || re[v] == '.')
                    match.add(v+1); 
            }

            // follow ε-transitions
            dfs = new DirectedDFS(G, match); 
            pc = new Bag<Integer>(); 
            for (int v = 0; v < G.V(); v++) 
                if (dfs.marked(v)) pc.add(v);
        }

        for (int v : pc) 
            if (v == M) return true; // accept if can end in state M
        return false;
    }
    
    private Digraph buildEpsilonTransitionDigraph() { 
        
        Digraph G = new Digraph(M+1); 
        Stack<Integer> ops = new Stack<Integer>(); 
        for (int i = 0; i < M; i++) { 
            int lp = i;
            if (re[i] == '(' || re[i] == '|') ops.push(i); // left parentheses and |
            else if (re[i] == ')') {
                int or = ops.pop(); 
                if (re[or] == '|') { // 2-way or
                    lp = ops.pop();
                    G.addEdge(lp, or+1);
                    G.addEdge(or, i); 
                } else lp = or;
            }
    
            // closure (needs 1-character lookahead)
            if (i < M-1 && re[i+1] == '*') { 
                G.addEdge(lp, i+1); 
                G.addEdge(i+1, lp); 
            }
            
            if (re[i] == '(' || re[i] == '*' || re[i] == ')') // metasymbols
                G.addEdge(i, i+1);
        } 
        return G;
    }
}
```

- In this implemenation, we only considered metacharacters: `( ) . * |`
  - Here are the construction rules:
    - <img src="https://i.imgur.com/k3BfTl3.jpg" style="width:400px" />
  - Building the NFA corresponding to `( ( A * B | A C ) D )`
    - <img src="https://i.imgur.com/6egCHo7.jpg" style="width:600px" />

## Data Compression

- This course only talked about **lossless compression**.

- A data compression algorithm includes:
  - **Message**. Binary data **B** we want to compress.
  - **Compress**. Generates a "compressed" representation **C (B)**.
  - **Expand**. Reconstructs original bitstream **B**.
- **Compression ratio**. Bits in **C (B)** / bits in **B**.

- A simple example is Run-length encoding.
  - Simple type of redundancy in a bitstream:
    - 0000000000 0000011111 1100000001 1111111111 <- 40 bits
  - Transfer to below by representing alternating runs of 0s and 1s:
    - 1111 0111 0111 1011 <- 16 bits
      - 15 0s, then 7 1s, then 7 0s, then 11 1s.

### Huffman compression

- Term: Variable-length preﬁx-free codes.
  - Use a binary trie to represent. Chars in leaves, and codeword is path from root to leaf:
    - <img src="https://i.imgur.com/3u2zUTk.jpg" style="width:400px"/>

- Compression.
  - Method 1: start at leaf; follow path up to the root; print bits in reverse.
  - Method 2: create ST of key-value pairs. Codeword table Trie representation
- Expansion.
  - Start at root.
  - Go left if bit is 0;
  - go right if 1.
  - If leaf node, print char and return to root.

- Java implementation
  - <https://algs4.cs.princeton.edu/55compression/Huffman.java.html>

- Constructing a Huffman encoding trie
  - <img src="https://i.imgur.com/cgswtxX.jpg" style="width:600px"/>
  - <img src="https://i.imgur.com/m2wozN1.jpg" style="width:600px"/>

### LZW compression

- Compression
  - Create ST associating W-bit codewords with string keys.
  - Initialize ST with codewords for single-char keys.
  - Find longest string s in ST that is a prefix of unscanned part of input.
  - Write the W-bit codeword associated with s.
  - Add s + c to ST, where c is next char in the input.
  - <img src="https://i.imgur.com/W5g6DC1.jpg" style="width:600px"/>

- Expansion
  - Create ST associating string values with W-bit keys.
  - Initialize ST to contain single-char values.
  - Read a W-bit key.
  - Find associated string value in ST and write it out.
  - Update ST.
  - <img src="https://i.imgur.com/FDK3EUu.jpg" style="width:600px"/>

- Java implementation
  - <https://algs4.cs.princeton.edu/55compression/LZW.java.html>

```java
public class LZW {
    private static final int R = 256;        // number of input chars
    private static final int L = 4096;       // number of codewords = 2^W
    private static final int W = 12;         // codeword width

    // Do not instantiate.
    private LZW() { }

    /**
     * Reads a sequence of 8-bit bytes from standard input; compresses
     * them using LZW compression with 12-bit codewords; and writes the results
     * to standard output.
     */
    public static void compress() { 
        String input = BinaryStdIn.readString();
        TST<Integer> st = new TST<Integer>();

        // since TST is not balanced, it would be better to insert in a different order
        for (int i = 0; i < R; i++)
            st.put("" + (char) i, i);

        int code = R+1;  // R is codeword for EOF

        while (input.length() > 0) {
            String s = st.longestPrefixOf(input);  // Find max prefix match s.
            BinaryStdOut.write(st.get(s), W);      // Print s's encoding.
            int t = s.length();
            if (t < input.length() && code < L)    // Add s to symbol table.
                st.put(input.substring(0, t + 1), code++);
            input = input.substring(t);            // Scan past s in input.
        }
        BinaryStdOut.write(R, W);
        BinaryStdOut.close();
    } 

    /**
     * Reads a sequence of bit encoded using LZW compression with
     * 12-bit codewords from standard input; expands them; and writes
     * the results to standard output.
     */
    public static void expand() {
        String[] st = new String[L];
        int i; // next available codeword value

        // initialize symbol table with all 1-character strings
        for (i = 0; i < R; i++)
            st[i] = "" + (char) i;
        st[i++] = "";                        // (unused) lookahead for EOF

        int codeword = BinaryStdIn.readInt(W);
        if (codeword == R) return;           // expanded message is empty string
        String val = st[codeword];

        while (true) {
            BinaryStdOut.write(val);
            codeword = BinaryStdIn.readInt(W);
            if (codeword == R) break;
            String s = st[codeword];
            if (i == codeword) s = val + val.charAt(0);   // special case hack
            if (i < L) st[i++] = val + s.charAt(0);
            val = s;
        }
        BinaryStdOut.close();
    }

    /**
     * Sample client that calls {@code compress()} if the command-line
     * argument is "-" an {@code expand()} if it is "+".
     *
     * @param args the command-line arguments
     */
    public static void main(String[] args) {
        if      (args[0].equals("-")) compress();
        else if (args[0].equals("+")) expand();
        else throw new IllegalArgumentException("Illegal command line argument");
    }

}
```
