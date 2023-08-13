---
weight: 1
title: "Week 10 - Large Scale Machine Learning"
---

# Week 10 - Large Scale Machine Learning

## Gradient Descent with Large Datasets

* Before we try to learn with large datasets. First we need to make sure our algorithm is high variance, which will need more data to minimize the error between $J_{CV}$ and $J_{\text{train} }$
  * Check [Week 6a#Bias vs Variance](/stanford-machine-learning/week-6a/#bias-vs-variance) for more details.

### Stochastic Gradient Descent

* In [Week 1#Gradient Descent](/stanford-machine-learning/week-1/#gradient-descent), we learned the **Batch Gradient Descent**(Use all of the training examples at a time). It costs lots of time to compute the derivative part($\frac{d}{d\theta}J(\theta)$). Because every time we sum all of the differences of the samples.
* **Stochastic Gradient Descent** define the cost function slightly differently, as $$\text{cost}(\theta, (x^{(i)}, y^{(i)})) = \frac{1}{2}(h_{\theta}(x^{(i)}) - y^{(i)})^2$$, The overall cost function is $$J_{\text{train} } = \frac{1}{m} \sum_{i=1}^m \text{cost}(\theta, (x^{(i)}, y^{(i)}))$$, which is equivalent to the **batch gradient descent**.
* The steps are:
    1. Randomly shuffle the training examples
    2. Repeat $$\begin{aligned}
        & \{ \\
        & \ \ \ \ \text{for } i := 1, \ldots, m \{ \\
        & \ \ \ \ \ \ \ \ \theta_j := \theta_j - \alpha(h_{\theta}(x^{(i)}) - y^{(i)})x_j^{(i)} \ (\text{for } j = 0, \ldots, n) \\
        & \ \ \ \ \} \\
        & \}
        \end{aligned}$$
    3. Normally, we always repeat the process **1 - 10** times.
* In **Batch Gradient Descent**, the derivative term is $\frac{1}{m} \sum\limits_{i=1}^{m}(h_\theta(x_{i}) - y_{i})x_j^{(i)}$, we sum all the differences. But in **Stochastic Gradient Descent**, we calculate it one by one in **m** loops: ($(h_{\theta}(x^{(i)}) - y^{(i)})x_j^{(i)}$).

* Comparison with Batch Gradient Descent
  * As we saw, batch gradient descent does something like this to get to a global minimum:
    * <img src="https://i.imgur.com/8bQcOSX.jpg" style="width:300px" />
  * With stochastic gradient descent every iteration is much faster, but every iteration is flitting a single example. So, stochastic gradient descent will never converges like batch gradient descent, but ends up wandering around some region close to the global minimum.
    * <img src="https://i.imgur.com/fkX087F.jpg" style="width:300px" />

### Mini-batch Gradient Descent

* Batch gradient descent: Use all **m** examples in each iteration
* Stochastic gradient descent: Use **1** example in each iteration
* Mini-batch gradient descent: Use **b** examples in each iteration
* The steps:
    1. Say **b = 10**, **m = 1000**.
    2. Repeat $$\begin{aligned}
        & \{ \\
        & \ \ \ \ \text{for } i := 1, 11, 21, 31, \ldots, 991 \ \{ \\
        & \ \ \ \ \ \ \ \ \theta_j := \theta_j - \alpha\frac{1}{10}\sum_{k=i}^{i+9}(h_{\theta}(x^{(k)}) - y^{(k)})x_j^{(k)} \ (\text{for } j = 0, \ldots, n) \\
        & \ \ \ \ \} \\
        & \}
        \end{aligned}$$
* Compared to batch gradient descent, this allows us to get through data in a much more efficient way.
* Compared to stochastic gradient descent, we can vectorize the data to partially parallelize the computation(i.e. do 10 at once).
* The relation with batch gradient descent and stochastic gradient descent are: If **b = 1**, then it will be stochastic gradient descent, and if **b = m**, it will be batch gradient descent.

### Stochastic Gradient Descent Convergence

* Batch gradient descent:
  * Plot as a function of the number of iterations of gradient descent. $$J_{\text{train} }(\theta) = \dfrac {1}{2m} \displaystyle \sum_{i=1}^m \left (h_\theta (x^{(i)}) - y^{(i)} \right)^2$$
* Stochastic gradient descent:
  * $$\text{cost}(\theta, (x^{(i)}, y^{(i)})) = \frac{1}{2}(h_{\theta}(x^{(i)}) - y^{(i)})^2$$
  * During learning compute $\text{cost}(\theta, (x^{(i)}, y^{(i)}))$ before updating $\theta$ using $(x^{(i)}, y^{(i)})$.
  * Every 1000 iterations (say), plot $\text{cost}(\theta, (x^{(i)}, y^{(i)}))$ averaged over the last 1000 examples processed by algorithm. we may get different result:
    * <img src="https://i.imgur.com/1UARsw9.jpg" style="width:500px" />
    * In the top two figures, we can see, if we average 5000 examples, the curve will be smoother.
    * The bottom left shows that, sometimes, a large average examples can make the the tendency more clear.
    * The bottom right shows, if the curve increases, you may need a smaller learning rate($\alpha$).
  * About the learning rate($\alpha$):
    * In most implementations the learning rate is held constant.
    * But if we want to converge to a minimum, we can slowly decrease the learning rate over time ((E.g. $\alpha = \frac{\text{const1} }{\text{interationNumber} + \text{const2} }$)

## Online Learning

* The online learning setting allows us to model problems where we have a continuous flood or a continuous stream of data coming in and we would like an algorithm to learn from that.
* Example: Shipping service. We want to build an algorithm to optimize what price we should offer to the users.
    1. Model the probability ($p(y=1|x;\theta)$) that user use our service or not.
    2. Gather the feature vector, including the price we offered, origin, destination, etc.
    3. Repeat forever $$\begin{aligned}
        & \{ \\
        & \ \ \ \ \text{Get}\ (x, y)\ \text{corresponding to user}\ \{ \\
        & \ \ \ \ \ \ \ \ \theta_j := \theta_j - \alpha(h_{\theta}(x) - y)x_j \ (\text{for } j = 0, \ldots, n) \\
        & \ \ \ \ \} \\
        & \}
        \end{aligned}$$

### Other Online Learning Examples

* Product search (learning to search)
  * User searches for "Android phone 1080p camera" Have 100 phones in store. Will return 10 results.
  * $x$ = features of phone, how many words in user query match name of phone, how many words in query match description of phone, etc.
  * $y = 1$ if user clicks on link. $y = 0$ otherwise.
  * Learn $p(y = 1 | x; \theta)$.
  * Use to show user the 10 phones they’re most likely to click on.
* Other examples: Choosing special offers to show user; customized selection of news articles; product recommendation; …

## Map Reduce and Data Parallelism

<img src="https://i.imgur.com/agbEw4a.jpg" style="width:600px" />

## Words

* **stochastic** [stɔ'kæstik, stəu-] adj. [数] 随机的；猜测的
* **parallelize** ['pærəlelaiz] vt. 平行放置；使……平行于……
