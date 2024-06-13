---
weight: 1
title: "Week 07 - Support Vector Machines(SVM)"
---

# Week 7 - Support Vector Machines(SVM)

* Compared to both logistic regression and neural networks, **SVM** sometimes gives a cleaner way of learning non-linear functions

## Optimization Objective

* Start with logistic regression, and modify it a bit to get the SVM.
* The logistic regression hypothesis is: $$h_{\theta}(x) = \frac{1}{1+e^{-\theta^{T}x} }$$
* And the sigmoid activation function looks like:
  * <img src="https://i.imgur.com/MqVJevd.jpg" style="width:250px" />
* If $y = 1$, we want $h_{\theta}(x) \approx 1$, $\theta^{T}x \gg  0$
* If $y = 0$, we want $h_{\theta}(x) \approx 0$, $\theta^{T}x \ll  0$
* Cost of single example: $$\begin{aligned} & -(y\log{h_{\theta}(x)} + (1 - y)\log{(1 - h_{\theta}(x)}))z \\ = &-(y\log{\frac{1}{1+e^{-\theta^{T}x} }} - (1 - y)\log{(1 - \frac{1}{1+e^{-\theta^{T}x} }}))\end{aligned}$$
* If $y = 1$ (want $\theta^Tx \gg 0$), then the cost will be: $-\log\dfrac{1}{1+e^{-z} }$
  * <img src="https://i.imgur.com/E8pq3Bn.jpg" style="width:200px" />
* If $y = 0$ (want $\theta^Tx \ll 0$), then the cost will be: $-\log{(1 - \dfrac{1}{1+e^{-z} }})$
  * <img src="https://i.imgur.com/cIqrK0l.jpg" style="width:200px" />
