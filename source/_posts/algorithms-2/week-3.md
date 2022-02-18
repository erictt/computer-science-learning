# Week 3 - Maximum Flow and Minimum Cut & Radix Sorts

## Maximum Flow and Minimum Cut

### Problems to Solve

* Minimum Cut Problem
    * A cut is a node partition (S, T) such that s is in S and t is in T.
        * capacity(S, T) = sum of weights of edges leaving S.
    * Find an s-t cut of minimum capacity.

    * An example of not being the minimum:
        * <img src="https://i.imgur.com/lTpwnlp.jpg" style="width:400px" />
    * The correct answer
        * <img src="https://i.imgur.com/7FabVRL.jpg" style="width:400px" />
    
* Max Flow Problem
    * Assign flow to edges so as to:
        * Maximize flow sent from s to t.
        * Equalize inflow and outflow at every intermediate vertex. 
    * <img src="https://i.imgur.com/VJC0V2z.jpg" style="width:300px" />


### Maxflow Mincut Theorem

* Some terminologies
    * Original graph
        * A graph keeps the capacity from each edges and the flow go through them.
    * Residual graph & Residual edge
        * A parallel graph as the original graph which keeps two capacities: the forward capacity(=original capacity - flow); the backward capacity(=flow).
            * The backward capacity is used for "undo" flow went through the edge. 
        * <img src="https://i.imgur.com/Xo4Y0pw.jpg" style="width:500px" />
            * **Key point.** Augmenting path in **original** network is equivalent to **directed path** in **residual** network.
    
    * Augmenting paths
        * path in residual graph, either:
            * increase flow along forward edges. 
                * <img src="https://i.imgur.com/d5iTrjm.jpg" style="width:500px" />
            * decrease flow along backward edges(not empty).
                * <img src="https://i.imgur.com/G6J5soQ.jpg" style="width:500px" />
                * The decrease on the backward edge is like re-distribute the flow to other place since the new flow we're trying to create add the same amount.
                * In the case above, 5 was deducted and added to the top edge, and pass long to t.

#### Relation between Maximum Flow and Minimum Cut

* Def. The **net flow across** a cut (A, B) is the sum of the flows on its edges from A to B minus the sum of the flows on its edges from from B to A.
* Theorems: 
    1. **Flow-value lemma**. Let f be a flow, and let (S, T) be any s-t cut. Then, the net flow sent across the cut is equal to the amount reaching t.
        * <img src="https://i.imgur.com/kw8OuxN.jpg" style="width:800px" />
        * Cut capacity always >= Flow value
    2. **Weak duality**. Let f be any flow and let (S, T) be any cut. Then, the value of the flow ≤ the capacity of the cut.
        * Value of flow f = net flow across cut (S, T) ≤ capacity of cut (S, T).

#### **Max Flow and Min Cut**

* Let f be a flow, and let (S, T) be an s-t cut whose capacity equals the value of f. Then f is a max flow and (S, T) is a min cut.
    * Re-phrase:
        * A flow f is a maxflow iff no augmenting paths. <-- **Augmenting Path Theorem**.
        * And, the value of max flow equals capacity of min cut. <--  **Max-Flow Min-Cut Theorem** (Ford-Fulkerson, 1956).
* In my understanding, the capacity of the **min-cut** (S, T) is the **bottleneck** of the graph, which means it's the **maximum flow** can be passed from S to T. Since the flow is equivalent, it must applies to s and t as well.
    * and since **max-flow** already matched the bottleneck, there will be no new augmenting path can increase the flow to break the bottleneck.
    * e.g. <img src="https://i.imgur.com/xijaZ5V.jpg" style="width:400px" />
    * TODO: My question is, is it possible that the max flow didn't reach the capacity of all cuts?

* **To compute mincut (S, T) from maxflow f** :
    * By augmenting path theorem, no augmenting paths with respect to f(the maxflow). 
    * Compute S = set of vertices connected to s by an undirected path with no full forward or empty backward edges.
        * **TODO**: Why?
    * <img src="https://i.imgur.com/mcJplpu.jpg" style="width:400px" />
    
### Ford-Fulkerson algorithm 

To find the maximum flow (and min-cut), the algorithm repeatedly finds **augmenting paths** through the **residual graph** and **augments the flow** until no more augmenting paths can be found.

* Steps:

    ```
    while (there exists an augmenting path) { 
        Find augmenting path P 
        Compute bottleneck capacity of P 
        Augment flow along P 
    }
    ```
#### How to find an augmenting path?

* Assume that all capacities are integers between 1 and U(which is true for lots of applications), the algorithm terminates in at most `V x U`.
    * The worst case:
        * <img src="https://i.imgur.com/qGJYKG7.jpg" style="width:300px" />
    * Every interation, it visit every vertices and only increase the flow by 1. So it needs 100 * 2 interations to finish.
