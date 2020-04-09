# Unit 2: Conditioning and independence

\[TOC\]

## Lec. 2: Conditioning and Bayes' rule

### Conditional probability

* Definition: \\(P\(A\|B\)\\) = "probability of **A**, given that **B** occurred": \\[P\(A\|B\) = \frac{P\(A \cap B\)}{P\(B\)}\\] defined only when \\(P\(B\) &gt; 0\\).

#### Example: two rolls of a Die 4-sided roll die

* Let \\(\color{red}{B}\\) be the event: \\(\min\(X, Y\) = 2\\)
* Let \\(\color{blue}{M}\\) be the event: \\(\max\(X, Y\)\\)
* ![](../.gitbook/assets/15254978309610%20%281%29.jpg)
* \\(P\(\color{blue}{M = 1}\|\color{red}{B}\) = 0\\)
* \\(P\(\color{blue}{M = 3}\|\color{red}{B}\) = \frac{P\(M = 3 \cap B\)}{P\(B\)} = \frac{2/16}{5/16} = 2/5\\)

### Models based on conditional probabilities and three basic tools

* A radar example: 
* Event \\(\color{blue}{A}\\): Airplane is flying above
* Event \\(\color{red}{B}\\): Something registers on radar screen
* ![](../.gitbook/assets/15254988153051.jpg)
* \\(P\(\color{blue}{A} \cap \color{red}{B}\) = 0.05 \cdot 0.99\\)
  * An airplane flight, and radar found it.
* \\(P\(\color{red}{B}\) = 0.05 \cdot 0.99 + 0.95 \cdot 0.1 = 0.1445\\)
  * Radar detected the sky whether there is an airplane flight by or not.
* \\(P\(\color{blue}{A} \| \color{red}{B}\) = \frac{P\(\color{blue}{A} \cap \color{red}{B}\)}{P\(\color{red}{B}\)} = \frac{0.05 \cdot 0.99}{0.1445} = 0.34\\)
  * Radar detected the sky and an airplane DID fly by.

#### Multiplication rule

* Take the radar example:
  * \\(P\(\color{blue}{A} \cap \color{red}{B}\) = P\(\color{red}{B}\) P\(\color{blue}{A} \| \color{red}{B}\) = P\(\color{blue}{A}\) P\(\color{red}{B} \|\color{blue}{A}\)\\)
  * Check the figure, we will find this is the trace of the branch from the origin, then \\(\color{blue}{A}\\), and finally end with \\(\color{blue}{A} \cap \color{red}{B}\\).
* Consider the experiment has an additional event \\(C\\),
  * ![](../.gitbook/assets/15255225188889%20%281%29.jpg)
  * Check this figure, we will get,
  * \\(P\(A^c \cap B \cap C^c\) = P\(A^c\) P\(B \| A^c\) P\(C^c \| A^c \cap B\) \\)
* **Theorem**: Assuming that all of the conditioning events have positive probability, we have \\[P\(\cap_{i=1}^n A\_i\) = P\(A\_1\)P\(A\_2\|A\_1\)P\(A\_2\|A\_1 \cap A\_2\)\cdots P\(A\_n \| \cap_{i=1}^{n-1} A\_i\)\\]

#### Total probability theorem

* **Theorem**: Let \\(A\_1, \ldots, A\_n\\) be disjoint events that form a partition of the sample space and assume that \\(P\(A\_i\) &gt; 0\\), for all \\(i = 1, \ldots, n\\). Then, for any event \\(B\\), we have \\[\begin{aligned}P\(B\) &= P\(A\_1 \cap B\) + \ldots + P\(A\_n \cap B\) \ &= P\(A\_1 \)P\(B \| A\_1 \) + \ldots + P\(A\_n\) P\(B \| A\_n \)\end{aligned}\\].
* B occurs is a **weighted average** of its conditional probability under each scenario, where each scenario is weighted according to its \(unconditional\) probability \(\\(P\(A\_i\)\\)\).
* ![](../.gitbook/assets/15255233436170%20%281%29.jpg)

#### Bayes' rules\( -&gt; inference\)

* **Theorem**: Let \\(A\_1, A\_2 , \ldots, A\_n\\) be disjoint events that form a partition of the sample space, and assume that \\(P\(A\_i\) &gt; 0\\), for all **i**. Then, for any event B such that \\(P\(B\) &gt; 0\\), we have \\[\begin{aligned} P\(A\_i \| B\) &= \frac{P\(A\_i\) P\(B \| A\_i\)}{P\(B\)} \ &= \frac{P\(A\_i\)P\(B \| A\_i\)}{P\(A\_1\)P\(B \| A\_1\) + \cdots + P\(A\_n\) P\(B \| A\_n\)} \end{aligned}\\]
* Bayes’ rule is often used for **inference**. There are a number of “causes” that may result in a certain “effect.” We observe the effect, and we wish to infer the cause. \\[\begin{aligned} & \color{blue}{A\_i} \xrightarrow\[P\(\color{red}{B}\|\color{blue}{A\_i}\)\]{\text{model} } \color{red}{B} \  & \ & \color{red}{B} \xrightarrow\[P\(\color{blue}{A\_i}\|\color{red}{B}\)\]{\text{inference} } \color{blue}{A\_i} \end{aligned}\\]

