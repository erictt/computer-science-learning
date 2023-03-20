# Lesson 7: Distributed Subsystems

Outline:
- GMS: How can we use peer memory for paging across LAN?
- DSM: Can we make the cluster appear like a shared memory machine?
- DFS: How to use cluster memory for cooperate caching of files?

## L07a: Global Memory System

page out the unused pages to other nodes in the cluster

no dirty cache in remote memory
    cache -> physical memory(i.e. DRAM)
local disk has whole pages.

in local can be private or shared.
pages in global are private copies

page coherence is the problem of the application. GMS only responsible for paging.

use LRU for purge global oldest page
    oldest can be in local or global 

page fault handling - case 1

## L07a: Global Memory Systems(GMS)

### Basics



### Handling Page Faults 

#### Case 1
#### Case 2
#### Case 3
#### Case 4

### Local and Global Boundary
### Behavior of Algorithm
### Geriatrics!

### Implementation in Unix

### Data Structures

### Putting the Data Structures to Work

### Conclusion


## L07b: Distributed Shared Memory

1. Distributed Shared Memory Introduction
2. Cluster as a Parallel Machine (Sequential Program)
3. Cluster as a Parallel Machine (Message Passing)
4. Cluster as a Parallel Machine (DSM)
5. History of Shared Memory Systems
6. Shared Memory Programming
7. Memory Consistency and Cache Coherence
8. Sequential Consistency
9. SC Memory Model
10. Typical Parallel Program
11. Release Consistency
12. RC Memory Model
13. Distributed Shared Memory Example
14. Advantage of RC over SC
15. Lazy RC
16. Eager vs Lazy RC
17. Pros and Cons of Lazy and Eager
18. Software DSM
20. LRC with Multi Writer Coherence Protocol
23. Implementation
25. Non Page Based DSM
26. Scalability
27. DSM and Speedup
28. Distributed Shared Memory Conclusion

## L07c: Distributed File Systems

### Outline

5. Preliminaries (Striping a File to Multiple Disks)
6. Preliminaries (Log Structured File System)
7. Preliminaries Software (RAID)
8. Putting Them All Together Plus More
9. Dynamic Management
10. Log Based Striping and Stripe Groups
11. Stripe Group
12. Cooperative Caching
13. Log Cleaning
14. Unix File System
15. xFS Data Structures
16. Client Reading a File Own Cache
17. Client Writing a File
18. Distributed File Systems Conclusion