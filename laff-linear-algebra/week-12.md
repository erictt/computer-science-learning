# Week 12 - Eigenvalues and Eigenvectors

## The Algebraic Eigenvalue Problem

* The algebraic eigenvalue problem is given by \\[Ax = \lambda x\\]
* where \\(A \in \mathbb{R}^{n \times n}\\) is a square matrix, \\(\lambda\\) is a scalar, and \\(x\\) is a nonzero vector.
    * If \\(x \ne 0\\), then \\(\lambda\\) is said to be an eigenvalue and x is said to be an **eigenvector** associated with the **eigenvalue** \\(\lambda\\).
    * The tuple \\((\lambda, x)\\) is said to be an **eigenpair**.
    * The set of all vectors **x** that satisfy \\(Ax = \lambda x\\) is a subspace, called **eigenspace**.
* Equivalent statements:
    * \\(Ax = \lambda x\\), where \\(x \ne 0\\).
    * \\((A - \lambda I) x = 0\\), where \\(x \ne 0\\).
    * \\(A - \lambda I\\) is singular.
    * \\(\mathcal{N}(A - \lambda I)\\) contains a nonzero vector x.
        * This is a consequence of there being a vector \\(x \ne 0\\) such that \\((A - \lambda I)x = 0\\).
    * \\(\text{dim}(\mathcal{N}(A - \lambda I)) > 0\\).
    * \\(\text{det}(A - \lambda I) = 0\\).
        * => \\(\mathcal{N}(A - \lambda I) \ne \{0\}\\)
        * A is a square matrix => \\((A - \lambda I)\\) is not invertible
        * => \\((A - \lambda I) x = 0\\) has many solutions.
        * More proves in **Week 7#Showing that A^T A is invertible**
        
* If we ﬁnd a vector \\(x \ne 0\\) such that \\(Ax = \lambda x\\), it is certainly not unique.
    * For any scalar \\(\alpha\\), \\(A(\alpha x) = \lambda (\alpha x)\\) also holds.
    * If \\(Ax = \lambda x\\) and \\(Ay = \lambda y\\), then \\(A(x + y) = Ax + Ay = \lambda x + \lambda y = \lambda (x + y)\\)
* We conclude that the set of all vectors \\(x\\) that satisfy \\(Ax = \lambda x\\) is a subspace.

## Simple cases

* The eigenvalue of the **zero** matrix is the scalar \\(\lambda = 0\\). All nonzero vectors are eigenvectors.
* The eigenvalue of the **identity** matrix is the scalar \\(\lambda = 1\\). All nonzero vectors are eigenvectors.
* The eigenvalues of a **diagonal** matrix are its elements on the diagonal. The unit basis vectors are eigenvectors.
* The eigenvalues of a **triangular** matrix are its elements on the diagonal.
    * Because if there is a zero on the diagonal, it is singular.
* The eigenvalues of a 2 × 2 matrix can be found by finding the roots of \\(p_2(\lambda) = \text{det}(A - \lambda I) = 0\\)
* The eigenvalues of a 3 × 3 matrix can be found by finding the roots of \\(p_3(\lambda) = \text{det}(A - \lambda I) = 0\\)

### Compute the eigenvalues and eigenvectors of 2×2 matrices

