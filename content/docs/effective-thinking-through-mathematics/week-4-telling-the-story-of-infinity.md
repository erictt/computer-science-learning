---
weight: 1
title: "Telling the Story of Infinity"
---

# Telling the Story of Infinity

## Cardinality: 1-1 Correspondence

* My answer:
    
    * Cardinality is used for comparing two data sets. If they have the same sizes, we say these two data sets have the same cardinality.
    * The 1-1 Correspondence theorem is to compare two data sets one by one. If all elements in one data set match the other data sets, we say they have the same cardinality, if not, they don't.
    * For example, data sets A [1, 2, 3, 4, 5] and B [6, 7, 8, 9 ,10]. In those two data sets, we can make 1 corresponds 6, 2 corresponds 3, and so on. So, we can conclude that A and B have the same cardinality.
    * The 1-1 Correspondence theorem is a stable relationship between two data sets. If we conclude that, the data sets A and B have the same cardinality, that means we can find a stable relationship, that given an element in A, to find its corresponding one in B, which is not random but constant, and don't miss one out.
    
## Cardinality of the Integers

* My answer:
    * This section we compare the natural numbers and the integers to see if they have the same cardinality.
    * First, we list some of the natural numbers and the integers to see the difference.
    * The natural numbers: [0, 1, 2, 3, ..., n-2, n-1, n]
    * The integers: [-n, -n+1, -n+2, ..., -3, -2, -1, 0, 1, 2, 3, ..., n-2, n-1, n]
    * The only difference between them is, the integers have lots of negative numbers. So to simplify the question, let's use the subset of the integers: [-3, -2, -1, 0, 1, 2, 3, ..., n-2, n-1, n]. How to make one-to-one correspondence between the subset of the integers and the natural numbers ? Quite simple, right? -3 -> 0, -2 -> 1, -1 -> 0, ..., but we can apply this method to the integers, it will cause one infinity append to another infinity.
    * Let's rewrite the integers' format to this [0, 1, -1, 2, -2, 3, -3, ..., n-2, -n+2, n-1, -n+1, n, -n]. We can see the data all flow to the right. Then compare to the natural numbers will be like: 0 -> 0, 1 -> 1, 2 -> -1, 3 -> 2, 4 -> -2, ... . So we proved the natural numbers and the integers 
    do have the same cardinality. And the key to this question is to let them flow to one side.
    
## Cardinality of the Rationals

* My answer:
    
    * Now, we compare the rational numbers and the natural numbers. Wikipedia says a rational number is any number that can be expressed as the quotient or fraction p/q of two integers. 
    * The numbers are too complex to us. So, to start with a small group will be a good strategy. Like the last question, we can start with all the positive numbers. But they are still too many to find a solution. So keep narrow down the range. what about the numbers between 0 and 1? They are 0, 1, 1/2, 1/3, 2/3, 1/4, 3/4, ..., 1/n, 2/n, ..., (n-1)/n. Seems like, we already arrange them as one-to-one to natural numbers.
    * Next step is to expand the range to all the positive numbers. We already got all the [0, 1] numbers, and we know that f(x) = 1/x, when x -> 0, f(x) -> infinity. So what if we flip all the numbers in the range [0, 1], will it be all the numbers greater than 1? Let's make some tests. Say 123/345, doesn't it exist in our list of [0, 1]? Since n -> infinity, so 123/345 and 345/123 should all be on our list. For now we covered all the positive numbers, and our list is [0, 1, 1/2, 2, 1/3, 3, 2/3, 3/2, 1/4, 4, 3/4, 4/3, ..., 1/n, n, 2/n, n/2, ..., (n-1)/n, n/(n-1)].
    * What about all negative numbers? Use the strategy in the last question, just insert them behind every positive number. Then the list will be: [0, 1, -1, 1/2, -1/2, 2, -2, 1/3, -1/3, 3, -3, 2/3, -2/3, 3/2, -3/2, 1/4, ...].
    
## Dodgeball

* My answer:
    
    * For a specific size N (N is a natural number) to fill in O or X, all the possibilities of combinations should be 2^N. For example, N = 6, as in the video, the possibilities of combinations are 2^6 = 64, and the player one can only fill in 6 rows. So the player two has 64 - 6 = 58 possibilities to win this game. 
    * Since the player two can only fill in one symbol once the player one finished a row. So the player two just need to focus on the current symbol to make it different from one of the symbols in the last row which the player one just filled in. In the end, the player two will get a row which different with all of the rows the player one filled in.

## Infinite Dodgeball

* My answer:
    
    * Like the statement, I wrote in the last question, the possibilities are 2^N. So to this question, I just need to prove 2^N > N. If you plot f(x) = 2^x, and f(x) = x, you will see that they never intersect with each other. So 2^N will always bigger than N. As N goes infinite, the possibilities of the player two wins will be higher.
    * Still, we just need to follow the strategy that the player two only focus on the single row and fill in the different one. Even N goes infinite, the player two will always have a different one with all the rows the player one filled in.
    
## Infinity Comes in Different Sizes

* My answer:
    
    * In this section, we compare the natural numbers with the real numbers. 
    * Base on the one-to-one correspondence theorem, if we can make every real number to correspond with every natural number, then we can say they have the same cardinality. 
    * Let's apply the numbers to the DodgeBall game. The rows numbers are more like the natural numbers, and replacing the O and X with [0, 9], every row is more like the real numbers. So for now, our goal is to figure out whether we can list all the real numbers to make the player two lose.
    * Let's apply the strategy we used before, only focus on a single number in a row. First number in first row, second number in second row, as the natural number grows, we can always fill in a number that different with the Nth number in N-row. It's not like rational numbers, that we can eventually find the match number in next steps, but always can't match that one, as the length N keep growing up. It means some real numbers are left out in the one-to-one correspondence theorem. And we can't build the solid relationship between every natural number and every real number and don't miss one out.
    
## Additional comments on your response

* My answer:

    * I think, "finding the relationship between two data sets, and don't miss one out" is an interesting expression to the one-to-one correspondence theorem, which makes my thought more clear. And calculating the possibility give me more confidence to say that player two is gonna win, even I don't understand what the rules imply at first place. But I didn't give more evidence that why I need to calculate the possibility. I essentially feel that there must be something related to it, like f(x) = x is a straight line, but f(x) = 10^x is an exponential curve, they have different growth rate. May be we can use the graphs to compare the cardinality? Can't say for sure. Guess I'll have to dig it deeper in the future.

## Reference

* [Cantor's diagonal argument](https://en.wikipedia.org/wiki/Cantor%27s_diagonal_argument)

