# Week 3 - Matrix-Vector Operations

[TOC]

## Special Matrices

* <img src="media/15115164411731.jpg" style="width:550px" />

* Special Vectors:
    * **Unit Vector**: Any vector of length one (unit length). For example, the vector  $$\begin{pmatrix}\frac{\sqrt{2}}{2} \\ \frac{\sqrt{2}}{2}\end{pmatrix}$$ has length one.
    * **Standard Unit Vector**: 
        * <img src="media/15095053286178.jpg" style="width:200px"/>

## Triangular Matrices

* <img src="media/15115164709330.jpg" style="width:550px" />

## Transpose Matrix

* <img src="media/15115165059094.jpg" style="width:550px" />

## Symmetric Matrix

* <img src="media/15115165316994.jpg" style="width:550px" />

## Scaling a Matrix

* <img src="media/15115165585084.jpg" style="width:550px" />

## Adding Matrices

* <img src="media/15115170233025.jpg" style="width:550px" />

## Matrix-vector Multiplication

* <img src="media/15115166290203.jpg" style="width:550px" />

## Cost of Matrix-Vector Multiplication

* Consider $$y := Ax+y\ \text{, where } A \in R^{m \times n}$$ :
    * Notice that there is a multiply and an add for every element of A.
    * Since A has $$m \times n = mn$$ elements, $$y := Ax+y$$, requires **mn** multiplies and **mn** adds, for a total of **2mn** ﬂoating point operations (ﬂops).

