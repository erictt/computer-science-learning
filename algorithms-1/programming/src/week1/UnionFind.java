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
