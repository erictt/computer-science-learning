# Week 4 - Matrix-Vector to Matrix-Matrix Multiplication

## Preparation

### Partitioned Matrix-vector Multiplication

* $$\displaystyle  \left( \begin{array}{ c | c | c | c } A_{0,0} &  A_{0,1} &  \cdots &  A_{0,N-1} \\ A_{1,0} &  A_{1,1} &  \cdots &  A_{1,N-1} \\ \vdots &  \vdots &  \ddots &  \vdots \\ A_{M-1,0} &  A_{M-1,1} &  \cdots &  A_{M-1,N-1} \end{array} \right) \left( \begin{array}{ c } x_0 \\ x_1 \\ \vdots \\ x_{N-1} \end{array} \right) = \left( \begin{array}{ c } A_{0,0} x_{0} + A_{0,1} x_{1} + \cdots + A_{0,N-1} x_{N-1} \\ A_{1,0} x_{0} + A_{1,1} x_{1} + \cdots + A_{1,N-1} x_{N-1} \\ \vdots \\ A_{M-1,0} x_{0} + A_{M-1,1} x_{1} + \cdots + A_{M-1,N-1} x_{N-1} \end{array} \right)$$

* Two different algorithms to calculate Matrix-vector Multiplication
    * <img src="https://i.imgur.com/bfCSSzl.png" style="width:600px" />
    * First one, is calculating by rows.
        * $\psi_1 := a_{10}^T x_0 + \alpha_{11} x_1 + a_{12}^T x_2 + \psi_1$
    * Second one is by columns.
        * $y_0 := \chi_1 a_{01} + y_0$
        * $\psi_1 := \chi_1 \alpha_{11} + \psi_1$
        * $y_2 := \chi_1 a_{21} + y_2$

### Transposing a Partitioned Matrix

* $$\left( \begin{array}{c | c | c | c} A_{0,0} &  A_{0,1} &  \cdots &  A_{0,N-1} \\ A_{1,0} &  A_{1,1} &  \cdots &  A_{1,N-1} \\ \vdots &  \vdots & &  \vdots \\ A_{M-1,0} &  A_{M-1,1} &  \cdots &  A_{M-1,N-1} \end{array} \right)^ T = \left( \begin{array}{c | c | c | c} A_{0,0}^ T &  A_{1,0}^ T &  \cdots &  A_{M-1,0}^ T \\ A_{0,1}^ T &  A_{1,1}^ T &  \cdots &  A_{M-1,1}^ T \\ \vdots &  \vdots & &  \vdots \\ A_{0,N-1}^ T &  A_{1,N-1}^ T &  \cdots &  A_{M-1,N-1}^ T \end{array} \right).$$

* Example
    * <img src="https://i.imgur.com/rOKh3xR.jpg" style="width:400px" />

### Matrix-Vector Multiplication with Special Matrices

* When doing calculation, we always concern flops and memops. And later we will prove that, **memops** is much slower that **flops**.
* Let's take an example. If we want calculate $y := A^T x + y$. Normally, we will do, set $B = A^T$, then $y := B x +y$
    * Which means, we are going to spend the most time to transpose matrix **A** to **B**, and little time computing.
    * What we want is, compute with $A^T$ without actually transposing.
    * The solution is, we can simply use columns of A for the dot products in the dot product based algorithm for $y := Ax + y$.

    
#### Triangular Matrix-Vector Multiplication

* Let $U \in \mathbb{R}^{n \times n}$ be an upper triangular matrix and $x \in \mathbb{R}^n$ be a vector. Consider
    * <img src="https://i.imgur.com/B7xe83S.jpg" style="width:400px" />
    * We notice that $u^T = 0$ (a vector of two zeroes) and hence we need not compute with it.
    * Let's calculate the **flops**:
        * The calculate step: $\psi_1 := u_{11} x_1 + u_{12}^T x_2 + \psi_1$, (without $u_{10}^T x_0$)
        * if we set the size of $U_{00}$ to $k$,then the size of $U_{02}$ and $U_{20}$ should be $n - k - 1$.
        * flops($u_{11} x_1$) = 1, flops($u_{12}^T x_2$) = $2(n-k-1)$, flops($u_{11} x_1 + u_{12}^T x_2$) = 1
        * So the flops = $\sum_{i=0}^k (2 + 2(n - k - 1)) = n*(n+1)$

#### Symmetric Matrix-Vector Multiplication

