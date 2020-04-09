# Week 6 - Chain Rule

\[TOC\]

## Differentiation Rules

### The Chain Rule

* Definition
  * If `g` is differentiable at `x` and `f` is differentiable at `g(x)`, then the composite function \\(F = f \circ g\\) defined by \\(F\(x\) = f\(g\(x\)\)\\) is differentiable at `x` and `F'` is given by the product \\[F'\(x\)=f'\(g\(x\)\) \cdot g'\(x\)\\]

### Implicit Differentiation

* This consists of differentiating both sides of the equation with respect to `x` and then solving the resulting equation for `y'`.
* Sample 1: \\(x^2+y^2=25\\), find \\(\frac{d}{dx}y\\), and the tangent to the circle at point `(3, 4)`.
  * ![](../.gitbook/assets/15047908083942%20%281%29.jpg)
    * \\[\begin{aligned}

        \frac{d}{dx}\(x^2+y^2\) &= \frac{d}{dx}\(25\) \

        \frac{d}{dx}\(x^2\) + \frac{d}{dx}\(y^2\) &= 0 \

        2x + 2y \cdot \frac{d}{dx}y &= 0 \

        \frac{d}{dx}y &= -\frac{x}{y}

      \end{aligned}\\]

    * PS: `y` is a function of `x` and using the Chain Rule, we have \\[\frac{d}{dx}\(y^2\) = \frac{d}{dy}\(y^2\) \cdot \frac{d}{dx}y = 2y\frac{d}{dx}y\\]
  * At the point `(3, 4)` we have `x = 3` and `y = 4`, so \\[\frac{d}{dx}y = -\frac{3}{4}\\]
* Sample 2: \\(x^3+y^3=axy\\) \(**folium of Descartes**\)
  * \\(x^3+y^3=6xy\\), find \\(\frac{d}{dx}y\\)
  * ![](../.gitbook/assets/15047911364682.jpg)
  * \\[\begin{aligned}

      3x^2 + 3y^2y' &= 6xy' + 6y \

      x^2 + y^2y' &= 2xy' + 2y \

      \(y^2 - 2x\)y' &= 2y - x^2 \

      y' &= \frac{2y - x^2}{y^2 - 2x}

    \end{aligned}\\]

### Derivatives of Inverse Function

* If `f` is a differentiable function, and `f'` is continuous, and \\(f'\(a\) \ne 0\\), then
  * \\(f^{-1}\(y\)\\) is defined for `y` near `f(a)`, \\(f^{-1}\\) is differentiable near `f(a)`, \\(\(f^{-1}\)'\\) is continuous near `f(a)`, and \\[\(f^{-1}\)'\(y\)=\frac{1}{f'\(f^{-1}\(y\)\)}\\]
* Sample: 

    \\[\begin{aligned}

  ```text
    f(x) &= x^2\ (x>0),\ f'(x) = 2x \\
    f^{-1}(x) &= \sqrt{x} \\
    (f^{-1})'(x) &= \frac{1}{f'(f^{-1}(x))} = \frac{1}{f'(\sqrt{x})} = \frac{1}{2\sqrt{x}}
  \end{aligned}\\]
  ```

### Derivatives of Logarithmic Functions

* Sample 1: 

    \\[\begin{aligned}

  ```text
    f(x) &= e^x,\ f'(x) = e^x \text{(proved in the end of week 5)} \\
    f^{-1}(x) &= \log{x} \\
    (f^{-1})'(x) &= \frac{1}{f'(f^{-1}(x))} = \frac{1}{f'(\log{x})} = \frac{1}{e^{\log{x}}} \\
    &= \frac{1}{x}
  \end{aligned}\\]
  ```

* Sample 2: 

    \\[\begin{aligned}

  ```text
    f(x) &= \log_{b}{x} \\
    f'(x) &= \frac{d}{dx}\frac{\log{x}}{\log{b}} = \frac{1}{\log{b}} \cdot \frac{d}{dx}\log{x} = \frac{1}{\log{b}} \cdot \frac{1}{x} \\
    &= \frac{1}{x \cdot \log{b}}
  \end{aligned}\\]  
  ```

* Sample 3: 

    \\[\begin{aligned}

  ```text
    f(x) &= b^x \\
    &= (e^{\log{b}})^x = e^{\log{b} \cdot x} \\
    f'(x) &= e^{\log{b} \cdot x} \cdot \frac{d}{dx}(\log{b} \cdot x)\ \text{(chain rules)} \\
    &= (e^{\log{b}})^{\cdot x} \cdot \log{b} \\
    &= b^x \cdot \log{b}
  \end{aligned}\\]  
  ```

#### Logarithmic Differentiation

* The calculation of derivatives of complicated functions involving products, quotients, or powers can often be simplified by taking logarithms.
* Sample: Differentiate \\(f\(x\)=\frac{\(1+x^2\)^5 \cdot \(1+x^3\)^8}{\(1+x^4\)^7}\\), 

    \\[\begin{aligned}

  ```text
    y &= \frac{(1+x^2)^5 \cdot (1+x^3)^8}{(1+x^4)^7} \\
    \log{y} &= \log{\frac{(1+x^2)^5 \cdot (1+x^3)^8}{(1+x^4)^7}} \\
    \frac{d}{dx}\log{y} &= \frac{d}{dx}\log{\frac{(1+x^2)^5 \cdot (1+x^3)^8}{(1+x^4)^7}} \\
    \frac{d}{dx}\log{y} &= \frac{d}{dx}(5\log{(1+x^2)} + 8\log{(1+x^3)} - 7\log{(1+x^4)}) \\
    \frac{1}{y} \cdot \frac{d}{dx}y &= 5\frac{d}{dx}\log{(1+x^2)} + 8\frac{d}{dx}\log{(1+x^3)} - 7\frac{d}{dx}\log{(1+x^4)} \\
    \frac{1}{y} \cdot \frac{d}{dx}y &= 5\frac{2x}{1+x^2} + 8\frac{3x^2}{1+x^3} - 7\frac{4x^3}{1+x^4} \\
    \frac{d}{dx}y &= (5\frac{2x}{1+x^2} + 8\frac{3x^2}{1+x^3} - 7\frac{4x^3}{1+x^4}) \cdot \frac{(1+x^2)^5 \cdot (1+x^3)^5}{(1+x^4)^7}\\
  \end{aligned}\\]
  ```

## Justify the Derivative Rules

### The Power Rule

* \\(\frac{d}{dx}x^{-n}=-nx^{-n-1}\\)
  * Before, the power rule only apply for the real numbers, this formula apply for all rational numbers.
* Use chain rules to find the derivative of \\(f\(x\)=\frac{1}{x^n}\\) : 
  * First use the limit theorem to find the derivative of \\(f\(x\)=\frac{1}{x}\\): 

    \\[\begin{aligned}

      \frac{d}{dx}\frac{1}{x} &= \lim\_{h \to 0}\frac{\frac{1}{x+h}-\frac{1}{x}}{h} \

      &= \lim\_{h \to 0}\frac{\frac{x-h-x}{x\(x+h\)}}{h} \

      &= \lim\_{h \to 0}\frac{\frac{-h}{x\(x+h\)}}{h} \

      &= \lim\_{h \to 0}\frac{-1}{x\(x+h\)} \

      &= -\frac{1}{x^2} \

    ```text
    \end{aligned}\\]
    ```

  * Then use chain rules to find the derivative of \\(f\(x\)=\frac{1}{x^n}\\): 

      \\[\begin{aligned}

      \frac{d}{dx}\frac{1}{x^n} &= - \frac{1}{\(x^n\)^2} \cdot \frac{d}{dx}x^n \

      &= - \frac{1}{\(x^n\)^2} \cdot nx^{n-1} \

      &= - nx^{-2n+n-1} \

      &= - nx^{-n-1}

    \end{aligned}\\]
* Sample: Differentiate \\(y=x^{\sqrt{2}}, \(x&gt;0\)\\), \\[\begin{aligned}

  ```text
    \log{y} &= \log{x^{\sqrt{2}}} \\
    \frac{d}{dx}\log{y} &= \frac{d}{dx}\log{x^{\sqrt{2}}} \\
    \frac{1}{y} \cdot \frac{d}{dx}y &= \frac{d}{dx}\sqrt{2}\log{x} \\
    \frac{1}{x^{\sqrt{2}}} \cdot \frac{d}{dx}y &= \sqrt{2} \cdot \frac{1}{x} \\
    \frac{d}{dx}y &= \sqrt{2} \cdot \frac{1}{x} \cdot x^{\sqrt{2}} \\
    \frac{d}{dx}y &= \sqrt{2} \cdot x^{\sqrt{2}-1} \\
  \end{aligned}\\]
  ```

### The Product Rule

* Use logarithms to prove: 

    \\[\begin{aligned}

  ```text
    f(x) &> 0,\ g(x) > 0, \\
    \log(f(x)g(x)) &= \log(f(x)) + \log(g(x)) \\
    \frac{d}{dx} \log(f(x)g(x)) &= \frac{d}{dx} \log(f(x)) + \frac{d}{dx} \log(g(x)) \\
    \frac{1}{f(x)g(x)} \cdot \frac{d}{dx}f(x)g(x) &= \frac{1}{f(x)} \cdot \frac{d}{dx}f(x) + \frac{1}{g(x)} \cdot \frac{d}{dx}g(x) \\
    \frac{d}{dx}f(x)g(x) &= g(x) \cdot \frac{d}{dx}f(x) + f(x) \cdot \frac{d}{dx}g(x)
  \end{aligned}\\]
  ```

### The Quotient Rule

* First we need to calculate the derivative of \\(\frac{1}{g\(x\)}\\) : \\[\begin{aligned} \text{we have proved this:} f\(x\) &= \frac{1}{x}, f'\(x\) = -\frac{1}{x^2} \ so, \frac{d}{dx}\frac{1}{g\(x\)} &= - \frac{1}{\(g\(x\)\)^2} \cdot g'\(x\) \end{aligned}\\]
* Then: \\[\begin{aligned} \frac{d}{dx}\frac{f\(x\)}{g\(x\)} &= \frac{d}{dx}\(f\(x\) \cdot \frac{1}{g\(x\)}\) \ &= f'\(x\) \cdot \frac{1}{g\(x\)} + f\(x\) \cdot \(- \frac{1}{\(g\(x\)\)^2} \cdot g'\(x\)\) \ &= \frac{f'\(x\) \cdot g\(x\) - f\(x\) \cdot g'\(x\)}{\(g\(x\)\)^2} \ \end{aligned}\\]

### Proof the Chain Rule

* **Recall** If `y = f(x)` and `x` changes from `a` to `a + ∆x`, we define the increment of `y` as 

    \\[\Delta y = f\(a+\Delta x\)-f\(a\)\\]. 

    According to the definition of a derivative, we have 

    \\[\lim\_{\Delta x \to o}\frac{\Delta y}{\Delta x}=f'\(a\)\\]. So if we denote by \\(\epsilon\\) the difference between the difference quotient and the derivative, we obtain 

    \\[\lim_{\Delta x \to 0}\epsilon = \lim_{\Delta x \to 0}\(\frac{\Delta y}{\Delta x}-f'\(a\)\) = f'\(a\)-f'\(a\) = 0\\]. 

    But 

    \\[\epsilon = \frac{\Delta y}{\Delta x}-f'\(a\) \Rightarrow \Delta y = f'\(a\)\Delta x + \epsilon \Delta x \\]. 

    If we define \\(\epsilon\\) to be 0 when `∆x = 0`, then \\(\epsilon\\) become a continuous function of `∆x`. Thus, for a differentiable function `f`, we can write 

    \\[\Delta y = f'\(a\)\Delta x + \epsilon \Delta x \text{ where } \epsilon \to 0 as \Delta x \to 0\\]

    and \\(\epsilon\\) is a continuous function of `∆x`. This property of differentiable functions is what enables us to prove the Chain Rule.

* **Now to Prove**: Suppose `u=g(x)` is differentiable at `a` and `y=f(u)` is differentiable at `b=g(a)`, If `∆x` is an increment in `x` and `∆u` and   `∆y` are corresponding increments in `u` and `y`, then we can use last equation to write 

    \\[\Delta u = g'\(a\)\Delta x + \epsilon\_1\Delta x = \(g'\(a\) + \epsilon\_1\)\Delta x\\]

    where \\(\epsilon\_1 \to 0\\) as \\(\Delta x \to 0\\). 

    Similarly 

    \\[\Delta y = f'\(b\)\Delta u + \epsilon\_2\Delta u = \(f'\(b\) + \epsilon\_2\)\Delta u\\] 

    where \\(\epsilon\_2 \to 0\\) as \\(\Delta x \to 0\\). If we now substitute the expression for `∆u`, we get 

    \\[\Delta y = \[f'\(b\) + \epsilon\_2\]\[g'\(a\) + \epsilon\_1\]\Delta x\\], so \\[\frac{\Delta y}{\Delta x} = \[f'\(b\) + \epsilon\_2\]\[g'\(a\) + \epsilon\_1\]\\] 

    As \\(\Delta x \to 0\\). So both \\(\epsilon\_2 \to 0\\) and \\(\epsilon\_1 \to 0\\) as \\(\Delta x \to 0\\). Therefore 

    \\[\begin{aligned}

  ```text
    \frac{dy}{dx} &= \lim_{\Delta x \to 0}\frac{\Delta y}{\Delta x} =   \lim_{\Delta x \to 0}[f'(b) + \epsilon_2][g'(a) + \epsilon_1] \\
    &= f'(b)g'(a) = f'(g(a))g'(a)
      \end{aligned}\\]. 
  ```

    This prove the **Chain Rule**.

