# Week 10 - Linear Approximation

## What is Linear Approximation

* <img src="https://i.imgur.com/lixorO6.jpg" style="width:200px" />
* We call the tangent line is the **linear approximation** to the function at $x=a$.
* $f(x+h) \approx f(x) + h \cdot f'(x)$

## Euler's Method 

* AKA, **Repeated Linear Approximation**
* Definition: Approximate values for the solution of the initial-value problem $y' = F(x,y)$, $y(x_0) = y_0$, with step size **h**, at $x_n = x_{n-1} + h$, are $$y_n = y_{n-1} + hF(x_{n-1},y_{n-1}) \text{, } n=1,2,3,...$$
    * <img src="https://i.imgur.com/lKFQF40.jpg" style="width:200px" />
    * Let's say $f(0) = a$, $a \in \mathbb{R}$, and **h** is small number.
    * So, 
        * $$\begin{aligned}
            f(h) &\approx f(0) + h \cdot F(0) \\
            f(2h) &\approx f(h) + h \cdot F(h) \\
            f(3h) &\approx f(h) + h \cdot F(2h)
            \end{aligned}$$
    * Since this is just an approximation of the derivative, it's better not to pick a point which is all the way on the **left hand side** of the interval, instead with **the middle value**: 
        * $$\begin{aligned}
            f(h) &\approx f(0) + h \cdot F(\frac{h}{2}) \\
            f(2h) &\approx f(h) + h \cdot F(\frac{3h}{2}) \\
            f(3h) &\approx f(h) + h \cdot F(\frac{5h}{2})
            \end{aligned}$$
* Take another example, why is $\log_{2}{3} \approx 19/12$?
    * Since $\log_{2}{3} = \frac{\log3}{\log2}$, Let's separate it, to estimate $\log2$ first.
    * Set our function $f(x) = \log{x}$, then $\log(1) = 0$, so let's start with $\log(1)$ with step size: **1/4** : 
        * So, $\log(1+\frac{1}{4}) \approx \log{1} + \frac{1}{4} \cdot f'(1+\frac{1}{8}) = 0 + \frac{1}{4} \cdot \frac{1}{1+\frac{1}{8}} = \frac{2}{9}$
            * PS, instead of using $f'(1)$, we used $f'(1+\frac{1}{8}) = f'(1+\frac{\frac{1}{4}}{2})$, which is more accurate.
            * $f'(x) = \frac{1}{x}$
        * Then use **Euler's Method**: $\log(1+\frac{1}{4}+\frac{1}{4}) \approx \log{(1+\frac{1}{4})} + \frac{1}{4} \cdot f'(1+\frac{1}{4}+\frac{1}{8}) = \frac{40}{99}$
        * Keep doing this, we got: $$\begin{aligned}\log(2) &\approx 0.693... \\ \log(3) &\approx 1.098... \\ \frac{\log(3)}{\log(2)} &\approx 1.584962... \end{aligned}$$
        * And $\frac{19}{12} = 1.58\bar{3}$, pretty close.

## Newton's Method

* Also called the **Newton-Raphson method**
* To solve the equation of the form $f(x) = 0$, so the roots of the equation(方程的根) correspond to the x-intercepts of the graph of $f$. The root that we are trying to find is labeled $r$ in the figure.
    * <img src="https://i.imgur.com/jOZq5fU.jpg" style="width:200px" />
    * We start with a first approximation $x_1$ , which is obtained by guessing,
    * Consider the tangent line **L** to the curve $y = f(x)$ at the point $(x_1, f(x_1))$ and look at the x-intercept of **L**, labeled $x_2$.
    * The idea behind **Newton’s method** is that the tangent line is close to the curve and so its x-intercept, $x_2$, is close to the x-intercept of the curve (namely, the root $r$ that we are seeking). Because the tangent is a line, we can easily find its x-intercept.
    * To find a formula for $x_2$ in terms of $x_1$ we use the fact that the slope of **L** is $f'(x_1)$, so its equation is:
        * $y - f(x_1) = f'(x_1)(x - x_1)$
    * Since the x-intercept of **L** is $x_2$, we know that point ($x_2, 0$) is on the line, and so:
        * $0 - f(x_1) = f'(x_1)(x_2 - x_1)$
    * If $f'(x_1) \ne 0$, we can solve this equation for $x_2$:
        * $x_2 = x_1 - \frac{f(x_1)}{f'(x_1)}$
        * Then $x_3 = x_2 - \frac{f(x_2)}{f'(x_2)}$
    * If we keep repeating this process, we obtain a sequence of approximations $x_1, x_2, x_3, x_4, \dots$ as shown:
        * <img src="https://i.imgur.com/hHtnG2a.jpg" style="width:180px" />
    * In general, if the $n$th approximation is $x_n$ and $f'(x_n) \ne 0$, then the next approximation is given by:
        * $x_{n+1} = x_n - \frac{f(x_n)}{f'(x_n)}$
    * If the number $x_n$ become closer and closer to $r$ as $n$ becomes large, then we say that the sequence **converges** to $r$ and we write $$\lim_{n \to \infty}x_n = r$$
* Sometimes **The Newton’s method fails**:
    * For example, if we choose $x_2$, then the approximation falls outside the domain of $f$:
        * <img src="https://i.imgur.com/LfmlPd1.jpg" style="width:180px" />
    * Then we need a better initial approximation $x_1$.

### Use Newton's Method to Divide Quickly

* Suppose we want to calculate $\frac{1}{b}$
* Here is one choice: $f(x) = \frac{1}{x} - b$:
    * Because $f(\frac{1}{b}) = \frac{1}{\frac{1}{b}} - b = b - b = 0$
    * So we can use Newton's Method to find **1/b**.
    * $$\begin{aligned}
        f'(x) &= - \frac{1}{x^2} \\
        x_{n+1} &= x_n - \frac{f(x_n)}{f'(x_n)} \\
        &= x_n - \frac{\frac{1}{x_n} - b}{-\frac{1}{x_n^2}} \cdot \frac{-x_n^2}{-x_n^2} \\
        &= x_n - (-x_n + bx_n^2) \\
        &= 2x_n - bx_n^2 \\
        &= x_n \cdot (2 - bx_n)
        \end{aligned}$$


