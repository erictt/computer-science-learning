# Week 3 - Matrix-Vector Operations

[TOC]

## Special Matrices

* <img src="media/15115164411731.jpg" width=550 />

* Special Vectors:
    * **Unit Vector**: Any vector of length one (unit length). For example, the vector  \\(\begin{pmatrix}\frac{\sqrt{2}}{2} \\ \frac{\sqrt{2}}{2}\end{pmatrix}\\) has length one.
    * **Standard Unit Vector**: 
        * <img src="media/15095053286178.jpg" width=200/>

## Triangular Matrices

* <img src="media/15115164709330.jpg" width=550 />

## Transpose Matrix

* <img src="media/15115165059094.jpg" width=550 />

## Symmetric Matrix

* <img src="media/15115165316994.jpg" width=550 />

## Scaling a Matrix

* <img src="media/15115165585084.jpg" width=550 />

## Adding Matrices

* <img src="media/15115170233025.jpg" width=550 />

## Matrix-vector Multiplication

* <img src="media/15115166290203.jpg" width=550 />

## Cost of Matrix-Vector Multiplication

* Consider \\(y := Ax+y\ \text{, where}\ A \in R m \times n\\) :
    * Notice that there is a multiply and an add for every element of A.
    * Since A has \\(m \times n = mn\\) elements, \\(y := Ax+y\\), requires **mn** multiplies and **mn** adds, for a total of **2mn** ﬂoating point operations (ﬂops).

