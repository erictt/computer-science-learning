# Week 9 - Vector Spaces

## When Systems Don’t Have a Unique Solution

* To solve $Ax = b$, we may face three different situations: Unique Solution, No Solution and Many Solutions.
* For example $\left(\begin{array}{c c c} 2 & 2 & -2 \\ -2 & -3 & 4 \\ 4 & 3 & -2\end{array}\right) \left(\begin{array}{c}\chi_0 \\ \chi_1 \\ \chi_2 \end{array}\right) = \left(\begin{array}{c} 0 \\ 3 \\ 4 \end{array}\right)$
    * We will end up with $\left(\begin{array}{c c c} 2 & 2 & -2 \\ 0 & -1 & 2 \\ 0 & 0 & 0\end{array}\right) \left(\begin{array}{c} 0 \\ 3 \\ 1 \end{array}\right)$
    * But $0 \ne 1$ => No solution
* For example $\left(\begin{array}{c c c} 2 & 2 & -2 \\ -2 & -3 & 4 \\ 4 & 3 & -2\end{array}\right) \left(\begin{array}{c}\chi_0 \\ \chi_1 \\ \chi_2 \end{array}\right) = \left(\begin{array}{c} 0 \\ 3 \\ 3 \end{array}\right)$
    * $\left(\begin{array}{c}\chi_0 \\ \chi_1 \\ \chi_2 \end{array}\right) = \left(\begin{array}{c} 3 \\ -3 \\ 0 \end{array}\right) + \beta \left(\begin{array}{c} -1 \\ 2 \\ 1 \end{array}\right)$
    * Many solutions

### When we have many solutions

* Consider $Ax=b$ and assume that we have
    * One solution to the system $Ax = b$, the specific solution we denote by $x_s$ so that $Ax_s = b$.
    * One solution to the system $Ax = 0$ that we denote by $x_n$ so that $Ax_n = 0$.
* Then 
    * $$A(x_s + x_n) = Ax_s + Ax_n = b + 0 = b$$
* So $x_s + x_n$ is also a solution
* Now $A(x_s + \beta x_n) = Ax_s + A(\beta x_n) = Ax_s + \beta A x_n = b + 0 = b$
* So $A(x_s + \beta x_n)$ is a solution for every $\beta \in \mathbb{R}$.
* Recall the example $\left(\begin{array}{c c c} 2 & 2 & -2 \\ -2 & -3 & 4 \\ 4 & 3 & -2\end{array}\right) \left(\begin{array}{c}\chi_0 \\ \chi_1 \\ \chi_2 \end{array}\right) = \left(\begin{array}{c} 0 \\ 3 \\ 3 \end{array}\right)$
    * After two steps of LU factorization, we get $$\begin{aligned} \chi_0 + \chi_2 &= 3 \\ \chi_1 - 2\chi_2 &= -3 \\ 0 &= 0 \end{aligned}$$
    * Set $\chi_2 = 0$, we conclude that a specific solution is given by $$x_s = \left(\begin{array}{c}\chi_0 \\ \chi_1 \\ \chi_2 \end{array}\right) = \left(\begin{array}{c} 3 \\ -3 \\ 0 \end{array}\right)$$
* Now, to calculate $x_n$. If we choose the free variable $\chi_2 = 0$, then it is easy to see that $\chi_0 = \chi_1 = 0$, and we end up with the trivial solution, $x = 0$. So, instead choose $\chi_2 = 1$: $$\begin{aligned} \chi_0 + 1 &= 0 \\ \chi_1 - 2(1) &= 0 \\ 0 &= 0 \end{aligned}$$
* $Ax = 0$: $$x_n = \left(\begin{array}{c} -1 \\ 2 \\ 1 \end{array}\right)$$
* But if $Ax_n = 0$, then $A(\beta x_n) = 0$. This means that all vectors $$x_s + \beta x_n = \left(\begin{array}{c} 3 \\ -3 \\ 0 \end{array}\right) + \beta \left(\begin{array}{c} -1 \\ 2 \\ 1 \end{array}\right)$$

#### Some terminology

