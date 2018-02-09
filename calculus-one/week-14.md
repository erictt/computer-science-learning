# Week 14 - Substitution Rule

[TOC]

## Theorem

* If \\(u = g(x)\\) is a differentiable function whose range is an interval \\(I\\) and \\(f\\) is continuous on \\(I\\), then \\[\int f(g(x))g'(x)dx = \int f(u) du\\]
    * Like reverse the chain rule.
    * It is permissible to operate with **dx** and **du** after integral signs as if they were differentials.

### Examples

* \\(\int\frac{ x }{ \sqrt{ 4-9x^2 } }dx\\)
    * \\[\begin{aligned}
        u &= 4-9x^2, du = -18x \\
        \int\frac{ x }{ \sqrt{ 4-9x^2 } } dx &= -\frac{1}{18} \int \frac{ -18x }{ \sqrt{4-9x^2 } } \\
        &= -\frac{1}{18} \int \frac{ du }{ \sqrt{ u } } \\
        &= -\frac{1}{18} \frac{ u^{ 1/2 } }{ 1/2 } + C \\
        &= -\frac{1}{9} \sqrt{4-9x^2} + C
        \end{aligned}\\]
* \\(\int\frac{ 1 }{ \sqrt{ 4-9x^2 } }dx\\)
    * \\[\begin{aligned}
        \int\frac{1}{ \sqrt{ 4-9x^2 } }dx &= \int\frac{1}{2\sqrt{ 1-(\frac{ 3 }{ 2 } x)^2 } }dx \\
        u &= \frac{3}{2}x, du = \frac{3}{2} \\
         \int\frac{ 1 }{ \sqrt{ 4-9x^2 } } dx &= \frac{1}{3}\int \frac{1}{ \sqrt{ 1-u^2 } }du \\
         &= \frac{1}{3} \arcsin{u} + C \\
         &= \frac{1}{3} \arcsin{\frac{ 3 }{ 2 } x } + C
        \end{aligned}\\]

## Handle the Endpoints
* Normally, we'll do \\[\int_a^bf'(g(x))g'(x)dx = f(g(x))\big]_a^b\\]
* Change the endpoints with **u** \\[\int_a^bf'(g(x))g'(x)dx = f(u)\big]_{g(a)}^{g(b)}\\]

### Example

* \\(\int_{x=0}^2 2x(x^2+1)^3 dx\\)
* set \\(u = x^2+1\\), we get \\(\int_{x=0}^2 u^3 du \\)
* In the normal way, \\(\int_{x=0}^2 u^3 du = \frac{u^4}{4}\big]_{x=0}^2 = \frac{(x^2+1)^4}{4}\big]_{x=0}^2 = \frac{(2^2+1)^4}{4} - \frac{(0^2+1)^4}{4} = 156\\).
* Another way, change the endpoints. \\(\int_{x=0}^2 u^3 du = \int_{u=1}^7 u^3 du = \frac{u^4}{4}\big]_{u=1}^7 = \frac{7^4}{4} - \frac{1^4}{4} = 156\\).

## Do U-substitution More Than Once

* \\(\int -2 \cos{x} \sin{x} \cos{(\cos^2{x}+1)} dx\\)
    * set \\(u = \cos{x}, du = -\sin{x} dx\\)
    * = \\(\int 2u \cos{(u^2+1)} du\\)
    * set \\(v = u^2+1, dv = 2u\\)
    * = \\(\int \cos{v} dv\\)
    * = \\(\sin{v} + C\\)
    * = \\(\sin{u^2+1} + C\\)
    * = \\(\sin{(\cos^2{x}+1)} + C\\)

## Some Tricks

