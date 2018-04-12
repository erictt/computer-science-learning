# Week 8 - More on Matrix Inversion

[TOC]

## Gauss-Jordan Elimination

* The key of Gauss-Jordan Elimination is to transfer matrix A to the identity matrix:
    * <img src="media/15235069828193.jpg" width=400 />

### Computing A^−1 via Gauss-Jordan Elimination

* <img src="media/15235069828192.jpg" width=600 />
* Notice ,\\(\alpha_{11} = 1 / \alpha_{11}\\). Every iteration, we scale \\(\alpha_{11}\\) to **1**.
* <img src="media/15235069828194.jpg" width=400 />
* <img src="media/15235209660728.jpg" width=300 />

### Cost of inverting a matrix

* Via Gauss-Jordan, taking advantage of zeroes in the appended identity matrix, requires approximately \\(2n^3\\) floating point operations.

### (Almost) never, ever invert a matrix

* Solving Ax = b should be accomplished by first computing its LU factorization (possibly with partial pivoting) and then solving with the triangular matrices.