* To build SVM, we redefine the cost functions:
  * If $y = 1$:
    * <img src="https://i.imgur.com/nXyoaBy.jpg" style="width:200px" />
    * Instead of a curve line, we create two straight lines which acts as an approximation to the logistic regression.
    * We call this function $cost_1(z)$.
  * If $y = 0$:
    * <img src="https://i.imgur.com/x3FawPD.jpg" style="width:200px" />
    * We call this function $cost_0(z)$.
  * **How to use formula to represent those two lines?** At least to calculate the cost?
    * Everything Prof Ng said about SVM training was an intuition. The actual SVM training method provided in the `svmTrain()` function is the SMO method. That method is too complex to be included as part of the course. -- from [Discuss Forms](https://www.coursera.org/learn/machine-learning/discussions/weeks/7/threads/uCyF4elMEeWK_Q7eN25hdw)
* **The complete SVM cost function**
  * As a comparison we have logistic regression:
  * $${\underset{\theta}{\text{min} } } \ - \frac{1}{m} \sum_{i=1}^m \large[ y^{(i)}\ \log (h_\theta (x^{(i)})) + (1 - y^{(i)})\ \log (1 - h_\theta(x^{(i)}))\large] + \frac{\lambda}{2m}\sum_{j=1}^n \theta_j^2$$
  * Replace the cost function with $cost_0(z)$ and $cost_1(z)$, we get:
  * $$\underset{\theta}{\text{min} }\ \frac{1}{m} \sum_{i=1}^m \large[ y^{(i)}\ cost_1(\theta^Tx^{(i)}) + (1 - y^{(i)})\ cost_0(\theta^Tx^{(i)})\large] + \frac{\lambda}{2m}\sum_{j=1}^n \theta_j^2$$
  * In convention with SVM notation, we adjust a little bit:
    * Get rid of $\dfrac{1}{m}$ term.
      * Because $\frac{1}{m}$ is a constant, so we should still end up with the same optimal value for $\theta$.
    * For logistic regression we have:
      * Training data set term **A**:
      * $$- \frac{1}{m} \sum_{i=1}^m \large[ y^{(i)}\ \log (h_\theta (x^{(i)})) + (1 - y^{(i)})\ \log (1 - h_\theta(x^{(i)}))\large]$$
      * and Regularization term **B**:
      * $$\frac{\lambda}{2m}\sum_{j=1}^n \theta_j^2$$
      * To conclude it, we get $A + \lambda B$
      * So $\lambda$ is the trade-off between training data set and regularization terms.
      * Instead of using $A + \lambda B$, In SVM, we rewrite it as $CA + B$, which **C** is a constant.
      * We can think of the parameter **C** playing a role similar to $\frac{1}{\lambda}$.
  * Overall optimization objective function for the SVM is:

$$J(\theta) = C \left[ \frac{1}{m} \sum_{i=1}^m y^{(i)} \mathbf{cost}_ {1}\left(\theta^{\top}x^{(i)}\right) + \left(1 - y^{(i)}\right)  \mathbf{cost}_ 0\left(\theta^{\top}x^{(i)}\right)\right] + \frac{1}{2} \sum_{j=1}^n \theta_j^2$$

* SVM Hypothesis:
  * Unlike logistic, $h_{\theta}(x)$ doesn't give us a probability, instead we get a direct prediction of **1** or **0**

$$h_{\theta}(x) = \begin{cases}
1 & \text{if } \theta^{\top}x \geq 0 \\
0 & \text{otherwise}
\end{cases}$$

## Large Margin Intuition

* Sometimes SVM called **Large Margin Classifier**.
* Here are two plots for the cost function:
  * <img src="https://i.imgur.com/XOGI1HA.jpg" style="width:500px" />
* If we want the cost to be small, then we will need $z$ to be more that **1** not just **0**. then:
  * If $y = 1$, we want $\theta^Tx \ge 1$ (not just $\ge 0$).
  * If $y = 0$, we want $\theta^Tx \le -1$ (not just $\le 0$).

### SVM Decision Boundary

* Use the simplified cost function $\text{min}_{\theta} = CA+B$
* If **C** is a huge number, like **100,000**, then we will need to make **A** to be very small, best to be 0, and in the same time minimize **B**.
  * Whenever $y^{(i)} = 1$: $\theta^Tx^{(i)} \ge 1$.
  * Whenever $y^{(i)} = 0$: $\theta^Tx^{(i)} \le -1$.
  * $\underset{\theta}{\text{min} }\ \dfrac{1}{2}\sum_{i=1}^n\theta_j^2$
* Let's check the result in a **linearly separable case**
  * <img src="https://i.imgur.com/vAhBiwV.jpg" style="width:200px" />
  * The green and magenta lines are functional decision boundaries which could be chosen by logistic regression
  * The black line, by contrast is chosen by the SVM because of this safety net imposed by the optimization graph
  * We can see that, there is a large margin between the black line and the training sets  which is called **the margin of the support vector machine**.
    * <img src="https://i.imgur.com/GZhrXmy.jpg" style="width:200px" />
  * In another situation:
    * <img src="https://i.imgur.com/xHnsmRF.jpg" style="width:200px" />
    * We can't get the result like the black line, since we set **A** to **0**, so the SVM is very sensitive to outliers. And we probably will get the magenta line below. Which lead to another way to fix this: set **C** to a small number, which means ignoring some outliers.
      * <img src="https://i.imgur.com/K219yh2.jpg" style="width:360px" />

## Mathematics Behind Large Margin Classification

### Vector Inter Productions

* <img src="https://i.imgur.com/1hNa8cz.jpg" style="width:250px" />
* $u = \begin{bmatrix} u_1 \\ u_2 \end{bmatrix}$, $v = \begin{bmatrix} v_1 \\ v_2 \end{bmatrix}$
* length of vector: $\lVert u \rVert = \sqrt{u_1^2+u_2^2}$
* **p** = length of projection of **v** onto **u**.
  * **p** is signed, which means it can be negative number.
* $\begin{aligned}u^tv &= p \cdot \lVert u \rVert \\ &= u_1v_1 + u_2v_2 \end{aligned}$

### SVM Decision Boundary

* $\underset{\theta}{\text{min} }\ \dfrac{1}{2}\sum_{i=1}^n\theta_j^2$
* $\begin{aligned}\text{s.t. } \theta^Tx^{(i)} &\ge 1\ \text{ if }y^{(i)} = 1 \\ \theta^Tx^{(i)} &\le -1\ \text{ if } y^{(i)} = 0\end{aligned}$
* **Simplification**: set $\theta_0 = 0\text{, }n = 2$(only 2 features). Then:
  * $\underset{\theta}{\text{min} }\ \dfrac{1}{2}\sum_{i=1}^n\theta_j^2 = \frac{1}{2}(\theta_1^2+\theta_2^2) = \frac{1}{2}(\sqrt{\theta_1^2+\theta_2^2})^2 = \frac{1}{2}{\lVert \theta \rVert}^2$
  * $\theta^Tx^{(i)} = \theta_1x_1^{(i)} + \theta_2x_2^{(i)} = p^{(i)} \cdot {\lVert \theta \rVert}$
    * <img src="https://i.imgur.com/GIhb9bM.jpg" style="width:200px" />
  * Redefine these functions, we get:
    * $\begin{aligned}\text{s.t. } p^{(i)} \cdot {\lVert \theta \rVert} &\ge 1\ \text{ if }y^{(i)} = 1 \\ p^{(i)} \cdot {\lVert \theta \rVert} &\le -1\ \text{ if } y^{(i)} = 0\end{aligned}$
    * where $p^{(i)}$ is the projection of $x^{(i)}$ onto the vector $\theta$.
  * So we want to maximize $p^{(i)}$, so $\lVert \theta \rVert$ can be small.
  * Note that, $\theta_0 = 0$, so  the boundary has to pass through the origin (0,0).
  * Let's consider the training examples like this:
    * <img src="https://i.imgur.com/HAJLqSf.jpg" style="width:200px" />
  * And draw an option, to see if it's possible that SVM would choose.
    * <img src="https://i.imgur.com/fJk14pw.jpg" width = 200 />
    * Note that **θ is always at 90 degrees to the decision boundary** (check linear algebra to find out why).
    * So vector $\theta$ should be:
      * <img src="https://i.imgur.com/erYtin7.jpg" style="width:200px" />
    * Then we can find the projection $p^{(i)}$ of $x^{(i)}$ onto $\theta$:
      * <img src="https://i.imgur.com/x2tqGMI.jpg" style="width:200px" />
      * We know that we need to make $p^{(i)} \cdot {\lVert \theta \rVert} \ge 1$, so:
        * if **p** is small, then ${\lVert \theta \rVert}$ should be very large
      * Similarly, for the negative examples.
    * But the optimization objective is trying to find a set of parameters where the norm of theta is small. So this doesn't seem like a good choice.
  * Let's another option:
    * <img src="https://i.imgur.com/B6DVnZs.jpg" style="width:200px" />
    * Now if you look at the projection $p^{(i)}$ of $x^{(i)}$ onto $\theta$, we find that **p** becomes large and ${\lVert \theta \rVert}$ can be small.
    * This is why the SVM choses this hypothesis as the better one, and how we generate the large margin.
    * <img src="https://i.imgur.com/7ma5kh3.jpg" style="width:280px" />
* Finally, we did this derivation assuming $\theta_0 = 0$.
  * It just means we are entertaining decision boundaries that pass through the origins of decision boundaries pass through the origin (0,0).
  * If you allow $\theta_0$ to be other values then this simply means you can have decision boundaries which cross through the x and y values at points other than (0,0).

## Kernels I

* Kernels is used to adapt support vector machines in order to develop complex nonlinear classifiers.
* Let's see a example(find a non-linear boundary):
  * <img src="https://i.imgur.com/7Lm10aX.jpg" style="width:300px" />
  * One way to distinguish the positive and negative examples is to come up with a set of complex polynomial features:

$$h_{\theta}(x) = \begin{cases}
1 & \text{if } \theta_0 + \theta_1 x_1 + \theta_2 x_2 + \theta_3 x_1 x_2 + \theta_4 x_1^2 + \theta_5 x_2^2 + \cdots \geq 0 \\
0 & \text{otherwise}
\end{cases}$$

  * Another way is using a new notation to denote $x_1, x_2, x_1 x_2, x_1^2, x_2^2$ as $f_1, f_2, f_3, f_4, f_5, \cdots$, so the hypothesis will be:

$$h_{\theta}(x) = \begin{cases}
1 & \text{if } \theta_0 + \theta_1 f_1 + \theta_2 f_2 + \theta_3 f_3 + \theta_4 f_4 + \theta_5 f_5 + \cdots \geq 0 \\
0 & \text{otherwise}
\end{cases}$$

  * Is there a different/better choice of the features $f_1, f_2, f_3, \cdots$ ?

### Create New Features

* First, manually pick a few points. In this case, we picked three points, and call them **landmarks** ($l^{(1)}, l^{(2)}, l^{(3)}$).
  * <img src="https://i.imgur.com/sD8ZPt4.jpg" style="width:250px" />
  * Later, will explain how to choose $l^{(i)}$
* Second, define $f_1, f_2, f_3$ as the similarity between $x$ and $l^{(i)}$(ignore $x_0$). Then:

$$\begin{aligned}
    f_1 &= \text{similarity}(x, l^{(1)}) = \text{exp}(-\frac{ {\lVert x - l^{(1)} \rVert}^2 }{2\sigma^2}) \\
    f_2 &= \text{similarity}(x, l^{(2)}) = \text{exp}(-\frac{ {\lVert x - l^{(2)} \rVert}^2 }{2\sigma^2}) \\
        &\vdots
    \end{aligned}$$
  * This similarity function is called a **Kernel**. And this **exp** function is a **Gaussian Kernel**.
  * So, instead of writing similarity between x and l we might write
   * $$f_1 = k(x, l^{(1)})$$
  * My Note: $\sigma$: the value of standard deviation. Gaussian Kernel is calculating the value correspond with mean($l^{(1)}$) and $\sigma$.

#### Kernels and Similarity

* If $x \approx l^{(1)}$:
  * $f_1 \approx \text{exp}(-\frac{0^2}{2\sigma^2}) \approx 1$
* If $x$ is far from $l^{(1)}$:
  * $f_1 \approx \text{exp}(-\frac{(\text{large number})^2}{2\sigma^2}) \approx 0$
* Example:
  * $l^{(1)} = \begin{bmatrix}3 \\ 5\end{bmatrix}$, $f_1 = \text{exp}(-\dfrac{ {\lVert x - l^{(1)} \rVert}^2 }{2\sigma^2})$.
  * Plot $f_1$ vs the kernel function, we get plots like:
    * <img src="https://i.imgur.com/76D8ujL.jpg" style="width:450px" />
    * Notice that when x = [3, 5], then $f_1 = 1$.
    * As x moves away from [3,5], then the feature takes on values close to zero. So this measures how close **x** is to this **landmark**.
    * $\sigma^2$ is parameter of the Gaussian Kernel, which defines the steepness of the rise around the landmark. We can see that the slop are getting smoother as $\sigma^2$ are bigger.
* Given this definition, what kind of hypothesis we can learn:
  * For example, let's say we already run the algorithm and got $\theta_0 = -0.5, \theta_1 = 1, \theta_2 = 1, \theta_3 = 0$. What happens if we evaluate the **magenta dot** below?
    * <img src="https://i.imgur.com/jhEkx7n.jpg" style="width:200px" />
    * We know that $x$ is close to $l^{(1)}$, so $f_1$ will be close to 1, and $f_2$ and $f_3$ and will be close to 0.
    * So $\theta_0 + \theta_1 f_1 + \theta_2 f_2 + \theta_3 f_3 = -0.5 + 1 + 0 + 0 = 0.5 \ge 0$. Then we predict $y = 1$.
    * After we tried different points, we will eventually get this non-linear boundary:
      * <img src="https://i.imgur.com/hqZUuLM.jpg" style="width:250px" />
* Next segment will talk about:
  * How we choose the landmarks;
  * What other kernels we can use (other than the Gaussian Kernel).

## Kernel II

### Choosing the Landmarks

* Put landmarks as exactly the same locations as the training examples.
* Then we will get **m** landmarks, which has the same number with the training examples.
* **SVM with Kernels**
  * Given $(x^{(1)}, y^{(1)}), (x^{(2)}, y^{(2)}), \ldots, (x^{(m)}, y^{(m)})$,
  * Choose $l^{(1)} = x^{(1)}, l^{(2)} = x^{(2)}, \ldots, l^{(m)} = x^{(m)}$.
  * For training example ($x^{(i)}, y^{(i)}$):
  * $$\begin{aligned}
        f_1^{(i)} &= \text{similarity}(x^{(i)}, l^{(1)}) \\
        f_2^{(i)} &= \text{similarity}(x^{(i)}, l^{(2)}) \\
        &\vdots \\
        f_i^{(i)} &= \text{similarity}(x^{(i)}, l^{(i)}) = \text{similarity}(x^{(i)}, x^{(i)}) = \text{exp}(-\frac{0}{2\sigma^2}) = 1\\
        &\vdots \\
        f_m^{(i)} &= \text{similarity}(x^{(i)}, l^{(m)})
        \end{aligned}$$
  * We got $f^{(i)} = \begin{bmatrix}f_0^{(i)} \\ f_1^{(i)} \\ \vdots \\ f_m^{(i)} \\ \end{bmatrix}$($f_0^{(i)} = 1$), which are our new training examples.
    * Our training set become a $m \times m$ matrix, because every sample have **m** features.
    * $f^{(i)} \in \mathbb{R}^{m+1}$ (included $f_0$).

  * Then, our hypothesis will be: Given $x$, compute features $f^{(i)} \in \mathbb{R}^{m+1}$. Predict $y = 1$ if $\theta^Tf \ge 0$.
  * And the training:
  * $$\underset{\theta}{\text{min} }\ C \sum_{i=1}^m \large[ y^{(i)}\ cost_1(\theta^Tf^{(i)}) + (1 - y^{(i)})\ cost_0(\theta^Tf^{(i)})\large] + \frac{1}{2}\sum_{j=1}^m \theta_j^2$$
    * Note that **m = n**, the number of features equals the number of training data examples.
    * Another mathematics detail about the training formula:
      * The regulation part: $\displaystyle\sum_{j=1}^m \theta_j^2 = \theta^T\theta$
      * What many implementations do is: $\theta^TM\theta$
        * Where the matrix **M** depends on the kernel you are using.
        * This is like a rescale version of the parameter vector theta.
        * Allows the SVM to run much more efficiently.

* You can apply kernels to other algorithms
  * But they tend to be very computationally expensive
  * But the SVM is far more efficient - so more practical

### SVM Parameters

* **C**($\frac{1}{\lambda}$)
  * Large C: Lower bias, high variance.
  * Small C: Higher bias, low variance.
* $\sigma^2$:
  * Large $\sigma^2$: Features $f_i$ vary more smoothly. Higher bias, lower variance.
  * Small $\sigma^2$: Features $f_i$ vary less smoothly. Lower bias, higher variance.

## Using an SVM

* Use SVM software package(e.g. liblinear, libsvm,...) to solve for parameters $\theta$.
* What do you need to do, is to specify:
  * Choice of parameter **C**
  * Choice of kernel

### Choice of kernel

* No kernel("linear kernel")
  * Predict "y = 1" if $\theta^Tx \ge 0$
* Gaussian kernel:
  * $f_i = \text{exp}(-\frac{ {\lVert x - l^{(2)} \rVert}^2 }{2\sigma^2})$, where $l^{(i)} = x^{(i)}$
  * Need to choose $\sigma^2$
  * Note: Do perform **feature scaling** before using a Gaussian kernel.
* Other choice of kernel
  * Not all similarity functions make valid kernels
  * Need to satisfy technical condition called "**Mercer's Theorem**" to make sure SVM packages' optimizations run correctly, an do not diverge.
  * Many off-the-shelf kernels available:
    * **Polynomial kernel**: $k(x,l) = (x^Tl+\text{constant})^{\text{degree} }$
      * For example: $k(x,l) = (x^Tl+1)^2$
    * More esoteric: String kernel, chi-square kernel, histogram intersection kernel,...

### Multi-class Classification

* Many SVM packages already have built-in multi-class classification functionality.
* Otherwise, use one-vs-all method.

### Logistic Regression vs. SVMs

* When should we use one algorithm versus the other?
* **n** = number of features ($x \in \mathbb{R}^{n+1}$), **m** = number of training examples
* If **n** is large(relative to **m**) (e.g. n = 10,000, m = 10-1000):
  * Use logistic regression, or SVM without a kernel("linear kernel")
* If **n** is small, **m** is intermediate (e.g. n = 1 - 1000, m = 10 - 10,000):
  * Use SVM with Gaussian kernel
* If **n** is small, **m** is large (e.g. n = 1 - 1000, m = 10 - 50,000+):
  * Create/add more features, then use logistic regression or SVM without a kernel
* Neural network likely to work well for most of these settings, but may be slower to train.