* **row-echelon form**: 
    * <img src="https://i.imgur.com/cedWScz.jpg" style="width:120px" />
    * The boxed values are known as the **pivots**.
    * In each row to the left of the vertical bar, the left-most nonzero element is the pivot for that row. 
    * Notice that the pivots in later rows appear to the right of the pivots in earlier rows.
* **reduced row-echelon form**: 
    * <img src="https://i.imgur.com/tsfoTco.jpg" style="width:120px" />

### Summary

* Whether a linear system of equations $Ax = b$ has a unique solution, no solution, or multiple solutions can be determined by writing the system as an appended system $$\left(A | b\right)$$ and transforming this appended system to **row echelon form**, swapping rows if necessary.

## Review of Sets

* A **set** is a collection of distinct objects.
* The objects are the elements of the set.
* $x \in S$: (object) x is an element of set $S$. an element of S.
* If S contains object x, y and z: $$\{x, y, z\}$$
    * Order doesn't matter.
* The size of a set denoted by $|S|$.
* $(S \subset T) \iff (x \in S \Rightarrow x \in T)$

### Examples

* $\{1, 2, 3\}$
* $|\{1, 2, 3\}| = 3$
* The collection of all integers denoted by $\mathbb{Z}$ => $\{\ldots, -2, -1, 0, 1, 2, \ldots\}$. $|\mathbb{Z}| = \infty$
* The collection of all real numbers denoted by $\mathbb{R}$. $|\mathbb{R}| = \infty$
* The set of all vectors of size $n$ whose components are real valued is denoted by $\mathbb{R}^n$.

### Operations with Sets

* **Union of two set**
    * Notation: $S \cup T$
    * Formal definition: $S \cup T = \{ x | x \in S \vee x \in T\}$
* **Interaction of two sets**
    * Notation: $S \cap T$
    * Formal definition: $S \cap T = \{ x | x \in S \land x \in T\}$
* **Complement of two sets**
    * Notation: $T \backslash S$
    * Formal definition: $T \backslash S = \{ x | x \notin S \land x \in T\}$

## Vector Spaces

### Definition

* a vector space is a subset, $S$, of $\mathbb{R}^n$ with the following properties:
* $0 \in S$ (the zero vector of size n is in the set S); and
* If $v, w \in S$ then $(v+w) \in S$; and
* If $\alpha \in \mathbb{R}$ and $v \in S$ then $\alpha v \in S$.

* Example: The set $\mathbb{R}^n$ is a vector space:
    * $0 \in \mathbb{R}^n$
    * If $v, w \in \mathbb{R}^n$ then $(v+w) \in \mathbb{R}^n$; and
    * If $\alpha \in \mathbb{R}$ and $v \in \mathbb{R}^n$ then $\alpha v \in \mathbb{R}^n$.

### Subspaces

* **Subspaces** of $\mathbb{R}^n$ are the subsets of $\mathbb{R}^n$, and also vector spaces.
* **Examples**:
    * The set $S \subset \mathbb{R}^n$ described by $\{\chi a | \chi \in \mathbb{R}\}$, where $a \in \mathbb{R}^n$, is a subspace of $\mathbb{R}^n$.
        * $0 \in S$: (pick $\chi = 0$).
        * If $u, w \in S$ then $(u + w) \in S$: Pick $u, w \in S$. Then for some scalars $\upsilon$ and some scalars $\omega$, vector $v = \upsilon a$ and vector $w = \omega a$. Then $v+w = \upsilon a+ \omega a= (\upsilon + \omega)a$, which is also in S.
        * If $\alpha \in \mathbb{R}$ and $v \in S$ then $\alpha v \in S$: Pick $\alpha \in \mathbb{R}$ and $v \in S$. Then for some $\upsilon$, $v = \upsilon a$. But $\alpha v = \alpha (\upsilon a) = (\alpha \upsilon) a$. which is also in S.

### Span and Linear Independence