1. use \\(\arctan{x} = \frac{1}{x^2+1}\\)
    * \\(\int \frac{1}{x^2+4x+7} dx = \int \frac{1}{(x+2)^2+3} dx = \int \frac{1}{(x+2)^2+3} dx = \frac{1}{3} \int \frac{1}{(\frac{1}{ \sqrt{ 3 } }(x+2))^2+1} dx\\)
        * set \\(u = \frac{1}{ \sqrt{ 3 } }(x+2), u' = \frac{1}{\sqrt{3} }\\)
        * \\(= \frac{1}{\sqrt{3} } \int \frac{1}{u^2+1} du = \frac{1}{\sqrt{3} }\arctan(u) + C = \frac{1}{\sqrt{3} }\arctan(\frac{1}{ \sqrt{ 3 } }(x+2)) + C\\)
2. rationalizing substitution
    * \\(\int \frac{x}{\sqrt[3]{x+1} }\\)
        * Take the whole denominator as \\(u\\): \\(u = \sqrt[3]{x+1}\\), then \\(x = u^3 - 1\\)
        * \\( = \int \frac{u^3-1}{u}du\\)
3. multiple a reciprocal to make the substitution visible.
    * \\(\int \frac{1}{1+\cos{x} } dx\\)
        * \\(= \int \frac{1}{1+\cos{x} }  \cdot \frac{1-\cos{x} }{1+\cos{x} } dx\\)
        * \\(= \int \frac{1-\cos{x} }{\sin^2{x} } dx = \int \frac{1}{\sin^2{x} } dx - \int \frac{\cos{x} }{\sin^2{x} } dx = - \cot{x} - \int \frac{\cos{x} }{\sin^2{x} } dx \\)
        * set \\(u = \sin{x}, u' = \cos{x}\\)
        * \\(= - \cot{x} - \int \frac{1}{u^2} du = - \cot{x} + \frac{1}{u} + C = - \cot{x} + \csc{x} + C\\)

## Differentiate Integral Functions

* Base on the limit theorem, we know that at point **x**, the change of the integral function should be **f(x)**. But what if the upper endpoint is a function? 
* Like \\(\frac{d}{dx}\int_0^{g(x)} f(x) dx\\).
* Use the chain rule: \\(\frac{d}{dx}f(g(x)) = f'(g(x)) \cdot g'(x)\\) and the Fundamental Theorem: \\(F'(x) = f(x)\\), we get:
    * \\(\frac{d}{dx}\int_0^{g(x)} f(x) dx = F'(g(x)) \cdot g'(x) = f(g(x)) \cdot g'(x)\\)
* For example: \\(\frac{d}{dx}\int_0^{x^2} \sin{t} dt\\), \\(g(x) = x^2\\)
    * \\(\frac{d}{dx} \int_0^{x^2} \sin{x} dt = \sin{x^2} \cdot 2x\\)

## Use The Extreme Value Theorem to Prove Fundamental Theorem

* We want to do two things. First to prove the limit exits, and second, find the value of that derivative: \\[F'(x) = \lim_{h \to 0^{+} } \frac{F(x+h) - F(x)}{h} = f(x)\\]
    * to make it a little easier, we only consider h is positive.
    * \\(F'(x) = \lim_{h \to 0^{+} } \frac{\int_a^{x+h} f(t) dt - \int_a^{x} f(t) dt}{h}\\)
    * = \\(\lim_{h \to 0^{+} } \frac{\int_x^{x+h} f(t) dt}{h}\\)
    * Base on the The Extreme Value Theorem, we know that there must be a: 
        * \\(m(h)\\) = min value of f on interval \\([x, x+h]\\)
        * \\(M(h)\\) = max value of f on interval \\([x, x+h]\\)
        * \\(m(h) \cdot h \le \int_x^{x+h} f(t) dt \le M(h) \cdot h\\)
        * \\(m(h) \le \frac{\int_x^{x+h} f(t) dt}{h} \le M(h)\\)
        * Use the Squeeze Theorem, we know that:
            * \\(\lim_{h \to 0^+}m(h) = f(x) = lim_{h \to 0+}M(h)\\)
            * Then \\(\lim_{h \to 0^+}\frac{\int_x^{x+h} f(t) dt}{h} = f(x)\\)
        * So \\(F'(x) = f(x)\\)

