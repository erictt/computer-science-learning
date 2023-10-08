%%  %%
Review Chapters 1, 2, 3.1-3.3, 4.1, 4.6, 5.4, 7.1, 7.3 of **Introduction to Probabilities**

Chapter 3

1. Search (Due 28)
	1. Chapter 3
	2. [Korf paper](https://www.cs.princeton.edu/courses/archive/fall06/cos402/papers/korfrubik.pdf)
	3. R&N slides on [Uninformed Search](http://www.cc.gatech.edu/~thad/6601-gradAI-fall2015/chapter03-clean.pdf) and [Informed Search](http://www.cc.gatech.edu/~thad/6601-gradAI-fall2015/chapter04a.pdf)
	4. A0: Hello AI World (Due **Sep 4**)
2. Simulated Annealing and Local Search (Due Sep 4)
	1. Chapter 4
	2. R&N slides on [Beyond Search](http://www.cc.gatech.edu/~thad/6601-gradAI-fall2015/chapter04b.pdf)
	3. Tri-directional search released (Due **Sept 11**)
3. Game Playing through Depth-limited Search; play each other in Isolation;  (Due Sep 11)
	1. Chapter 1-2; Chapter 5.0-5.2 
	2. R&N slides on [Game Playing](http://www.cc.gatech.edu/~thad/6601-gradAI-fall2015/chapter06.pdf)
	3. Tri-directional search due (Due **Sept 11**)
	4. [[BONUS]: The Race!](https://gatech.instructure.com/courses/336792/assignments/1476746) Not available until Sep 4, Due Sep 18
4. Game Playing through the end (Due Sep 18)
	1. Chapter 5.3-5.7 
	2. [Korf: 3 player alpha-beta](http://www.cc.gatech.edu/~thad/6601-gradAI-fall2015/Korf_Multi-player-Alpha-beta-Pruning.pdf)


In this assignment, you will first implement the basic search algorithms like BFS, UCS, and A*, followed by more challenging versions of them for bidirectional and tridirectional searches. Check out the Assignment 1 Ed posts to get started with it.


FAIL: test_bfs_romania (__main__.SearchRomaniaTests) (case=('d', 'f'))
Test breadth first search with Romania data
----------------------------------------------------------------------
Traceback (most recent call last):
  File "search_romania_tests.py", line 245, in run_romania_test
    self.assertTrue(verdict, msg=err)
AssertionError: False is not true : Path ['d', 'c', 'r', 's', 'f'] for goal nodes ('d', 'f') does not match reference. Path cost was 445 and expected path cost was 570. Expected path is ['d', 'c', 'p', 'b', 'f']


FAIL: test_ucs_romania (__main__.SearchRomaniaTests) (case=('z', 'h'))
Test uniform cost search with Romania data
----------------------------------------------------------------------
Traceback (most recent call last):
  File "search_romania_tests.py", line 245, in run_romania_test
    self.assertTrue(verdict, msg=err)
AssertionError: False is not true : Path ['z', 'o', 's', 'f', 'b', 'u', 'h'] for goal nodes ('z', 'h') does not match reference. Path cost was 715 and expected path cost was 676. Expected path is ['z', 'a', 's', 'r', 'p', 'b', 'u', 'h']


FAIL: test_bi_ucs_romania (__main__.SearchRomaniaTests) (case=('c', 'u'))
Test Bi-uniform cost search with Romania data.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "search_romania_tests.py", line 262, in run_romania_test
    self.assertTrue(verdict, msg=err)
AssertionError: False is not true : Path ['c', 'p', 'b', 'u'] for goal nodes ('c', 'u') explored more nodes than allowed maximum. Explored count was 40 and max allowed count was 15

FAIL: test_bi_ucs_romania (__main__.SearchRomaniaTests) (case=('p', 'o'))
Test Bi-uniform cost search with Romania data.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "search_romania_tests.py", line 262, in run_romania_test
    self.assertTrue(verdict, msg=err)
AssertionError: False is not true : Path ['p', 'r', 's', 'o'] for goal nodes ('p', 'o') explored more nodes than allowed maximum. Explored count was 13 and max allowed count was 11


explored:  {'a': 1, 'z': 1, 's': 0, 't': 1, 'b': 1, 'u': 1, 'p': 1, 'g': 1, 'f': 0, 'c': 1, 'd': 0, 'r': 1, 'm': 1, 'e': 0, 'h': 0, 'i': 0, 'v': 0, 'n': 0, 'l': 1, 'o': 1}
explored:  {'a': 1, 'z': 1, 's': 0, 't': 1, 'b': 1, 'u': 1, 'p': 1, 'g': 0, 'f': 0, 'c': 1, 'd': 0, 'r': 1, 'm': 0, 'e': 0, 'h': 0, 'i': 0, 'v': 0, 'n': 0, 'l': 0, 'o': 1}


sum:  p a 14
explored:  {'a': 1, 'z': 1, 's': 1, 't': 1, 'b': 1, 'u': 1, 'p': 1, 'g': 1, 'f': 0, 'c': 1, 'd': 1, 'r': 1, 'm': 0, 'e': 0, 'h': 1, 'i': 0, 'v': 0, 'n': 0, 'l': 1, 'o': 1}





after append:  [(0, 0, ['p'])]
after append:  [(0, 0, ['a'])]
pop:  (0, 0, ['p'])
after pop:  []
after append:  [(101, 1, 'b')]
after append:  [(101, 1, 'b'), (138, 2, 'c')]
after append:  [(97, 3, 'r'), (138, 2, 'c'), (101, 1, 'b')]
pop:  (0, 0, ['a'])
after pop:  []
after append:  [(75, 1, 'z')]
after append:  [(75, 1, 'z'), (140, 2, 's')]
after append:  [(75, 1, 'z'), (140, 2, 's'), (118, 3, 't')]
pop:  (97, 3, 'r')
after pop:  [(101, 1, 'b'), (138, 2, 'c')]
after append:  [(101, 1, 'b'), (138, 2, 'c'), (177, 4, 's')]
pop:  (75, 1, 'z')
after pop:  [(118, 3, 't'), (140, 2, 's')]
after append:  [(118, 3, 't'), (140, 2, 's'), (146, 4, 'o')]
pop:  (101, 1, 'b')
after pop:  [(138, 2, 'c'), (177, 4, 's')]
after append:  [(138, 2, 'c'), (177, 4, 's'), (186, 5, 'u')]
after append:  [(138, 2, 'c'), (177, 4, 's'), (186, 5, 'u'), (191, 6, 'g')]
after append:  [(138, 2, 'c'), (177, 4, 's'), (186, 5, 'u'), (191, 6, 'g'), (312, 7, 'f')]
pop:  (118, 3, 't')
after pop:  [(140, 2, 's'), (146, 4, 'o')]
after append:  [(140, 2, 's'), (146, 4, 'o'), (229, 5, 'l')]
pop:  (138, 2, 'c')
after pop:  [(177, 4, 's'), (191, 6, 'g'), (186, 5, 'u'), (312, 7, 'f')]
after append:  [(177, 4, 's'), (191, 6, 'g'), (186, 5, 'u'), (312, 7, 'f'), (258, 8, 'd')]
pop:  (140, 2, 's')
after pop:  [(146, 4, 'o'), (229, 5, 'l')]
new path: 317 ['p', 'r', 's'] ['a', 's']
after append:  [(146, 4, 'o'), (229, 5, 'l'), (239, 6, 'f')]
after append:  [(146, 4, 'o'), (220, 7, 'r'), (239, 6, 'f'), (229, 5, 'l')]
pop:  (177, 4, 's')
after pop:  [(186, 5, 'u'), (191, 6, 'g'), (258, 8, 'd'), (312, 7, 'f')]
pop:  (146, 4, 'o')
after pop:  [(220, 7, 'r'), (229, 5, 'l'), (239, 6, 'f')]
pop:  (186, 5, 'u')
after pop:  [(191, 6, 'g'), (312, 7, 'f'), (258, 8, 'd')]
after append:  [(191, 6, 'g'), (284, 9, 'h'), (258, 8, 'd'), (312, 7, 'f')]
after append:  [(191, 6, 'g'), (284, 9, 'h'), (258, 8, 'd'), (312, 7, 'f'), (328, 10, 'v')]
pop:  (220, 7, 'r')
after pop:  [(229, 5, 'l'), (239, 6, 'f')]
pop:  (191, 6, 'g')
after pop:  [(258, 8, 'd'), (284, 9, 'h'), (328, 10, 'v'), (312, 7, 'f')]
pop:  (229, 5, 'l')
after pop:  [(239, 6, 'f')]
after append:  [(239, 6, 'f'), (299, 8, 'm')]
pop:  (258, 8, 'd')
after pop:  [(284, 9, 'h'), (312, 7, 'f'), (328, 10, 'v')]
after append:  [(284, 9, 'h'), (312, 7, 'f'), (328, 10, 'v'), (333, 11, 'm')]
pop:  (239, 6, 'f')
after pop:  [(299, 8, 'm')]
pop:  (284, 9, 'h')
after pop:  [(312, 7, 'f'), (333, 11, 'm'), (328, 10, 'v')]
after append:  [(312, 7, 'f'), (333, 11, 'm'), (328, 10, 'v'), (370, 12, 'e')]
pop:  (299, 8, 'm')
after pop:  []
['p', 'r', 's']
['a', 's']
final result:  s ['p', 'r', 's'] ['a', 's']
sum:  p a 14
explored:  {'a': 1, 'z': 1, 's': 1, 't': 1, 'b': 1, 'u': 1, 'p': 1, 'g': 1, 'f': 0, 'c': 1, 'd': 1, 'r': 1, 'm': 0, 'e': 0, 'h': 1, 'i': 0, 'v': 0, 'n': 0, 'l': 1, 'o': 1}



g -> b(90) -> p 



FAIL: test_bi_a_star_euclidean_romania (__main__.SearchRomaniaTests) (case=('r', 'z'))
Test Bi-A* search with Romania data and the Euclidean heuristic.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "search_romania_tests.py", line 245, in run_romania_test
    self.assertTrue(verdict, msg=err)
AssertionError: False is not true : Path ['r', 's', 'o', 'z'] for goal nodes ('r', 'z') does not match reference. Path cost was 302 and expected path cost was 295. Expected path is ['r', 's', 'a', 'z']


FAIL: test_bi_a_star_euclidean_romania (__main__.SearchRomaniaTests) (case=('e', 's'))
Test Bi-A* search with Romania data and the Euclidean heuristic.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "search_romania_tests.py", line 245, in run_romania_test
    self.assertTrue(verdict, msg=err)
AssertionError: False is not true : Path ['e', 'h', 'u', 'b', 'f', 's'] for goal nodes ('e', 's') does not match reference. Path cost was 579 and expected path cost was 547. Expected path is ['e', 'h', 'u', 'b', 'p', 'r', 's']


FAIL: test_bi_a_star_euclidean_romania (__main__.SearchRomaniaTests) (case=('i', 's'))
Test Bi-A* search with Romania data and the Euclidean heuristic.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "search_romania_tests.py", line 262, in run_romania_test
    self.assertTrue(verdict, msg=err)
AssertionError: False is not true : Path ['i', 'v', 'u', 'b', 'p', 'r', 's'] for goal nodes ('i', 's') explored more nodes than allowed maximum. Explored count was 14 and max allowed count was 12


FAIL: test_bi_a_star_euclidean_romania (__main__.SearchRomaniaTests) (case=('o', 'p'))
Test Bi-A* search with Romania data and the Euclidean heuristic.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "search_romania_tests.py", line 245, in run_romania_test
    self.assertTrue(verdict, msg=err)
AssertionError: False is not true : Path ['o', 'z', 'a', 's', 'r', 'p'] for goal nodes ('o', 'p') does not match reference. Path cost was 463 and expected path cost was 328. Expected path is ['o', 's', 'r', 'p']


$\pi(v)$ : estimated distance from v to target
	$\pi_f(v)$ estimated v -> t
	$\pi_r(v)$ estimated s -> v
$d(v)$: distance from start to v
$k(v)$: estimated shortest s-t path via v



======================================================================
FAIL: test_tri_ucs_romania (__main__.SearchRomaniaTests) (case=('h', 'i', 'o'))
Test Tri-UC search with Romania data.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "search_romania_tests.py", line 245, in run_romania_test
    self.assertTrue(verdict, msg=err)
AssertionError: False is not true : Path ['h', 'u', 'b', 'p', 'r', 's', 'o', 's', 'r', 'p', 'b', 'u', 'v', 'i'] for goal nodes ('h', 'i', 'o') does not match reference. Path cost was 1360 and expected path cost was 944. Expected path is ['i', 'v', 'u', 'h', 'u', 'b', 'p', 'r', 's', 'o']

the best path:  ['h', 'u', 'b', 'p', 'r', 's', 'o', 's', 'r', 'p', 'b', 'u', 'v', 'i']
