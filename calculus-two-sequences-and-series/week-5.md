# Week 5 - Power Series

\[TOC\]

## Definition

* A **power series** is a series of the form \\[\sum\_{n=0}^{\infty}c\_n x^n = c\_0 + c\_1 x + c\_2 x^2 + c\_3 x^3 + \cdots\\] where **x** is a variable and the \\(c\_n\\)’s are constants called the **coefficients** of the series.
* The sum of the series is a function \\[f\(x\) = c\_0 + c\_1 x + c\_2 x^2 + \cdots + c\_n x^n + \cdots \\] whose domain is the set of all x for which the series converges. Notice that \\(f\\) resembles a polynomial.

## Convergence of Power Series

### Interval of convergence

* \\[C = { x \in \mathbb{R} \| \sum\_{n = 0}^{\infty} a\_n x^n \text{converge}}\\]
* **C** is called the **interval of convergence**.

### Theorem

* Suppose \\(\displaystyle \sum\_{n = 0}^{\infty} a\_n x^n\\) converge when \\(x = x\_0\\), then the series converge absolutely x between \\(-x\_0\\) and \\(x\_0\\).
* Prove:
  * Suppose \\(\displaystyle \sum\_{n = 0}^{\infty} a\_n x^n\\) converge when \\(x = x\_0\\)
  * So, \\(\displaystyle \lim\_{n \to \infty} a\_n x\_0^n = 0\\),
  * There is an **M**, so that for all **n**, \\(\|a\_n x\_0^n\| \le M\\),
  * Pick \\(x \in \(-\|x\_0\|, \|x\_0\|\)\\),
  * \\(\|a\_n x^n\| = \|a\_n x\_0^n\| \cdot \|\frac{x^n}{x\_0^n}\| \le M \cdot \|\frac{x^n}{x\_0^n}\|\\)
  * With ratio test, \\(r = \|\frac{x^n}{x_0^n}\| &lt; 1\\), we can get \\(\sum_{n = 0}^{\infty} M \cdot r^n\\) converge,
  * So \\(\sum\_{n=0}^{\infty} \|a\_n x^n\|\\) converge.
* Corollary:
  * Consider \\(\sum\_{n=0}^{\infty} a\_n x^n\\).
  * There is an **R**, so that the series,
    * converges absolutely for \\(x \in \(-R, R\)\\),
    * diverges for \\(x &gt; R \text{ or } x &lt; -R\\)
  * The number **R** is called the **radius of convergence** of the power series.

### Example

* What's the interval of convergence of the series \\(\displaystyle \sum\_{n=1}^{\infty}\frac{x^n}{n}\\)
* First, we ask the easier question. What's its radius of convergence?
  * Think this series converge absolutely, and use ratio test:
    * \\(\displaystyle\lim\_{n \to \infty}\|\frac{x^{n+1}/{n+1} }{x^n/n}\| = \|x\|\\)
    * \\(\|x\|&lt;1\\), the series converges,
    * \\(\|x\|&gt;1\\), the series diverges.
  * So the radius of convergence is **1**.
* What about the endpoints **1** and **-1**?
  * if x = 1, then the series = \\(\sum\_{n=1}^{\infty} \frac{1}{n}\\), which is harmonic series, also diverges.
  * if x = -1, then the series = \\(\sum\_{n=1}^{\infty} \frac{\(-1\)^n}{n}\\), that's the alternating harmonic series, and converges.
* To summarize this: 
  * The interval of convergence of series \\(\displaystyle \sum\_{n=1}^{\infty}\frac{x^n}{n}\\) is \\(\[-1, 1\)\\)

## Differentiation and integration of power Series

### Power Series Centered Around a

* \\(\displaystyle\sum\_{n=0}^{\infty}c\_n \(x - a\)^n\\)
* Use ratio test:
  * \\(\displaystyle \lim_{n \to \infty} \|\frac{c_{n+1} \cdot \(x - a\)^{n+1} }{c_n \cdot \(x - a\)^n}\| = \lim_{n \to \infty} \|\frac{c\_{n+1} }{c\_n}\| \cdot \|x - a\|\\)
  * To get the interval of convergence, let's set \\(\|\frac{c\_{n+1} }{c\_n}\| = \frac{1}{R}\\)
    * \\(\frac{1}{R} \cdot \|x - a\| &lt; 1\\)
    * \\(a - R &lt; x &lt; a + R\\)

### Differentiate a Power Series

