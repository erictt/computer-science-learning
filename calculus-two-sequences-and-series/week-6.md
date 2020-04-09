# Week 6 - Taylor Series

\[TOC\]

## Brief

* This week talks about how to transfer a function \\(f\(x\)\\) to a power series.

## Better Than Linear Approximation

* In calculus one, we've learned \\(f\(x\) \approx f\(a\) + f'\(a\) \(x - a\)\\) to approximately get value of \\(f\(x\)\\).
* This time we use another function \\(g\(x\) = f\(a\) + f'\(a\) \cdot \(x - a\) + \frac{f''\(a\)}{2} \cdot \(x -a\)^2 + \frac{f'''\(a\)}{6} \cdot \(x - a\)^3\\)
* With some calculation, we can get:
  * \\(g\(a\) = f\(a\)\\)
  * \\(g'\(a\) = f'\(a\)\\)
  * \\(g''\(a\) = f''\(a\) + f''\(a\) \(x - a\)\\)
  * \\(g'''\(a\) = f'''\(a\) + f'''\(a\) \(x - a\)\\)
* So, \\(g\(x\)\\) is a better approximation for \\(f\(x\)\\).
* Example: \\(f\(x\) = \sin\(x\)\\)
  * \\(f\(x\) = \sin\(x\), f\(0\) = 0\\)
  * \\(f\(x\) = \cos\(x\), f'\(0\) = 1\\)
  * \\(f\(x\) = - \sin\(x\), f''\(0\) = 0\\)
  * \\(f\(x\) = - \cos\(x\), f'''\(0\) = -1\\)
  * \\(g\(x\) = 0 + 1 \cdot x + \frac{0}{2} \cdot \(x\)^2 + \frac{-1}{6}\(x\)^3 = x - \frac{x^3}{6}\\)
  * \\(f\(\frac{1}{2}\) = \sin\(\frac{1}{2}\) \approx 0.4794\\)
  * \\(g\(\frac{1}{2}\) = \frac{1}{2} - \frac{\(1/2\)^3}{6} \approx 0.4792\\)

## Taylor Theorem

### the Taylor Series for f Around Zero\(Maclaurin Series\)

* Suppose \\(f\(x\) = \sum\_{n=0}^{\infty} a\_n x^n, \|x\| &lt; R\\)
  * \\(= a\_0 + a\_1 x + a\_2 x^2 + a\_3 x^3 + \cdots\\)
