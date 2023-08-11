---
weight: 1
title: ""
---

Spring System
-------------

1) What are the pros and cons of object orientation in the context
   of designing an Operating System?  Explain the approach taken in Spring.

2) Explain the basic abstractions supported by the nucleus of Spring.
   Compare the microkernel in Spring with Liedtke's recommendation
   on microkernel construction.

3) What is the role played by subcontract in the Spring system?  Explain
   with example scenarios (such as singleton and replicated implementation
   of servers).

4) Explain the security model of Spring.  How does this facilitate 
   secure object invocation?

5) What is the relation between the address space, pager, cache,
   and memory objects in the Spring system?  How do they work together
   to provide the virtual memory support in Spring?

6) Discuss the Spring File System (SFS) and its relationship to the virtual
   memory system.  What is semantically different about SFS compared to NFS?

Distributed Object Model for Java
---------------------------------

1) Summarize the similarities and differences between the Java object model
   and its distributed counterpart.

2) Explain with justification the difference in the semantics for the
   default implementations for some of the methods of the "Object class"
   for remote objects.

3) Explain with justification the difference in the semantics of
   parameters passing for remote Java objects compared to local ones.

4) What are the transport level abstractions in the RMI system?
   Explain the choice of these abstractions with respect to the RMI
   semantics.

5) Explain how garbage collection works in Java in the presence of
   remote objects.

6) Compare the Java remote object model to CORBA.

Enterprise Java Beans
---------------------

1) Explain the term "Java Beans".  What are N-tier applications?
   How are Java Beans useful in constructing such applications?

2) What is reflection as it pertains to Java Beans?  How is this
   useful in building complex web applications?  Illustrate with
   an example.

3) The paper describes 5 different implementation methods for an
   EJB application.  Discuss qualitatively the pros and cons of each
   method.

4) From the qualitative discussion in question 3, hypothesize the
   expected performance of each of the implementation choices.

5) At a high level compare your hypothesis with the actual performance
   results presented in the paper.
