package week1;


import common.StdIn;

import java.io.FileNotFoundException;
import java.util.Scanner;

  public class WeightedQuickUnionUF {

    private int count;
    private int[] ids;
    private int[] sz;

    WeightedQuickUnionUF(int n) {
      count = n;
      ids = new int[n];
      sz = new int[n];
      for(int i=0; i<n; i++) {
        ids[i] = i;
        sz[i] = 1;
      }
    }

    public int root(int id) {
      while (ids[id] != id) id = ids[id];
      return id;
    }

    public boolean connected(int p, int q) {
      return root(p) == root(q);
    }

    public void union(int p, int q) {
      int rootP = root(p);
      int rootQ = root(q);
      if(sz[rootP] <= sz[rootQ]) {
        ids[rootP] = rootQ;
        sz[rootQ] += sz[rootP];
      } else {
        ids[rootQ] = rootP;
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
//      sc = new Scanner(StdIn.getDataFile("mediumUF.txt"));
        sc = new Scanner(StdIn.getDataFile("largeUF.txt"));
      } catch (FileNotFoundException e) {
        e.printStackTrace();
      }
      int n = sc.nextInt();
      WeightedQuickUnionUF uf = new WeightedQuickUnionUF(n);
//      edu.princeton.cs.algs4.WeightedQuickUnionUF uf = new edu.princeton.cs.algs4.WeightedQuickUnionUF(n);
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
