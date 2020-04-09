# Week 3 - Logistic Regression & Regularization

\[TOC\]

## Classification and Representation

### Classification

* to determine what class a new input should fall into, \\(y \in {0, 1, ..., n}\\) 
* Classification problems
  * Email -&gt; spam/not spam?
  * Online transactions -&gt; fraudulent?
  * Tumor -&gt; Malignant/benign
* Sometimes, Linear Regression may work, like the sample below:
  * ![](../.gitbook/assets/15057384338295%20%281%29.jpg)
  * But most time the training set won't be so perfect
* Here we use **Logistic regression**, which generates a value where is always either 0 or 1

### Hypothesis Representation

* To change our hypotheses \\(h_θ\(x\)\\) to satisfy \\(0 \leq h_\theta \(x\) \leq 1\\) . 
* Our new form uses the "**Logistic Function**" , also called the "Sigmoid Function":
  * \\(\begin{aligned}& h\_\theta \(x\) = g \( \theta^T x \)\end{aligned}\\) 
  * \\(\begin{aligned} z = \theta^T x \end{aligned}\\) 
  * \\(\begin{aligned} g\(z\) = \dfrac{1}{1 + e^{-z}}\end{aligned}\\) 
    * \\(e\\) : Exponents 
* The following image shows us what the logistic function looks like:
  * ![week-3-1](../.gitbook/assets/week-3-1%20%283%29.png)
* Interpreting hypothesis output, we can use:
  * \\(h\_\theta\(x\) = P\(y=1 \| x ; \theta\)\\) , it give us the **probability** that output is 1.
    * probability that y = 1, given x, paramerterized by \\(\theta\\)
    * \\(h_\theta\(x\) = P\(y=1 \| x ; \theta\) + h_\theta\(x\) = P\(y=0 \| x ; \theta\) = 1\\)

### Decision Boundary

* In order to get our discrete 0 or 1 classification, we can translate the output of the hypothesis function as follows:
  * \\(\begin{aligned}& h_\theta\(x\) \geq 0.5 \rightarrow y = 1 \& h_\theta\(x\) &lt; 0.5 \rightarrow y = 0 \\end{aligned}\\) 
  * so \\(\begin{aligned}& g\(z\) \geq 0.5 \text{, when } z \geq 0\end{aligned}\\) 
    * \\(\begin{aligned}z=0, e^{0}=1 &\Rightarrow g\(z\)=1/2\ z \to \infty, e^{-\infty} \to 0 &\Rightarrow g\(z\)=1 \ z \to -\infty, e^{\infty}\to \infty &\Rightarrow g\(z\)=0 \end{aligned}\\) 
    * so if our input to \\(g\\) is \\(\theta^TX\\) , then that means: \\(\begin{aligned}& h\_\theta\(x\) = g\(\theta^T x\) \geq 0.5 \text{, when} \theta^T x \geq 0\end{aligned}\\) 
* Sample:
  * \\(h\_\theta\(x\) = g\(\theta\_0 + \theta\_1x\_1 + \theta\_2x\_2\)\\) :
  * ![week-3-2](../.gitbook/assets/week-3-2%20%281%29.png)
  * \\(\theta\_0 = -3, \theta\_1 = 1, \theta\_2 = 1\\) 
* So our parameter vector is a column vector with the above values: \\(\theta = \begin{bmatrix} -3\1\1\end{bmatrix}\\) 
* Then \\(z\\) becomes \\(\theta^TX\\) 
* We predict " \\(y=1\\) " if 
  * \\[\begin{aligned}-3x\_0 + 1x\_1 + 1x\_2 &\geq 0 \

      -3 + x\_1 + x\_2 &\geq 0 \

      x\_1 + x\_2 &\geq 3\end{aligned}\\]
* So \\(x\_1 + x\_2 = 3\\) we graphically plot our decision boundary:
  * ![week-3-3](../.gitbook/assets/week-3-3%20%281%29.png)
  * Means:
    * Blue = false, Magenta = true
    * Line = decision boundary

### Non-linear decision boundaries

