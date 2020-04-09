# Unit 2: Derivatives of multivariable functions

\[TOC\]

## Partial Derivative and Gradient

### Introduction to partial derivatives

* For a multivariable function, like \\( f\(x, y\) = x^2 y \\), computing **partial derivatives** looks something like this:
  * ![](../.gitbook/assets/15256736088648.jpg)
* `\partial` ∂, called "del", is used to distinguish partial derivatives from ordinary single-variable derivatives.

#### Formal Definition

* \\[ \frac{\partial f}{\color{green}{ \partial x} }\(x_0, y\_0\) = \lim_{h \to 0} \frac{ f\(x\_0 \color{green}{+ h}, y\) - f\(x\_0, y\_0\) } { \color{green}{ h } }\\] 

| Symbol | Informal understanding | Formal understanding |
| :--- | :--- | :--- |
| \\( \partial x \\) | A tiny nudge in the \\( x \\) direction. | A limiting variable \\( h \\) which goes to \\( 0 \\), and will be added to the first component of the function's input. |
| \\( \partial f \\) | The resulting change in the output of \\( f \\) after the nudge. | The difference between \\( f\(x\_0 + h, y\_0\) \\) and \\( f\(x\_0, y\_0\) \\), taken in the same limit as \\( h \to 0 \\). |

### Second partial derivatives

* notation:
  * ![](../.gitbook/assets/15256736088649.jpg)
* The second partial derivatives which involve multiple distinct input variables, such as \\( f_{ \color{red}{y}\color{blue}{x} } \\) and \\( f_{ \color{blue}{x}\color{red}{y} } \\), are called "**mixed partial derivatives**".

### Symmetry of second derivatives

* ![](../.gitbook/assets/15256752242980.jpg) 
* The two mixed partial derivatives are the same.
* **Schwarz's theorem** or **Clairaut's theorem**, which states that **symmetry of second derivatives** will always hold at a point if the second partial derivatives are **continuous around that point**. 

### Higher order derivatives

* ![](../.gitbook/assets/15256751228826.jpg) 
* the order of differentiation is indicated by the order of the terms in the denominator from **right to left**.

### The gradient

* The **gradient** of a function \\( f \\), denoted as \\( \nabla f \\), is the collection of all its partial derivatives into a vector.
  * ![](../.gitbook/assets/15256837586341.jpg) 
* **The most important thing to remember about the gradient**:
  * The gradient of \\( f \\), is evaluated at an input \\( \(x\_0, y\_0\) \\), points in the direction of steepest ascent.
  * The gradient is perpendicular to contour lines.
* Example differential operators
  * ![](../.gitbook/assets/15257761183480.jpg) 

### Directional derivatives

* If you have some multivariable function, \\( f\(x, y\) \\) and some vector in the function's input space, \\( \vec{\textbf{v}} \\), the **directional derivative** of \\( f \\) along \\( \vec{\textbf{v}} \\) on top tells you the rate at which \\( f \\) will change while the input moves with velocity vector \\( \vec{\textbf{v}} \\).
* The notation here is \\( \nabla\_{\vec{\textbf{v}}} f \\), and it is computed by taking the dot product between the gradient of \\( f \\) and the vector \\( \vec{\textbf{v}} \\), that is, \\( \nabla f \cdot \vec{\textbf{v}} \\).
  * ![](../.gitbook/assets/15257902396433.jpg)
* **Remember**: If the directional derivative is used to compute slope, either \\( \vec{\textbf{v}} \\)  must be a unit vector or you must remember to divide by \\( \lVert \vec{\textbf{v}}\rVert \\) at the end. 
  * Because the slope of a graph in the direction of \\( \vec{\textbf{v}} \\) only depends on the direction of \\( \vec{\textbf{v}} \\) not the magnitude \\( \lVert \vec{\textbf{v}}\rVert \\)
* **Alternate definition of directional derivative:** \\[ \nabla_{ \vec{ \textbf{v} } } f = \lim_{h \to 0} \frac{ f\(x + h \vec{ \textbf{v} }\) - f\(x\) }{ h \color{green}{\lVert \vec{ \textbf{v} } \rVert} }\\] 

### Why does the gradient point in the direction of steepest ascent?

* \\( \nabla_{ \hat{ u} } f\(x\_0, y\_0\) = \underbrace{ \hat{ u} \cdot \nabla f\(x\_0, y\_0\) }_{ \text{Maximize this quantity} }\\)
  * Which is the product of two vectors.
* And Cauchy-Schwarz inequality tells us: 
  * Let \\( x, y \in R^n \\), then \\(\|x y\| \le \lVert x \rVert \lVert y \rVert\\)
  * And \\(\|x y\| = \lVert x \rVert \lVert y \rVert \\), iff \\( x = cy, c \in \mathbb{R}\\).
  * ![](../.gitbook/assets/15257945739342.jpg) 

    ​    
* So the gradient points in the direction of steepest ascent is the unit vector in the direction \\( \nabla f\(x\_0, y\_0\) \\).

## Differentiating vector-valued functions

### Derivatives of vector-valued functions

* \\[\frac{d}{dt}\begin{bmatrix}  x\(t\) \ y\(t\)\end{bmatrix} = \begin{bmatrix}  x'\(t\) \ y'\(t\)\end{bmatrix}\\]

### Curvature

### Multivariable chain rule, simple version

### Partial derivatives of parametric surfaces

## Words

* **nudge** \[nʌdʒ\] n. 推动；用肘轻推；没完没了抱怨的人 vt. 推进；用肘轻推；向…不停地唠叨 vi. 轻推；推进；唠叨
* **parametrization** \[pə,ræmitrai'zeiʃən, -tri'z-\] n. \[数\] 参数化；参数化法；\[计\] 参量化
* **parallelogram** \[,pærə'leləɡræm\] n. 平行四边形
* **magnitude** \['mæɡnitju:d\] n. 大小；量级；\[地震\] 震级；重要；光度

