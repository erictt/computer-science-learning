---
weight: 1
title: "Week 03 - Matrix-Vector Operations"
---

# Week 3 - Matrix-Vector Operations

* element $a_{i,j}$: the **i**th row, **j**th column.

## Special Matrices

* <img src="https://i.imgur.com/wmbHvH8.jpg" style="width:550px" />

* Special Vectors:
  * **Unit Vector**: Any vector of length one (unit length). For example, the vector  $\begin{pmatrix}\frac{\sqrt{2}}{2} \\ \frac{\sqrt{2}}{2}\end{pmatrix}$ has length one.
  * **Standard Unit Vector**:
    * <img src="https://i.imgur.com/rbwLAAY.jpg" style="width:200px"/>

## Triangular Matrices

* <img src="https://i.imgur.com/prHUxYi.jpg" style="width:550px" />

## Transpose Matrix

* <img src="https://i.imgur.com/KT0p6Zj.jpg" style="width:550px" />

## Symmetric Matrix

* <img src="https://i.imgur.com/qF5tkQq.jpg" style="width:550px" />

## Scaling a Matrix

* <img src="https://i.imgur.com/bUbW96j.jpg" style="width:550px" />

## Adding Matrices

* <img src="https://i.imgur.com/zLPy73l.jpg" style="width:550px" />

## Matrix-vector Multiplication

* <img src="https://i.imgur.com/z8KsE1o.jpg" style="width:550px" />

  * where $\tilde{a}_i$ is the (column) vector which, when transposed($\tilde{a}_i^T$), becomes the **i**th row of the matrix.
  * $a_i = \begin{bmatrix} a_{0,i} \\ a_{1,i} \\ \vdots \\ a_{m-1,i} \end{bmatrix}, \tilde{a}_i = \begin{bmatrix} a_{i,0} \\ a_{i,1} \\ \vdots \\ a_{i,n-1} \end{bmatrix}, \tilde{a}_i ^T= \begin{bmatrix} a_{i,0} & a_{i,1} & \ldots & a_{i,n-1} \end{bmatrix}, $

## Cost of Matrix-Vector Multiplication

* Consider $y := Ax+y\ \text{, where } A \in R^{m \times n}$ :
  * Notice that there is a multiply and an add for every element of A.
  * Since A has $m \times n = mn$ elements, $y := Ax+y$, requires **mn** multiplies and **mn** adds, for a total of **2mn** ﬂoating point operations (ﬂops).

## Review Questions

1. what is zero/identity/diagonal matrix?
2. what is triangular matrics?
    1. [strictly/unit] lower/upper triangular
3. what is a symmetric matrix?
4. how to calculate matrix-vector multiplication?
    1. the result is depended on matrix or vector?
    2. how many calculation does it take?