* Get logistic regression to fit a complex non-linear data set
* \\(h\_\theta\(x\) = g\(\theta\_0 +\theta\_1x\_1 + \theta\_2x\_2 + \theta\_3x\_1^2 + \theta\_4x\_2^2\)\\) 
* Say \\(\theta^T = \begin{bmatrix}-1, 0, 0, 1, 1\end{bmatrix}\\) :
* Predict that " \\(y = 1\\) ", if \\(x\_1^2 + x\_2^2 \geq 1\\) 
* If we plot \\(x\_1^2 + x\_2^2 = 1\\) , then this gives us a circle with a radius of 1 around 0:
  * ![week-3-4](../.gitbook/assets/week-3-4%20%281%29.png)
* Mean we can build more complex decision boundaries by fitting complex parameters to this \(relatively\) simple hypothesis

## Logistic Regression Model

### Cost function

* Define the optimization object for the cost function we use to fit the parameters
  * Training set: \\({\(x^{\(1\)}, y ^ {\(1\)}\), \(x^{\(2\)}, y ^ {\(2\)}\),... , \(x^{\(m\)}, y ^ {\(m\)}\) }\\) 
  * m example: \\(x \in \begin{bmatrix}x\_0\ x\_1\ ... \ x\_n \end{bmatrix}; x\_0 = 1, y \in {0, 1}\\) 
  * \\(h\_\theta\(x\) = \dfrac{1}{1 + e^{-\theta^Tx}}\\) 
    * Each example is a feature vector which is \\(n+1\\) dimensional
* Linear regression uses the following function to determine \\(\theta\\)
  * \\(J\(\theta\) = \dfrac {1}{m} \displaystyle \sum _{i=1}^m \dfrac{1}{2}\left \(h_\theta \(x^{\(i\)}\) - y^{\(i\)} \right\)^2\\) 
  * define `Cost` function to simplify the function:
    * \\(Cost\(h_\theta\(x^{\(i\)}\), y^{\(i\)}\) = \dfrac{1}{2}\(h_\theta\(x^{\(i\)}\) - y^{\(i\)}\)^2\\) 
  * then we got:
    * \\( J\(\theta\) = \dfrac{1}{m} \displaystyle \sum_{i=1}^m \mathrm{Cost}\(h_\theta\(x^{\(i\)}\),y^{\(i\)}\)\\) 
  * to further simplify it, we can get rid of the superscripts:
    * \\( J\(\theta\) = \dfrac{1}{m} \displaystyle \sum_{i=1}^m \mathrm{Cost}\(h_\theta\(x\),y\)\\) 
* If we use this function for logistic regression, it will be a **non-convex function** which has many local optimum. Like:
  * ![week-3-5](../.gitbook/assets/week-3-5%20%281%29.png)
* So we come out a new convex logistic regression cost function:
  * \\(\begin{aligned} & \mathrm{Cost}\(h_\theta\(x\),y\) = -\log\(h_\theta\(x\)\) \; & \text{if y = 1} \ & \mathrm{Cost}\(h_\theta\(x\),y\) = -\log\(1-h_\theta\(x\)\) \; & \text{if y = 0}\end{aligned}\\) 
  * We only care \\(\(0 \le h\(x\) \le 1\)\\), so:
  * ![week-3-6](../.gitbook/assets/week-3-6%20%281%29.png)
  * ![week-3-7](../.gitbook/assets/week-3-7%20%281%29.png)
  * \\(\begin{aligned}& \mathrm{Cost}\(h_\theta\(x\),y\) = 0 \text{ if } h_\theta\(x\) = y \ & \mathrm{Cost}\(h_\theta\(x\),y\) \rightarrow \infty \text{ if } y = 0 \; \mathrm{and} \; h_\theta\(x\) \rightarrow 1 \ & \mathrm{Cost}\(h_\theta\(x\),y\) \rightarrow \infty \text{ if } y = 1 \; \mathrm{and} \; h_\theta\(x\) \rightarrow 0 \ \end{aligned}\\) 

### Simplified cost function and gradient descent

* Compress cost function's two conditional cases into one case:
  * \\(\mathrm{Cost}\(h_\theta\(x\),y\) = - y \; \log\(h_\theta\(x\)\) - \(1 - y\) \log\(1 - h\_\theta\(x\)\)\\) 
  * Cause y can either be 0 or 1,
    * if y = 1, then \\( \(1 - y\) \log\(1 - h\_\theta\(x\)\) = 0\\)
    * if y = 0, then \\( y \log\(h\_\theta\(x\)\) = 0\\)
  * this cost function can be derived from statistics using the principle of **maximum likelihood estimation**.
    * the idea of how to efficiently find parameters' data for different models.
