# Week 4 - Alternating Series

## Absolutely Convergent Series

### Theorem

* The series \\(\sum a_n\\) **converges absolutely** if the series \\(\sum \lvert a_n \lvert \\) converges.

### Examples

* \\(\sum \frac{(-1)^n}{n^2}\\)
    * \\(\sum \lvert \frac{(-1)^n}{n^2} \rvert = \sum \frac{1}{n^2}\\)
    * And we have proven that \\(\sum \frac{1}{n^2}\\) converges.
    * So \\(\sum \frac{(-1)^n}{n^2}\\) **converges absolutely**.

### Procedures to Analyze Series

* Check \\(\displaystyle \lim_{n \to \infty} a_n\\), 
    * if \\( \ne 0\\) then diverge.
    * else if \\(a_n \ge 0\\), apply usual convergence tests, like Ratio Test, Root Test and Integral Test. 
    * else: Apply tests to \\(\sum \lvert a_n \rvert\\). Try to prove the series convergence.

## Conditional Convergence

### Theorem

* \\(\sum a_n\\) is **conditional convergence**,
    * if \\(\sum a_n\\) converges, 
    * but \\(\sum \lvert a_n \rvert\\) diverges.

### Examples

* \\(\sum \frac{(-1)^n}{n}\\)
    * \\(\sum \lvert \frac{(-1)^n}{n} \rvert = \sum \frac{1}{n}\\) diverges.
    * But it converges, because \\(\sum \frac{(-1)^n}{n} = - \log 2\\)

## Alternating Series

### Definition

* An alternating series is a series whose terms are alternately positive and negative. Here are some examples:
    * \\(\sum \frac{(-1)^{n+1} } {n}\\) is alternating series.
        * = \\(\frac{1}{1} - \frac{1}{2} + \frac{1}{3} - \frac{1}{4} + \frac{1}{5} - \ldots\\)
    * \\(\sum \frac{(-1)^{n} \cdot \sin n } {n}\\) **IS NOT**.
    * \\(\sum \frac{(-1)^{n} \cdot \sin^2 n } {n}\\) is.

### Alternating Series Test

#### Theorem

* If the alternating series \\[\sum_{n=1}^{\infty} (-1)^{n-1} b_n = b_1 - b_2 + b_3 - b_4 + b_5 - \cdots b_n > 0\\] satisfies \\[\begin{aligned}& b_{n+1} \le b_n \ \text{for all}\ n \\ & \lim_{n \to \infty} b_n = 0\end{aligned}\\], 
* Then, the series converges.

#### Proven

* <img src="https://i.imgur.com/qLDVjBv.jpg" style="width:400px" />
* From this figure, we can get:
    * \\(s_{2n}\\) is increasing and bounded above by \\(s_1\\), so \\(\displaystyle \lim_{n \to \infty} s_{2n}\\) exists.
    * \\(s_{2n-1}\\) is decreasing and bounded below by \\(s_2\\), so \\(\displaystyle \lim_{n \to \infty} s_{2n-1}\\) exists.
* And we know \\(\displaystyle \lim_{n \to \infty}(s_{2n} - s_{2n-1}) = \lim_{n \to \infty}(-b_{2n})\\), and our conditions already says \\(\displaystyle \lim_{n \to \infty}(b_{n}) = 0\\)
* So, \\(\displaystyle \lim_{n \to \infty}(s_{2n}) - \lim_{n \to \infty}(s_{2n-1}) = 0\\), then we can say \\(\displaystyle \lim_{n \to \infty}(s_{n})\\) also exits and \\(\displaystyle = \lim_{n \to \infty}(s_{2n}) = \lim_{n \to \infty}(s_{2n-1}) = s\\).
* And also, we know, alternating series, is between neighboring partial sums: \\(s_{2n-1} \le s \le s_{2n}\\)

#### Examples

* Use the fact: **alternating series, is between neighboring partial sums**: \\(s_{2n-1} \le s \le s_{2n}\\) to prove \\(e\\) is irrational.
    * Definition of Irrational: A real number x is irrational if it cannot be expressed as \\(\frac{p}{q}\\) for p, q are integers.
* Let's declare \\(\frac{1}{e} = \sum \frac{(-1)^n}{n!}\\) (will learn it in Week 6), so our goal is, to prove \\(\sum \frac{(-1)^n}{n!}\\) irrational.
* \\(\sum \frac{(-1)^n}{n!}\\) is an alternating series. so \\(s_b < \frac{1}{e} < s_{b+1}\\)
* So we can get \\(0 < \lvert \frac{1}{e} - s_b \rvert < \frac{1}{(b+1)!}\\) base on \\(s_{b+1} - s_b = \frac{1}{(b+1)!}\\)
* Then \\(0 < b! \cdot \lvert \frac{1}{e} - s_b \rvert < \frac{b!}{(b+1)!} = \frac{1}{b+1}\\)
* Assume we can rewrite \\(\frac{1}{e}\\) to \\(\frac{a}{b}\\): \\(0 < \lvert b! \cdot \frac{a}{b} - b! \cdot s_b \rvert < \frac{1}{b+1} < 1\\)
* We know \\(b! \cdot \frac{a}{b}\\) is an integer. And \\(b! \cdot s_b = b! \sum_{n=0}^{b} \frac{(-1)^{n+1} }{n!} = \sum_{n=0}^{b} \frac{(-1)^{n+1} \cdot b!}{n!}\\)
    * **b** is at least as big as **n**, so \\(\sum_{n=0}^{b} \frac{(-1)^{n+1} \cdot b!}{n!}\\) is an integer too.
