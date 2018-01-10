package week1.assignment;

import edu.princeton.cs.algs4.StdOut;
import edu.princeton.cs.algs4.StdRandom;
import edu.princeton.cs.algs4.WeightedQuickUnionUF;

public class Percolation {

  private final WeightedQuickUnionUF sites;
  private final WeightedQuickUnionUF sites2;
  private final int length;
  private boolean[] opened;
  private int openedCount = 0;
  private final int virtualTop;
  private final int virtualBottom;

  // create n-by-n grid, with all sites blocked
  public Percolation(int n) {
    if (n <= 0) {
      throw new IllegalArgumentException("n should be great that 0");
    }
    length = n;
    int count = n * n;
    sites = new WeightedQuickUnionUF(count + 2);

    // to avoid backwash, use this to check isFull()
    // check http://coursera.cs.princeton.edu/algs4/checklists/percolation.html to find out what is backwash
    sites2 = new WeightedQuickUnionUF(count + 1);
    virtualTop = count;
    virtualBottom = count + 1;
    opened = new boolean[count];
    for (int i = 0; i < count; i++) {
      opened[i] = false;
    }
  }

  private int convertCoordinateToIndex(int row, int col) {
    validate(row, col);
    return (row - 1) * length + (col - 1);
  }

  private void validate(int row, int col) {
    if (row > length || col > length || row < 1 || col < 1)
      throw new IllegalArgumentException(
          "invalid row: " + row + ", and col: " + col
      );
  }

  // open site (row, col) if it is not open already
  public void open(int row, int col) {
    if (isOpen(row, col)) return;
    int p = convertCoordinateToIndex(row, col);
    opened[p] = true;
    openedCount++;

    if (row == 1) {
      sites.union(p, virtualTop);
      sites2.union(p, virtualTop);
    }
    if (row == length) {
      sites.union(p, virtualBottom);
    }
    if (row < length && isOpen(row + 1, col)) {
      int q = convertCoordinateToIndex(row + 1, col);
      sites.union(p, q);
      sites2.union(p, q);
    }
    if (row > 1 && isOpen(row - 1, col)) {
      int q = convertCoordinateToIndex(row - 1, col);
      sites.union(p, q);
      sites2.union(p, q);
    }
    if (col > 1 && isOpen(row, col - 1)) {
      int q = convertCoordinateToIndex(row, col - 1);
      sites.union(p, q);
      sites2.union(p, q);
    }
    if (col < length && isOpen(row, col + 1)) {
      int q = convertCoordinateToIndex(row, col + 1);
      sites.union(p, q);
      sites2.union(p, q);
    }
  }

  // is site (row, col) open?
  public boolean isOpen(int row, int col) {
    int p = convertCoordinateToIndex(row, col);
    return opened[p];
  }

  // is site (row, col) full?
  public boolean isFull(int row, int col) {
    int index = convertCoordinateToIndex(row, col);
    return sites2.connected(index, virtualTop);
  }

  // number of open sites
  public int numberOfOpenSites() {
    return openedCount;
  }

  // does the system percolate?
  public boolean percolates() {
    return sites.connected(virtualTop, virtualBottom);
  }

  // test client (optional)
  public static void main(String[] args) {
//    Scanner sc = null;
//    try {
//      sc = new Scanner(new File("./percolation/input8.txt"));
//    } catch (FileNotFoundException e) {
//      e.printStackTrace();
//    }
//
//    int length = sc.nextInt();
//    Percolation p = new Percolation(length);
//    while (sc.hasNext()) {
//      int row = sc.nextInt();
//      int col = sc.nextInt();
//      if (!p.isOpen(row, col)) {
//        p.open(row, col);
//      }
//      StdOut.println(row + " " + col + " " + p.percolates());
//    }
    int length = 20;
    Percolation p = new Percolation(length);

    while (!p.percolates()) {
      int row = StdRandom.uniform(1, length + 1);
      int col = StdRandom.uniform(1, length + 1);
      StdOut.println(row + " " + col);
      if (!p.isOpen(row, col)) {
        p.open(row, col);
      }
    }
    StdOut.println(p.numberOfOpenSites());
  }
}
