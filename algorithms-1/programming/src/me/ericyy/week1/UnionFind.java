package me.ericyy.week1;

import java.io.File;
import java.io.FileNotFoundException;
import java.util.Scanner;

public class UnionFind {

  UnionFind(int N) {
    N = N;
  }

  boolean connected(int p, int q) {
    return false;
  }

  void union(int p, int q) {

  }

  int count() {
    return 0;
  }

  public static void main(String[] args) {
    Scanner sc = null;
    try {
      sc = new Scanner(new File(args[0]));
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
