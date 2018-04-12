# Week 7 - More Gaussian Elimination and Matrix Inversion

[TOC]

## When Gaussian Elimination Breaks Down

* Let \\(A \in \mathbb{R}^{n \times n}\\) and assume that \\(A \to LU\\) completes with a matrix \\(U\\) that has no zero elements on its diagonal.
    * \\(Ax=b\\) has a unique solution.

### Permutation

* Let \\(p = (k_0, \ldots, k_{n-1})^T\\) be a permutation vector. Then \\[
    P = P(p) = \left(\begin{array}{c}
    e_{k_0}^T \\ e_{k_1}^T \\ \vdots \\ e_{k_{n-1} }^T
    \end{array}\right)
\\] is said to be a **permutation matrix**.
    * \\[\text{If}\ p = \left(\begin{array}{c}0 \\ 1 \\ 2 \\ 3\end{array}\right)\ \text{then}\ P(p) = \left(\begin{array}{c c c c}1 & 0 & 0 & 0\\ 0 & 1 & 0 & 0 \\ 0 & 0 & 1 & 0 \\ 0 & 0 & 0 & 1\end{array}\right)\\]
* \\[
    P x = P(p) x = \left(\begin{array}{c}
    e_{k_0}^T \\ e_{k_1}^T \\ \vdots \\ e_{k_{n-1} }^T
    \end{array}\right) x = \left(\begin{array}{c}
    e_{k_0}^T x \\ e_{k_1}^T x \\ \vdots \\ e_{k_{n-1} }^T x
    \end{array}\right) = \left(\begin{array}{c}
    x_{k_0} \\ x_{k_1} \\ \vdots \\ x_{k_{n-1} }
    \end{array}\right)
\\]

* Let \\[A = \left(\begin{array}{c}
    	\widetilde a_0^T \\ \widetilde a_1^T \\ \vdots \\ \widetilde a_{n-1}^T
    \end{array}\right)\\]
    * \\[PA = P(p)A = \left(\begin{array}{c}
    e_{k_0}^T \\ e_{k_1}^T \\ \vdots \\ e_{k_{n-1} }^T
    \end{array}\right) A = \left(\begin{array}{c}
    \widetilde a_{k_0}^T \\ \widetilde a_{k_1}^T \\ \vdots \\ \widetilde a_{k_{n-1} }^T
    \end{array}\right) \\]
    
* Let \\[A = \left(\begin{array}{c | c | c | c}
    	a_0 & a_1 & \ldots & a_{n-1}
    \end{array}\right)\\]
    * \\[AP^T = \left(\begin{array}{c | c | c | c}
    	a_{k_0} & a_{k_1} & \ldots & a_{k_{n-1} }
    \end{array}\right) \\]

* If \\(P\\) is a permutation matrix, then so is \\(P^T\\).

#### Pivot matrix

* <img src="media/15234335856239.jpg" width=400 />
    * Swap the \\(\pi\\)th row with the \\(0\\)th.

* \\(\widetilde P(\pi) = (\widetilde P(\pi))^T\\)

* **Summary**
    * Permutation matrices, when applied from the left, swap rows.
    * Permutation matrices, when applied from the right, swap columns.

### LU factorization algorithm that incorporates row (partial) pivoting

* <img src="media/15234370309760.jpg" width=400 />
* Solving \\(Ax = b\\) then changes to 
    * Compute \\(P, L \text{ and } U\\) such that \\(PA = LU\\).
    * Update \\(b:= Pb\\).
    * Solve \\(Lz = b\\) (forward substitution)
    * Solve \\(Ux = z\\) (backward substitution)

## The Inverse Matrix

### Inverse Functions in 1D

* \\(f: \mathbb{R} \to \mathbb{R}\\) maps a rea to a real and it is a **bijection**(both one-to-one and onto)
    * bijection means: every element in R, there
is a unique output in R. 
* then
    * \\(f(x) = y\\) has a unique solution for all \\(y \in  \mathbb{R}\\).
    * The function that maps y to x so that \\(g(y) = x\\) is called the inverse of \\(f\\).
    * It is denoted by \\(f^{-1}: \mathbb{R} \to \mathbb{R}\\).
    * \\(f(f^{-1}(x)) = f^{-1}(f(x)) = x\\)

### General principle

* If \\(A, B \in R^{n \times n}\\) and \\(AB = I\\), then \\(Ab_j = e_j\\), where \\(b_j\\) is the \\(j\\)th column of B and \\(e_j\\) is the \\(j\\)th unit basis vector.

### Properties of the inverse

* Assume A, B, and C are square matrices that are nonsingular. Then
    * \\((\alpha B)^{-1} = \frac{1}{\alpha} B^{-1}\\)
    * \\((AB)^{-1} = B^{-1} A^{-1}\\)
    * \\((ABC)^{-1} = C^{-1} B^{-1} A^{-1}\\)
    * \\((A^T)^{-1} = (A^{-1})^{T}\\)
    * \\((A^{-1})^{-1} = A\\)

* The following statements are equivalent statements about \\(A \in \mathbb{R}^{n \times n}\\) :
    * A is nonsingular(不可逆).
    * A is invertible.
    * \\(A^{-1}\\) exists.
    * \\(AA^{-1} = A^{-1}A = I\\).
        * \\(A^{-1}\\) undoes what matrix A did.
        * \\(AA^{-1}x = Ix = x\\)
        * [Identity Matrix](/laff-linear-algebra/week-3.html#special-matrices)
    * A represents a linear transformation that is a bijection.
    * Ax = b has a unique solution for all \\(b \in \mathbb{R}^n\\).
    * \\(Ax = 0\\) implies that \\(x = 0\\).
    * \\(Ax = e_j\\) has a solution for all \\(j \in {0, \ldots, n-1}\\).
    * The determinant of A is nonzero: \\(det(A) \ne 0\\).

* **Theorem**: Let \\(P\\) be a permutation matrix. Then \\(P^{-1} = P^T\\).

### Inverses of special matrices

* <img src="media/15234520168657.jpg" width=500 />

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