* To Avoid the worst case, we can choose different algorithms for choosing augmenting paths.
    1. Fewest number of arcs. (shortest path)
    2. Max bottleneck capacity. (fattest path)
* Shortest augmenting path.
    * Easy to implement with BFS.
    * Finds augmenting path with fewest number of arcs. 
    * Facts:
        * At most $EV$ total augmenting paths.
        * O($E^2V$) running time.
* Fattest augmenting path.
    * Finds augmenting path whose **bottleneck** capacity is maximum. 
    * Delivers most amount of flow to sink.
    * Solve using Dijkstra-style (PFS) algorithm.
    * Fact. 
        * O($E\log{U}$) augmentations if capacities are between 1 and U.

### Java API

* Flow Edge API
    
    ```java
    public class FlowEdge {
        private final int v, w; // from and to 
        private final double capacity; // capacity 
        private double flow; // flow
        
        int FlowEdge(int v, int w, double capacity) { // create a flow edge v→w
            this.v = v;
            this.w = w;
            this.capacity = capacity;
        }
        int from() { return v; } // vertex this edge points from
        int to() { return w; } // vertex this edge points to
        int other(int v) { return v; } // other endpoint
        double capacity() { return capacity; }// capacity of this edge 
        double flow() { return flow; }// flow in this edge 
        
        double residualCapacityTo(int v) { // residual capacity toward v 
            if (vertex == v) return flow; // backward edge
            else if (vertex == w) return capacity - flow; // forward edge
            else throw new IllegalArgumentException(); 
        }
        
        void addResidualFlowTo(int v, double delta) { // add delta flow toward v 
            if (vertex == v) flow -= delta;
            else if (vertex == w) flow += delta;
            else throw new IllegalArgumentException();
        }
        
        String toString() // string representation
    }
    ```
    
* Flow Network API

    ```java
    public class FlowNetwork {
        // same as EdgeWeightedGraph, but adjacency lists of FlowEdges instead of Edges
        private final int V; // number of vertices
        private Bag<FlowEdge>[] adj;
        
        public FlowNetwork(int V) { 
            this.V = V; 
            adj = (Bag<FlowEdge>[]) new Bag[V]; 
            for (int v = 0; v < V; v++) 
                adj[v] = new Bag<FlowEdge>(); 
        }
        
        public void addEdge(FlowEdge e) { 
            int v = e.from(); 
            int w = e.to(); 
            //  add forward edge add backward edge
            adj[v].add(e); 
            adj[w].add(e); 
        }
        
        public Iterable<FlowEdge> adj(int v) { 
            return adj[v]; 
        }
    }
    ```
    
    * <img src="https://i.imgur.com/cm3Px4e.jpg" style="width:500px" />

* **Ford-Fulkerson: Java implementation**

    ```java
    public class FordFulkerson {
        private boolean[] marked; // true if s->v path in residual network
        private FlowEdge[] edgeTo; // last edge on s->v path
        private double value; // value of flow

        public FordFulkerson(FlowNetwork G, int s, int t) {
            value = 0.0; 
            while (hasAugmentingPath(G, s, t)) {

                double bottle = Double.POSITIVE_INFINITY;
                for (int v = t; v != s; v = edgeTo[v].other(v)) // compute bottleneck capacity
                    bottle = Math.min(bottle, edgeTo[v].residualCapacityTo(v));
                
                for (int v = t; v != s; v = edgeTo[v].other(v)) // augment flow
                    edgeTo[v].addResidualFlowTo(v, bottle);
                
                value += bottle;
            }
        }

        private boolean hasAugmentingPath(FlowNetwork G, int s, int t) {
            edgeTo = new FlowEdge[G.V()]; 
            marked = new boolean[G.V()];

            Queue<Integer> queue = new Queue<Integer>(); 
            queue.enqueue(s); marked[s] = true; 
            while (!queue.isEmpty()) { 
                int v = queue.dequeue();
                for (FlowEdge e : G.adj(v)) { 
                    int w = e.other(v); 
                    // found path from s to w in the residual network?
                    if (e.residualCapacityTo(w) > 0 && !marked[w]) { 
                        edgeTo[w] = e; // save last edge on path to w; 
                        marked[w] = true; // mark w; 
                        queue.enqueue(w); // add w to the queue 
                    }
                }
            }
            return marked[t]; // is t reachable from s in residual network?
        }

        public double value() { return value; }
        
        // is v reachable from s in residual network?
        public boolean inCut(int v) { return marked[v]; }
    }
    ```
    
### Additional Resouces

* https://www.cs.princeton.edu/courses/archive/spr04/cos226/lectures/maxflow.4up.pdf
    * Note: slides 16 and 17 have a mistake. The flow on edges(s-4 and 4-7) should both be 14.
