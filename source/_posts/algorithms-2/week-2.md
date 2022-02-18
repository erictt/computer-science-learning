# Week 2 - Minimum Spanning Trees & Shortest Path

[TOC]

## Minimum Spanning Trees

### Definition

* find the minimum weight to connect all vertices.

### Greedy Algorithm

* Simplifying assumptions
    * each edge's weight is different with the others. 
    * graph is connected.
* So that the MST exist and is unique.
* Cut properly
    * Def: A **cut** in a graph is a partition of its vertices into two arbitraty sets.
    * Def: A **crossing edge** connects a vertext in one set with a vertex in the other.
    * Given any cut, the **crossing edge of min weight** is in the MST. (Proof: Page 606)
        * <img src="https://i.imgur.com/yTMDuEl.jpg" style="width:300px" />

### Edge-weighted graph API

* Weighted edge API
    * <img src="https://i.imgur.com/p6bYXS8.jpg" style="width:400px" />
    * Idiom for processing an edge e: int v = e.either(), w = e.other(v);

* Edge-weighted graph API
    * <img src="https://i.imgur.com/xjHWxq0.jpg" style="width:400px" />
* Minimum spanning tree API
    * <img src="https://i.imgur.com/6Oe0LT9.jpg" style="width:400px" />

### Kruskal's algorithm

* Summarize:
    * Consider edges in **ascending order** of weight. Add next edge to the MST tree **unless** doing so would **create a cycle**.
* Why there is no crossing edge has lower weight? Because we sorted the weight at the beginning, any edges left have larger weight.
* Two challenge problems
    * How to organize a sorted edges with weight? use Priority Queue.
    * How to avoid cycle? Create a separted union-find data struture, and maintain a set for each connected components in the MST.
* Java implemenation
    * <img src="https://i.imgur.com/WIJvQaZ.jpg" style="width:600px" />
* Running time
    * <img src="https://i.imgur.com/OzHtFiA.jpg" style="width:300px" />

### Prim's algorithm

* Summarize:
    * Start with vertex 0 and greedily grow tree T. Add to T the min weight edge with exactly one endpoint in T. Repeat until **V - 1** edges.
    * More explanation. For example, add 0 at first, then explore all of the edges that connected to 0. Pick up the minimum one, let's say 7, and add the new vertex into tree and then compare all edges connected to both 0 and 7. Repeat this process until adding v-1 edges.

#### Lazy Implementation

1. Start with an arbitrary endpoint. add it in the MST, and all edges connected to it into a min-PQ.
2. Pop the minimum one edge, add it to MST, then add all associated edges to PQ.
    1. If the two endpoints that the edge connected to already exists in the MST, just ignore it.
3. Repeat until V-1 edges are added in MST.

* Java Implemenatation
    * <img src="https://i.imgur.com/Ncr8etA.jpg" style="width:600px" />

* running time
    * <img src="https://i.imgur.com/q0KtqXl.jpg" style="width:300px" />

#### Eager Implementation

* Different from lazy, eager turuns to maintain a PQ proactively to avoid useless edges been added, and replace the ones that are connected to the MST with better edges.
    * For example, if 2,3,4 are added in the MST, and in the PQ, we have 6-4 edge with weight 0.52. When we add a vertex 5 in the MST, we realize that the weight of 5-6 is smaller that 4-6. Then we replace the edge in the PQ.
        * This will require that the PQ being indexed and support motification.
* More details:
    1. Maintain a PQ of **vertices** connected by an edge to the MST, where (priority of vertex v) = (weight of shortest edge connecting v to the MST).
    2. Delete min vertex v from the PQ and add its associated edge **e = v–w** to the MST.
    3. Update PQ by considering all edges **e = v–x** incident to v.

* e.g. 
    * <img src="https://i.imgur.com/io4r4xS.jpg" style="width:500px" />
        * start with 0, added to MST. The vertices connected to 0 are 7, 2, 4, 6, corresponding the weights: 0.16, 0.26, 0.38, 0.58. In the PQ, it will be sorted as [7, 7-0, 0.16], [2, 2-0, 0.26], [4, 4-0, 0.38], [6, 6-0, 0.58].
        * then pop 7, and add it the MST. Then check the vertices connected to 0 and 7. 5 and 1 are new, add to the PQ directly. 4 is connected with both 7 and 0. 4-7 is lower than 0-7, replace 4's weight to 0.37, and the edge associated with 4 to 4-7. Then the queue became [1, 1-7, 0.19], [2, 2-0, 0.26], [5, 5-7, 0.28], [4, 4-7, 0.37], [6, 6-0, 0.58]
        * then pop 1, add it to MST. 3 is new, add it to Q. Compare 1-5 and 5-7, no need to change. Then the queue became [2, 2-0, 0.26], [5, 5-7, 0.28], [3, 3-1, 0.29], [4, 4-7, 0.37], [6, 6-0, 0.58]
        * then pop 2, add it to MST. 6 is new, add it to Q. **1 already existed in Q, ignore.** **compare 3-1 and 3-2, 3-2 is smaller, update the Q.** compare 6-0, 6-2, 6-3. 6-2 is smaller, update the queue the queue became [3, 3-1, 0.17], [5, 5-7, 0.28], [4, 4-7, 0.37], [6, 6-2, 0.40]
        * then keep going until MST got V-1 vertices.

