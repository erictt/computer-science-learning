# Week 3 - Matrix-Vector Operations

## Special Matrices

* <img src="https://i.imgur.com/wmbHvH8.jpg" style="width:550px" />

* Special Vectors:
    * **Unit Vector**: Any vector of length one (unit length). For example, the vector  \\(\begin{pmatrix}\frac{\sqrt{2}}{2} \\ \frac{\sqrt{2}}{2}\end{pmatrix}\\) has length one.
    * **Standard Unit Vector**: 
        * <img src="https://i.imgur.com/rbwLAAY.jpg" style="width:200px"/>

## Triangular Matrices

* <img src="https://i.imgur.com/prHUxYi.jpg" style="width:550px" />

## Transpose Matrix

* <img src="https://i.imgur.com/KT0p6Zj.jpg" style="width:550px" />

## Symmetric Matrix

* <img src="https://i.imgur.com/qF5tkQq.jpg" style="width:550px" />

## Scaling a Matrix

* <img src="https://i.imgur.com/bUbW96j.jpg" style="width:550px" />

## Adding Matrices

* <img src="https://i.imgur.com/zLPy73l.jpg" style="width:550px" />

## Matrix-vector Multiplication

* <img src="https://i.imgur.com/z8KsE1o.jpg" style="width:550px" />

## Cost of Matrix-Vector Multiplication

* Consider \\(y := Ax+y\ \text{, where } A \in R^{m \times n}\\) :
    * Notice that there is a multiply and an add for every element of A.
    * Since A has \\(m \times n = mn\\) elements, \\(y := Ax+y\\), requires **mn** multiplies and **mn** adds, for a total of **2mn** ﬂoating point operations (ﬂops).

