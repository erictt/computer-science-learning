# Week 5 \(Telling the Story of Euler Circuit Theorem\)

## From Königsberg Bridges to Graphs

* My answer:
  * The Königsberg Bridges problem illustrate a map which has three isolated lands connected with bridges. Land A has 2 bridges to B and 1 bridge to C, B has 1 bridge to C and 2 bridges to D, and C has 1 bridge to D. The question is, can you transverse all the bridges exactly once, and go back to start land? To understand the question deeply, we can abstract the map to point and lines, and take every point as a vertex, every line as an edge.

## Isolating a Concept: Degree of a Vertex

* My answer:
  * After several attempts,  we got the conclusion that whatever we tried, we always stuck on some vertices, away from the start vertex, and some edges left. Seems like, we can only leave a vertex, but no way to come back if it only has odd edges connect to it. Then another concept come out, the Degree of a Vertex, which is the number of connected edges to a certain vertex. In the Königsberg Bridges problem, we know this: the degree of A is 3, the degree of B is 5, the degree of C is 3, the degree of D is 3. 

## Raise Questions: Euler Circuit Conjecture

* My answer:
  * For example, if we start at A, and leave, come back, then leave again, there is no way to come back, we are going to stuck at somewhere else. So we get this conclusion: if the degree of the first vertex is odd, we can't perform the circuit, no mater how many the degrees of other vertices are. 
  * Now we got a question. What if the degree of the first vertex is even, and there is one vertex somewhere else has an odd degree? 
  * Let's see. Use the conclusion we got before. If we got this vertex with odd degree, leave, come back, then there is no way to leave, we stuck in the vertex. So to be more precise, the conclusion should be: if there is an odd degree in the circuit, then it's impossible to trace all the edges wherever you start it. This is another concept: Euler Circuit Conjecture.

## Make Mistakes: Go Until Stuck

* My answer:
  * There is another situation. What if the degrees of all the vertices are even. Is it possible that wherever we start, we will always come back to the vertex we start? 
  * Let's start with a certain vertex with degree 4: go out, come back, go out, and then come back. Seems like, if the degree of a vertex is even, it can come back in the future. So if all of the vertices have even degrees, they will all have a way to come back to themselves. But is it going to get back to the start vertex? In the Euler Circuit Conjecture, we know that we will be stuck at the vertex with odd degree eventually. So in our situation, when you start to traverse the first edge, which left the last one with odd degrees. And We also know that it won't be stuck at the vertex with even degrees. So when we traversed other edges, it will eventually be stuck with the one with odd degrees.

## Persist: Proving the Euler Circuit Theorem

* My answer:
  * Imagine the graph is a huge map, and you can't just try every possibility to see if it is true that we will always come back if all of the vertices have even degrees. What are you going to do? 
  * Try it with parts of the map, and then step by step to enlarge the partials. If we can prove the conclusion works in partials, then we can say that it will works in larger partials too. And in the end, the whole map works.
  * Let's start with a single vertex, the first job is to only traverse all of the edges it connected with. Then, to enlarge the map, we start with the vertex that we've already covered and still has available edges but only focus on traversing all of the left edges. Eventually, we will cover the whole map by parts. The next step is to try to splice two parts in once, then three parts in once. Seem like, we can use this strategy to cover the whole map in once. In the end, we proved the Euler Circuit Theorem, which says that if you have a connected graph where every vertex has even degree, then it's possible to start at any vertex, traverse all of the edges in the graph, never going over the same edge twice, and returning to where we started.
  * Now, let's review the whole question.
  * First, we abstracted the map to points and lines, just tried to understand the question deeply.
  * Then, we did several attempts, but always got stuck somewhere. Even we are frustrated but also got some clues. We found out all of the points connected with odd lines. To get better illustrating, we come out some concepts, like vertex, edge and the degree of the vertex. If there are some vertices has odd degree,  we can't transverse all the edges.
  * Last, to get a better understanding of this problem, we raised two questions. The first one is some of the vertices have odd degree, some don't. The last one is all of the vertices have even degree. In the process of figuring out the questions.
  * We learned:
    * Extracting the essence will help us to find the key to the question.
    * Make mistakes also can help us to understand the question.
    * It is always a good try with old strategy. 
    * Start with partials if the question is too big.