* **Definition**: 
    * **Linear Combination**: Let $u,v \in \mathbb{R}^m$ and $α,β \in \mathbb{R}$. Then $αu + βv$ is said to be a **linear combination** of vectors $u$ and $v$.
        * like we use `α` and `β` to scale vectors `u` and `v`.
        * For example, we can use vectors $u = \left(\begin{array}{c}1 \\ 2\end{array}\right) \text{ and } v = \left(\begin{array}{c}2 \\ 1\end{array}\right)$ to represent a plane by scaling them with `α` and `β`.
    * **Span**: Let $\{v_0, v_1, \cdots, v_{n-1} \} \subset \mathbb{R}^m$. Then the **span** of these vectors, Span $\{v_0, v_1, \cdots, v_{n-1}\}$, is said to be the set of all vectors that are a **linear combination** of the given set of vectors. 
       * Let $u,v \in \mathbb{R}^m$. $\text{Span }(u, v) = \mathbb{R}^m$ means we can use the linear combination of vectors **u** and **v** to represent all of the vectors $\in \mathbb{R}^m$.

* **Definition**: A **spanning set of a subspace** S is a set of vectors $\{v_0, v_1, \cdots, v_{n-1} \}$ such that Span($\{v_0, v_1, \cdots, v_{n-1} \}$) = S.
    * For example: $\text{Span }\{ \left(\begin{array}{c}1 \\ 2\end{array}\right), \left(\begin{array}{c}2 \\ 1\end{array}\right) \} = \mathbb{R}^2$
* **Definition**: Let $\{v_0, v_1, \cdots, v_{n-1} \} \subset \mathbb{R}^m$. Then this set of vectors is said to be **linearly independent** if $\chi_0 v_0 + \chi_1 v_1 + \cdots + \chi_{n-1} v_{n-1} = 0$ implies that $\chi_0 = \chi_1 = \cdots = \chi_{n-1} = 0$. A set of vectors that is not linearly independent is said to be **linearly dependent**.
    * In other words, the only solution for $Ax = 0$ is $\overrightarrow{x} = \overrightarrow{0}, \text{ where, } A = \{v_0, v_1, \cdots, v_{n-1}\}, x^T = \{\chi_0, \chi_1, \cdots, \chi_{n-1} \}$
    * For example: $\text{Span }\{ \left(\begin{array}{c}1 \\ 2\end{array}\right), \left(\begin{array}{c}2 \\ 4\end{array}\right) \}$ is **linearly dependent**.
        * Because the set $\left(\begin{array}{c}2 \\ 4\end{array}\right)$ can be represent with $2 \left(\begin{array}{c}1 \\ 2\end{array}\right)$. We can do: $2 \left(\begin{array}{c}1 \\ 2\end{array}\right) - \left(\begin{array}{c}2 \\ 4\end{array}\right) = 0$ to make the linear combination to be 0. And don't have to make all $\chi_n = 0$.
        * In other words, $\left(\begin{array}{c}2 \\ 4\end{array}\right)$ doesn't give us any new dimension, still the same as $\left(\begin{array}{c}1 \\ 2\end{array}\right)$.
        * So $\text{Span }\{ \left(\begin{array}{c}1 \\ 2\end{array}\right), \left(\begin{array}{c}2 \\ 4\end{array}\right) \} = \text{Span }\{ \left(\begin{array}{c}1 \\ 2\end{array}\right) \}$
        * $\left(\begin{array}{c}1 \\ 2\end{array}\right), \left(\begin{array}{c}2 \\ 1\end{array}\right)$ is **linear independent** set.
        * Also, we know that two vectors with different directions can span a plane. So if we add any vectors to $\{ \left(\begin{array}{c}1 \\ 2\end{array}\right), \left(\begin{array}{c}2 \\ 1\end{array}\right) \}$, it will be linear dependent set.

### The Column Space

* **Definition**: Let $A \in \mathbb{R}^{m \times n}$. Then **the column space** of A equals the set $\{Ax | x \in \mathbb{R}^n\}$. It is denoted by $\mathcal{C}(A)$. $$Ax = \left(\begin{array}{c|c|c|c} a_0 & a_1 & \cdots & a_{n-1}\end{array}\right) \left(\begin{array}{c} \chi_0 \\ \chi_1 \\ \vdots \\ \chi_{n-1}\end{array}\right) = \chi_0 a_0 + \chi_1 a_1 + \cdots + \chi_{n-1} a_{n-1}$$
    * Thus $\mathcal{C}(A)$ equals the set of **all linear combinations** of the columns of matrix A.
