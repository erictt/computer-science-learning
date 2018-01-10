package week1.assignment;

import edu.princeton.cs.algs4.StdOut;
import edu.princeton.cs.algs4.StdRandom;
import edu.princeton.cs.algs4.StdStats;

public class PercolationStats {

  private static final double CONFIDENCE_95 = 1.96;
  private final double[] results;
  private double mean;
  private double stddev;

  // perform trials independent experiments on an n-by-n grid
  public PercolationStats(int n, int trials) {
    results = new double[trials];
    for (int i = 0; i < trials; i++) {
      Percolation p = new Percolation(n);
      while (!p.percolates()) {
        int row = StdRandom.uniform(1, n + 1);
        int col = StdRandom.uniform(1, n + 1);
//        System.out.println("row: " + row + ", and col: " + col);
        if (!p.isOpen(row, col)) {
          p.open(row, col);
        }
      }
      results[i] = (double) p.numberOfOpenSites() / (n * n);
    }
    mean = StdStats.mean(results);
    stddev = StdStats.stddev(results);
  }

  // sample mean of percolation threshold
  public double mean() {
    return mean;
  }

  // sample standard deviation of percolation threshold
  public double stddev() {
    return stddev;
  }

  // low endpoint of 95% confidence interval
  public double confidenceLo() {
    return mean - CONFIDENCE_95 * stddev / Math.sqrt(results.length);
  }

  // high endpoint of 95% confidence interval
  public double confidenceHi() {
    return mean + CONFIDENCE_95 * stddev / Math.sqrt(results.length);
  }

  // test client (described below)
  public static void main(String[] args) {
    int n = Integer.parseInt(args[0]);
    int trials = Integer.parseInt(args[1]);
    PercolationStats p = new PercolationStats(n, trials);
    StdOut.println("mean\t = " + p.mean());
    StdOut.println("stddev\t = " + p.stddev());
    StdOut.println("95% confidence interval\t = [" + p.confidenceLo() + ", " + p.confidenceHi() + "]");
  }
}