* Then, \\(f\(0\) = a\_0 + a\_1 \cdot 0 + a\_2 \cdot 0 + a\_3 \cdot 0 + \cdots = a\_0\\)
* \\(f'\(x\) = \sum\_{n=1}^{\infty} a\_n \cdot n \cdot x^{n-1}, \|x\| &lt; R\\)
  * \\(= a\_1 + a\_2 \cdot 2 \cdot x + \cdots\\)
  * =&gt; \\(f'\(0\) = a\_1\\)
* \\(f''\(x\) = \sum\_{n=2}^{\infty} a\_n \cdot n \cdot \(n-1\) \cdot x^{n-2}, \|x\| &lt; R\\)
  * \\(= a\_2 \cdot 2 \cdot 1 \cdot 1  + a\_3 \cdot 3 \cdot 2 \cdot x + \cdots\\)
  * =&gt; \\(f''\(0\) = a\_2 \cdot 2\\)
  * =&gt; \\(a\_2 = \frac{f''\(0\)}{2}\\)
* \\(a\_3 = \frac{f'''\(0\)}{3!}\\)
* \\(\cdots\\)
* So, Assume \\(f\(x\) = \sum\_{n=0}^{\infty} a\_n x^n, \|x\| &lt; R\\)
  * Then \\(a\_n = \frac{f^{n}\(0\)}{n!}\\)

#### Definition

* If \\(\displaystyle f\(x\) = \sum\_{n=0}^{\infty} a\_n x^n, \text{where} \|x\| &lt; R\\)
* Then \\(\displaystyle f\(x\) = \sum\_{n=0}^{\infty} \frac{f^{\(n\)}\(0\)}{n!} \cdot x^n\\)
  * This series is called Taylor series of the function **f** at **0** or **Maclaurin series**.

### The Taylor Series for f Centered Around a

* \\(\displaystyle f\(x\) = \sum\_{n=0}^{\infty} c\_n \(x-a\)^n\\)
  * \\(c\_0 + c\_1 \(x - a\) + c\_2 \(x - a\)^2 + \cdots\\)
  * \\(f\(a\) = c\_0\\)
  * \\(f'\(a\) = c\_1\\)
  * ...
* To summary this:
  * The Taylor Series for f Centered Around a is \\[f\(x\) = \sum\_{n=0}^{\infty} \frac{f^{\(n\)}\(a\)}{n!} \cdot \(x-a\)^n\\]
* Example \\(f\(x\) = \sin\(x\)\\)
  * The Taylor Series for \\(\sin\\) around 0 is \\[f\(x\) = \sum\_{n=0}^{\infty} \frac{\(-1\)^n}{\(2n+1\)!} \cdot x^{2n+1}\\]
* Quiz 6: Let \\(f\(x\) = \cos\(x^5\)\\). By considering the Taylor series for \\(f\\) around 0, compute \\(f^{\(90\)}\(0\)\\).
  * The Taylor Series for \\(\cos\\) around 0 is \\[f\(x\) = \sum\_{n=0}^{\infty} \frac{\(-1\)^n}{\(2n\)!} \cdot x^{2n}\\]
  * \\(f\(x\) = 1 - \frac{x^2}{2!} + \frac{x^4}{4!} - \frac{x^6}{6!} + \cdots + \frac{x^{16} }{16!} - \frac{x^{18} }{18!} + \cdots\\)
  * \\(f\(x^5\) = 1 - \frac{x^{10} }{2!} + \frac{x^{20} }{4!} - \frac{x^{30} }{6!} + \cdots + \frac{x^{80} }{16!} - \frac{x^{90} }{18!} + \cdots\\)
  * So we just need to differentiate term \\(\frac{d^{90} }{dx^{90} } \(- \frac{x^{90} }{18!}\)\\) which \\(= - \frac{90! \cdot x^0}{18!} = - \frac{90!}{18!}\\)

### Taylor's Theorem

* Suppose \\(f: \mathbb{R} \to \mathbb{R}\\) is infinitely differentiable.
  * \\[f\(x\) = \(\sum\_{n=0}^{N} \frac{f^{\(n\)}\(0\)}{n!} \cdot x^n\) + R\_N{x}\\]. **R** stands for remainder.
* Then \\[R\_N\(x\) = \frac{f^{\(N+1\)}\(z\)}{\(N+1\)!} x^{N+1}\\] for some **z** between **x** and **0**.

#### Usage

* Use Taylor's Theorem to prove \\[\sin{x} = \sum\_{n=0}^{\infty}\frac{\(-1\)^n}{\(2n+1\)!} \cdot x^{2n+1}\\]
* \\(f\(x\) = \sin x\\)
* With Taylor's Theorem, \\[\begin{aligned}

    \sin{x} &- \sum\_{n=0}^{N} \frac{f^{\(n\)}\(0\)}{n!} \cdot x^n = R\_N\(x\) \ 

    R\_N\(x\) &= \frac{f^{\(N+1\)}\(z\)}{\(N+1\)!} x^{N+1}

    \end{aligned}\\]

* We know: \\(f^{\(N+1\)}\(x\) = \pm \sin x  \text{or}  \pm \cos x \\), so \\(f^{\(N+1\)}\(x\) \le 1\\)
* Then, \\(R\_N\(x\) \le \frac{1}{\(N+1\)!} x^{N+1}\\)
* So, if \\(\displaystyle \lim_{N \to \infty}\|\frac{x^{N+1} }{\(N+1\)!}\| = 0\\), \\(\displaystyle \lim_{N \to \infty}\|R\_N\(x\)\| = 0\\). 
  * Then \\(\displaystyle \sin{x} = \sum_{n=0}^{\infty} \frac{f^{\(n\)}\(0\)}{n!} \cdot x^n = \sum_{n=0}^{\infty} \frac{\(-1\)^n}{\(2n+1\)!} \cdot x^{\(2n+1\)}\\)
* So we need to prove \\(\displaystyle \lim\_{N \to \infty}\|\frac{x^{N+1} }{\(N+1\)!}\| = 0\\). 
  * And if \\(\displaystyle \sum\_{N=0}^{\infty}\|\frac{x^{N+1} }{\(N+1\)!}\|\\) converge, then the limit must be **0**.
* Now, use ratio test to prove the series converge:
  * \\(\displaystyle \lim_{N \to \infty } \frac{x^{N+2}/{\(N+2\)!} } { x^{N+1}/{\(N+1\)!} } = \lim_{N \to \infty} \frac{x \cdot \(N+1\)! } { \(N+2\)! } = \lim\_{N \to \infty} \frac{x } { N+2 } = 0 \\)

#### the Radius of Convergence of 1/\(1+x^2\)

* \\(\displaystyle \frac{1}{1-x} = \sum\_{n=0}^{\infty} x^n\\), if \\(\|x\| &lt; 1\\).
  * the radius of convergence is 1.
* \\(\displaystyle \frac{1}{1+x} = \sum_{n=0}^{\infty} \(-x\)^n = \sum_{n=0}^{\infty} \(-1\)^n x^n\\), if \\(\|x\| &lt; 1\\).
  * the radius of convergence is 1.
* \\(\displaystyle \frac{1}{1+x^2} = \sum_{n=0}^{\infty} \(-1\)^n\(x^2\)^n = \sum_{n=0}^{\infty} \(-1\)^n x^{2n}\\), if \\(\|x\| &lt; 1\\).
  * the radius of convergence is 1.
* The question is why the radius of convergence of function \\(\frac{1}{1+x^2}\\) at 0 is 1, and at 1 is \\(\sqrt{2}\\)
  * We can understand that the radius of convergence of \\(\frac{1}{1-x}\\) at 0 is 1, because \\(x \ne 1\\).
  * But \\(\sin x\\) is very similar to \\(\frac{1}{1+x^2}\\), and the radius of convergence of \\(\sin x\\) at 0 is \\(\infty\\).
    * \\(\displaystyle \sin x = \sum\_{n=0}^{\infty} \frac{\(-1\)^n}{\(2n+1\)!} x^{2n+1}\\) for all **x**.
* The answer is, if we set \\(i = \sqrt{-1}\\), then \\[f\(i\) = \frac{1}{1+\(i\)^2} = \frac{1}{1+\(-1\)}\\], which doesn't exist.
* So there is a bad point\(间断点\) where the function is undefined. It's just the bad point isn't a real point.\(这个间断点不在实轴上，是个虚数\) 
* The bad point in the complex plane is messing up the radius of convergence even along the real line. So complex numbers is very important, even in the thery of real value Taylor Series.\(这个在复平面上的间断点限制了收敛半径，所以复数在实数域的泰勒展开式中同样重要。\)
* Additional evidence is \\[e^{ix} = \cos x + i \cdot \sin x.  \(i = \sqrt{-1}\)\\] . Interpret this as a statement about power series: \\[

    \sum_{n=0}^{\infty} \frac{\(ix\)^n}{n!} = \sum_{n=0}^{\infty} \frac{\(-1\)^n x^{2n} }{2n!} +     i \cdot \sum\_{n=0}^{\infty} \frac{\(-1\)^n x^{2n+1} }{\(2n+1\)!} \\]. Set \\(x = \pi\\): \\[e^{i \pi} = \cos \pi + i \cdot \sin \pi = -1\\]

* Taylor series are the first step into the theory of complex analysis\(复分析理论\).

#### Mean Value Theorem

* \\(f: \[a, b\] \to \mathbb{R} \text{ continuous}\\)
  * and, on \\(\(a, b\)\\) differentiable,
* Then, there is a point \\(c \in \(a, b\)\\), so that \\[f'\(c\) = \frac{f\(b\) - f\(a\)}{b - a}\\]
* replace **c** and **b** with **z** and **x**, we get:
  * \\(f'\(z\) = \frac{f\(x\) - f\(a\)}{x - a}\\)
  * \\(f\(x\) = f\(a\) + R\_0\(x\), \text{where} R\_0\(x\) = \frac{f'\(z\)}{1!} \cdot \(x-a\)^1\\), and **z** is between **x** and **a**.
  * It is the Taylor Theorem when \\(N = 0\\) 
* Example \\(f\(t\) = \text{your position at time t sec}\\)
  * \\(f\(0\) = 0\\), \\(f'\(0\) = 0\\), \\(f''\(t\) \le 250 \frac{m}{s^2}\\)
  * Question: How big can \\(f\(60\)\\) be?
  * Use Taylor Theorem, we get:
    * \\(f\(t\) = f\(0\) + f'\(0\) \cdot \(t - 0\) + R\_1\(t\)\\), \\(R\_1\(t\) = \frac{f''\(z\)}{2!} \cdot \(t - 0\)^2\\)
    * \\(\|R\_1\(t\)\| \le \frac{250}{2!} \cdot t^2\\)
  * So \\(f\(t\) \le f\(0\) + f'\(0\) \cdot t + \frac{250}{2!} \cdot t^2 = 125 t^2\\)
  * \\(f\(60\) \le 125 \cdot 60^2 = 450000 \text{m} = 450 \text{km}\\)

## Practice

### Uniform Convergence

#### Approximate cos x when x is near zero

* Goal: Find polynomial \\(p\(x\)\\) so that \\(\|p\(x\) - \cos x\| &lt; \frac{1}{100}\\), where \\(x \in \[-1, 1\]\\)
* \\(\displaystyle \cos x = \sum\_{n=0}^{\infty}\frac{\(-1\)^n}{\(2n\)!} \cdot x^{2n}\\)
* \\(\displaystyle \cos x - \sum\_{n=0}^{N}\frac{f^{\(n\)}\(0\)}{n!} \cdot x^{n} = R\_N\(x\)\\)
* \\(\displaystyle R\_N\(x\) = \frac{f^{\(N+1\)}\(z\)}{\(N+1\)!} \cdot x^{N+1}\\), \\(z \in \(0, x\)\\)
* \\(x \in \[-1, 1\]\\), then \\(\|x^{N+1}\| \le 1\\)
  * =&gt; \\( R\_N\(x\) \le \frac{f^{\(N+1\)}\(z\)}{\(N+1\)!} \\)
* \\(f^{\(N+1\)}\(z\) = \pm \sin z \text{or} \pm \cos z \le 1\\)
  * =&gt; \\( R\_N\(x\) \le \frac{1}{\(N+1\)!} \\)
* We want \\(\frac{1}{\(N+1\)!} &lt; \frac{1}{100}\\) and \\(\frac{1}{5!} = \frac{1}{120}\\)
  * =&gt; \\(N = 4\\)
* \\(\cos x = 1 - \frac{x^2}{2} + \frac{x^4}{24} -\frac{x^6}{720} + \cdots\\)
  * There is no x to the 5th term, so we can make \\(N = 5\\)
* \\(\cos x = 1 - \frac{x^2}{2} + \frac{x^4}{24} -R\_5\\)
  * =&gt; \\( R\_5\(x\) \le \frac{1}{\(5+1\)!} = \frac{1}{6!} = \frac{1}{720} &lt; \frac{1}{100} \\)
* So \\(p\(x\) = 1 - \frac{x^2}{2} + \frac{x^4}{24} \approx \cos x\\)

### Limits

* \\(\displaystyle \lim\_{x \to 0} \frac{\sin x}{x}\\)
* use Taylor Series, we know:
  * \\(\sin x = x - \frac{x^3}{6} + \frac{x^5}{5!} - \cdots\\)
  * \\(\sin x \approx x + \text{higher order terms}\\)
* then \\(\displaystyle \lim_{x \to 0} \frac{\sin x}{x} = \lim_{x \to 0} \frac{x + \text{higher order terms} }{x} = 1 + \lim\_{x \to 0} \frac{\text{higher order terms} }{x}\\)

### Real Analytic Function

* Theorem:
  * The function \\(f\\) is **real analytic** at **a** if there is some \\(R &gt; 0\\),
  * So that \\[f\(x\) = \sum\_{n = 0}^{\infty} \frac{f^{\(n\)}\(a\)}{n!}\(x-a\)^n  \text{when } \|x-a\|&lt;R\\]
* Real Analytic Functions ∈ Infinitely Differentiable Functions\(Smooth Functions\(\\(C^{\infty}\\)\)\) ∈ Differentiable Functions ∈ Continuous Functions ∈ All Functions

#### Holograms

* A little bit of a hologram records everything in the function.
* For example \\(\sin x\\). 
  * Only look the points near 0, we know:
    * \\(f\(0\) = 0\\)
    * \\(f'\(0\) = 1\\)
    * \\(f''\(0\) = 0\\)
    * \\(f'''\(0\) = -1\\)
    * We can calculate all of the derivatives of the function by just looking the area near 0.
  * And use Taylor Series, we can get \\(\displaystyle f\(x\) = \sum\_{n = 0}^{\infty} \frac{f{\(n\)}\(0\)}{n!} x^n\\)

## Important Taylor Series and Their Radii of Convergence

* \\[\frac{1}{1-x} = \sum\_{n=0}^{\infty} x^n = 1 + x + x^2 + x^3 + \cdots, R = 1\\]
* \\[e^x = \sum\_{n=0}^{\infty} \frac{x^n}{n!} = 1 + \frac{x}{1!} + \frac{x^2}{2!} + \frac{x^3}{3!} + \cdots, R = \infty\\]
* \\[\sin x = \sum\_{n=0}^{\infty} \frac{\(-1\)^n x^{2n+1} }{\(2n+1\)!} = x - \frac{x^3}{3!} + \frac{x^5}{5!} - \frac{x^7}{7!} + \cdots, R = \infty\\]
* \\[\cos x = \sum\_{n=0}^{\infty} \frac{\(-1\)^n x^{2n} }{\(2n\)!} = 1 - \frac{x^2}{2!} + \frac{x^4}{4!} - \frac{x^6}{6!} + \cdots, R = \infty\\]
* \\[\tan^{-1} x = \sum\_{n=0}^{\infty} \frac{\(-1\)^n x^{2n+1} }{2n+1} = x - \frac{x^3}{3} + \frac{x^5}{5} - \frac{x^7}{7} + \cdots, R = 1\\]
* \\[\ln \(1 + x\) = \sum\_{n=0}^{\infty} \frac{\(-1\)^{n-1} x^{n} }{n} = x - \frac{x^2}{2} + \frac{x^3}{3} - \frac{x^4}{4} + \cdots, R = 1\\]
* \\[\(1 - x\)^k = \sum\_{n=0}^{\infty} \(n {k}\)x^{n} = 1 + kx + \frac{k\(k-1\)}{2!}x^2 + \frac{k\(k-1\)\(k-2\)}{3!}x^3 + \cdots, R = 1\\]

