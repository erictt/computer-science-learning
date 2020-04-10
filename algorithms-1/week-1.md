# Union-Find & Analysis of Algorithms

[TOC]

* This case shows that, how to improve algorithm step by step.

## Dynamic Connectivity

* Given a set of N objects.
    * **Union command**: connect two objects.
    * **Find/connected query**: is there a path connecting the two objects?
* <img src="https://i.imgur.com/PanRco4.jpg" style="width:500px" />

* **We assume "is connected to" is an equivalence relation**:
    * Reflexive: **p** is connected to **p**.
    * Symmetric: if **p** is connected to **q**, then **q** is connected to **p**. 
    * Transitive: if **p** is connected to **q** and **q** is connected to **r**, then **p** is connected to **r**.

### First Solution: Connected components

* Maximal set of objects that are mutually connected.
* <img src="https://i.imgur.com/HffCUzo.jpg" style="width:250px" />

### Second Solution: Quick Find

* To merge components containing p and q, change all entries
whose id equals id[p] to id[q].
* <img src="https://i.imgur.com/kVqWbnt.jpg" style="width:500px" />

### Third Solution: Quick Union

* <img src="https://i.imgur.com/kLwiO2O.jpg" style="width:500px" />

### Forth Solution: Improved Quick Union

* <img src="https://i.imgur.com/6kAXl04.jpg" style="width:500px" />


### Final Solution: Weighted quick-union with path compression

* **quick-union**:
    * <img src="https://i.imgur.com/wZrkcK7.jpg" style="width:580px" />
* **weighted**: Keep track of size of each tree (number of objects). Balance by linking root of smaller tree to root of larger tree.
    * Keep the depth of any node `x` is at most `lg N`.
* **path compression**: Make every other node in path point to its grandparent.
* Code:

    ```java
    package week1;

    import common.StdIn;
    
    import java.io.FileNotFoundException;
    import java.util.Scanner;
    
    public class UnionFind {
    
      private int count;
      private int[] parent;
      private int[] sz; // record the weight
    
      UnionFind(int n) {
        count = n;
        parent = new int[n];
        sz = new int[n];
        for(int i=0; i<n; i++) {
          parent[i] = i;
          sz[i] = 1;
        }
      }
    
      public int root(int id) {
        while (parent[id] != id) {
          parent[id] = parent[parent[id]]; // improve
          id = parent[id];
        }
        return id;
      }
    
      public boolean connected(int p, int q) {
        return root(p) == root(q);
      }
    
      // quick union
      public void union(int p, int q) {
        int rootP = root(p);
        int rootQ = root(q);
        if(sz[rootP] <= sz[rootQ]) {
          parent[rootP] = rootQ;
          sz[rootQ] += sz[rootP];
        } else {
          parent[rootQ] = rootP;
          sz[rootP] += sz[rootQ];
        }
        count --;
      }
    
      public int count() {
        return count;
      }
    
      public static void main(String[] args) {
        Scanner sc = null;
        try {
          sc = new Scanner(StdIn.getDataFile("mediumUF.txt"));
        } catch (FileNotFoundException e) {
          e.printStackTrace();
        }
        int n = sc.nextInt();
        UnionFind uf = new UnionFind(n);
        while (sc.hasNext()) {
          int p = sc.nextInt();
          int q = sc.nextInt();
          if (uf.connected(p, q)) continue;
          uf.union(p, q);
          System.out.println(p + " " + q);
        }
        System.out.println(uf.count() + " components");
      }
    }
    ```

## Analysis of Algorithms

### Common Order-of-growth Classifications

* \\(1, \log{N}, N \log{N}, N^2, N^3, \text{ and } 2^N\\)
    * order of growth discards leading coefficient
* <img src="https://i.imgur.com/zVwGKBU.jpg" style="width:300px" />
    * \\(\text{time} = \lg{T(N)}\\)
    * \\(\text{size} = \lg{N}\\)
* <img src="https://i.imgur.com/1L86Sel.jpg" style="width:600px" />

### Theory of Algorithms

* <img src="https://i.imgur.com/ReIJab3.jpg" style="width:600px" />


### Why Big-Oh Notation

* Formal Definition: \\(T(n) = O(f(n))\\) if and only if there exist constants \\(c,n_0 > 0\\) such that \\(T(n) \le c \cdot f(n)\\) for all \\(n \ge n_0\\)
    * \\(T(n)\\) is the function of the running time of an algorithm.
    * Warning \\(c, n_0\\) cannot depend on **n**.
* [NOTE] It kinds of says, we use \\(n^k\\), but not \\(n^{k-1}\\)
    * Because \\(O(n^{k-1}) = c \cdot n^{k-1}\\) will always less then \\(n^k\\) (**c** is a constant, but n is not).
    * And we need that, T(n) is bounded above by a constant multiple of f(n).
        * <img src="https://i.imgur.com/e4QDv7A.jpg" style="width:200px" />
* Example
    * <img src="https://i.imgur.com/xaIpA3R.jpg" style="width:400px" />

* <img src="https://i.imgur.com/NAo87Zc.jpg" style="width:500px" />

## Assignment (Percolation)

* Write a program to estimate the value of the percolation threshold via Monte Carlo simulation.
    * [Details](http://coursera.cs.princeton.edu/algs4/assignments/percolation.html)
* My Code: [https://github.com/erictt/algorithms-practice/tree/master/src/week1](https://github.com/erictt/algorithms-practice/tree/master/src/week1)

## Words

* **asymptotic** [,æsimp'tɔtik,-kəl] adj. 渐近的；渐近线的
* **ubiquitous** [ju:'bikwitəs] adj. 普遍存在的；无所不在的