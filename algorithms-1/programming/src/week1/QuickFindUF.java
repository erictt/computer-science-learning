package week1;

import common.StdIn;

import java.io.FileNotFoundException;
import java.util.Scanner;

public class QuickFindUF {

  private int count;
  private int[] ids;

  QuickFindUF(int n) {
    count = n;
    ids = new int[n];
    for(int i=0; i<count; i++)
      ids[i] = i;
  }

  boolean connected(int p, int q) {
    return ids[p] == ids[q];
  }

  void validate(int p) {
    if (p < 0 || p > ids.length) {
      throw new IllegalArgumentException( "index " + p + " is not between 0 and" + ids.length );
    }
  }

  void union(int p, int q) {
    validate(p);
    validate(q);
    int indexQ = ids[q];
    if(ids[p] == ids[q]) return;
    for(int i=0; i<ids.length; i++) {
      if(ids[i] == indexQ) {
        ids[i] = ids[p];
      }
    }
    count --;
  }

  int count() {
    return count;
  }

  public static void main(String[] args) {
    Scanner sc = null;
    try {
//      sc = new Scanner(StdIn.getDataFile("tinyUF.txt"));
//      sc = new Scanner(StdIn.getDataFile("mediumUF.txt"));
      sc = new Scanner(StdIn.getDataFile("largeUF.txt"));
    } catch (FileNotFoundException e) {
      e.printStackTrace();
    }
    int n = sc.nextInt();
    QuickFindUF uf = new QuickFindUF(n);
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
