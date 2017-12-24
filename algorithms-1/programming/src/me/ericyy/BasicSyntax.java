package me.ericyy;

public class BasicSyntax {
  public static void main(String[] args) {
    double[] a;
    int N = 10000;
    a = new double[N];
    for (int i = 0; i < N; i++) {
      a[i] = 0.0;
    }
    int[] b = {1, 2, 3, 4, 5, 6};
    System.out.println(b);
    System.out.println( ('A' + 4));
  }

  public static double sqrt(double c) {

    if (c < 0) return Double.NaN;
    double err = 1e-15;
    double t = c;
    while (Math.abs(t - c / t) > err * t)
      t = (c / t + t) / 2.0;
    return t;
  }
}
