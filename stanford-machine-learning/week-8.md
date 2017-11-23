# Week 8 - Unsupervised Learning & Dimensionality Reduction

[TOC]

## Unsupervised Learning

### Clustering

* Check [Computational Thinking(Lecture 12)](https://cs.ericyy.me/computational-thinking/lecture-12.html#clustering) for the **clustering** and **k-means algorithm** notes.
* <img src="media/15114179881526.jpg" width=500 />

#### Optimization Objective

* Cost Function: \\[J(c^{(1)}), \ldots, c^{(m)}, \mu_{1}, \ldots, \mu_{k}) = \frac{1}{m}\sum_{i=1}^{m} \lVert x^{(i)} - \mu_{c^{(i)}} \rVert^2\\]
    * \\(c^{(i)}\\) = index of cluster(1,2,...,K) to which exampe \\(x^{(i)}\\) is currently assigned.
    * \\(\mu_{k}\\) = cluster centroid \\(k\\) (\\(\mu_k \in \mathbb{R}^n\\))
* a little explanation about the **k-means algorithm** 
    * cluster assigned step: minimize \\(J(\ldots)\\)
    * move centroid step: choose \\(\mu\\) which minimized \\(J(\ldots)\\)

#### Random Initialization

* \\(K < m\\)
* Randomly pick **K** training examples
* Set \\(\mu_1, \ldots, \mu_K\\) equal to these **K** examples.
     
* How to fix **Local Optima**
    * the situation like:
        * <img src="media/15114196883603.jpg" width=300 />
    * The solution is: Try multiple times of random initialization.
    * <img src="media/15114197571420.jpg" width=360 />
     
####  Choosing the Number of Clusters
    
* First method is to use **Elbow method**: 
    * <img src="media/15114210748168.jpg" width=200 />
    * Sometimes, you won't get an elbow, instead with a smooth line, which means this method doesn't work in this way.
* Another method: **market segmentation**
    * For example: T-shirt size
        * If you have three sizes (S,M,L)
        * Or five sizes (XS, S, M, L, XL)

        
## Dimensionality Reduction



