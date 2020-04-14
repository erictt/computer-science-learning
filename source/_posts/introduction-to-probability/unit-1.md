# Unit 1: Probability models and axioms

##  Lec. 1: Probability models and axioms

### Sample Space

* **Definition**: the set of all of possible outcomes is called the **sample space** of the experiment,. Denoted by \\(\Omega\\)
* A subset of the sample space is called **event**. **Probability** is assigned to events.
* sample space can be finite, infinite, continuous, etc.
* The construction of a sample space is a description of the possible outcomes of a **probabilistic experiment**.

#### Examples

* **discrete/finite example**:
    * Two rolls of a tetrahedral die.
        * roll twice, get 16 outcomes. (the order sometimes matters)
* **continuous example**:
    * (x, y) such that \\(0 \le x, y \le 1\\): a square box.

### Probability axioms

* Non-negativity: \\(P(A) \ge 0\\)
* **Normalization**: \\(P(\Omega) = 1\\)
* (Finite) additivity: \\(\text{If } A \cap B = \emptyset,\text{then } P(A \cup B) = P(A) + P(B)\\)
    * \\(\emptyset\\) denote empty set.
    * \\( A \cap B = \emptyset\\) means A and B are disjoint events.

#### Consequences
    
* \\(P(A) \le 1\\)
* \\(P(\emptyset) = 0\\)
* \\(P(A) + P(A^c) = 1\\)
* \\(P(A \cup B \cup C) = P(A) + P(B) + P(C)\\)
    *  A, B and C are disjoint events.
    * and similarly for k disjoint events.
* \\(P({s_1, s_2, \ldots, s_k}) = P({s_1} \cup {s_2} \cup \ldots \cup {s_k})= P({s_1}) + P({s_2}) + \ldots + P({s_k})\\)
* \\(\text{If } A \subset B = \phi,\text{then } P(A) \le P(B)\\)
* \\(P(A \cup B) = P(A) + P(B) - P(A \cap B)\\)
* \\(P(A \cup B) \le P(A) + P(B)\\)
* \\(P(A \cup B \cup C) = P(A) + P(A^c \cap B) + P(A^c \cap B^c \cap C)\\)

### Discrete Models

* Example: **Coin tosses**. Consider an **experiment** involving a single coin toss. There are two possible outcomes, heads (H) and tails (T). The **sample space** is \\(\Omega = \{H, T\}\\), and the **events** are \\[\{H, T\}, \{H\}, \{T\}, \emptyset.\\]

#### Discrete Probability Law

* the probability of any event \\(\{s_1, s_2, \ldots, s_n \}\\) is the sum of the probabilities of its elements: \\[P(\{s_1, s_2, \ldots, s_n \}) = P(\{s_1\}) + P(\{s_2\}) + \ldots + P(\{s_n\})\\]

#### Discrete Uniform Law

* Assume \\(\Omega\\) consists of **n** equals likely elements
* Then the probability of any event A is given by \\[P(A) = \frac{\text{Number of elements of} A}{n}\\]

### Continuous Models

* Example: (x, y) such that \\(0 \le x, y \le 1\\)
* \\(P({(x, y)| x + y \le 1/2}) = \frac{1}{2} \cdot \frac{1}{2} \cdot \frac{1}{2} = \frac{1}{8}\\)
    * Because it's a right triangle with length 1/2 of each side.
*  \\(P({(0.5, 0.3)}) = 0 \\)
    *  Because it's the area of a single point.

### Countable additivity

#### Probability calculation: discrete but infinite sample space

* Keep tossing a coin and the outcome is the number of tosses until we observe heads for the first time.
* Probability: \\(P(n) = \frac{1}{2^n},\ n = 1,2,\ldots\\)
* Legitimate check: \\(P(\Omega) = 1\\)
    * \\(\sum_{n = 1}^{\infty} \frac{1}{2^n} = \frac{1}{2}\sum_{n = 0}^{\infty} \frac{1}{2^n} = \frac{1}{2} \cdot \frac{1}{1-1/2} = 1\\)
        * Geometric Series Theorem
* \\(P(\text{outcome is even}) = P(\{2, 4, 6, \ldots\}) = P(\{2\}), P(\{4\}), P(\{6\}), \ldots = \frac{1}{2^2} + \frac{1}{2^4} + \frac{1}{2^6} + \cdots = \frac{1}{4} \cdot \frac{1}{1 - \frac{1}{4} } = \frac{1}{3} \\)
    * To support this calculation, we'll need:

#### Countable Additivity Axiom

* If \\(A_1, A_2, \ldots\\) is an infinite **sequence** of **disjoint** events, then \\[P(A_1 \cup A_2 \cup \cdots) = P(A_1) + P(A_2) + \cdots\\]
* Notice the events should be sequence, like the example above. 
    * Example (x, y) such that \\(0 \le x, y \le 1\\) can not be arranged in a sequence. and the elements are NOT countable.
* Additivity holds only for "**countable**" sequences of events.

#### Countable and uncountable sets

* Countable: can be put in 1-1 correspondence with positive integers
    * positive integers: \\(1, 2, 3, \ldots\\)
    * integers: \\(0, 1, -1, 2, -2, \ldots\\)
    * pairs of positive integers
    * rational numbers q with 0 < q < 1
        * \\(1/2, 1/3, 2/3, 1/4, 3/4, 1/5, 2/5, \ldots\\)
* Uncountable:
    * the interval [0, 1]
    * the reals, the plane...

### Interpretations of probability theory

* A framework for analyzing phenomena with uncertain outcomes
    * Rules for consistent reasoning
    * Used for predictions and decisions

## Words

* **tetrahedral** [,tetrə'hi:drəl, -'he-] adj. 四面体的；有四面的
* **axiom** ['æksiəm] n. [数] 公理；格言；自明之理
* **discrete** [dis'kri:t] adj. 离散的，不连续的
* **legitimate** [li'dʒitimət, li'dʒitimeit] adj. 合法的；正当的；合理的；正统的 vt. 使合法；认为正当（等于legitimize）
* **additivity** [,ædi'tivəti] n. 添加；相加性
* **unit square** [数] 单位平方形


