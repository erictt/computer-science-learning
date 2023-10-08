# Probabilities

##  Basic Probability Notation

- **Event Probability**: $P(A)$ denotes the probability of event $A$ occurring.
- **Complementary Event**: $P(A^c)$ or $P(\neg A)$ represents the probability that event $A$ does not occur.
- **Joint Probability**: $P(A \cap B)$ or $P(A, B)$ denotes the probability of both events $A$ and $B$ occurring simultaneously.
- **Conditional Probability**: $P(A|B)$ represents the probability of event $A$ occurring given that event $B$ has occurred.
- **Union Probability**: $P(A \cup B)$ denotes the probability that either event $A$, event $B$, or both occur.

## Rules and Theorem

- **Addition Rule**: $P(A \cup B) = P(A) + P(B) - P(A \cap B)$
- **Marginal Probability** is often simply called the marginal. the probability of a single event occurring without reference to any other events.
	- Suppose you have a deck of cards, 
		- the marginal probability of drawing an Ace: $P(Ace)=4/52​$
		- the marginal probability of drawing a Red card: $P(Red) = 26/52$(heart or diamond)
- **Independence($A \perp B$) of Two Events**: In the context of a **joint probability table**(JPT), each cell (other than the marginals) represents a joint probability.
	- If $A$ and $B$ are **independent**:
		- $P(A \cap B) = P(A) \times P(B)$ <-- **Multiplication Rule**
	- If **not independent**:
		- $P(A \cap B) = P(A|B) \times P(B)$
		- or $P(A \cap B) = P(B|A) \times P(A)$
	- First example:
		* The probability of drawing a Red Ace: $P(Ace, Red) = 2/52$
		* $P(Ace) \times P(Red) = 4/52 \times 26/52 = 2/52$
		* Thus, being an Ace and being Red are **independent**.
		* In other words, being Ace doesn't affect the probability of being Red.
	* Second example:
		* When flipping a coin, **ASSUME** that the probability of getting heads at the first flip is 1/2: $P(X_1=H) = 1/2$, and the second flip is **dependent** to first flip and
			* $P(X_2 = H | X_1 = H) = 0.9$
			* $P(X_2 = T | X_1 = T) = 0.8$
		* Then
			* $P(X_2 = H) = P(X_2 = H | X_1 = H) \times P(X_1 = H) + P(X_2 = H | X_1 = T) \times P(X_1 = T) = 0.9 * 0.5 + (1 - 0.8) * 0.5$
			* Because the second flip is dependent to the first flip.
* **Total Probability**: $P(Y) = \sum_{i}{P(Y|X=i)P(X=i)}$
	* When Y depends on X
* **Negation of Probability**: $P(\neg X | Y) = 1 - P(X|Y)$
- **Bayes' Theorem**: $P(A|B) = \frac{\color{red}{P(B|A)}\color{blue}{P(A)}}{P(B)}$
	- $P(A|B)$: the posterior
	- $P(B|A)$: the likelihood
	- $P(A)$: the prior probability of $A$ occurring.
	- $P(B)$: the marginal likelihood or the total probability of $B$ occurring.
		- $P(B) = \sum_{\alpha}{P(B|A=\alpha)P(A=\alpha)}$
	- For example, when a person underwent a cancer(C) screening test, and it comes back positive(+). What's the actual probability that this person has cancer?
		- Given that:
			- the prevalence of this cancer in general population is $P(C) = 0.01$ <- **prior probability**.
			- the test's accuracy:
				- If a person has cancer, there is a 99% chance the test will be positive $P(+|C) = 0.99$ <- **likelihood**.
				- If a person don't have cancer, there is 5% chance the test will still be positive(false positive): $P(+|\neg C) = 0.05$
		- With Bayes' Theorem:
			- $P(C|+) = \frac{P(+|C) \times P(C)}{P(+)} = \frac{0.99 \times 0.01}{0.0594} \approx 0.166$
				- $P(+) = P(+|C) \times P(C) + P(+|\neg C) \times P(\neg C) = 0.01×0.99+0.99×0.05 = 0.0594$

// TODO
## Additional

normalization

## Random Variables and Distributions

- **Random Variable**: $X$ represents a variable that can take on different values according to some probability distribution.
- **Expected Value**: $\mathbb{E}[X]$ denotes the average or mean value of the random variable $X$.
- **Variance**: $\text{Var}(X)$ or $\sigma^2_X$ represents the measure of the spread of the values of $X$.
- **Standard Deviation**: $\sigma_X$ is the square root of the variance.
- **Probability Mass Function (for discrete variables)**: $P(X=x)$
- **Probability Density Function (for continuous variables)**: $f_X(x)$
## Common Distributions

- **Bernoulli Distribution**: $P(X=k) = p^k (1-p)^{1-k}$ for $k \in{0,1}$
- **Binomial Distribution**: $P(X=k) = \binom{n}{k} p^k (1-p)^{n-k}$
- **Normal Distribution**: $f(x) = \frac{1}{\sqrt{2\pi\sigma^2}} e^{-\frac{(x-\mu)^2}{2\sigma^2}}$