* The only challenging problem: How to maintain a PQ that support **decreasing**(no need for increasing) weight?
    * Start with same code as MinPQ.
    * Maintain parallel arrays keys[], pq[], and qp[] so that:
        * keys[i] is the priority of i, aka the weight of each vertices.
        * pq[i] is the index of the key in heap position i (1-based indexing)
        * qp[i] is the heap position of the key with index i (qp[pq[i]] = pq[qp[i]] = i)
            * This is for look up the index. For example, we want to **decrease** key[6]'s weight. we first look up where the key is in PQ with the array of **qp**, qp[6] = 2, then we know 6 is the 2nd. Then we can update the weight of pq[2] = whatever, and **swim it up**.
    * Use swim(qp[i]) implement decreaseKey(i, key).
    * <img src="https://i.imgur.com/CythQOi.jpg" style="width:300px" />


* Java implemenation
    * <img src="https://i.imgur.com/5p8Mxmd.jpg" style="width:600px" />

* running time
    * Depends on PQ implementation: V insert, V delete-min, E decrease-key.
    * <img src="https://i.imgur.com/L4a9nko.jpg" style="width:500px" />


## Shortest Path

### API

* Weighted directed edge API
    * <img src="https://i.imgur.com/VUq50eN.jpg" style="width:500px" />

* Edge-weighted digraph API
    * <img src="https://i.imgur.com/yN3KfHq.jpg" style="width:500px" />
    
* Single-source shortest paths API
    * <img src="https://i.imgur.com/yUpPpW0.jpg" style="width:500px" />

### Shortest-paths optimality conditions

* <img src="https://i.imgur.com/bUirevT.jpg" style="width:500px" />

* <img src="https://i.imgur.com/tF06irL.jpg" style="width:300px" />

### Generic shortest-paths algorithm

* Generic algorithm (to compute SPT from s) Initialize distTo[s] = 0 and distTo[v] = ∞ for all other vertices. 
* Repeat until optimality conditions are satisﬁed:
    - Relax any edge.

### Dijkstra's Algorithm

* Consider vertices in increasing order of distance from **s** (non-tree vertex with the lowest distTo[] value).
* Add vertex to tree and relax all edges pointing from that vertex.
* Pick the vertex that has minimum distance to the origin to repeat the process until the last vertex.

#### Correctness proof

* Each edge e = v→w is relaxed exactly once (when v is relaxed), leaving distTo[w] ≤ distTo[v] + e.weight().
* Inequality holds until algorithm terminates because:
    * distTo[w] cannot increase <- distTo[] values are monotone decreasing
    * distTo[v] will not change <- we choose lowest distTo[] value at each step (and edge weights are nonnegative)
* Thus, upon termination, shortest-paths optimality conditions hold.

#### Java Implementation

* <img src="https://i.imgur.com/CsjFiXZ.jpg" style="width:400px" />
* <img src="https://i.imgur.com/wWmPoU3.jpg" style="width:400px" />


### Acyclic Shortest Path in DAG(Directed acyclic graph)

* Steps:
    * Consider vertices in topological order.
    * Relax all edges pointing from that vertex.
* Proposition:
    * Topological sort algorithm computes SPT(Shortest path tree) in any edgeweighted DAG in time proportional to E + V.
* Java implementation
    * <img src="https://i.imgur.com/njiBOtj.jpg" style="width:400px" />

### Bellman-Ford algorithm

* Initialize distTo[s] = 0 and distTo[v] = ∞ for all other vertices.
* Repeat V times:
    - Relax each edge.
* <img src="https://i.imgur.com/NjAONrX.jpg" style="width:400px" />

### Single source shortest-paths implementation: cost summary

* * Negative cycles
    * Def. A negative cycle is a directed cycle whose sum of edge weights is negative.

* <img src="https://i.imgur.com/g6IcSth.jpg" style="width:400px" />

    * Remark 1. Directed cycles make the problem harder. 
    * Remark 2. Negative weights make the problem harder. 
    * Remark 3. Negative cycles makes the problem intractable. 

### Finding a negative cycle

* If there is a negative cycle, Bellman-Ford gets stuck in loop, updating distTo[] and edgeTo[] entries of vertices in the cycle.
    * If any vertex v is updated in phase V, there exists a negative cycle (and can trace back edgeTo[v] entries to find it).