* **Theorem**: The column space of $A \in \mathbb{R}^{m \times n}$ is a subspace of $\mathbb{R}^m$
* **Theorem**: Let $A \in \mathbb{R}^{m \times n}, x \in \mathbb{R}^n$, and $b \in \mathbb{R}^m$. Then $Ax = b$ has a solution if and only if $b \in \mathcal{C}(A)$.

### The Null Space

* **Definition**: Let $A \in \mathbb{R}^{m \times n}$. The set of all vectors $x \in \mathbb{R}^n$ that have the property that $Ax = 0$ is called **the null space** of A. 
    * Frankly speaking, all of the possible vector x that satisfy $Ax = 0$.
        * So $x$ should be perpendicular to $A$.
* **Notation**: $\mathcal{N}(A) = \{x|Ax = 0\}$
* **Theorem**: Let $A \in \mathbb{R}^{m \times n}$. The null space of $A, \mathcal{N}(A)$, is a subspace.
* Example:
    * $A = \begin{bmatrix} 1 & 1 & 1 & 1 \\ 1 & 2 & 3 & 4 \\ 4 & 3 & 2 & 1 \end{bmatrix}$
    * $\text{rref }(A) = \begin{bmatrix} 1 & 0 & -1 & -2 \\ 0 & 1 & 2 & 3 \\ 0 & 0 & 0 & 0 \end{bmatrix}$
        * **rref**: reduced row-echelon form.
    * => $\chi_0 - \chi_2  - 2\chi_3 = 0, \chi_1 + 2 \chi_2 + 3 \chi_3 = 0$
    * => $\begin{bmatrix} \chi_0 \\ \chi_1 \\ \chi_2 \\ \chi_3 \end{bmatrix} = \chi_2 \begin{bmatrix} 1 \\ -2 \\ 1 \\ 0 \end{bmatrix} + \chi_3\begin{bmatrix} 2 \\ -3 \\ 0 \\ 1 \end{bmatrix}$
    * We defined: $\chi_2 \in \mathbb{R}, \chi_3 \in \mathbb{R}$
    * So, $\mathcal{N}(A) = \text{Span }\left( \begin{bmatrix} 1 \\ -2 \\ 1 \\ 0 \end{bmatrix},\begin{bmatrix} 2 \\ -3 \\ 0 \\ 1 \end{bmatrix}\right)$
    * $\mathcal{N}(A) = \mathcal{N}(\text{rref }(A))$

### More about Span, Linear Independence, and Bases

* **Theorem**: Let the set of vectors $\{  v_0, v_1 , \ldots , v_{n-1} \}  \subset \mathbb {R}^ m$ be linearly dependent. Then at least one of these vectors can be written as a linear combination of the others.
    * In other words, the dependent vector $a_j$ can be written as a linear combination of the other n−1 vectors.
    * <img src="https://i.imgur.com/3Yb11Fc.jpg" style="width:400px" />
* **Theorem**: Let  $\{  a_0, a_1 , \ldots , a_{n-1} \}  \subset \mathbb {R}^ m$ and let $A = \left(\begin{array}{c|c|c|c} a_0 & a_1 & \cdots & a_{n-1}\end{array}\right)$. Then the vectors $\{ a_0, a_1 , \ldots , a_{n-1} \}$ are **linearly independent** if and only if $\mathcal{N}(A) = \{0\}$.
    * aka $\chi_0 = \chi_1 = \cdots = \chi_{n-1} = 0$
* **Definition**: **A basis for a subspace S** of $R^n$ is a set of vectors in S that 
    1. is linearly independent and 
    2. Spans S.
    
    * **Basis** is the minimum set of vectors  that spans the subspace.
    * Let $\{v_1, v_2, \cdots, v_n\} = \text{ Basis of subspace U }$. Then $\{v_1, v_2, \cdots, v_n\}$ are linear independent, 
    * And all of the linear combinations of $\{v_1, v_2, \cdots, v_n\}$ can get **all of the possible components** of $U$. And each member of U can be uniquely defined by a unique combination of $\{v_1, v_2, \cdots, v_n\}$.
