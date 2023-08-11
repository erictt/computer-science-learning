---
weight: 1
title: "Week 02 - Linear Transformations and Matrices"
---

# Week 2 - Linear Transformations and Matrices

## Opening Remarks  

### Rotations in 2D

* <img src="https://i.imgur.com/pFAMSiE.jpg" style="width:400px" />
* $\alpha R_{\theta}(x) = R_{\theta}(\alpha x)$,
* $R_{\theta}(x+y) = R_{\theta}(x) + R_{\theta}(x)$

## Linear Transformations

* **A linear transformation** is a vector function that has the following two properties:
  * Transforming a scaled vector is the same as scaling the transformed vector: $$L(\alpha x) = \alpha L(x)$$
  * Transforming the sum of two vectors is the same as summing the two transformed vectors: $$L(x + y) = L(x) + L(y)$$
* **Lemma**: $L: \mathbb{R}^n \to \mathbb{R}^m$ is a linear transformation if and only if(iff) for all $u,v \in \mathbb{R}^n$ and $\alpha, \beta \in \mathbb{R}^n$ $$L(\alpha u + \beta v) = \alpha L(u) + \beta L(v)$$
* **Lemma**: Let $v_0, v_1, \ldots, v_{k-1} \in \mathbb{R}^n$ and let $L: \mathbb{R}^n \to \mathbb{R}^m$ be a linear transformation. Then
  * $$L(v_0 + v_1 + \ldots + v_{k-1}) = L(v_0) + L(v_1) + \ldots + L(v_{k-1})$$

## Mathematical Induction

* What is the **Principle of Mathematical Induction**(week induction)(数学归纳法)?
  * if one can show that:
    * (**Base case**) a property holds for $k = k_b$; and
    * (**Inductive step**) if it holds for $k = K$, where $K \ge k_b$ , then it is also holds for $k = K +1$,
  * then one can conclude that the property holds for all integers $k \ge k_b$ . Often $k_b = 0$ or $k_b = 1$.
* Example: To proof: $\displaystyle\sum_{i=0}^{n-1}{i} = n(n-1)/2$
  * **Base case**: $n = 1$. For this case, we must show that $\displaystyle\sum_{i=0}^{i-1}{i} = 1(1-1)/2$
    * $\displaystyle\sum_{i=0}^{i-1}{i} = 0 = 1(1-1)/2$
    * So this proves the base case.
  * **Inductive step**: Inductive Hypothesis (IH): Assume that the result is true for $n = k$ where $k \ge 1$: $\displaystyle\sum_{i=0}^{k-1}{i} = k(k-1)/2$
    * We need to show that the result is then also true for $n=k+1$: $\displaystyle\sum_{i=0}^{(k+1)-1}{i} = (k+1)((k+1)-1)/2$
    * Assume that $k \ge 1$, Then
      * $$\begin{aligned}\sum_{i=0}^{(k+1)-1}{i} &= \sum_{i=0}^{k-1}{i} + k \\
                &= k(k-1)/2 + k = k(k+1)/2 \\
                &= (k+1)((k+1)-1)/2 \end{aligned}$$
    * This proves the inductive step.

## What is Matrices

* $\begin{bmatrix} 1 & 2 \\ 3 & 4 \\ 5 & 6 \end{bmatrix}$ is a 3 by 2 **matrix**: m = 3 **rows** and n = 2 **columns**.

## Representing Linear Transformations as Matrices

* <img src="https://i.imgur.com/UFUjKgr.jpg" style="width:600px" />
* **The Big Idea**. The linear transformation **L** is completely described by the vectors
  * $a_0 ,a_1 ,...,a_{n-1}$, where $a_j = L(e_j)$
* because for any vector **x**, $L(x) = \sum^{n-1}_{j=0} x_j a_j$.
* <img src="https://i.imgur.com/a7OYOtf.jpg" style="width:600px" />
* e.g. $Ax = \begin{bmatrix} 1 & 2 \\ 3 & 4 \\ 5 & 6 \end{bmatrix} \begin{bmatrix} x_1 \\ x_2 \end{bmatrix}$ is a **combination of the columns**. $Ax = x_1 \begin{bmatrix} 1 \\ 3 \\ 5 \end{bmatrix} + x_2 \begin{bmatrix} 2 \\ 4 \\ 6 \end{bmatrix}$

### Theorem

* Let $L: \mathbb{R}^n \to \mathbb{R}^m$ be defined by $L(x) = Ax$ where $A \in \mathbb{R}^{m \times n}$. Then **L** is a linear transformation.
* Alternatively, A vector function $f: \mathbb{R}^n \to \mathbb{R}^m$ is a linear transformation if and only if it can be represented by an $m \times n$ **matrix**, which is a very special two dimensional array of numbers (elements).
* The **set of all real valued** $m \times n$ **matrices** is denoted by $\mathbb{R}^{m \times n}$

### How to check if a vector function is a linear transformation

* Check if $f(0)=0$. If it isn't, it is not a linear transformation.
* If $f(0)=0$ then either:
  * Prove it is or isn't a linear transformation from the definition:
    * Find an example where $f(\alpha x) \ne \alpha f(x)$ or $f(x + y) \ne f(x) + f(y)$. In this case the function is not a linear transformation; or
    * prove that $f(\alpha x) = \alpha f(x)$ or $f(x + y) = f(x) + f(y)$ for all $\alpha, x, y$.
    * or
  * Compute the possible matrix A that represents it and see if $f(x)=Ax$. If it is equal, it is a linear transformation. If it is not, it is not a linear transformation.

### Rotations and Reflections, Revisited

<img src="https://i.imgur.com/N4lDdfv.jpg" style="width:600px" />
<img src="https://i.imgur.com/5D5NEid.jpg" style="width:600px" />

## Some Summations will be Used in Future Weeks

* $\sum _{i=0}^{n-1} i = n ( n-1 ) / 2 \approx n^2 / 2$
* $\sum _{i=1}^{n} i = n ( n+1 ) / 2 \approx n^2 / 2$
* $\sum _{i=0}^{n-1} i^2 = (n-1) n ( 2n-1 ) / 6 \approx \frac{1}{3} n^3$

## Words

* arithmetic [ə'riθmətik, ,æriθ'metik] n. 算术，算法

## Review Questions

1. what is linear transformation?
2. how to verify if a vector function is linear transformation?
