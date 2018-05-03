# Week 6 - Gaussian Elimination

[TOC]

## Gaussian Elimination

* To solv the linear system: \\[\begin{array}{c c c c c c}
    2 \chi_0 & + & 4 \chi_1 & - & 2 \chi_2 & = & -10 \\
    4 \chi_0 & - & 2 \chi_1 & + & 6 \chi_2 & = & 20 \\
    6 \chi_0 & - & 4 \chi_1 & + & 2 \chi_2 & = & 18
    \end{array}\\]

### Procedures

* **Transform linear system of equations to an upper triangular system**
    * Subtract \\(\lambda_{1,0} = (\color{blue}{4} / \color{red}{2} ) = 2\\) times the first equation from the second equation: \\[\begin{array}{c | c}
        \text{Before} & \text{After} \\
        \begin{array}{c c c c c c}
    \color{red}{2} \chi_0 & + & 4 \chi_1 & - & 2 \chi_2 & = & -10 \\
    4 \chi_0 & - & 2 \chi_1 & + & 6 \chi_2 & = & 20 \\
    6 \chi_0 & - & 4 \chi_1 & + & 2 \chi_2 & = & 18
    \end{array} & \begin{array}{c c c c c c}
    2 \chi_0 & + & 4 \chi_1 & - & 2 \chi_2 & = & -10 \\
    & - & 10 \chi_1 & + & 10 \chi_2 & = & 40 \\
    6 \chi_0 & - & 4 \chi_1 & + & 2 \chi_2 & = & 18
    \end{array}
    \end{array}\\]
    
    * Subtract \\(\lambda_{2,0} = ( \color{blue}{6} / \color{red}{2} ) = 3\\) times the first equation from the third equation: \\[\begin{array}{c | c}
        \text{Before} & \text{After} \\
        \begin{array}{c c c c c c}
    \color{red}{2} \chi_0 & + & 4 \chi_1 & - & 2 \chi_2 & = & -10 \\
    & - & 10 \chi_1 & + & 10 \chi_2 & = & 40 \\
    \color{blue}{6} \chi_0 & - & 4 \chi_1 & + & 2 \chi_2 & = & 18
    \end{array} & \begin{array}{c c c c c c}
    2 \chi_0 & + & 4 \chi_1 & - & 2 \chi_2 & = & -10 \\
    & - & 10 \chi_1 & + & 10 \chi_2 & = & 40 \\
    & - & 16 \chi_1 & + & 8 \chi_2 & = & 48
    \end{array}
    \end{array}\\]
    
    * Subtract \\(\lambda_{2,0} = ( \color{blue}{-16} / \color{red}{-10} ) = 1.6\\) times the second equation from the third equation: \\[\begin{array}{c | c}
        \text{Before} & \text{After} \\
        \begin{array}{c c c c c c}
    2 \chi_0 & + & 4 \chi_1 & - & 2 \chi_2 & = & -10 \\
    & \color{red}{-} & \color{red}{10 \chi_1} & + & 10 \chi_2 & = & 40 \\
    & \color{red}{-} & \color{red}{16 \chi_1} & + & 8 \chi_2 & = & 48
    \end{array} & \begin{array}{c c c c c c}
    2 \chi_0 & + & 4 \chi_1 & - & 2 \chi_2 & = & -10 \\
    & - & 10 \chi_1 & + & 10 \chi_2 & = & 40 \\
    & & & - & 8 \chi_2 & = & - 16
    \end{array}
    \end{array}\\]
    
    * This now leaves us with an upper triangular system of linear equations.

