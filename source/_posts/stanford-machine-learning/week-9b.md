# Week 9b - Recommender Systems

## Introduction

* Two motivations for talking about recommender systems
    * Important application of ML systems
    * Share some big ideas in machine learning
        * like, learn what features to use.

## Problem Formulation

* Example: Predicting movie ratings
    * <img src="https://i.imgur.com/YF4H0KX.jpg" style="width:500px" />
    * The users have already rated some of movies. And we want to know that if they like the movies they haven't rated.
    * To simplify this example, we set that, users rates movies using from zero to five stars.
    * Notations:
        * $n_u$ = no. users
        * $n_m$ = no. movies
            * In this case, $n_u = 4, n_m = 5$
        * $r(i,j)$ = 1 if user **j** has rated movie **i** (o otherwise).
        * $y^{ (i,j) }$ = rating given by user **j** to movie **i** (defined only if $r(i,j)=1$.
    * For each user $j$, learn a parameter $\theta^{ (j) } \in \mathbb{ R }^3$. Predict user $j$ as rating movie $i$ with $(\theta^{ (j) })^T(x^{ (i) })$ stars.
        * More generally, $\theta^{ (j) } \in \mathbb{ R }^{ n+1 }$, included the bias term $\theta_0^{ (j) }$. **n** is the number of features.
        * In this example, we got **romance** and **action** two features for every movie.
    * Extra notaions:
        * $\theta^{ (j) }$ = parameter vector for user $j$
            * $\theta^{ (1) }$ is for Alice
        * $x^{ (i) }$ = feature vector for movie $i$
            * For movie "Love at Last": $x^{ (1) } = \begin {bmatrix}1 \\ 0.9 \\ 0\end {bmatrix}$
        * $m^{ (j) }$ = no. of movies rated by user $j$.
    * For user $j$, movie $i$, predicted rating: $(\theta^{ (j) })^T(x^{ (i) })$
    * So if  $\theta^{ (1) } = \begin {bmatrix}0 \\ 5 \\ 0\end {bmatrix}$. Check the movie "Cute puppies of love":  $x^{ (3) } = \begin {bmatrix}1 \\ 0.99 \\ 0\end {bmatrix}$, then $(\theta^{ (1) })^T(x^{ (3) }) = 5 \times 0.99 = 4.95$, which is pretty good estimate for user Alice.

### Optimization objective

* To learn $\theta^{ (j) }$ ( parameter for user $j$ ): $$\underset{ \theta^{ (j) } }{ \text{ min } } \frac{ 1 }{ 2 } \sum_{ i: r(i,j) = 1 }((\theta^{ (j) })^Tx^{ (i) } - y^{ (i,j) })^2 + \frac{ \lambda }{ 2 }\sum_{ k=1 }^n(\theta_k^{ (j) })^2$$
    * Compare to the linear regression, we just get rid of the $\frac{ 1 }{ m }$ term.
* To learn $\theta^{ (1) }, \theta^{ (2) }, \ldots, \theta^{ (n_u) }$: $$\underset{ \theta^{ (1) }, \ldots, \theta^{ (n_u) } }{ \text{ min } } \frac{ 1 }{ 2 } \sum_{ j=1 }^{ n_u }\sum_{ i: r(i,j) = 1 }((\theta^{ (j) })^Tx^{ (i) } - y^{ (i,j) })^2 + \frac{ \lambda }{ 2 }\sum_{ j=1 }^{ n_u }\sum_{ k=1 }^n(\theta_k^{ (j) })^2$$
* Gradient descent update: $$\begin {aligned}
    \theta_k^{ (j) } &:= \theta_k^{ (j) } - \alpha \sum_{ i: r(i,j) = 1 }((\theta^{ (j) })^T x^{ (i) } - y^{ (i,j) }) x_k^{ (i) } \ (\text{ for }\ k = 0) \\
    \theta_k^{ (j) } &:= \theta_k^{ (j) } - \alpha \Big(\sum_{ i: r(i,j) = 1 }((\theta^{ (j) })^T x^{ (i) } - y^{ (i,j) }) x_k^{ (i) } + \lambda \theta_k^{ (j) }\Big) \ (\text{ for }\ k \ne 0)
    \end {aligned}$$

## Collaborative Filtering

* One of the property of collaborative filtering is: **feature learning**, which is an algorithm that can learn for itself what features to use.

* Let's make a different assumption: 
    * <img src="https://i.imgur.com/wcqYMwY.jpg" style="width:500px" />
    * We don't know the movies' categories, romance or action. 
    * But we know our users' hobbits. Alice and Bob like romance movie, and Carol and Dave like action movie. So we generated the $\theta{ (j) }$ vectors above.
    * So, to movie "Love at last" ($x^{ (1) }$) and User "Alice" ($\theta^{ (1) }$), we should get $(\theta^{ (1) })^Tx^{ (1) } = 5$, and to the rest users: $(\theta^{ (2) })^Tx^{ (1) } = 5, (\theta^{ (3) })^Tx^{ (1) } = 0, (\theta^{ (4) })^Tx^{ (1) } = 0$, then we can guess: $$x^{ (1) } = \begin {bmatrix}1 \\ 1.0 \\ 0.0 \end {bmatrix}$$

### Optimization Algorithm

* Given $\theta^{ (1) }, \ldots, \theta^{ (n_u) }$, to learn $x^{ (i) }$ : $$\underset{ x^{ (i) } }{ \text{ min } } \frac{ 1 }{ 2 } \sum_{ i: r(i,j) = 1 }((\theta^{ (j) })^Tx^{ (i) } - y^{ (i,j) })^2 + \frac{ \lambda }{ 2 }\sum_{ k=1 }^n(x_k^{ (j) })^2$$
* Given $\theta^{ (1) }, \ldots, \theta^{ (n_u) }$, to learn $x^{ (1) }, x^{ (2) }, \ldots, x^{ (n_m) }$: $$\underset{ x^{ (1) }, \ldots, x^{ (n_m) } }{ \text{ min } } \frac{ 1 }{ 2 } \sum_{ i=1 }^{ n_m }\sum_{ j: r(i,j) = 1 }((\theta^{ (j) })^Tx^{ (i) } - y^{ (i,j) })^2 + \frac{ \lambda }{ 2 }\sum_{ i=1 }^{ n_m }\sum_{ k=1 }^n(x_k^{ (i) })^2$$

### Combine the Algorithms Together

* In the past two part we know:
    * Given $\theta^{ (1) }, \ldots, \theta^{ (n_u) }$, can estimate $x^{ (1) }, x^{ (2) }, \ldots, x^{ (n_m) }$,
    * Given $x^{ (1) }, x^{ (2) }, \ldots, x^{ (n_m) }$, can estimate $\theta^{ (1) }, \ldots, \theta^{ (n_u) }$.
* But which goes first?
* In some ideas, we can random initialize $\Theta$s to get $X$, then use $X$ to get a better $\Theta$. In this back and forth process to estimate **theta** and **x**.

### Collaborative Filtering Algorithm

* To avoid back and forth process, we come out this new algorithm, to minimize $x^{ (1) }, x^{ (2) }, \ldots, x^{ (n_m) }$ and $\theta^{ (1) }, \ldots, \theta^{ (n_u) }$ simultaneously: $$J(x^{ (1) },  \ldots, x^{ (n_m) }, \theta^{ (1) }, \ldots, \theta^{ (n_u) }) =  \frac{ 1 }{ 2 } \sum_{ (i,j): r(i,j) = 1 }((\theta^{ (j) })^Tx^{ (i) } - y^{ (i,j) })^2 + \frac{ \lambda }{ 2 }\sum_{ i=1 }^{ n_m }\sum_{ k=1 }^n(x_k^{ (i) })^2 + \frac{ \lambda }{ 2 }\sum_{ j=1 }^{ n_u }\sum_{ k=1 }^n(\theta_k^{ (j) })^2$$
* $$\underset{ x^{ (1) }, \ldots, x^{ (n_m) }, \theta^{ (1) }, \ldots, \theta^{ (n_u) } }{ \text{ min } }\ J(x^{ (1) },  \ldots, x^{ (n_m) }, \theta^{ (1) }, \ldots, \theta^{ (n_u) })$$
    * Notice, $\displaystyle\sum_{ (i,j): r(i,j) = 1 }((\theta^{ (j) })^Tx^{ (i) } - y^{ (i,j) })^2$
        *  = $\displaystyle\sum_{ i=1 }^{ n_m }\sum_{ j: r(i,j) = 1 }((\theta^{ (j) })^Tx^{ (i) } - y^{ (i,j) })^2$
        *  = $\displaystyle\sum_{ j=1 }^{ n_u }\sum_{ i: r(i,j) = 1 }((\theta^{ (j) })^Tx^{ (i) } - y^{ (i,j) })^2$

* For convenience, we get rid of $\theta_0^{ (j) }$ and $x_0^{ (i) }$, so $x^{ (i) } \in \mathbb{ R }^n$ and $\theta^{ (i) } \in \mathbb{ R }^n$. 
    * The reason we do this, is that we are now learning all the features, so, there is no need to hard code the feature which always equals one.

### Steps of Collaborative Filtering Algorithm

1. Initialize $x^{ (1) },  \ldots, x^{ (n_m) }, \theta^{ (1) }, \ldots, \theta^{ (n_u) }$ to small random values.
2. Minimize $J(x^{ (1) },  \ldots, x^{ (n_m) }, \theta^{ (1) }, \ldots, \theta^{ (n_u) })$ use gradient descent (or an advanced optimization algorithm). E.g. for every $j = 1, \ldots, n_u, i= 1, \ldots, n_m$: $$\begin {aligned}
    x_k^{ (j) } &:= x_k^{ (j) } - \alpha \Big(\sum_{ j: r(i,j) = 1 }((\theta^{ (j) })^T x^{ (i) } - y^{ (i,j) }) \theta_k^{ (j) } + \lambda x_k^{ (i) }\Big) \\
    \theta_k^{ (j) } &:= \theta_k^{ (j) } - \alpha \Big(\sum_{ i: r(i,j) = 1 }((\theta^{ (j) })^T x^{ (i) } - y^{ (i,j) }) x_k^{ (i) } + \lambda \theta_k^{ (j) }\Big)
    \end {aligned}$$
    * We already get rid of $\theta_0^{ (j) }$ and $x_0^{ (i) }$, so no special cases. 
3. For a user with parameters $theta$ and a movie with (learned) features $x$, predict a star rating of $\theta^T x$.

## Low Rank Matrix Factorization

### Vectorization: Low Rank Matrix Factorization

* <img src="https://i.imgur.com/rTKruWo.jpg" style="width:400px" />
* Group the data with matrix, we get: $$Y = \begin {bmatrix}5 & 5 & 0 & 0 \\ 5 & ? & ? & 0 \\ ? & 4 & 0 & ? \\ 0 & 0 & 5 & 4 \\ 0 & 0 & 5 & 0 \end {bmatrix}$$
* And the predicted ratings algorithms can be writen as: $$\begin {bmatrix} (\theta^{ (1) })^T(x^{ (1) }) & (\theta^{ (2) })^T(x^{ (1) }) & \ldots & (\theta^{ (n_u) })^T(x^{ (1) }) \\ (\theta^{ (1) })^T(x^{ (2) }) & (\theta^{ (2) })^T(x^{ (2) }) & \ldots & (\theta^{ (n_u) })^T(x^{ (2) }) \\ 
  \vdots & \vdots & \vdots & \vdots & \\
  (\theta^{ (1) })^T(x^{ (n_m) }) & (\theta^{ (2) })^T(x^{ (n_m) }) & \ldots & (\theta^{ (n_u) })^T(x^{ (n_m) }) \\ \end {bmatrix}$$
    * The index $(i, j)$ corresponds to the rating that we predict user **j** give to movie **i**, which is $(\theta^{ (j) })^T(x^{ (i) })$
* There is a vectorized way to write this:
    * In particular, if we define the matrix: $$X = \begin {bmatrix} - & (x^{ (1) })^T & - \\ & \vdots & \\ - & (x^{ (n_m) } & - \end {bmatrix},\ \Theta = \begin {bmatrix} - & (\theta^{ (1) })^T & - \\ & \vdots & \\ - & (\theta^{ (n_u) } & - \end {bmatrix}$$
    * Then we can write the predicted ratings as $X\Theta^T$.
    * And this algorithm called **Low Rank Matrix Factorization**(矩阵分解).
        * 将高维矩阵映射为两个低维矩阵.

### Finding Related Movies

* For each product $i$, we learn a feature vector $x^{ (i) } \in \mathbb{ R }^n$.
    * Like, x_1 = romance, x_2 = action, ...
* How to find movies $j$ related to movie $i$ ?
    * If the value of $\lVert x^{ (i) } - x^{ (j) } \rVert$ is small.
* So, if we want 5 most movies to movie $i$:
    * Just find the 5 movies $j$ with the smallest $\lVert x^{ (i) } - x^{ (j) } \rVert$.

### Implementational Detail: Mean Normalization

* Say, we have a user **Eve** who haven't rated any movie yet. So,
    * <img src="https://i.imgur.com/JEJffVt.jpg" style="width:500px" />
* We can initial all of the rating values to **0**. Then to minimize cost **J**.
    * Since all of the ratings are **0**, the other terms are irrelevant. We just need to minimize $\frac{ \lambda }{ 2 }\sum_{ j=1 }^{ n_u }\sum_{ k=1 }^n(\theta_k^{ (j) })^2$, which equals $\frac{ \lambda }{ 2 }\Big[(\theta^{ (5) }_1)^2 + (\theta^{ (5) }_2)^2\Big]$. We can easily get $\theta^{ (5) } = \begin {bmatrix}0 \\ 0\end {bmatrix}$. But this conclusion doesn't help, we need a better way to do this.

#### Mean Normalization

* Calculate all of the movies' average rating, then set their means to zero.
* We know that $$Y = \begin {bmatrix}5 & 5 & 0 & 0 & ? \\ 5 & ? & ? & 0 & ? \\ ? & 4 & 0 & ? & ? \\ 0 & 0 & 5 & 4 & ? \\ 0 & 0 & 5 & 0 & ? \end {bmatrix}$$
* Then $$\mu = \begin {bmatrix} 2.5 \\ 2.5 \\ 2 \\ 2.25 \\ 1.25 \end {bmatrix} \to Y = \begin {bmatrix}2.5 & 2.5 & -2.5 & -2.5 & ? \\ 2.5 & ? & ? & -2.5 & ? \\ ? & 2 & -2 & ? & ? \\ -2.25 & -2.25 & 2.75 & 1.75 & ? \\ -1.25 & -1.25 & 3.75 & -1.25 & ? \end {bmatrix}$$
* And we can initialize $$\theta^{ (5) } = \begin {bmatrix} 0 \\ 0 \\ 0 \\ 0 \\ 0 \end {bmatrix}$$
* This makes sense. Because, if Eve hasn't rated any movies, predict the average rating should be the best.
* Don't forgot that, for predicting user $j$ on movie $i$, we should plus the mean: $$(\theta^{ (j) })(x^{ (i) })+\mu_i$$

