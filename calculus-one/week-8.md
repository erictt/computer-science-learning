# Week 8 - Derivatives in the Real World

\[TOC\]

## L'Hôpital's Rule

* Definition:
  * Let `f` and `g` be functions differentiable near `a`. If \\[\displaystyle\lim_{x \to a}f\(x\) = \lim_{x \to a}g\(x\) = 0\\] or that \\[\displaystyle\lim_{x \to a}f\(x\) = \pm\infty and \lim_{x \to a}g\(x\) = \pm\infty\\], and \\(\displaystyle\lim_{x \to a}\frac{f'\(x\)}{g'\(x\)}\\) exists, and \\(g'\(x\) \ne 0\\) for all `x` near `a`, then \\[\lim_{x \to a}\frac{f\(x\)}{g\(x\)} = \lim\_{x \to a}\frac{f'\(x\)}{g'\(x\)}\\].
    * \(In other words, we have an indeterminate form of type \\(0/0\\) or \\(\infty/\infty\\)\).
* Extensions:
  * \\(0 \cdot \infty = \frac{\infty}{1/0} = \frac{0}{1/\infty}\\)
  * \\(1^{\infty} = e^{\infty \cdot \log{1}}\\)
  * \\(\infty^0 = e^{0 \cdot \log\infty}\\)
  * \\(0^0 = e^{0 \cdot \log{0}}\\)
  * \\(\infty - \infty = \frac{\frac{1}{\infty} - \frac{1}{\infty}}{\frac{1}{\infty \cdot \infty}}\\)
* Samples 1:
  * \\[\begin{aligned}

      \displaystyle\lim\_{x \to \infty}\(1+\frac{1}{x}\)^x 

      &= e^{\log{\displaystyle\lim\_{x \to \infty}\(1+\frac{1}{x}\)^x}} \

      &= e^{\displaystyle \lim\_{x \to \infty}\log{\(1+\frac{1}{x}\)^x}} \

      &= e^{\displaystyle \lim\_{x \to \infty}x \log{\(1+\frac{1}{x}\)}} \

      &= e^{\displaystyle \lim\_{x \to \infty}\frac{\log{\(1+\frac{1}{x}\)}}{\frac{1}{x}}}

      \end{aligned}\\]

  * use **L'Hôpital's Rule** : 

    \\[\begin{aligned}

      \lim\_{x \to \infty}\(1+\frac{1}{x}\)^x 

      &= e^{\displaystyle\lim\_{x \to \infty}\frac{\frac{1}{1+\frac{1}{x}} \cdot -\frac{1}{x^2}}{-\frac{1}{x^2}}} \

      &= e^{\displaystyle\lim\_{x \to \infty}\frac{1}{1+\frac{1}{x}}} \

      &= e^{1} = e

    \end{aligned}\\]
* Samples 2:
  * \\[\begin{aligned}

      \lim_{x \to \infty}\(\sqrt{x^2+x}-x\) &= \lim_{x \to \infty}\(x \cdot \(\sqrt{1+\frac{1}{x}}-1\)\) \

      &= \lim\_{x \to \infty}\frac{\sqrt{1+\frac{1}{x}}-1}{\frac{1}{x}} \

      &= \lim\_{x \to \infty}\frac{\frac{1}{2} \cdot \(1+\frac{1}{x}\)^{-\frac{1}{2}} \cdot -\frac{1}{x^2}}{-\frac{1}{x^2}} \

      &= \lim\_{x \to \infty}\frac{1}{2\sqrt{1+\frac{1}{x}}} \

      &= \frac{1}{2}

    \end{aligned}\\]
* Some situations the L'Hôptial's Rule doesn't apply
  * Samples: \\(\displaystyle\lim\_{x \to \infty}\frac{x+\sin{x}}{x}\\)
    * apply the L'Hôptial's Rule, we get:
      * \\(\displaystyle\lim_{x \to \infty}\frac{x+\sin{x}}{x} = \lim_{x \to \infty}\cos{x} \\) DNE\(does not exist\)
    * But this limit is equal to the limit of the derivative over the derivative, provided this limit exists. And this limit doesn't exist in this case. So we can't use the rule here.
    * The best way to solve this is using algebraic manipulation to calculate:
      * \\(\displaystyle\lim_{x \to \infty}\frac{x+\sin{x}}{x} = 1+\lim_{x \to \infty}\frac{\sin{x}}{x} = 1+0 = 1\\)

## How can derivatives help me to understand rates of change in the real world?

* A light is placed on the ground 30 ft from a building. A man 6 ft tall walks from the light toward the building at the rate of 5 ft/sec. Find the rate at which the length of his shadow is changing when he is 15 ft from the building.
  * ![](../.gitbook/assets/15094341802303.jpg)
  * [Rate of shadow in the wall of a building](https://www.mathalino.com/reviewer/differential-calculus/17-18-rate-shadow-wall-building)