* Then we can fully write out our entire cost function as follows:
  * \\(J\(\theta\) = - \frac{1}{m} \displaystyle \sum_{i=1}^m \[y^{\(i\)}\log \(h_\theta \(x^{\(i\)}\)\) + \(1 - y^{\(i\)}\)\log \(1 - h\_\theta\(x^{\(i\)}\)\)\]\\) 
  * and a vectorized implementation is:
    * \\(\begin{aligned} & h = g\(X\theta\)\ & J\(\theta\) = \frac{1}{m} \cdot \left\(-y^{T}\log\(h\)-\(1-y\)^{T}\log\(1-h\)\right\) \end{aligned}\\) 
* **Gradient Descent**
  * the general form is:
    * \\(\begin{aligned}& Repeat \; \lbrace \ & \; \theta\_j := \theta\_j - \alpha \dfrac{\partial}{\partial \theta\_j}J\(\theta\) \ & \rbrace\end{aligned}\\) 
  * We can work out the derivative part using calculus to get:
    * \\(\begin{aligned} & Repeat \; \lbrace \ & \; \theta_j := \theta\_j - \frac{\alpha}{m} \sum_{i=1}^m \(h\_\theta\(x^{\(i\)}\) - y^{\(i\)}\) x\_j^{\(i\)} \ & \rbrace \end{aligned}\\) 
  * A vectorized implementation is:
    * \\(\theta := \theta - \frac{\alpha}{m} X^{T} \(g\(X \theta \) - \vec{y}\)\\) 

### Advanced Optimization

* Alternatively, instead of gradient descent to minimize the cost function we could use
  * **Conjugate gradient** 
  * **BFGS** \(Broyden-Fletcher-Goldfarb-Shanno\)
  * **L-BFGS** \(Limited memory - BFGS\)
* Some properties
  * **Advantages**
    * No need to manually pick alpha \(learning rate\)
    * Have a clever inner loop \(line search algorithm\) which tries a bunch of alpha values and picks a good one
    * Often faster than gradient descent
    * Do more than just pick a good learning rate
    * Can be used successfully without understanding their complexity
  * **Disadvantages**
    * Could make debugging more difficult
    * Should not be implemented themselves
    * Different libraries may use different implementations - may hit performance
* Using advanced cost minimization algorithms
  * Example:
    * \\(\theta = \begin{bmatrix}\theta\_1\ \theta\_2\end{bmatrix}\\)
    * \\(J\(\theta\) = \(\theta\_1 - 5\)^2 + \(\theta\_2 - 5\)^2\\)
    * \\(\dfrac{\partial}{\partial \theta\_1}J\(\theta\) = 2\(\theta\_1 - 5\)\\)
    * \\(\dfrac{\partial}{\partial \theta\_2}J\(\theta\) = 2\(\theta\_2 - 5\)\\)
    * Example above
      * \\(θ\_1\\) and \\(θ\_2\\) \(two parameters\)
      * Cost function here is \\(J\(\theta\) = \(\theta\_1 - 5\)^2 + \(\theta\_2 - 5\)^2\\) 
      * The derivatives of the \\(J\(θ\)\\) with respect to either \\(θ\_1\\) and \\(θ\_2\\) turns out to be the \\(2\(θ\_i - 5\)\\) 
  * First, define our cost function:

    ```text
      > function [jVal, gradient] = costFunction(theta)
      >     jVal = [...code to compute J(theta)...];
      >     gradient = [...code to compute derivative of J(theta)...];
      > end
    ```

    * `jVal` = \\(\(\theta\_1 - 5\)^2 + \(\theta\_2 - 5\)^2\\) 
    * `gradient` is a 2 by 1 vector, and 2 elements are the two partial derivative terms

  * Then,

    ```text
      > options = optimset('GradObj', 'on', 'MaxIter', 100);
      > initialTheta = zeros(2,1);
      > [optTheta, functionVal, exitFlag] = fminunc(@costFunction, initialTheta, options);
    ```

    * Here,
      * **options** is a data structure giving options for the algorithm
      * **fminunc**
        * function minimize the cost function \(**f**ind **min**imum of **unc**onstrained multivariable function\)
      * **@costFunction** is a pointer to the costFunction function to be used
    * For the octave implementation
      * **initialTheta** must be a matrix of at least two dimensions 

