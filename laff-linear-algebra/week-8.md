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


## Symmetric Positive Deﬁnite(SPD) Matrices

* Deﬁnition: Let \\(A \in \mathbb{R}^{n \times n}\\). Matrix A is said to be symmetric positive definite(SPD) if
    * A is symmetric; and
    * \\(x^T A x > 0 \\) for all nonzero vector \\(x \in \mathbb{R}^n\\).

### Solving Ax = b when A is Symmetric Positive Deﬁnite

#### Cholesky factorization theorem

* Let \\(A \in \mathbb{R}^{n \times n}\\) be a SPD matrix. Then there exists a lower trianglar matrix \\(L \in \mathbb{R}^{n \times n}\\) such that \\(A = LL^T\\). If the diagonal elements of L are chosen to be positive, this factorization is unique.
* <img src="media/15235262730253.jpg" width=400 />
* Algorithm:
    * <img src="media/15235263481224.jpg" width=300 />
* Notice that \\(\alpha_{11} := \sqrt{\alpha_{11} }\\) and \\(a_{21} := a_{21}/\alpha_{11}\\) which are legal if \\(\alpha > 0\\). It turns out that if **A** is SPD, then
    * \\(\alpha_{11} > 0\\) in the first iteration and hence \\(\alpha_{11} := \sqrt{\alpha_{11} }\\) and \\(a_{21} := a_{21}/\alpha_{11}\\) are legal; and
    * \\(A_{22} := A_{22} - a_{21} a_{21}^T\\) is again a SPD matrix. 


