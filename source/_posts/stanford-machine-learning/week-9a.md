# Week 9a - Anomaly Detection

## Density Estimation

### Problem Motivation

* Fraud detection:
    * \\(x^{(i)}\\) = features of user \\(i\\)'s activities on the website.
    * Model \\(p(x)\\) from data.
    * Identify unusual users by checking which have \\(p(x) < \epsilon \\)
        * if \\(p(x) < \epsilon\\) flag this as an anomaly
        * otherwise, this is OK
* Manufacturing
    * Aircraft engine manufacturer
        * Check if the new engine is anomalous
* Monitoring computers in a data center.
    * \\(x^{(i)}\\) = features of machine \\(i\\)
    * \\(x_1\\) = memory use,     
    * \\(x_2\\) = number of disk accesses/sec,
    * \\(x_3\\) = CPU load,
    * \\(x_4\\) = CPU load/network traffic.
    * ...

### Gaussian(Normal) Distribution

* Have learned it from [Lecture 6(Computational Thinking)](https://cs.ericyy.me/computational-thinking/lecture-6-7/index.html)

* Notation [From Wikipedia](https://en.wikipedia.org/wiki/Normal_distribution)
    * When a random variable \\(X\\) is distributed normally with mean \\(\mu\\)  and variance \\(\sigma ^{2}\\), one may write \\[{\displaystyle X\ \sim \ {\mathcal {N}}(\mu ,\sigma ^{2}).}\\]
    * The probability of x can be written as \\[p(x;\mu, \sigma^2) = \frac{1}{\sqrt{2\pi} \sigma} \exp(-\frac{x-\mu^2}{2\sigma^2})\\]

### Algorithm

1. Choose features \\(x_i\\) that you think might be indicative of anomalous examples.
2. Fit parameters \\(\mu_1, \ldots, \mu_n, \sigma_1^2, \ldots, \sigma_n^2 \\)
    * \\[\mu_j = \frac{1}{m}\sum_{i=1}^m x_j^{(i)}\\]
    * \\[\sigma_j^2 = \frac{1}{m}\sum_{i=1}^m (x_j^{(i)} - \mu_j)^2\\]
3. Given new example x, compute \\(p(x)\\):
    * \\[\begin{aligned}p(x) &= p(x_1;\mu_1,\sigma_1^2) \cdot p(x_2;\mu_2,\sigma_2^2) \cdot p(x_3;\mu_3,\sigma_3^2) \cdot \ldots \cdot p(x_n;\mu_n,\sigma_n^2) \\ 
        &= \prod_{j=1}^n p(x_j;\mu_j, \sigma_j^2)
    \end{aligned}\\]
    * Anomaly if \\(p(x) < \epsilon\\).
* The problem of estimating this distribution **p** of **x**, sometimes called **the problem of density estimation**.

#### Example

* <img src="https://i.imgur.com/Hh2szfM.jpg" style="width:500px" />

## Building an Anomaly Detection System

### Developing and Evaluating an Anomaly Detection System

* Assume we have some labeled data, of anomalous and non-anomalous examples. (y =0 if normal, y = 1 if anomalous).
* Training set: \\(x^{(1)}, x^{(2)}, \ldots, x^{(m)}\\) (assume normal examples/not anomalous)
* Cross validation set: \\((x^{(1)}_{cv}, y^{(1)}_{cv}), \ldots, (x^{(m_{cv})}_{cv}, y^{(m_{cv})}_{cv})\\)
* Test set: \\((x^{(1)}_{test}, y^{(1)}_{test}), \ldots, (x^{(m_{test})}_{test}, y^{(m_{test})}_{test})\\)

#### Aircraft engines motivating example

* Data set:
    * 10000 good(normal) engines
    * 20 flawed engines (anomalous)
* Separate Data set:
    * Training set: 6000 good engines
    * CV: 2000 good engines (y = 0), 10 anomalous (y = 1)
    * Test: 2000 good engines (y = 0), 10 anomalous (y = 1)
* Algorithm evaluation
    * Fit model \\(p(x)\\) on training set \\(\{ x^{(1)}, \ldots, x^{(m)} \}\\)
    * On a cross validation/test examples \\(x\\), predict \\[y = \begin{cases}
            1 &\text{if}\ p(x) < \epsilon \text{(anomaly)}\\
            0 &\text{if}\ p(x) \ge \epsilon \text{(normal)}
        \end{cases}\\]
    * Possible evaluation metrics:
        - True positive, false positive, false negative, true negative 
        - Precision/Recall
        - \\(F_1\\)-score
    * Can also use cross validation set to choose parameter \\(\epsilon\\)

### Anomaly Detection vs Supervised Learning

* Anomaly Detection
    * Very small number of positive examples (y=1). (0-20 is common).
    * Large number of negative (y=0) examples.
    * Many different "types" of anomalies. Hard for any algorithm to learn from positive examples what the anomalies look like;
    * Further anomalies may look nothing like any of the anomalous examples we've seen so far.
* Supervised Learning
    * Large number of positive and negatives.
    * Enough positive examples for algorithm to get a sense of what positive examples are like, future positive examples likely to be similar to ones in training set.
* Examples can use Anomaly detection
    * Fraud detection
    * Manufacturing (e.g. aircraft engines)
    * Monitering machines in a data center
* Examples can use Supervised learning
    * Email spam classification
    * Weather prediction
    * Cancer classification

### Choosing What Features to Use

* **Non-gaussian features**
    * Plot a histogram of data to check if it has a Gaussian description. If it doesn't, we can transfer the feature with:
        * \\(\log(x+C)\\), where **C** is a constant
        * \\(x^{\frac{1}{2}}\\)
        * \\(x^{\frac{1}{3}}\\)
        * ...
        * to make it more Gaussian
            * <img src="https://i.imgur.com/TcIZjMZ.jpg" style="width:500px" />

* **Error analysis for anomaly detection**
    * When we get a wrong result on CV test, need to find out why the algorithm doesn't work.
    * For example:
        * We have one dimension, and our anomalous value is sort of buried in it (in green - Gaussian superimposed in blue)
        * So we need to come out a new feature to make this data set in two dimensions, and hopefully, the green spot will be out of our normal range.
        * <img src="https://i.imgur.com/PtfZCmU.jpg" style="width:450px" />

    * Another example:
        * Monitoring computers in a data center
        * Choose features that might take on unusually large or small values in the event of an anomaly.
            * \\(x_1\\) = memory use of computer
            * \\(x_2\\) = number of disk accesses/sec
            * \\(x_3\\) = CPU load
            * \\(x_4\\) = network traffic
        * If some program are running infinity, we will get a high CPU load, and low network traffic. But the features above can't detect this issue, so we come out a new feature = \\(\frac{\text{CPU load}}{\text{network traffic}}\\)

## Multivariate Gaussian Distribution

* \\(x \in \mathbb{R}^n\\).
* Formula: \\[p(x;\mu,\Sigma)= \frac{1}{\sqrt { (2\pi)^n| \Sigma| } }  \exp\left(-{1 \over 2} (\mathbf{x}-\mu)^{\rm T} \Sigma^{-1} ({\mathbf x}-\mu)\right)\\]
    * \\(\mu \in \mathbb{R}^n, \Sigma \in \mathbb{R}^{n \times n}\\) (covariance matrix)
    * \\(\lvert \Sigma \rvert\\): matrix determinant. In Matlab: `det(Sigma)`
* Examples
    * <img src="https://i.imgur.com/6ol1UBo.jpg" style="width:500px" />
    * <img src="https://i.imgur.com/hdC1t0i.jpg" style="width:500px" />
    * <img src="https://i.imgur.com/vL0WPC5.jpg" style="width:500px" />

### Anomaly Detection using the Multivariate Gaussian Distribution

0. Given training set \\(\{ x^{(1)}, x^{(2)}, \ldots, x^{(m)} \}\\)
1. Fit model \\(p(x)\\) by setting 
    * \\(\displaystyle \mu = \frac{1}{m} \sum_{i=1}^m x^{(i)}\\)
    * \\(\displaystyle \Sigma = \frac{1}{m}\sum_{i=1}^m (x^{(i)} - \mu)(x^{(i)} - \mu)^T\\)
2. Given a new example \\(x\\), compute \\[p(x) = \frac{1}{\sqrt { (2\pi)^n| \Sigma| } }  \exp\left(-{1 \over 2} (\mathbf{x}-\mu)^{\rm T} \Sigma^{-1} ({\mathbf x}-\mu)\right)\\]
    * Flag an anomaly if \\(p(x) < \epsilon\\)

#### Relationship to original model

* Original model: \\[p(x) = p(x_1;\mu_1,\sigma_1^2) \cdot p(x_2;\mu_2,\sigma_2^2) \cdot p(x_3;\mu_3,\sigma_3^2) \cdot \ldots \cdot p(x_n;\mu_n,\sigma_n^2)\\] Corresponds to multivariate Gaussian \\[p(x;\mu,\Sigma)= \frac{1}{\sqrt { (2\pi)^n| \Sigma| } }  \exp\left(-{1 \over 2} (\mathbf{x}-\mu)^{\rm T} \Sigma^{-1} ({\mathbf x}-\mu)\right)\\] where \\[\Sigma = \begin{bmatrix}\sigma_1^2 & 0 & 0 & 0 \\ 0 & \sigma_2^2 & 0 & 0 \\ 0 & 0 & \ddots & 0 \\ 0 & 0 & 0 & \sigma_n^2 \end{bmatrix}\\]

### Original model vs Multivariate Gaussian
    
* Original model
    * [Disadvantage] Manually create features to capture anomalies where \\(x_1, x_2\\) take unusual combinations of values.
    * [Advantage] Computationally cheaper
    * [Advantage] Works fine even **m**(training set size) is small.
* Multivariate Gaussian
    * [Advantage] Automatically captures correlations between features
    * [Disadvantage] Computationally more expensive
        * try to reduce the feature size
    * [Disadvantage] Must have \\(m > n\\), or \\(\Sigma\\) is not-invertible.
        * In practice, we should make sure \\(m \ge 10n\\).

## Words

* **covariance matrix** 协方差矩阵
* **off-diagonal** adj. [数] 非对角的，[数] 对角线外的