* **Theorem**: Let S be a subspace of $\mathbb{R}^m$ and let $\{v_0, v_1, \cdots, v_{k-1} \} \subset \mathbb{R}^m$ and $\{w_0, w_1, \cdots, w_{n-1} \} \subset \mathbb{R}^m$ both be basis for S. Then $k = n$. In other words, the number of vectors in a basis is unique.
* **Definition**: **The dimension of a subspace S** equals the number of vectors in a basis for that subspace.
    * For example: $A = \begin{bmatrix}1 & 1 & 2 & 3 & 2 \\ 1 & 1 & 3 & 1 & 4\end{bmatrix}$
    * $\text{rref }(A) = \begin{bmatrix}1 & 1 & 2 & 3 & 2 \\ 0 & 0 & 1 & -2 & 2\end{bmatrix}$
    * => $\begin{bmatrix} \chi_0 \\ \chi_1 \\ \chi_2 \\ \chi_3 \\ \chi_4 \end{bmatrix} = \chi_1 \begin{bmatrix} -1 \\ 1 \\ 0 \\ 0 \\ 0 \end{bmatrix} + \chi_3\begin{bmatrix} -7 \\ 0 \\ 2 \\ 1 \\ 0 \end{bmatrix} + \chi_4\begin{bmatrix} 2 \\ 0 \\ -2 \\ 0 \\ 1 \end{bmatrix}$
    * set $v_0 = \begin{bmatrix} -1 \\ 1 \\ 0 \\ 0 \\ 0 \end{bmatrix} , v_1 = \begin{bmatrix} -7 \\ 0 \\ 2 \\ 1 \\ 0 \end{bmatrix}, v_2 = \begin{bmatrix} 2 \\ 0 \\ -2 \\ 0 \\ 1 \end{bmatrix}$
    * then $\{v_0, v_1, v_2\}$ is the basis of $\mathcal{N}(A)$.
    * $\mathcal{N}(A) = \mathcal{N}(\text{rref}(A)) = \text{Span }(v_0, v_1, v_2)$.
    * the dimension of null space of A = 3, which also equals to the number of non-pivot columns of $\text{rref}(A)$.
    * $\mathcal{C}(A) = \text{Span}(\begin{pmatrix}1 \\ 1\end{pmatrix}, \begin{pmatrix}2 \\ 3\end{pmatrix})$.
    * the dimension of A = 2, which also equals to the number of pivot columns of $\text{rref}(A)$.
* **Definition**: Let $A \in \mathbb{R}^{m \times n}$. **The rank of A** equals the number of vectors in a basis for the column space of A. Denoted by $\text{rank}(A)$.

## Showing that A^T A is invertible

* Let $A \in \mathbb{R}^{m \times k}$, and $\{a_0, a_2, \cdots, a_{m-1}\}$ are linearly independent. Is $A^T A$ invertible?
* $A^T A \in \mathbb{R}^{k \times k}$.
* So, we only need to prove $A^T A$'s columns also linear independent.
    * Because, $A^T A$ is a square matrix, if $A^T A$'s columns are linear independent, the reduced row-echelon form of $A^T A$ will be $I$.
* Let $v \in \mathcal{N}(A^T A)$
    * then $A^T A v = 0$ => $v^T A^T A v = v^T \overrightarrow{0} = 0$ => $(A v)^T A v = 0$ 
    * which means $\lVert Av \rVert _2 = 0$ => $A v = 0$
    * We've assumed $A$'s columns are linearly independent, 
    * so $v \in \mathcal{N}(A) = \{\overrightarrow{0}\}$ => $v = \overrightarrow{0}$
    * So, the only solution of $A^T A v = 0$ is $v = \overrightarrow{0}$
* Then $A^T A$'s columns are linearly independent, which means $A^T A$ is invertible.

## Refers

* [https://www.khanacademy.org/math/linear-algebra/vectors-and-spaces](https://www.khanacademy.org/math/linear-algebra/vectors-and-spaces)
* [https://www.khanacademy.org/math/linear-algebra/matrix-transformations/matrix-transpose/v/lin-alg-showing-that-a-transpose-x-a-is-invertible](https://www.khanacademy.org/math/linear-algebra/matrix-transformations/matrix-transpose/v/lin-alg-showing-that-a-transpose-x-a-is-invertible)

## Words

* **echelon** ['eʃəlɔn] n. 梯形；梯次编队；梯阵；阶层 vi. 形成梯队 vt. 排成梯队

