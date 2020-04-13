# Week 13 - Fundamental Theorem of Calculus

The Fundamental Theorem of Calculus is appropriately named because it establishes a connection between the two branches of calculus: **differential calculus** and **integral calculus**.

## Theorem

* Suppose \\(f: [a, b] \to \mathbb{R}\\) is continuous. Let \\(F\\) be the accumulation function, given by \\[F(x) = \int_a^x f(t) dt \\]. Then \\(F\\) is continuous on \\([a, b]\\), differentiable on (a, b), and \\(F'(x) = f(x)\\).
    * To prove: \\[F'(x) = \frac{F(x+h) - F(x)}{h} \approx \frac{f(x) \cdot h}{h} = f(x)\\]

* Suppose\\(f: [a, b] \to \mathbb{R}\\) is continuous, and \\(F\\) is an antidirevative of \\(f\\). Then \\[\int_a^b f(x) dx = F(b) - F(a)\\]
    * To prove: 
        * We say \\(G(x)\\) is the antidirevative of \\(f\\). Then, \\(G'(x) = f(x)\\), and also, we know \\(f(x) = F'(x)\\).
            * where \\(F(x) = \int_a^x f(t) dt\\) 
        * In the chapter of antiderivative we have proved that, the antiderivative of \\(f\\) should be some function plus a constant, then we can get \\(F(x) = G(x) + C\\)
            * \\(F(x)\\) and \\(G(x)\\) are both the antidirevative functions of \\(f\\).
        * Another fact, we know, is: \\(F(a) = \int_a^a f(t) dt = 0 = G(a) + C\\), so \\(C = -G(a)\\).
        * Then, we get \\(F(x) = G(x) - G(a)\\), so \\(\int_a^x f(t) dt = G(x) - G(a)\\)
        * Let x = b, we get: \\(\int_a^b f(t) dt = G(b) - G(a) = (F(b) - C) - (F(a) - C) = F(b) - F(a)\\)

### Examples

* \\(\int_0^\pi \sin{x} dx\\):
    * \\[\begin{aligned}
        F(x) &= \int_0^\pi \sin{x} dx \\
        F'(x) &= f(x) = \sin{x} \\
        F(x) &= -\cos{x} + C\\
        \int_0^\pi \sin{x} dx &= F(\pi) - F(0) \\
        &= -\cos{\pi} - (-\cos{0}) \\
        &= -(-1) - (-1) = 2
        \end{aligned}\\]
* \\(\int_0^1 x^4\\):
    * \\[\begin{aligned}
        F(x) &= \int_0^1 x^4 \\
        F'(x) &= f(x) = x^4 \\
        F(x) &=  \frac{x^5}{5} + C \\
        \int_0^1 x^4 &= \frac{1^5}{5} - \frac{0^5}{5} \\
        &= \frac{1}{5}
        \end{aligned}\\]

* The area between \\(\sqrt{x}\\) and \\(x^2\\):
    * <img src="https://i.imgur.com/BkQe7cA.jpg" style="width:100px" />

    * \\[\int_0^1 \sqrt{x} - x^2 dx = [\frac{x^{3/2} }{3/2} - \frac{x^3}{3}]_0^1 = (\frac{2}{3} - \frac{1}{3}) - 0 = \frac{1}{3}\\]


* \\(\int_0^t\sqrt{1-x^2}dx\\)
    * <img src="https://i.imgur.com/NOG2L21.jpg" style="width:300px" />
    * Method 1 (use geometrical calculation):
        * Break the area to a circular sector and a triangle.
        * Then, we get:
            * the triangle = \\(\frac{t \cdot \sqrt{1-t^2} }{2}\\)
            * the circular sector = \\(\frac{\arcsin{t} }{2}\\)
        * So \\[\int_0^t\sqrt{1-x^2}dx = \frac{t \cdot \sqrt{1-t^2} }{2} + \frac{\arcsin{t} }{2} \\]
            * The area of the circular is \\(\frac{\theta}{2\pi} \cdot \pi r^2\\), where \\(r = 1\\), so the area is \\(\frac{\theta}{2} = \frac{\arcsin{t} }{2}\\)

    * Method 2 (Use calculus):
        * Let's say \\(F(x) = \frac{x \cdot \sqrt{1-x^2} }{2} + \frac{\arcsin{x} }{2}\\). Then we just need to prove \\(F'(x) = \sqrt{1-x^2}\\)
        * // skip

## The Fundamental Theorem in Physics

* In physics, \\(v(t)\\) = velocity at time \\(t\\), the displacement can written by \\(\int_a^b v(t) dt\\) (Distance from time t=0 to t=b).
* Use Riemann sum, we can get:
    * \\(\text{from } t = 0 \text{ to } t = h\\), \\(D_1 = h \cdot v(0)\\)
    * \\(\text{from } t = h \text{ to } t = 2h\\), \\(D_2 = D_1 + h \cdot v(h)\\)
    * \\(\text{from } t = 2h \text{ to } t = 3h\\), \\(D_3 = D_2 + h \cdot v(2h)\\)
    * keep add this down to \\(t=b\\), and as **h** goes to zero, the Riemann sum will compute \\(\int_a^b v(t) dt\\)
* Summarize this, the accumulation function of velocity is displacement, and the derivative of the displacement is velocity.

## d/da integral f(x) dx from x = a to x =b

* \\(\frac{d}{da} \int_a^bf(x)dx\\)
* We know that \\(\frac{d}{db} \int_a^bf(x)dx = f(b)\\)
    * The rate of the change of the accumulation function is the functions value
* Imagine we are calculating the area from **a** to **b**. When calculating \\(\frac{d}{db}\\), we want to know how does that integral change when wiggling **b**.
* Compare to \\(\frac{d}{da}\\), we want to know how does the integral change when wiggling **a**.
* Let's set the x changes **h**, So the integral's change should be \\(\frac{\int_a^bf(a+h)dx - \int_a^bf(a)dx}{h} \approx \frac{-hf(a)}{h} = -f(a)\\)

