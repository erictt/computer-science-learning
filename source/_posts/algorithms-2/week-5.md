# Regular Expressions & Data Compression

## Regular Expressions 

### DFA vs NFA

- Deterministic finite state automata (DFA); 
- Nondeterministic finite state automata (NFA).

* Basic plan:
    1. Build DFA/NFA from RE.
    2. Simulate DFA/NFA with text as input.

* refer to [week 4#knuth-morris-pratt-kmp](week-4/index.html#knuth-morris-pratt-kmp) for the DFA implementation
    * Bad news with DFA is, it may have exponential # of states.
* NFA is widely used in modern languages.

### NFA

* Features:
    * RE enclosed in parentheses.
    * One state per Re character (start = 0, accept = M).
    * Red $\color{red}{\epsilon\text{-transition}}$ (change state, but don't scan text);
    * Black match transition (change state and scan to next text char).
    * Accept if **any** sequence of transitions ends in accept state.
* RE:
    * <img src="https://i.imgur.com/OZPphzB.jpg" style="width:600px" />
    * Red directions are $\epsilon$ transition which are stored in a **digraph** G.
        * 0→1, 1→2, 1→6, 2→3, 3→2, 3→4, 5→8, 8→9, 10→11
* The general steps are to find states reachableeither by either match transitions or $\color{red}{\epsilon\text{-transition}}$ alternatively.
* Take `A A B D` as an example to simulate the RE. 
    * <img src="https://i.imgur.com/ezeRWid.jpg" style="width:600px" />

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

* In this implemenation, we only considered metacharacters: `( ) . * |`
    * Here are the construction rules:
        * <img src="https://i.imgur.com/k3BfTl3.jpg" style="width:400px" />
    * Building the NFA corresponding to `( ( A * B | A C ) D )`
        * <img src="https://i.imgur.com/6egCHo7.jpg" style="width:600px" />

## Data Compression 