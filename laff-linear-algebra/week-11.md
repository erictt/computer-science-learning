# Week 11 - Orthogonal Projection, Low Rank Approximation, and Orthogonal Bases

[TOC]

## Projecting a Vector onto a Subspace


### Projection

* <img src="media/15246609225677.jpg" style="width:300px" />
* Here, we have two vectors, \\(a, b \in \mathbb{R}^m\\). They exist in the plane deﬁned by \\(\text{Span}({a, b})\\) which is a two dimensional space (unless a and b point in the same direction). 
* \\(b = z + w\\)
* \\(z = \chi a \text{ with } \chi \in \mathbb{R}\\)
* \\(a^T w = 0\\)
* \\(0 = a^T w = a^T(b - z) = a^T (b - \chi a)\\)
* \\(a^T a \chi = a^T b\\).
* Provided \\(a \ne 0\\), \\(\chi = (a^T a)^{-1}(a^T b)\\).
* Thus, the component of \\(b\\) in the direction of \\(a\\) is given by \\[z = \chi a = (a^T a)^{-1} (a^T b) a = a(a^T a)^{-1}(a^T b) = [a(a^T a)^{-1}a^T ] b = [\frac{1}{a^T a} a a^T ] b\\]
    * Notice \\((a^Ta)^{-1}\\) and \\(a^T b\\) are both scalars.
    * We say that, given vector \\(a\\), the matrix that projects any given vector \\(b\\) onto the space spanned by a is given by \\[a(a^T a)^{-1}a^T = \frac{1}{a^T a} a a^T \\]
* The component of \\(b\\) orthogonal (perpendicular) to \\(a\\) is given by \\[w = b - z = b - (a(a^T a)^{-1}a^T ) b = Ib - (a(a^T a)^{-1}a^T )b = (I - a(a^T a)^{-1}a^T )b\\]
    * We say that, given vector \\(a\\), the matrix that projects any given vector \\(b\\) onto the space spanned by a is given by \\[I - a(a^T a)^{-1}a^T = I - \frac{1}{a^T a} a a^T \\]
* Set \\(v^T = (a^T a)^{-1}a^T\\),
    * \\(z = (a v^T) b\\)
    * \\(w = (I - a v^T) b\\)
    * Notice \\((I - a v^T)\\) is a rank-1 update to the identity matrix.
* Given \\(a, x \in \mathbb {R}^ m\\), we can use \\(P_ a( x )\\) and \\(P_ a ^{\perp}( x )\\) to represent the projection of vector \\(x\\) onto \\({\rm Span}(\{ a\} )\\) and \\({\rm Span}(\{ a\} )^{\perp}\\).

* Given \\(A \in \mathbb{R}^{m \times n}\\) with linearly independent columns and vector \\(\\) :