* https://www.youtube.com/watch?v=LdOnanfc5TM

## Radix Sorts

### Strings in Java 

* Sequence of characters (immutable)

* **String vs. StringBuilder**

    * Quadratic time
        
        ```java
        public static String reverse(String s) { 
            String rev = ""; 
            for (int i = s.length() - 1; i >= 0; i--) 
                rev += s.charAt(i); 
            return rev; 
        }
        ```
    * Linear time
    
        ```java
        public static String reverse(String s) { 
            StringBuilder rev = new StringBuilder(); 
            for (int i = s.length() - 1; i >= 0; i--) 
                rev.append(s.charAt(i)); 
            return rev.toString(); 
        }
        ```
        
#### Alphabets

* **Digital key**. Sequence of digits over fixed alphabet.
* **Radix**. Number of digits R in alphabet.
* <img src="https://i.imgur.com/A4jI4sP.jpg" style="width:600px" />

    
### key-indexed counting 

* **Assumption**. Keys are integers between 0 and R - 1.
* **Goal**. Sort an array a[] of N integers between 0 and R - 1.
* **Implementation**.

    ```java
    int N = a.length; 
    // EXTENDED_ASCII 256 8 extended ASCII characters
    // R = 256
    int[] count = new int[R+1];

    // 1. Count frequencies of each letter using key as index.
    for (int i = 0; i < N; i++) 
        count[a[i]+1]++;

    // 2. Compute frequency cumulates which specify destinations.
    for (int r = 0; r < R; r++) 
        count[r+1] += count[r];

    // 3. Access cumulates using key as index to move items.
    for (int i = 0; i < N; i++) 
        aux[count[a[i]]++] = a[i];

    // 4. Copy back into original array.
    for (int i = 0; i < N; i++) 
        a[i] = aux[i];
    ```

* <img src="https://i.imgur.com/88fitXA.jpg" style="width:600px" />
    * **Notice**: use a for 0, b for 1, c for 2, d for 3, e for 4, f for 5 for better explanation

* **Proposition**. Key-indexed counting uses ~ 11 N + 4 R array accesses to sort N items whose **keys are integers between 0 and R - 1**.

### LSD radix sort 

* Least-signiﬁcant-digit-ﬁrst string sort
* LSD string (radix) sort.
    * Consider characters from right to left.
    * Stably sort using d^th character as the key (using key-indexed counting).
* <img src="https://i.imgur.com/8qaZdGr.jpg" style="width:600px" />
* <img src="https://i.imgur.com/60ABADp.jpg" style="width:600px" />


### 马上到！ radix sort 

* Most-signiﬁcant-digit-ﬁrst string sort
    * Partition array into R pieces according to first character (use key-indexed counting).
    * Recursively sort all strings that start with each character (key-indexed counts delineate subarrays to sort).
* <img src="https://i.imgur.com/X3yqp4c.jpg" style="width:600px" />
* Treat strings as if they had an extra char at end (smaller than any char).
    * <img src="https://i.imgur.com/V7owW3R.jpg" style="width:400px" />
* implementation
    * <img src="https://i.imgur.com/29vzTCy.jpg" style="width:600px" />
* potential for disastrous performance
    1. much too slow for small subarrays
    2. Huge number of small subarrays
    
    * Solution: Cutoff to insertion sort for small subarrays.
        * Insertion sort, but start at d th character.
        * Implement less() so that it compares starting at d^th character.
        * <img src="https://i.imgur.com/2iHxCJM.jpg" style="width:600px" />
    
### 3-way radix quicksort 

* <img src="https://i.imgur.com/HiwhpWZ.jpg" style="width:600px" />
* <img src="https://i.imgur.com/WnJymHE.jpg" style="width:600px" />
* faster than the other two algorithms, but not stable.

### suffix arrays

#### Suffix sort

* <img src="https://i.imgur.com/cVsQdT1.jpg" style="width:600px" />
* Can be used for finding longest repeated substring
* **worst-case input**: longest repeated substring very long.
    * LRS needs at least 1 + 2 + 3 + ... + D character compares, where D = length of longest match.

#### Manber-Myers 马上到！ algorithm

* Sufﬁx sorting in linearithmic time
    * linear: N, linearithmic: a * N
* overview
    * **Phase 0**: sort on first character using key-indexed counting sort. 
    * **Phase i**: given array of suffixes sorted on first 2 i - 1 characters, create array of suffixes sorted on first 2 i characters.
* Key process: Constant-time string compare by indexing into inverse
    * <img src="https://i.imgur.com/mCQHMGs.jpg" style="width:600px" />
    * inverse[]:
        * before: {0: 17, 1: 16, 2: 15, ..., 9: 1, ..., 12: 2, ..., 14: 0 }
        * after: { 0: 14, 1: 9, 2: 12, ...}