## Multiclass Classification: One-vs-all

* Divide our problem into n+1 \(+1 because the index starts at 0\) binary classification problems; in each one, we predict the probability that `y` is a member of one of our classes.
  * \\(\begin{aligned}& y \in \lbrace0, 1 ... n\rbrace \& h_\theta^{\(0\)}\(x\) = P\(y = 0 \| x ; \theta\) \& h_\theta^{\(1\)}\(x\) = P\(y = 1 \| x ; \theta\) \& \cdots \& h_\theta^{\(n\)}\(x\) = P\(y = n \| x ; \theta\) \& \mathrm{prediction} = \max\_i\( h_\theta ^{\(i\)}\(x\) \)\\end{aligned}\\) 
  * The following image show how one could classify 3 classes:
  * ![week-3-8](../.gitbook/assets/week-3-8%20%281%29.png)
* Overall
  * Train a logistic regression classifier \\(h\_{θ}^{\(i\)}\(x\)\\) for each class i to predict the probability that \\(y = i\\) 
  * On a new input, \\(x\\) to make a prediction, pick the class \\(i\\) that maximizes the probability that \\(h\_θ^{\(i\)}\(x\) = 1\\) 

## The Problem of Overfitting

### Problems:

* Three figures to shows that **underfitting**, **fitting** and **overfitting**: \(take housing price as sample\)
  * ![week-3-9](../.gitbook/assets/week-3-9%20%281%29.png)
  * under-fitting or high bias: leftmost, \\(y = θ\_0 + θ\_1x\\) , doesn't really lie on straight line.
  * overfitting: rightmost, \\(y = \sum\_{j=0} ^5 \theta\_j x^j\\) , not a good predictor.
  * fitting one: \\(y = \theta\_0 + \theta\_1x + \theta\_2x^2\\) , obtain a slightly better fit to the data.

### Addressing overfitting

* Reduce the number of features:
  * Manually select which features to keep.
  * Use a model selection algorithm.
* Regularization
  * Keep all the features, but reduce the magnitude of parameters \\(\theta\_j\\) .
  * Regularization works well when we have a lot of slightly useful features.

### Cost Function

* if we have overfitting from our hypothesis function , we can reduce the weight that some of the terms in our function carry by increasing their cost.
* Say we wanted to make the following function more quadratic:
  * \\(\theta\_0 + \theta\_1x + \theta\_2x^2 + \theta\_3x^3 + \theta\_4x^4\\) 
* We'll want to eliminate the influence of \\(\theta\_3x^4\\) and \\(\theta\_4x^4\\) . Without actually getting rid of these features or changing the form of our hypothesis, we can instead modify our cost function:
  * \\(min_\theta \dfrac{1}{2m}\sum_{i=1}^m \(h\_\theta\(x^{\(i\)}\) - y^{\(i\)}\)^2 + 1000\cdot\theta\_3^2 + 1000\cdot\theta\_4^2\\) 
  * Add two extra terms at the end to inflate the cost of \\(\theta\_3\\) and \\(\theta\_4\\) . This will in turn greatly reduce the values of \\(\theta\_3x^4\\) and \\(\theta\_4x^4\\) in our hypothesis function.
* We could also regularize all of our theta parameters in a single summation as:
  * \\(min_\theta \dfrac{1}{2m} \left\[ \sum_{i=1}^m \(h_\theta\(x^{\(i\)}\) - y^{\(i\)}\)^2 + \lambda \sum_{j=1}^n \theta\_j^2 \right\]\\) 
  * \\(\lambda\\) \(lambda\), is the **regularization parameter**. It determines how much the costs of our theta parameters are inflated.
  * But if lambda is chosen to be too large, it may smooth out the function too much and cause under-fitting. 

### Regularized Linear Regression

