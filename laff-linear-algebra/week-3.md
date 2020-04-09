# Week 3 - Matrix-Vector Operations

\[TOC\]

## Special Matrices

* ![](../.gitbook/assets/15115164411731.jpg)
* Special Vectors:
  * **Unit Vector**: Any vector of length one \(unit length\). For example, the vector  \\(\begin{pmatrix}\frac{\sqrt{2}}{2} \ \frac{\sqrt{2}}{2}\end{pmatrix}\\) has length one.
  * **Standard Unit Vector**: 
    * ![](../.gitbook/assets/15095053286178.jpg)

## Triangular Matrices

* ![](../.gitbook/assets/15115164709330%20%281%29.jpg)

## Transpose Matrix

* ![](../.gitbook/assets/15115165059094%20%281%29.jpg)

## Symmetric Matrix

* ![](../.gitbook/assets/15115165316994.jpg)

## Scaling a Matrix

* ![](../.gitbook/assets/15115165585084.jpg)

## Adding Matrices

* ![](../.gitbook/assets/15115170233025%20%281%29.jpg)

## Matrix-vector Multiplication

* ![](../.gitbook/assets/15115166290203%20%281%29.jpg)

## Cost of Matrix-Vector Multiplication

* Consider \\(y := Ax+y \text{, where } A \in R^{m \times n}\\) :
  * Notice that there is a multiply and an add for every element of A.
  * Since A has \\(m \times n = mn\\) elements, \\(y := Ax+y\\), requires **mn** multiplies and **mn** adds, for a total of **2mn** ﬂoating point operations \(ﬂops\).