* **Back substitution (solve the upper triangular system)**
    * The equivalent upper triangular system of equations is now solved via back substitution:
        * Consider the last equation, \\[-8 \chi_2 = -16.\\] Scaling both sides by by 1/(−8) we find that \\[\chi_2 = -16/(-8) = 2.\\]
        * Next, consider the second equation, \\[-10 \chi_1 + 10 \chi_2 = 40.\\] We know that \\(\chi_2 = 2\\), which we plug into this equation to yield \\[-10\chi_1 + 10( \color{blue}{2} = 40.)\\] Rearranging this we find that \\[\chi_1 = (40 - 10( \color{blue}{2} ))/(-10) = -2.\\]
        * Finally, consider the first equation, \\[2\chi_0 + 4\chi_1 - 2\chi_2 = -10 \\] We know that \\(\chi_2 =  \color{blue}{2} \\) and \\(\chi_1 = \color{blue}{-2} \\), which we plug into this equation to yield \\[2\chi_0 + 4( \color{blue}{-2} ) - 2( \color{blue}{2} ) = -10.\\] Rearranging this we find that \\[\chi_0 = (-10 - (4( \color{blue}{-2} ) - (2)( \color{blue}{2} )))/2 = 1.\\]
* Thus, the solution is vector \\[x = \left(\begin{array}{c} \chi_0 \\ \chi_1 \\ \chi_2 \end{array}\right) = \left(\begin{array}{c} 1 \\ -2 \\ 2 \end{array}\right).\\]
* **Check your answer** (by plugging \\(\chi_0 = 1, \chi_1 = -2, \text{and} \ \chi_2 = 2\\) into the original system).

### Representing the system of equations with an appended matrix

* <img src="media/15231973476841.jpg" style="width:600px"/>

### Transform to matrix to upper triangular matrix

* <img src="media/15231974994600.jpg" style="width:600px"/>

* **Forward substitution (applying the transforms to the right-hand side)**
* <img src="media/15231975659888.jpg" style="width:600px"/>

### Algorithms

* <img src="media/15231979384284.jpg" style="width:400px"/>

* <img src="media/15231979559406.jpg" style="width:400px"/>

## Solving Ax = b via LU Factorization

### LU Factorization

* A matrix \\(A \in R^{n \times n}\\) can be factored into the product of two matrices \\(L,U \in R^{n \times n}\\) : \\[A= LU\\] where L is unit lower triangular and U is upper triangular.
* LU Factorization is transfer A to a LU combined matrix.
    * We can do this, because L is unit lower triangle matrix and U is upper triangle matrix.
* <img src="media/15231982087014.jpg" style="width:500px" />
* <img src="media/15231982335804.jpg" style="width:400px" />
* After rearrange, we get:
    * <img src="media/15231983143005.jpg" style="width:250px"/>
* Partition matrix A:
    * Update \\(a_{21} = a_{21}/ \alpha_{11} (= l_{21})\\)
    * Update \\(A_{22} = A_{22} - a_{21} a_{12}^T\\) (Rank-1 update!)
    * Overwrite \\(A_{22}\\) with \\(L_{22}\\) and \\(U_{22}\\) by repeating with \\(A = A_{22}\\).
* This will leave U in the upper triangular part of A and the strictly lower triangular part of L in the strictly lower triangular part of A. The diagonal elements of L need not be stored, since they are known to equal one.

#### Algorithm

* <img src="media/15231985740688.jpg" style="width:450px" />

### Where is this going?

1. Want to solve: \\(Ax = b\\)
    * Give A and b, solve x.
    * \\[A = \left(\begin{array}{c c c}
    2 & + 4 & - 2 \\
    4 & - 2 & + 6 \\
    6 & - 4 & + 2
    \end{array}\right), 
    b = \left(\begin{array}{c}
    -10 \\ 20 \\ 18
    \end{array}\right)\\]
2. Now we find triangular L and U so that: \\(A = LU\\)
    * U is the transformed A matrix
    * A is the coefficients which transfers A to U
    * Transfered: \\[A \to \left(\begin{array}{c c c}
    2 & + 4 & - 2 \\
    \scriptsize{2} & - 10 & - 10 \\
    \scriptsize{3} & \scriptsize{1.6} & - 8
    \end{array}\right),
    L = \left(\begin{array}{c c c}
    1 & 0 & 0 \\
    2 & 1 & 0 \\
    3 & 1.6 & 1
    \end{array}\right),
    U = \left(\begin{array}{c c c}
    2 & + 4 & - 2 \\
    0 & - 10 & + 10 \\
    0 & 0 & - 8
    \end{array}\right)\\]