* Compute \\[\text{det}(\begin{pmatrix} (\alpha_{0,0} - \lambda) & \alpha_{0,1} \\ \alpha_{1,0} & (\alpha_{1,1} - \lambda)\end{pmatrix}) = (\alpha_{0,0} - \lambda)(\alpha_{1,1} - \lambda) - \alpha_{0,1}\alpha_{1,0} = 0\\]
* Recognize that this is a second degree polynomial in \\(\lambda\\).
* It is called the **characteristic polynomial** of the matrix \\(A, p_2(\lambda)\\).
* Compute the coefficients of \\(p_2(\lambda)\\) so that \\[p_2(\lambda) = - \lambda^2 + \beta \lambda + \gamma\\]
* Solve \\[- \lambda^2 + \beta \lambda + \gamma = 0\\]
* for its roots. You can do this either by examination, or by using the quadratic formula: \\[\lambda = \frac{-\beta \pm \sqrt{\beta^2 + 4 \gamma} }{-2}\\]
* Find all of the eigenvectors that satisﬁes \\[\begin{pmatrix} (\alpha_{0,0} - \lambda) & \alpha_{0,1} \\ \alpha_{1,0} & (\alpha_{1,1} - \lambda)\end{pmatrix}\begin{pmatrix} \chi_0 \\ \chi_1\end{pmatrix} = \begin{pmatrix} 0 \\ 0\end{pmatrix}\\]
    * Transform \\(\begin{pmatrix} (\alpha_{0,0} - \lambda) & \alpha_{0,1} \\ \alpha_{1,0} & (\alpha_{1,1} - \lambda)\end{pmatrix}\\) to row-echelon form with different \\(\lambda\\)s, find the eigenspaces.
* Check your answer! It is a matter of plugging it into \\(Ax = \lambda x\\) and seeing if the computed \\(\lambda\\) and \\(x\\) satisfy the equation.

#### Example

* \\(A = \begin{bmatrix} 1 & 2 \\ 4 & 3 \end{bmatrix}\\)
* \\(\text{det}(\begin{bmatrix} 1 - \lambda & 2 \\ 4 & 3 - \lambda \end{bmatrix}) = 0\\)
* \\((1 - \lambda) (3 - \lambda)- 8 = 0\\)
* => \\(\lambda = 5 \text{ or } \lambda = -1\\)
* For any eigenvalues \\(\lambda\\), \\(\mathcal{E}_A(\lambda) = \mathcal{N}(\lambda I_n - A)\\)
    * \\(\mathcal{E}_A(\lambda)\\): **eigenspace**.
* when \\(\lambda = 5\\), then \\(\mathcal{E}_A(5) = \mathcal{N}(\begin{bmatrix} 4 & -2 \\ -4 & 2 \end{bmatrix})\\). 
    * Transform to row-echelon form, we get \\(\begin{bmatrix} 1 & -1/2 \\ 0 & 0 \end{bmatrix} \begin{bmatrix} \chi_0 \\ \chi_1 \end{bmatrix} = \begin{bmatrix} 0 \\ 0 \end{bmatrix}\\)
* then \\(\chi_0 = \frac{1}{2} \chi_1\\)
* \\(\mathcal{E}_A(5) = \{\begin{bmatrix} \chi_0 \\ \chi_1 \end{bmatrix} = \epsilon \begin{bmatrix} 1/2 \\ 1 \end{bmatrix}, \epsilon \in \mathbb{R}\}\\)
* \\(\mathcal{E}_A(5) = \text{Span}(\begin{bmatrix} 1/2 \\ 1 \end{bmatrix})\\)
* Same way, we get \\(\mathcal{E}_A(-1) = \text{Span}(\begin{bmatrix} -1 \\ 1 \end{bmatrix})\\)

## Diagonalization

* **Theorem**: Let \\(A \in \mathbb{R}^{n \times n}\\). Then there exists a nonsingular matrix \\(X\\) such that \\(X^{-1} A X = \Lambda\\) iff \\(A\\) has **n** **linearly independent eigenvectors**. Then \\[\begin{aligned} X^{-1} A X &= \Lambda \\ A X &= X \Lambda \\ A &= X \Lambda X^{-1}\end{aligned}\\]
    * \\[\Lambda = \begin{pmatrix} \lambda_1 & & & \\ & \lambda_2 & & \\ & & \ddots & \\ & & & \lambda_n \end{pmatrix}\\]