* Theorem: 
  * \\(\displaystyle f\(x\) = \sum\_{n=0}^{\infty} a\_n x^n\\), **R** = radius of convergence.
  * Then \\(\displaystyle f'\(x\) = \sum\_{n=1}^{\infty} n \cdot a\_n \cdot x^{n-1} \text{ for } x \in \(-R, R\)\\)
    * Notice the index of **n** start from 1, because when \\(n = 0, f'\(x\) = 0\\)

### Integrate a Power Series

* Theorem: 
  * \\(\displaystyle f\(x\) = \sum\_{n=0}^{\infty} a\_n x^n\\), **R** = radius of convergence.
  * Then \\(\displaystyle \int_0^t f\(x\) dx = \sum_{n=1}^{\infty} \frac{a\_n \cdot t^{n+1} }{n+1} \text{ for } x \in \(-R, R\)\\)
* Example: \\(\displaystyle \int_{x=0}^{t} \sum_{n=0}^{\infty} x^n dx\\)
  * First to prove: \\(\displaystyle \sum\_{n=0}^{\infty} x^n = \frac{1}{1-x}\\), \\(\|x\| &lt; 1\\) =&gt; \\(R = 1\\)
    * Use Geometric Series theorem, we know \\(\displaystyle \sum_{n=1}^{\infty} x^n = \sum_{n=1}^{\infty} x \cdot x^{n-1} = \frac{x}{1-x}\\)
    * So \\(\displaystyle \sum\_{n=0}^{\infty} x^n = \frac{x}{1-x} + x^0 = \frac{1}{1-x}\\)
  * \\(\displaystyle \int\_{x = 0}^t \frac{1}{1-x} dx\\), use substitution rule, set \\(u = 1 - x, du = -dx\\)
  * \\(\displaystyle \int_{x = 0}^t \frac{1}{1-x} dx = - \int_{x = 0}^t \frac{du}{u} \\)
  * \\(= -\log\|u\| \rbrack_{x=0}^t = - \log\|1-x\|\rbrack_{x=0}^t = - \log \|1 - t\|\\)
  * In another way, we can backwards the derivation:
    * \\(\displaystyle - \log \|1 - t\| = \int\_{x=0}^t \frac{1}{1-x} dx\\)
    * \\(\displaystyle = \int_{x=0}^{t} \sum_{n=0}^{\infty} x^n dx = \sum_{n=0}^{\infty} \int_{x=0}^{t} x^n dx\\)
    * \\(\displaystyle = \sum\_{n=0}^{\infty} \frac{t^{n+1} }{n+1}, \|t\| &lt; 1\\)

### e^x

* To prove \\(\displaystyle \sum\_{n=0}^{\infty} \frac{x^n}{n!} = e^x\\)
  * It's the sum, n goes from 0 to infinity of x to the n over n factorial
* \\(\displaystyle f\(x\) = \sum\_{n=0}^{\infty} \frac{x^n}{n!}\\)
* prove \\(f\(0\) = e^0 = 0\\):
  * \\(\displaystyle f\(0\) = \sum\_{n=0}^{\infty} \frac{0^n}{n!} = 1\\)
    * \\(0^0 = 1, 0^1 = 0, \ldots, 0^n = 0\\)
    * \\(0! = 1\\). because: \\(\(n+1\)! = \(n+1\) \cdot n!\\)
  * \\(e^0 = 1\\)
* after differentiation, both functions still themselves:
  * \\(\displaystyle \frac{d}{dx} \sum_{n=0}^{\infty} \frac{x^n}{n!} = \sum_{n=0}^{\infty} \frac{x^{n-1} }{\(n-1\)!} = \sum\_{n=0}^{\infty} \frac{x^n}{n!} \\)
  * \\(\frac{d}{dx}e^x = e^x\\)
    * These two star-crossed functions agree at a single point, and they're changing in the same way, and consequently, they must be the same function. 

### Multiply Two Power Series

* \\(\displaystyle \(\sum_{n=0}^{\infty} a\_n x^n\) \cdot \(\sum_{n=0}^{\infty} b\_n x^n\) \\)
* \\(=\(a\_0 + a\_1 x + a\_2 x^2 + \cdots\) \cdot \(b\_0 + b\_1 x + b\_2 x^2 + \cdots\)\\)
* \\(= a\_0 b\_0 + \(a\_1 + b\_1\) x + \(a\_0 b\_2 + a\_1 b\_1 + a\_2 b\_0\) x^2 + \cdots\\)
* \\(\displaystyle \(\sum_{n=0}^{\infty} a\_n x^n\) \cdot \(\sum_{n=0}^{\infty} b_n x^n\) = \sum_{n=0}^{\infty} \(\sum_{i=0}^{n} a\_i b_{n-i}\) x^n\\)

#### Theorem

* \\(f\(x\) = \displaystyle \(\sum_{n=0}^{\infty} a\_n x^n\)\\), \\(g\(x\) = \displaystyle \(\sum_{n=0}^{\infty} b\_n x^n\)\\), and their radius of convergence \\(\ge \mathbb{R}\\)
* Then we can get: \\(\displaystyle f\(x\) g\(x\) = \sum_{n=0}^{\infty} \(\sum_{i=0}^{n} a_i b_{n-i}\) x^n\\), for \\(x \in \(-R, R\)\\)
* Example:
  * \\(\displaystyle e^x = \sum\_{n=0}^{\infty} \frac{x^n}{n!} = 1 + x + \frac{x^2}{2} + \frac{x^3}{6} + \cdots \\)
  * \\(\(e^x\)^2 = e^{\(2x\)}\\)
  * \\(e^{\(2x\)} = 1 + 2x + 2x^2 + \frac{8x^3}{6} + \cdots \\)
  * \\(\(e^x\)^2 = \(1 + x + \frac{x^2}{2} + \frac{x^3}{6} + \cdots\)^2 \\)
    * \\(= 1 + 2x + \(\frac{1}{2} + 1 + \frac{1}{2}\) x^2 + \(\frac{1}{6} + \frac{1}{2} + \frac{1}{2} + \frac{1}{6}\) x^3 + \cdots\\)

## Fibonacci Numbers

### Transform 1/\(1-x\)

* \\(\displaystyle \sum\_{n=0}^{\infty} x^n = \frac{1}{1-x}\\)
* Two ways to transfer \\(\frac{1}{\(1-x\)^2}\\)
  * First:
    * \\(\displaystyle \frac{1}{\(1-x\)^2} = \frac{d}{dx} \(\frac{1}{1-x}\) = \frac{d}{dx} \sum_{n=0}^{\infty} x^n = \sum_{n=0}^{\infty} \frac{d}{dx}\(x^n\) = \sum\_{n=1}^{\infty} n \cdot x^{n-1}\\)
    * \\(= 1 \cdot x^0 + 2 \cdot x^1 + 3 \cdot x^2 + \cdots \\)
    * \\(\displaystyle = \sum\_{n=0}^{\infty} \(n+1\) \cdot x^n\\)
  * Second:
    * \\(\displaystyle \(\sum\_{n=0}^{\infty} x^n\)^2 = \(1+x+x^2+x^3+\cdots\)\(1+x+x^2+x^3+\cdots\) \\)
    * \\(= 1 + 2x + 3x^2 + 4x^3 + \cdots\\)
    * \\(\displaystyle = \sum\_{n=0}^{\infty} \(n+1\) \cdot x^n\\)
    * Or we can use the theorem of **Multiply Two Power Series** 
      * \\(\displaystyle \sum_{n=0}^{\infty} \(\sum_{i=0}^{n} a_i b_{n-i}\) x^n\\)
      * In this case, \\(a_i = b_{n-i} = 1\\),
      * So  \\(\displaystyle = \sum_{n=0}^{\infty} \(\sum_{i=0}^{n} 1\) x^n = \sum\_{n=0}^{\infty} \(n+1\) \cdot x^n\\)

### A Formula for the Fibonacci Numbers

* Let's say, \\({a_n}\\) is Fibonacci Sequence, and \\(f\(x\) = \displaystyle \sum_{n=0}^{\infty} a\_n x^n\\)
  * \\( = x + x^2 + 2x^3 + 3x^4 + 5x^5 + \cdots\\)
* Then:
  * \\( x \cdot f\(x\) = x^2 + x^3 + 2x^4 + 3x^5 + 5x^6 + \cdots\\)
  * \\( x^2 \cdot f\(x\) = x^3 + x^4 + 2x^5 + 3x^6 + 5x^7 + \cdots\\)  
* Conclude above equations, we get:
  * \\(f\(x\) - x \cdot f\(x\) - x^2 \cdot f\(x\) = x\\)
* So \\(\displaystyle f\(x\) = \frac{x}{1-x-x^2}\\)
* set \\(\displaystyle \phi = \frac{1+\sqrt{5} }{2}\\), after some calculation we get:
* \\[\begin{aligned} 

    f\(x\) &= \frac{1/{\sqrt{5} } }{1-\(x \cdot \phi\)} + \frac{-1/{\sqrt{5} } }{1-\(x \cdot \(1-\phi\)\)} \

    &= \frac{1}{\sqrt{5} } \cdot \frac{1}{1-\(x \cdot \phi\)} + \frac{-1}{\sqrt{5} } \cdot \frac{1}{1-\(x \cdot \(1-\phi\)\)} \

    &= \frac{1}{\sqrt{5} } \sum_{n=0}^{\infty} \(x \cdot \phi\)^n + \frac{-1}{\sqrt{5} } \sum_{n=0}^{\infty} \(x \cdot \(1 - \phi\)\)^n \

    &= \sum\_{n=0}^{\infty} \(\frac{1}{\sqrt{ 5 } } \cdot \phi^{n} - \frac{1}{\sqrt{ 5 } } \cdot \(1 - \phi\)^{n}\) x^n \

    &= \sum_{n=0}^{\infty} \frac{\phi^n - \(1 - \phi\)^n}{\sqrt{5} } x^n = \sum_{n=0}^{\infty} a\_n x^n

    \end{aligned}\\]

* So, \\(\displaystyle a\_n = \frac{\phi^n - \(1 - \phi\)^n}{\sqrt{5} } \\)