3. Substitute: \\((LU)x = b\\) => \\(L(Ux) = b\\)
4. Replace Ux with y. (\\(y = Ux\\)) => \\(Ly = b\\)
5. Solve \\(Ly = b\\) for \\(y\\). (**Next Section**)
    * This is forward substitution (applying the transforms to the right-hand side).
    * \\[\left(\begin{array}{c c c}
    1 & 0 & 0 \\
    2 & 1 & 0 \\
    3 & 1.6 & 1
    \end{array}\right) \times 
    \left(\begin{array}{c} 
    y_0 \\ y_1 \\ y_2
    \end{array}\right) =
    \left(\begin{array}{c}
    -10 \\ 20 \\ 18
    \end{array}\right) \to \left(\begin{array}{c}
        -10 \\
        20 - 2 y_0 \\ 
        18 - 3 y_0
    \end{array}\right) \to \left(\begin{array}{c}
        -10 \\
        40 \\ 
        48 - 1.6 y_1
    \end{array}\right) \to \left(\begin{array}{c}
        -10 \\
        40 \\ 
        -16
    \end{array}\right)\\]
    
6. Solve \\(Ux = y\\) for \\(x\\). (**Next Next Section**)
    * This is back substitution (solve x).
    * \\[\left(\begin{array}{c c c}
    2 & + 4 & - 2 \\
    0 & - 10 & + 10 \\
    0 & 0 & - 8
    \end{array}\right) \times 
    \left(\begin{array}{c} 
    x_0 \\ x_1 \\ x_2
    \end{array}\right) = \left(\begin{array}{c}
        -10 \\ 40 \\  -16
    \end{array}\right) \\]
    * \\[ \to \left(\begin{array}{c}
        -10 \\ 40 \\  \frac{-16}{-8} = \color{blue}{2}
    \end{array}\right) \to \left(\begin{array}{c} - 10 \\
        \frac{40 - 10 \times \color{blue}{2} }{-10} = \color{red}{- 2} \\ 
        \color{blue}{2}
    \end{array}\right) \to \left(\begin{array}{c}
        \frac{-10 - 4 \times ( \color{red}{- 2} ) - ( -2 ) \times \color{blue}{2}}{2} = \color{green}{1} \\ \color{red}{- 2} \\ \color{blue}{2}
    \end{array}\right) \to \left(\begin{array}{c}
        \color{green}{1} \\ \color{red}{- 2} \\ \color{blue}{2}
    \end{array}\right)\\]

### Solving Lz = b (Forward substitution)

* Given a unit lower triangular matrix \\(L \in \mathbb{R}^{n \times n}\\) and vectors \\(z, b \in \mathbb{R}^{n}\\) , consider the equation \\(Lz = b\\) where L and b are known and z is to be computed. Partition
* <img src="media/15232550852200.jpg" style="width:600px" />
* So, solving \\(Lz = b\\), overwriting b with z, is forward substitution when L is the unit lower triangular matrix that results from LU factorization.

#### Algorithm

* Algorithm for solving Lx = b, overwriting b with the result vector x. Here L is a lower triangular matrix.
* <img src="media/15231996544107.jpg" style="width:450px" />

### Solving Ux = b (Back substitution)

* <img src="media/15232553109209.jpg" style="width:600px" />

#### Algorithm

* <img src="media/15231996940363.jpg" style="width:380px" />

### Cost

* Factoring \\(A = LU\\) requires, approximately, \\(\frac{2}{3}n^3\\) floating point operations.
* Solve \\(Lz = b\\) requires, approximately, \\(n^2\\) floating point operations.
* Solve \\(Ux = z\\) requires, approximately, \\(n^2\\) floating point operations.