* If \\(\Lambda\\) is in addition diagonal, then the diagonal elements of \\(\Lambda\\) are **eigenvalues** of **A** and the columns of **X** are **eigenvectors** of **A**.
* For example:
    * \\(A = \begin{pmatrix} 1 & -1 \\ 2 & 4 \end{pmatrix}\\)
    * the eigenpairs are \\((2, \begin{pmatrix} -1 \\ 1 \end{pmatrix}), (3 \begin{pmatrix} -1 \\ 2 \end{pmatrix})\\)
    * Then:
    * <img src="https://i.imgur.com/UYfYgSZ.jpg" style="width:600px" />
    * **The matrix A can be diagonalized**.


### Defective matrices

* A **defective matrix** is a square matrix that does not have a complete basis of eigenvectors, and is therefore not **diagonalizable**. In particular, an n × n matrix is defective if and only if it does **not** have **n linearly independent eigenvectors**.

#### Jordan Block

* In general, the k ×k matrix \\(J_k(\lambda)\\) given by \\[J_k(\lambda) = \begin{pmatrix} \lambda & 1 & 0 & \cdots & 0 & 0 \\ 0 & \lambda & 1 & \cdots & 0 & 0 \\ 0 & 0 & \lambda & \cdots & 0 & 0 \\ \vdots & \vdots & \vdots & \ddots & \vdots & \vdots \\ 0 & 0 & 0 & \cdots & \lambda & 1 \\ 0 & 0 & 0 & \cdots & 0 & \lambda \end{pmatrix}\\] 
* a simple example: \\[\begin{pmatrix} \lambda & 1 \\ 0 & \lambda \end{pmatrix}\\]
* Any nontrivial Jordan block of size 2×2 or larger (that is, not completely diagonal) is defective.

* **Example**
    * A simple example of a defective matrix is: \\[{ {\begin{bmatrix}3&1\\0&3\end{bmatrix} } }\\]
    * which has a double eigenvalue of **3** but only **one** distinct eigenvector \\[{\begin{bmatrix}1\\0\end{bmatrix} }\\]

## General case

* **Theorem**: The matrix \\(A \in \mathbb{R}^{n \times n}\\) is **nonsingular** iff \\(\text{det}(A) \ne 0\\).
* **Theorem**: Given \\(A \in \mathbb{R}^{n \times n}\\), \\[p_n(\lambda) = \text{det}(A - \lambda I) = \lambda^n + \gamma_{n-1} \lambda^{n-1} + \cdots + \gamma_1 \lambda + \gamma_0\\] for some **coefficients** \\(\gamma_1, \ldots, \gamma_{n-1} \in \mathbb{R}\\)
* **Definition**: Given \\(A \in \mathbb{R}^{n \times n}\\), \\(p_n(\lambda) = \text{det}(A - \lambda I)\\) is called the **characteristic polynomial**.

* <img src="https://i.imgur.com/kcwPmSK.jpg" style="width:650px" />

## Properties of eigenvalues and eigenvectors

* **Definition**: Given \\(A \in \mathbb{R}^{n \times n}\\) and nonzero vector \\(x \in \mathbb{R}^{n}\\) , the scalar \\(x^T Ax/x^T x\\) is known as the **Rayleigh quotient**.
* **Theorem**: Let \\(A \in \mathbb{R}^{n \times n}\\) and x equal an eigenvector of A. Assume that x is real valued as is the T eigenvalue λ with \\(Ax = \lambda x\\). Then \\(\lambda = x x^T Ax x\\) is the eigenvalue associated with the eigenvector x.
* **Theorem**: Let \\(A \in \mathbb{R}^{n \times n}\\) , β be a scalar, and \\(\lambda \in \Lambda(A)\\). Then \\(\beta \lambda \in \Lambda(\beta A)\\).
* **Theorem**: Let \\(A \in \mathbb{R}^{n \times n}\\) be nonsingular, \\(\lambda \in \Lambda(A)\\), and \\(Ax = \lambda x\\). Then \\(A^{-1} x = \frac{1}{\lambda} x\\).
* **Theorem**: Let \\(A \in \mathbb{R}^{n \times n}\\), \\(\lambda \in \Lambda(A)\\),  Then \\((\lambda - \mu ) \in \Lambda(A - \mu I)\\).