* <img src="https://i.imgur.com/LAGhDU3.jpg" style="width:300px" />
* We purposely chose the matrix on the right to be symmetric. We notice that $a_{10}^T = a_{01}$ , $A_{20}^T = A_{02}$ , and $a_{12}^T = a_{21}$.
* So we just need to change the step of calculation
    * By rows:
        * from $\psi_1 := a_{10}^T x_0 + \alpha_{11} x_1 + a_{12}^T x_2 + \psi_1$ 
        * to $\psi_1 := a_{01} x_0 + \alpha_{11} x_1 + a_{12}^T x_2 + \psi_1$
    * By columns:
        * from 
            * $y_0 := \chi_1 a_{01} + y_0$
            * $\psi_1 := \chi_1 \alpha_{11} + \psi_1$
            * $y_2 := \chi_1 a_{21} + y_2$
        * to
            * $y_0 := \chi_1 a_{01} + y_0$
            * $\psi_1 := \chi_1 \alpha_{11} + \psi_1$
            * $y_2 := \chi_1 (a_{11}^T)^T + y_2$ 

## Composing linear transformations

* Let $L_ A: \mathbb {R}^ k \rightarrow \mathbb {R}^ m$ and $L_ B: \mathbb {R}^ n \rightarrow \mathbb {R}^ k$ both be linear transformations and, for all $x \in \mathbb{R}^n$, define the function $L_ C: \mathbb {R}^ n \rightarrow \mathbb {R}^ m$ by $L_ C( x ) = L_ A( L_ B( x ) )$. Then $L_ C( x )$ is a linear transformations.

## Matrix-matrix multiplication

* $$A B = A \left( \begin{array}{c | c | c | c } b_0 &  b_1 &  \cdots &  b_{n-1} \end{array} \right) = \left( \begin{array}{c | c | c | c } A b_0 &  A b_1 &  \cdots &  A b_{n-1} \end{array} \right).$$
* If $$C = \begin{bmatrix} \gamma _{0,0} &  \gamma _{0,1} &  \cdots &  \gamma _{0,n-1} \\ \gamma _{1,0} &  \gamma _{1,1} &  \cdots &  \gamma _{1,n-1} \\ \vdots &  \vdots &  \vdots &  \vdots \\ \gamma _{m-1,0} &  \gamma _{m-1,1} &  \cdots &  \gamma _{m-1,n-1} \\ \end{bmatrix},\quad A = \begin{bmatrix} \alpha _{0,0} &  \alpha _{0,1} &  \cdots &  \alpha _{0,k-1} \\ \alpha _{1,0} &  \alpha _{1,1} &  \cdots &  \alpha _{1,k-1} \\ \vdots &  \vdots &  \vdots &  \vdots \\ \alpha _{m-1,0} &  \alpha _{m-1,1} &  \cdots &  \alpha _{m-1,k-1} \\ \end{bmatrix}, \\ \text{and} \quad B = \begin{bmatrix}{c c c c } \beta _{0,0} &  \beta _{0,1} &  \cdots &  \beta _{0,n-1} \\ \beta _{1,0} &  \beta _{1,1} &  \cdots &  \beta _{1,n-1} \\ \vdots &  \vdots &  \vdots &  \vdots \\ \beta _{k-1,0} &  \beta _{k-1,1} &  \cdots &  \beta _{k-1,n-1} \\ \end{bmatrix}.$$
* Then **C = AB** means that $\gamma _{i,j} = \sum _{p=0}^{k-1} \alpha _{i,p} \beta _{p,j}$

* A table of matrix-matrix multiplications with matrices of special shape is given at the end of this unit.

### Outer product

* Let $x \in \mathbb{R}^m$ and $y \in \mathbb{R}^n$. Then the outer product of **x** and **y** is given by $xy^T$. Notice that this yields an $m \times n$ matrix: 
    * $$\begin{aligned}
        xy^T &= \left( \begin{array}{c} \chi _0 \\ \chi _1 \\ \vdots \\ \chi _{m-1} \end{array} \right) \left( \begin{array}{c} \psi _0 \\ \psi _1 \\ \vdots \\ \psi _{n-1} \end{array} \right)^ T = \left( \begin{array}{c} \chi _0 \\ \chi _1 \\ \vdots \\ \chi _{m-1} \end{array} \right) \left( \begin{array}{c c c c} \psi _0 &  \psi _1 &  \cdots &  \psi _{n-1} \end{array} \right) \\
        &= \left( \begin{array}{c c c c} \chi _0 \psi _0 &  \chi _0 \psi _1 &  \cdots &  \chi _0 \psi _{n-1} \\ \chi _1 \psi _0 &  \chi _1 \psi _1 &  \cdots &  \chi _1 \psi _{n-1} \\ \vdots &  \vdots & &  \vdots \\ \chi _{m-1} \psi _0 &  \chi _{m-1} \psi _1 &  \cdots &  \chi _{m-1} \psi _{n-1} \end{array} \right).
         \end{aligned}$$
* <img src="https://i.imgur.com/X0nGqs6.jpg" style="width:600px" />
* The cost of memops of matrix-matrix multiplication is $2kmn$.

### Flops and Memops

* <img src="https://i.imgur.com/OHXo3JN.jpg" style="width:600px" />