## Lec. 3: Independence

### A coin tossing example

* 3 tosses of a biased coin: \\(P\(H\) = p, P\(T\) = 1 - p\\)
* ![](../.gitbook/assets/15255268282636.jpg)
* \\(P\(\text{only 1 head}\) = 3 p \(1 - p\)^2\\)
* \\(P\(H\_1 \| \text{only 1 head}\) = \frac{P\(H\_1 \cap \text{ only 1 head}\)}{\text{only 1 head} } = \frac{p \(1-p\)^2}{3 p \(1-p\)^2} = \frac{1}{3}\\)
  * first toss is H is denoted by \\(H\_1\\) and the probability is **p**.

### Independence

* Two events A and B are said to **independent** if \\[P\(A \cap B\) = P\(A\)P\(B\)\\] If in addition, \\(P\(B\) &gt; 0\\), independence is equivalent to the condition \\[P\(A \| B\) = P\(A\)\\]
* If A and B are independent, so are A and \\(B^c\\).
* Two events A and B are said to be **conditionally independent**, given another event C with \\(P\(C\) &gt; 0\\), if \\[P\(A \cap B \| C\) = P\(A \| C\)P\(B \| C\).\\] If in addition, \\(P\(B \cap C\) &gt; 0\\), conditional independence is equivalent to the condition \\[P\(A \| B \cap C\) = P\(A \| C\).\\]
* **Independence does not imply conditional independence**, and vice versa.

### Conditional independence example

* Two unfair coins, A and B:
  * \\(P\(H \| \text{coin } A\) = 0.9, P\(H \| \text{coin } B\) = 0.1\\)
* choose either coin with equal probability.
* ![](../.gitbook/assets/15255750032414.jpg)
* Compare:
  * \\(P\(\text{toss } 11 = H\) = P\(A\) P\(H_{11} \| A\) + P\(B\) P\(H_{11}\| B\) = 0.5  _0.9 + 0.5_  0.1 = 0.5\\)
  * \\(P\(\text{toss } 11 = H \| \text{first 10 tosses are heads}\) = P\(H\_{11} \| A\) = 0.9\\)
* So in this experiment, A and B are conditional independent.

### Independence of a collection of events

* We say that the events \\(A_1, A\_2, \ldots, A\_n\\) are **independent** if \\[P\(\bigcap_{i \in S}A_i\) = \prod_{i \in S} P\(A\_i\), \text{ for every subset S of }{1, 2, \ldots, n}.\\]

### Independence versus pairwise independence

* **Pairwise independence does not imply independence.**
* For example: two independent fair coin tosses

  | HH | HT |
  | :---: | :---: |
  | TH | TT |

  * \\(H\_1\\): First toss is H
  * \\(H\_2\\): First toss is H
  * \\(P\(H\_1\) = P\(H\_2\) = 1/2\\)
  * \\(C\\): the two tosses had the same result = \\({HH, TT}\\)

* We know, 
  * \\(P\(H\_1 \cap C\) = P\(H\_1 \cap H\_2\) = 1/4\\)
  * \\(P\(H\_1\) P\(C\) = 1/2 \* 1/2 = 1/4\\)
* So \\(P\(H\_1\), P\(H\_2\), \text{ and } P\(C\)\\) are pairwise independent.
* If \\(P\(H\_1\), P\(H\_2\), \text{ and } P\(C\)\\) are independent, use the formula, we will get:
  * \\(P\(H\_1 \cap H\_2 \cap C\) = P\(H\_1\) \cap P\(H\_2\) \cap P\(C\) = 1/2  _1/2_  1/2 = 1/8\\)
* But check the figure, we know:
  * \\(P\(H\_1 \cap H\_2 \cap C\) = P\(HH\) = 1/4\\)
* So \\(P\(H\_1\), P\(H\_2\), \text{ and } P\(C\)\\) are **NOT** independent.
* Another way to prove \\(P\(H\_1\), P\(H\_2\), \text{ and } P\(C\)\\) are pairwise independent.
  * \\(P\(C\|H\_1\) = P\(H\_2 \| H\_1\) = P\(H\_2\) = 1/2 = P\(C\)\\)
  * \\(P\(C\| H\_1 \cap H\_2\) = 1 \ne P\(C\) = 1/2\\)
* Conclusion: **H\_1, H\_2, and C are pairwise independent, but not independent.** 