## Relative Definitions

### Eigenspaces

* the nullspace \\(A - I\lambda\\) is the **eigenspace** of A for λ denoted by \\(\mathcal{E}_A(\lambda)\\). In other words, \\(\mathcal{E}_A(\lambda)\\) consists of all the eigenvectors of A for λ and the zero vector.


### Algebraic and Geometric Multiplicity

* Example: Let \\(A = \begin{bmatrix} 1 & 2 \\ 1 & 0 \end{bmatrix}\\)
    * -1 is an eigenvalue of A. and the correspond eigenvector is \\(\begin{bmatrix} -1 \\ 1 \end{bmatrix}\\)
* \\(\mathcal{E}_A(-1) = \text{Span}(\begin{bmatrix} -1 \\ 1\end{bmatrix})\\)
* The **geometric multiplicity** of an eigenvalue λ of A is the dimension of \\(\mathcal{E}_A(\lambda)\\)
    * the geometric multiplicity of −1 is 1.
* The **algebraic multiplicity** of an eigenvalue λ of A is the number of times λ appears as a root of \\(p_A\\). 
    * −1  appears only **once** as a root.  the algebraic multiplicity of -1 is 1.
* In general, the algebraic multiplicity and geometric multiplicity of an eigenvalue can differ. However, the geometric multiplicity can **never exceed** the algebraic multiplicity.
* If for every eigenvalue of A, the **geometric multiplicity** equals the **algebraic multiplicity**, then A is said to be **diagonalizable**.

### Singular Matrix

* **A matrix is singular** if and only if 0 is one of its **eigenvalues**. A singular matrix can be either diagonalizable or not diagonalizable. For example:
    * \\(\left(\begin{array}{c c} 1 & 0 \\ 0 & 0\end{array}\right)\\) is diagonalizable
    * \\(\left(\begin{array}{c c} 0 & 1 \\ 0 & 0\end{array}\right)\\) is not diagonalizable.

### Polynomial Roots

* A root of a polynomial \\(P(z)\\) is a number \\(z_i\\) such that \\(P(z_i)=0\\). The fundamental theorem of algebra states that a polynomial \\(P(z)\\) of degree n has n roots, some of which may be degenerate. 
* For example, the roots of the polynomial \\(x^3-2x^2-x+2=(x-2)(x-1)(x+1)\\) are -1, 1, and 2. 


## Refers

* [http://mathworld.wolfram.com/SingularMatrix.html](http://mathworld.wolfram.com/SingularMatrix.html)
* [https://en.wikipedia.org/wiki/Invertible_matrix](https://en.wikipedia.org/wiki/Invertible_matrix)
* [http://mathworld.wolfram.com/Determinant.html](http://mathworld.wolfram.com/Determinant.html)
* [https://en.wikipedia.org/wiki/Defective_matrix](https://en.wikipedia.org/wiki/Defective_matrix)
* [http://people.math.carleton.ca/~kcheung/math/notes/MATH1107/wk10/10_algebraic_and_geometric_multiplicities.html](http://people.math.carleton.ca/~kcheung/math/notes/MATH1107/wk10/10_algebraic_and_geometric_multiplicities.html)
* [http://mathworld.wolfram.com/PolynomialRoots.html](http://mathworld.wolfram.com/PolynomialRoots.html)

## Words 

* **eigenvalue** ['aiɡən,vælju:] n. [数] 特征值
* **eigenvector** ['aiɡən,vektə] n. [数] 特征向量；本征矢量
* **diagonalization** [dai,æɡənəlai'zeiʃən, -li'z-] n. [数] 对角化；对角线化
* **multiplicity** [,mʌlti'plisəti] n. 多样性；[物] 多重性
* **algebraic and geometric multiplicity** 代数重数与几何重数
* **companion matrix** 友（矩）[数] 阵
* **spectrum** ['spektrəm] n. 光谱；频谱；范围；余象