* So \\(\lvert b! \cdot \frac{a}{b} - b! \cdot s_b \rvert\\) should be an integer too. But \\(0 < \lvert b! \cdot \frac{a}{b} - b! \cdot s_b \rvert < 1\\). That's a contradiction.
* So \\(e\\) must be irrational.

## Limit Comparison Test

### Theorem

* If \\(a_n \ge 0\\), \\(b_n \ge 0\\) and \\(\displaystyle \lim_{n \to \infty} \frac{a_n}{b_n} = L > 0\\), 
* Then, \\(\sum b_n\\) converges, if and only if \\(\sum a_n\\) converges.

## One of the Practice Quiz

* You may remember that \\[\frac{d}{dx}\arctan(x) = \frac{1}{1+x^2}.\\] By computing some terms of the (alternating!) Taylor series for arctangent, approximate \\(\arctan(\frac{1}{2})\\) to within \\(\frac{1}{33}\\)
    * From the formula for geometric series shows that \\[1+y+y^2+y^3+\cdots = \frac{1}{1-y}\qquad\text{if } \lvert y \rvert \lt 1.\\]
    * And we know \\(x = \frac{1}{2} < 1\\), so we can plug in \\(-x^2\\) for \\(y\\), we get that \\[\begin{aligned}
\frac{1}{1+x^2} &= \frac{1}{1-(-x^2)} \\
&= 1 + (-x^2) + (-x^2)^2 + (-x^2)^3 + \cdots + (-x^2)^n + \cdots\\
&= 1 - x^2 + x^4 - x^6 + x^8 - x^{10} + \cdots
\end{aligned}\\]
    * So we have \\[\frac{d}{dx}\arctan(x) = 1 - x^2 + x^4 - x^6 + x^8 - x^{10}+\cdots\qquad\text{if }|x|\lt 1\\]
    * Then \\[\begin{aligned}
\arctan(x) &= \int\left(\frac{d}{dx}\arctan (x)\right)\,dx \\
&= \int\left(1 - x^2 + x^4 - x^6 + x^8 - x^{10}+\cdots\right)\,dx\\
&= \int\left(\sum_{n=0}^{\infty}(-1)^{n}x^{2n}\right)\,dx\\
&= \sum_{n=0}^{\infty}\left(\int (-1)^{n}x^{2n}\,dx\right)\\
&= \sum_{n=0}^{\infty}\left((-1)^{n}\int x^{2n}\,dx\right)\\
&= \sum_{n=0}^{\infty}\left((-1)^{n}\frac{x^{2n+1} }{2n+1}\right) + C\\
&= C + \left( x - \frac{x^3}{3} + \frac{x^5}{5} - \frac{x^7}{7} + \frac{x^9}{9} - \frac{x^{11} }{11} +\cdots\right).
\end{aligned}\\]
    * Evaluating at \\(x = 0\\) gives \\(0 = \arctan(0) = C\\), so we get \\[\arctan(x) = x - \frac{x^3}{3} + \frac{x^5}{5} - \frac{x^7}{7} + \frac{x^9}{9} - \frac{x^{11} }{11} + \cdots,\qquad\text{if }|x|\lt 1.\\]
    * \\(\frac{x^5}{5} < \frac{1}{33}\\), so the approximate value of \\(\arctan(\frac{1}{2}) = \frac{1}{2} - \frac{1}{24} = \frac{11}{24}\\) 

* Note we are assuming \\(|x| < 1\\), but arctangent is defined for all real numbers. The series we have here is \\[\sum_{n=0}^{\infty}(-1)^{n}\frac{x^{2n+1} }{2n+1}.\\]
* Using the **Ratio Test**, we have that \\[\begin{aligned}
\lim_{n\to\infty}\frac{|a_{n+1}|}{|a_n|} &= \lim_{n\to\infty}\frac{\quad\frac{|x|^{2n+3} }{2n+3}\quad}{\frac{|x|^{2n+1} }{2n+1} }\\
&= \lim_{n\to\infty}\frac{(2n+1)|x|^{2n+3} }{(2n+3)|x|^{2n+1} }\\
&= \lim_{n\to\infty}\frac{|x|^2(2n+1)}{2n+3}\\
&= |x|^2\lim_{n\to\infty}\frac{2n+1}{2n+3}\\
&= |x|^2.
\end{aligned}\\]
* By the Ratio Test, the series converges absolutely if \\(|x|^2 < 1\\) (that is, if \\(|x| < 1\\)) and diverges if \\(|x| > 1\\). At \\(x=1\\) and \\(x=-1\\), the series is known to converge. So the radius of convergence is 1, and the equality is valid for \\(x \in [-1,1]\\) only.
* This answer is copied from [https://math.stackexchange.com/questions/29649/why-is-arctanx-x-x3-3x5-5-x7-7-dots](https://math.stackexchange.com/questions/29649/why-is-arctanx-x-x3-3x5-5-x7-7-dots).

## Rearrangement Theorem

* Let **L** be a real number, \\(\sum a_n \\) is a **conditional convergent**.
* Then \\(a_n\\) can be rearranged to form \\(b_n\\) and \\(\sum b_n = L\\).

### Example

* \\(\sum \frac{(-1)^{n+1} }{n} = \frac{1}{1} - \frac{1}{2} + \frac{1}{3} - \frac{1}{4} + \frac{1}{5} - \frac{1}{6} + \frac{1}{7} - \cdots\\) 
* Take the even terms, we get \\(\sum \frac{1}{2n} = \frac{1}{2} \sum \frac{1}{n}\\), which diverges.
* Take the odd terms, we get \\(\sum \frac{1}{2n-1} > \sum \frac{1}{2n-1}\\), which diverges too.
* So whichever we picked, can easily get a number **L** as large as we want to.


