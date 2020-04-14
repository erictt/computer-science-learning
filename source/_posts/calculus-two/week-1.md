# Week 1 - Sequences

## Definition

* A sequence can be thought of as a list of numbers written in a definite order:
    * \\(a_1, a_2, a_3, a_4, \ldots , a_n, \ldots\\)

### Notation

* The sequence \\({a_1, a_2, a_3, \ldots}\\) also denoted by
    * \\(\{a_n\}\\) or \\(\{a_n\}_{n=1}^{\infty}\\)
        * \\(n \in \mathbb{N}\\) (whole number)

### Example: The Fibonacci Sequence

* **Definition**: \\(\{f_n\}\\) is defined recursively by the conditions
    * \\(f_1 = 1\\), \\(f_2 = 1\\), \\(f_n = f_{n-1} + f_{n-2}\\), \\(n \ge 3\\)

### Different Ways to Present Sequence

* Two sequences \\(a_n\\) and \\(b_n\\) are **equal** if they begin at the same index **N**, and \\(a_n = b_n\\) whenever \\(n \ge N\\).
* For example:
    * \\(a_n = 2^n\ \text{for}\ n \ge 0\\)
    * \\(b_0 = 1\ \text{and}\ b_n = 2 \cdot b_{n-1}\\)

## Examples

### Tribonacci Sequence

* **Definition**: \\(a_0 = a_1 = a_2 = 1\\), \\(a_n = a_{n-1} + a_{n-2} + a_{n-3}\\)
    * Samples: 1, 1, 1, 3, 5, 9, 17, 31, 57, 105, 193, 355
* We can build a new sequence from this:
    * \\(b_n = \frac{a_n + 1}{a_n}\\)
    * Samples: \\(1, 1, 1, 3, \frac{5}{3}, \frac{9}{5}, \frac{17}{9}, \frac{31}{17}, \frac{57}{31}, \frac{105}{57}, \frac{193}{105}, \frac{355}{193}\\)
    * So \\(\displaystyle\lim_{n \to \infty} b_n = ?\\)

### Arithmetic Progression

* **Definition**: An **arithmetic progression** is an sequence with a **common difference** between the terms.
* **Example**: \\(5, 12, 19, 26, 33, \ldots : a_n = 5 + 7n\\)
* **Formula**: \\(a_n = a_0 + d_n\\)
* In a **arithmetic progression**, each term is the **arithmetic mean** of its neighbors.
    * **arithmetic mean**: \\(\displaystyle a_n = \frac{a_{n-1} + a_{n+1}}{2}\\)

### Geometric Progression

* **Definition**: An **geometric progression** is an sequence with a **common ratio** between the terms.
* **Example**: \\(3, 6, 12, 24, 48, 96, \ldots : a_n = 3 \cdot 2^n\\)
* **Formula**: \\(a_n = a_0 \cdot r^n\\)
* In a **geometric progression**, each term is the **geometric mean** of its neighbors.
    * **geometric mean**: \\(\displaystyle a_n = \sqrt{a_{n-1} a_{n+1}}\\)
        * for example, an area of a square with side length of \\(\sqrt{ab}\\) is \\(ab\\)
* \\(\displaystyle\lim_{n \to \infty} a_n\\)
    * if the **common ratio** > 1, then \\(\displaystyle\lim_{n \to \infty} a_n = \infty\\)
    * if the **common ratio** < 1, then \\(\displaystyle\lim_{n \to \infty} a_n = 0\\)

## Limit of a Sequence

* **Definition**: \\(\displaystyle \lim_{n \to \infty} a_n = L\\) means that, for every \\(\epsilon > 0\\), there is a whole number **N**, so that, whenever \\(n \ge N\\), \\(\lvert a_n - L \rvert < \epsilon\\).

## Sequence Bounded

* **Definition**: 
    * \\(a_n\\) is "**bounded above**" means there is a real number **M**, so that, for all \\(n \ge 0, a_n \le M\\).
    * \\(a_n\\) is "**bounded below**" means there is a real number **M**, so that, for all \\(n \ge 0, a_n \ge M\\).
    * \\(a_n\\) is "**bounded**" means \\(a_n\\) is "bounded above" and "bounded below".
* **Example**: 
    * \\(a_n = \sin n, -1 \le \sin n \le 1 \\). So \\(a_n\\) bounded.
    * \\(b_n = n \cdot \sin(\frac{\pi \cdot n}{n})\\), not bounded.

## Sequence Increasing

* **Definition**: 
    * A sequence (\\(a_n\\)) is **increasing** if whenever m > n, then \\(a_m > a_n\\).
    * A sequence (\\(a_n\\)) is **decreasing** if whenever m > n, then \\(a_m < a_n\\).
    * A sequence (\\(a_n\\)) is **non-decreasing** if whenever m > n, then \\(a_m \ge a_n\\).
    * A sequence (\\(a_n\\)) is **non-increasing** if whenever m > n, then \\(a_m \le a_n\\).

## The Monotone Convergence Theorem

* **Definition**: If the sequence (\\(a_n\\)) is **bounded** and **monotone**, then \\(\displaystyle\lim_{n \to \infty} a_n\\) exists.
* **Example**: \\(a_1 = 1, a_{n+1} = \sqrt{a_n +2}\\)
    * To prove the limit of this sequence exists, we need to this sequence is
        * **bounded**: \\(0 \le a_n \le 2\\)
            * \\(0 \le a_{n+1} = \sqrt{2+2} = 2\\)
            * \\(0 \le a_1 \le 2 \implies 0 \le a_2 \le 2 \implies \ldots\\)
        * **monotone**(non-decreasing): \\(a_n \le a_{n+1}\\) 
            * \\(a_n \le a_{n+1} = \sqrt{a_n + 2}\\) 
            * \\(a_n^2 - a_n - 2 \ge 0\\) 
            * \\((2 - a_n)(1 + a_n) \ge 0\\) which is true
    * So the limit of \\(a_n\\) exists.

## Extra

### A Sequence Includes Every Integer

* \\[C_n = \begin{cases}
   -(n+1)/2 &\text{if } n\ \text{odd}  \\
   n/2 &\text{if } n\ \text{even}
\end{cases}\\]
    * Starting with index 0.
* An infinite quantity is a quantity that won't be smaller, when you take something away.
    * Like we take away the negative integers from all integers, which is still infinite.
* Note: I've taken a similar course talked about it: 
    * [Effective Thinking Through Mathematics (Week 4: Telling the Story of Infinity)](https://cs.ericyy.me/effective-thinking-through-mathematics/week-4-telling-the-story-of-infinity/index.html)

### A Sequence Includes Every Real Number

* **Real Number**: The real numbers include all the rational numbers, such as the integer −5 and the fraction 4/3, and all the irrational numbers, such as √2 (1.41421356..., the square root of 2, an irrational algebraic number). Included within the irrationals are the transcendental numbers, such as π (3.14159265...). -- from [Wikipedia](https://en.wikipedia.org/wiki/Real_number)
* Doesn't exist.
* Prove: [Effective Thinking Through Mathematics (Week 4#infinity-comes-in-different-sizes)](https://cs.ericyy.me/effective-thinking-through-mathematics/week-4-telling-the-story-of-infinity/index.html#infinity-comes-in-different-sizes)

## Words

* **monotone function** 单调函数；单弹数
* **monotone increasing** 单调递增
* **monotone regression** 单调回归
* **parity** n. 平价；同等；相等
* **quantitative** adj. 定量的；量的，数量的
* **qualitative** adj. 定性的；质的，性质上的
* **quantitative and qualitative change** 量变与质变


