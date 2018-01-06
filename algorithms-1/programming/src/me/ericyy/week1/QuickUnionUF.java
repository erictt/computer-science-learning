package me.ericyy.week1;

import me.ericyy.StdIn;

import java.io.FileNotFoundException;
import java.util.Scanner;

public class QuickUnionUF {

  private int count;
  private int[] ids;

  QuickUnionUF(int n) {
    count = n;
    ids = new int[n];
    for(int i=0; i<n; i++) {
      ids[i] = i;
    }
  }

  public String toString() {
    String str = "";
    for(int i=0; i<ids.length; i++)
      str += ids[i]  + " ";
    return str;
  }

  public int root(int id) {
    while (ids[id] != id) id = ids[id];
    return id;
  }

  public boolean connected(int p, int q) {
    return root(p) == root(q);
  }

  public void union(int p, int q) {
    ids[root(q)] = root(p);
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
    QuickUnionUF uf = new QuickUnionUF(n);
    while (sc.hasNext()) {
      int p = sc.nextInt();
      int q = sc.nextInt();
      if (uf.connected(p, q)) continue;
      uf.union(p, q);
      System.out.println(p + " " + q);
    }
    System.out.println(uf.count() + " components");
    System.out.println(uf);
  }
}