* Gradient Descent
* > \\(\begin{aligned} & \text{Repeat} \lbrace \ &     \theta_0 := \theta\_0 - \alpha \frac{1}{m} \sum_{i=1}^m \(h_\theta\(x^{\(i\)}\) - y^{\(i\)}\)x\_0^{\(i\)} \ &     \theta\_j := \theta\_j - \alpha \left\[ \left\( \frac{1}{m} \sum_{i=1}^m \(h\_\theta\(x^{\(i\)}\) - y^{\(i\)}\)x\_j^{\(i\)} \right\) + \frac{\lambda}{m}\theta\_j \right\] &          j \in \lbrace 1,2...n\rbrace\ & \rbrace \end{aligned}\\)

  * The term \\(\frac{\lambda}{m}\theta\_j\\) performs our regularization. With some manipulation our update rule can also be represented as:
    * \\(\theta_j := \theta\_j\(1 - \alpha\frac{\lambda}{m}\) - \alpha\frac{1}{m}\sum_{i=1}^m\(h\_\theta\(x^{\(i\)}\) - y^{\(i\)}\)x\_j^{\(i\)}\\) 
  * The first term in the above equation, \\(1 - \alpha\frac{\lambda}{m}\\) will always be less than 1. Intuitively you can see it as reducing the value of \\(θ\_j\\) by some amount on every update. Notice that the second term is now exactly the same as it was before.

#### Normoal Equation

* To add in reguarlization, the equation is the same as our original, except that we add another term inside the parentheses:
  * \\(\begin{aligned}& \theta = \left\( X^TX + \lambda \cdot L \right\)^{-1} X^Ty \& \text{where}  L = \begin{bmatrix} 0 & & & & \ & 1 & & & \ & & 1 & & \ & & & \ddots & \ & & & & 1\end{bmatrix}\end{aligned}\\) 
* L is a matrix with 0 at the top left and 1's down the diagonal, with 0's everywhere else. It should have dimension \(n+1\)×\(n+1\). Intuitively, this is the identity matrix \(though we are not including \\(x\_0\\) \), multiplied with a single real number \\(\lambda \\) .
* Recall that if \\(m \le n\\) , then \\(X^TX\\) is non-invertible. However, when we add the term \\(\lambda \cdot L\\) , then \\(X^TX + \lambda \cdot L\\) becomes invertible.

### Regularized Logistic Regression

* Cost function:
  * \\(J\(\theta\) = - \frac{1}{m} \sum_{i=1}^m \large\[ y^{\(i\)} \log \(h_\theta \(x^{\(i\)}\)\) + \(1 - y^{\(i\)}\) \log \(1 - h\_\theta\(x^{\(i\)}\)\) \large\]\\) 
* Regularize this equation by adding a term to the end:
  * \\(J\(\theta\) = - \frac{1}{m} \sum_{i=1}^m \large\[ y^{\(i\)} \log \(h_\theta \(x^{\(i\)}\)\) + \(1 - y^{\(i\)}\) \log \(1 - h_\theta\(x^{\(i\)}\)\)\large\] + \frac{\lambda}{2m}\sum_{j=1}^n \theta\_j^2\\) 
  * The second sum, \\(\sum\_{j=1}^n \theta\_j^2\\) means to explicitly exclude the bias term, \\(\theta\_0\\) . I.e. the \\(\theta\\) vector is indexed from 0 to n \(holding n+1 values, \\(\theta\_0\\) through \\(\theta\_n\\) \), and this sum explicitly skips \\(\theta\_0\\) , by running from 1 to n, skipping 0 \(This is because for regularization we don't penalize \\(θ\_0\\) so treat it slightly differently\). Thus, when computing the equation, we should continuously update the two following equations:
  * ![week-3-10](../.gitbook/assets/week-3-10.png)

## Words

**logistic** \[ləu'dʒistik\] adj. \[数\] 符号逻辑的

**fraudulent** \['frɔ:djulənt\] adj. 欺骗性的；不正的

**malignant** \[mə'liɡnənt\] adj. \[医\] 恶性的；

**benign** \[bi'nain\] adj. 良性的；

**polynomial** \[,pɔli'nəumiəl\] n. \[数\] 多项式；

**quadratic** \[kwɔ'drætik\] adj. \[数\] 二次的 n. 二次方程式;

**penalize** \['pi:nəlaiz\] vt. 处罚；处刑；使不利

**sigmoid function** \['sigmɔid\] 双弯曲函数

