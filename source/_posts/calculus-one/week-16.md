# Week 16 - Applications of Integration

## Area between Curves

* The area between the curves $y=f(x)$ and $y=g(x)$ and between $x=a$ and $x=b$ is $$A=\int_a^b |f(x) - g(x)| dx$$
* For example, $f(x) = x^2, g(x) = 1, a = -1, b = 1$
    * <img src="https://i.imgur.com/47Gd8Aw.jpg" style="width:400px" />
    * we can simply get the integral function $\int_{-1}^{1} 1 - x^2 \ dx$
* Some regions are best treated by regarding **x** as a function of **y**. If a region is bounded by curves with equations $x=f(y)$, $x=g(y)$, $y=c$, and $y=c$, where **f** and **g** are continuous and $f(y) \ge g(y)$ for $c \le y \le d$, then its area is $$A=\int_c^d |f(y) - g(y)| dy$$
* For example, $f(x)=\sqrt{x}, g(x) = \sqrt{2x-1}, a = 0, b = 1$
    * <img src="https://i.imgur.com/23ls4gq.jpg" style="width:150px" />
    * If treat them as functions of **x**, we need to split the area to two parts.
    * So we rewrite the functions to $f(y) = y^2, g(y) = \frac{y^2 + 1}{2}, c = 0, d = 1$
    * <img src="https://i.imgur.com/hLcnN0Z.jpg" style="width:400px" />

## Volumes

### Sphere's Volume 

* <img src="https://i.imgur.com/tvybTNG.jpg" style="width:200px" />
* The cross-sectional area is $$A(x) = \pi y^2 = \pi(r^2 - x^2)$$
* Using the definition of volume with $a = -r$ and $b = r$, we have $$\begin{aligned}
    V &= \int_{-r}^{r}A(x) dx = \int_{-r}^{r} \pi(r^2 - x^2) dx \\
    &= 2\pi \int_0^r(r^2 - x^2)\ dx \\
    &= 2\pi \big[r^2x - \frac{x^3}{3}\big]_0^r = 2\pi(r^3-\frac{r^3}{3}) \\
    &= \frac{4}{3}\pi r^3
    \end{aligned}$$

### Use Washer Method

* The region $\mathscr{R}$ enclosed by the curves $f(x) = x, g(x) = x^2$ is rotated about the x-axis. Find the volume of the resulting solid.
* <img src="https://i.imgur.com/nPAJljm.jpg" style="width:500px" />
* The curves $y = x \text{ and } y = x^2$ intersect at the points **(0, 0)** and **(1, 1)**. The region between them, the solid of rotation, and a cross-section perpendicular to the x-axis are shown above. A cross-section in the plane $P_x$ has the shape of a **washer** (an annular ring) with inner radius $x^2$ and outer radius $x$, so we find the cross-sectional area by subtracting the area of the inner circle from the area of the outer circle: $$A(x) = \pi x^2 - \pi (x^2)^2 = \pi(x^2 - x^4)$$
* Therefore we have $$V = \int_0^1 A(x)dx = \int_0^1 \pi(x^2 - x^4) \ dx  = \pi \big[\frac{x^3}{3} - \frac{x^5}{5}\big]_0^1 = \frac{2\pi}{15}$$

### Use Shells Method

* To face a situation like below. If we slice perpendicular to the y-axis, we get a washer. But to compute the inner radius and the outer radius of the washer, we’d have to solve the cubic equation $f(x)$ for x in terms of y; that’s not easy.
    * <img src="https://i.imgur.com/u0ux56t.jpg" style="width:400px" />
* For this situation, we use the **method of cylindrical shells**.
* Instead of slicing the perpendicular to the x-axis:
    * <img src="https://i.imgur.com/eSeBHid.jpg" style="width:200px" />
* Then, flatten as below:
    * <img src="https://i.imgur.com/Gnd1CEf.jpg" style="width:500px" />
    * Radius $x$, circumference $2 \pi x$, height $f(x)$, and thickness $\Delta x$ or $dx$:
        * <img src="https://i.imgur.com/yWGMU9m.jpg" style="width:200px" />
* For example: Find the volume of the solid obtained by rotating the region bounded by $y=x-x^2$ and $y=0$ about the line $x = 2$.
    * The figure below shows the region and a cylindrical shell formed by rotation about the line $x = 2$. It has radius $2 - x$, circumference $2\pi (2-x)$, and height $x - x^2$.
    * <img src="https://i.imgur.com/5C6eyWm.jpg" style="width:500px" />
    * The volume of the given solid is: $$\begin{aligned}
        V &= \int_0^1 2 \pi (2 - x) (x - x^2) dx \\
        &= 2 \pi \int_0^1 (x^3-3x^2 + 2x) dx \\
        &= 2 \pi \big[\frac{x^4}{4} - x^3 + x^2\big]_0^1 = \frac{\pi}{2}
        \end{aligned}$$


### Disks and Washers versus Cylindrical Shells

* If the region more easily described by top and bottom boundary curves of the form $y = f(x)$, or by left and right boundaries $x = g(y)$, use **Washers**.
* If we decide that one variable is easier to work with than the other, then this dictates which method to use. 
* Draw a sample rectangle in the region, corresponding to a cross-section of the solid. The thickness of the rectangle, either $\Delta x$ or $\Delta y$, corresponds to the integration variable. If you imagine the rectangle revolving, it becomes either a disk (washer) or a shell.

## Arc Length

* **Formula**: If $f'$ is continuous on [a, b], then the length of the curve $y = f(x), a \le x \le b$, is $$L = \int_a^b \sqrt{1+[f'(x)]^2}dx$$
* **Proves**:
    * Suppose that a curve **C** is defined by the equation $y = f(x)$, where $f$ is continuous and $a \le x \le b$. We obtain a polygonal approximation to **C** by dividing the interval **[a, b]** into n subintervals with endpoints $x_0, x_1, \ldots, x_n$ and equal width $\Delta x$. If $y_i = f(x_i)$, then the point $P_i(x_i, y_i)$ lies on **C** and the polygon with vertices $P_0, P_1, \ldots, P_n$, is an approximation of **C**.
    * <img src="https://i.imgur.com/ETradYS.jpg" style="width:250px" />
    * We define the length **L** of the curve **C** as thee limit of the lengths $|P_{i-1}P_i|$: $$L = \lim_{n \to \infty} \sum_{i=1}^n |P_{i-1}P_i|$$
    * If we let $\Delta y_i = y_i - y_{i-1}$, then $$\begin{aligned} 
        |P_{i-1}P_i| &= \sqrt{(x_i-x_{i-1})^2 + (y_i-y_{i-1})^2} = \sqrt{(\Delta x_i)^2 + (\Delta y_i)^2} \\
        &= \Delta x_i \sqrt{1 + (\frac{\Delta y_i}{\Delta x_i})^2} \\
        &= \sqrt{1 + (f'(x))^2}dx
        \end{aligned}$$
    * So $$L = \int_a^b\sqrt{1 + [f'(x)]^2}dx$$


