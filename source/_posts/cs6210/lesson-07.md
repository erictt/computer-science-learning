# Lesson 7: Distributed Subsystems

Outline:
- GMS: How can we use peer memory for paging across LAN?
- DSM: Can we make the cluster appear like a shared memory machine?
- DFS: How to use cluster memory for cooperate caching of files?

## L07a: Global Memory Systems(GMS)

In a working set of multiple machines connected to LAN, some machines have more memory presure than the others. To utilize the memory from other machines to alleviate the busy ones is the main goal of GMS. The assumption is accessing the local disks take much more time than using the memory for paging accross the network. (Modern LANs can provide Gigabit or even 10 Gigabit connectivity between nodes, which can make it faster to access data from remote nodes than accessing data from a local disk.) In addition, we want to use idl cluster memory for other nodes in the network.

Comparing to tradition memory management: virtrual address -> physical address or disk, GMS trades network communication for disk I/O, changes the mapping to: virtrual address -> physical address or cluster memory or disk.

GMS only works for read across the network. The only pages that been paged out to the cluster memories are not dirty. GMS only serves as another level in the memory hierachy. The disk always has all of the copies of the pges.

### Basics

- In GSM, "cache" refers to physical memory, specifically dynamic random access memory (DRAM).
- Physical memory at each node is split into "local" (working set of currently executing processes) and "global" (community service for holding swapped out pages from fellow nodes).
- The split between local and global is dynamic and responds to memory pressure.
* Pages can be private or shared, and shared pages are the concern of the application for maintaining the **page coherence**.
	- The pages in "global" are always private to some processes.
	- The pages in "local" can be private or shared among multiple processes.
- GSM serves as a paging facility for remote paging and uses a page replacement algorithm (typically LRU) to manage memory.
- One of the key technical contributions of GSM is managing age information to pick the globally oldest page for replacement in the community service for handling page faults.

### Handling Page Faults 

#### Case 1

![](https://i.imgur.com/JADVQuh.png)
- Physical memory on each host is divided into local and global parts.
- Page fault handling in GMS involves finding if the page is in the global cache of another node in the cluster.
- If the page is found in another node's global cache, that node sends the page to the requesting node.
- The requesting node's local allocation of physical memory increases by one.
- To make space for the new page, the requesting node sends the oldest page from its global cache to the node that had the requested page in its cache.
- The global allocation (community service part) of the requesting node decreases by one, while the global allocation of the sending node remains unchanged.

#### Case 2

![](https://i.imgur.com/XSHGtGw.png)

- In this case, there is no community service happening on host P due to high memory pressure.
- If there is another page fault, the only option is to throw out some page from its current working set to make room for the missing page.
- The victim candidate for the page is chosen from the local part of host P.
- The oldest page from the local part of host P is sent out as a victim.
- The distribution of local and global on host P remains unchanged, as global is already zero.
- There is no change on host Q in terms of the split between local and global.

#### Case 3

![](https://i.imgur.com/30dNwHF.png)
- In this case, the faulting page is not available in the cluster memories and needs to be fetched from disk.
- The local allocation of physical memory on host P increases by one as the working set grows due to the page fault.
- To make room for the new page, the global allocation on host P decreases by one and the oldest page from the global cache is sent to a peer memory in the cluster.
- The peer memory that receives the replacement page could be either in the local or global part of the host.
- If the oldest page on the peer memory is in the global cache, it is discarded. If it is in the local part, it could be dirty and needs to be written back to disk.
- The local allocation of physical memory on the peer memory could decrease if the globally oldest page is in the local part and can be thrown out.
- The local and global allocation on host P changes as described above, while the allocation on the peer memory could remain unchanged or decrease depending on the globally oldest page.

#### Case 4

![](https://i.imgur.com/ONGX0Ip.png)

- In this case, a page is actively shared between host P and host Q.
- When a page fault occurs on host P for page X, GMS finds that page X is in the local cache of host Q and makes a copy of it into the local cache of host P.
- The working set on host P increases, so the local allocation of physical memory on host P goes up by one and the global allocation goes down by one.
- GMS picks an arbitrary page from the global cache on host P to send to the host R that has the globally oldest page.
- The total memory pressure in the cluster goes up by one, so host R must pick an LRU candidate from its physical memory to send to the disk and make room for the incoming page from host P.
- If the LRU candidate comes from the local cache of host R, the working set on host R decreases and the local allocation goes down by one, while the global allocation goes up by one.
- The active sharing of page X between host P and host Q does not concern GMS for maintaining coherence between the copies on multiple nodes.

### Local and Global Boundary

![](https://i.imgur.com/PF6RiZy.png)

- In all cases except where the global part of the faulting node's cache is empty, the local part goes up by one and the global part comes down by one.
- When the faulting page is in the global cache of a different node, there is no change in the balance between local and global on either node.
- If the faulting page is on disk, we have to make space in the cluster memory by throwing out a page, and if the LRU page on the node with the globally oldest page is in the local cache, the local part goes down by one and the global part goes up by one.
- If the page is actively shared, there is no change in the balance between local and global on either node, but one of the node's global pages has to be sent to the node with the globally oldest page, and if the replacement candidate comes from the local cache, the local part shrinks by one and the global part increases by one to accommodate the new page.

### Behavior of Algorithm

- The behavior of GMS global memory management is dynamic, not static.
- The split between local and global cache changes based on the memory pressure at a particular node.
- Idle nodes with a decreasing working set can become memory servers for peers on the network.
- The algorithm does not handle coherence maintenance, which must be managed at a higher level of software.
- The global cache acts as a surrogate for the disk, providing faster access to pages than the disk itself.
- The algorithm optimizes memory usage by swapping pages between nodes in the LAN.

### Geriatrics!(Age management)

![](https://i.imgur.com/XAZXJfL.png)

- Age management is a critical part of the GMS system, as it determines which pages should be evicted and replaced with new pages.
- The age of a page represents how long it has been since it was last accessed, with smaller ages indicating more recently accessed pages.
- The GMS system breaks age management into epochs, which are time periods during which management work is done by a single node.
- The duration of an epoch is set by the parameter T, which is the maximum duration that an epoch can last.
- The epoch management work is either time-bound (limited by T) or space-bound (limited by M replacements). M is another parameter that represents the maximum number of page replacements that can occur in an epoch.
- At the beginning of each epoch, each node sends its age information to the initiator node. This includes the age of all local and global pages residing on the node.
- The initiator node calculates the minimum age of the M pages that will be replaced in the upcoming epoch. It also computes the weight for each node, which represents the fraction of replacements that will come from that node.
- The node with the highest weight becomes the initiator for the next epoch.
- When a page fault occurs, the node checks the age of the page that needs to be replaced. If the age is greater than the minimum age, the page is discarded. If it is less than the minimum age, the node sends the page to a peer node based on the weight distribution.
- By using age management to approximate a global LRU (Least Recently Used) algorithm, the GMS system ensures that older pages are evicted and replaced with newer pages, thus improving overall system performance.
- The GMS system also follows the principle of thinking globally but acting locally, where global information is used to make local decisions.

### Implementation in Unix

![](https://i.imgur.com/hD6Yv6m.png)

- In systems research, identifying a pain point and coming up with a clever solution is important.
- Implementing the solution, even if it's a simple idea, requires heavy lifting and technical details.
- Implementation tricks and techniques can be reusable knowledge for other systems research.
- The authors of GSM used the OSF/1 operating system by DEC(Digital Equipment Corporation) operating system as the base system for their memory management system.
- The OSF/1 memory system has two key components: the virtual memory system (VM) and the unified buffer cache (UBC).
- The virtual memory system (VM) is responsible for mapping process virtual address space to physical memory, and the unified buffer cache (UBC) is used by the file system to cache disk-resident files in physical memory.
- The GMS implementation required modifying both the VM and UBC components of the operating system to support the global memory system.
- Writing pages to disk remains unchanged in the GMS implementation, as only page faults are redirected to the cluster memory.
- Collecting age information for anonymous pages in the VM is challenging since the operating system doesn't see individual memory accesses made by a user process. To address this, the GMS implementation includes a daemon that periodically dumps the contents of the Translation Lookaside Buffer (TLB) to collect age information for anonymous pages.
- The GMS implementation also includes modifications to the pageout daemon and free list maintenance for allocating and freeing frames on each node.
- The technical details of how GMS integrates with the VM, UBC, and other components of the operating system are important and may be reusable knowledge for other systems research.

### Data Structures

![](https://i.imgur.com/UNrPfGS.png)

- GMS uses distributed data structures for virtual memory management across the cluster.
- The virtual address is converted into a universal ID (UID) to uniquely identify a virtual address.
- Three key data structures are used: PFD (Page frame Directory), GCD (Global Cache Directory), and POD (Page Ownership Directory).
- The **POD tells which node owns which pages**, and it is replicated on all nodes in the cluster. The **GCD maps UIDs (unique identifiers for virtual addresses) to the nodes that host the corresponding PFDs**. The **PFD contains the mapping between UIDs and page frame numbers (PFNs)** and is stored on the node that owns the page.
- When a **page fault occurs**, the node first converts the virtual address to a UID and uses the POD to determine the owner of the page. It then uses the GCD to find the node that hosts the PFD for that UID and sends the UID to that node. The node with the PFD retrieves the page and sends it back to the requesting node.
	- ![](https://i.imgur.com/FA1JAou.png)
	- Node A converts virtual address to UID and goes to page ownership directory (POD)
	- POD tells Node A who the owner of the page is (Node B), which has the Global Page Frame Directory (GCD)
	- Node B looks up its GCD and sends UID to node C, which has the Page Frame Directory (PFD) for that UID
	- Node C retrieves the page, sends it to Node A, which maps it and resumes the process
- Network communication occurs only when there is a page fault, and most page faults are for non-shared pages, meaning the POD and GCD are co-resident on the same node. In this case, there is no network communication to look up the GCD.
- There can be a **miss when requesting a page**, which can happen if the page has been evicted from the PFD or if the POD information is stale due to changes in the network. In these cases, the request can be retried after looking up the updated POD or GCD.
	- ![](https://i.imgur.com/Ie6o0Rf.png)
	- Misses are uncommon compared to page faults, and network communication is mostly local to the node
- To handle **page evictions**, each node has a paging daemon that puts evicted pages onto a candidate node based on weight information obtained from the geriatric management system (GMS). The paging daemon also coordinates with the GMS to update the GCD with the new PFD location for the corresponding UID. This happens in an aggregated manner when the free list falls below a threshold.
	- ![](https://i.imgur.com/e1KKUws.png)

### Conclusion

The concept of paging across a network is interesting but may not be feasible in certain environments such as individual-owned workstations. However, it may be feasible in large-scale clusters in data centers. The enduring aspects of this research are the techniques, distributed data structures, and algorithms for implementing the concept. The next lesson module will feature another thought experiment on using cluster memory.

## L07b: Distributed Shared Memory

## Introduction

- Distributed Shared Memory (DSM) is a software implementation that provides the illusion of shared memory to applications in a distributed system.
- DSM allows exploiting remote memories in a cluster to make it appear as a shared memory machine, simplifying application development.
- DSM works by creating an operating system abstraction that provides the illusion of shared memory to applications, even though nodes in the local area network do not physically share memory.

## Cluster as a Parallel Machine 

### Sequential Program

![](https://i.imgur.com/2o38mhX.png)

- To exploit a cluster starting from a sequential program, one possibility is automatic parallelization, which means writing a sequential program and letting a tool identify opportunities for parallelism and map it to the cluster.
- Automatic parallelization is an example of implicitly parallel programming, where the program is not written explicitly in parallel but the tool identifies opportunities for parallelism and maps it to the cluster.
- High Performance Fortran is an example of a programming language that does automatic parallelization, where the user uses directives for distribution of data and computation.
- Automatic parallelization works well for certain classes of programs called data parallel programs, where the data accesses are fairly static and determinable at compile time.

### Message Passing

![](https://i.imgur.com/tPeuuQC.png)

- The other way to exploit a cluster is to write the program as a truly parallel program, or explicitly parallel program, where the application programmer thinks about the application and writes the program explicitly in parallel.
- There are two styles of explicitly parallel programs: message passing style and shared memory style.
- The message passing style of explicitly parallel program is true to the physical nature of the cluster, where every processor has its private memory and cannot directly access the memory of another processor. It uses a message passing library that provides primitives for application threads to do sends and receives to peers executing on other nodes of the cluster.
- Examples of message passing libraries include MPI, PVM, and CLF from Digital Equipment Corporation, and many scientific applications running on large scale clusters use this style of programming using MPI as the message passing fabric.
- The downside to the message-passing style of programming is that it is difficult to program, as it requires the programmer to think in terms of coordinating the activities on different processes by explicitly sending and receiving messages from their peers, which is a radical change of thinking in terms of how to structure a program.

### DSM

![](https://i.imgur.com/MZj30m5.png)

- The DSM abstraction is a way of giving the illusion to the application programmer that all of the memory in the entire cluster is shared, even though it is not physically shared.
- The DSM library provides a shared memory semantic to the application program, allowing for an easier transition path from a sequential program or program written on an SMP to a program that runs on the cluster.
- The DSM abstraction eliminates the need for marshaling and unmarshaling arguments being passed from one processor to another, as all of that is handled by the fact that there is shared memory.
- The DSM abstraction gives the same level of comfort to a programmer who is used to programming on a true shared memory machine when they move to a cluster, as they can use the same set of primitives for synchronization and thread creation.
- The advantage of DSM style of writing an explicitly parallel program is that it allows for thinking in terms of shared memory, sharing pointers across the entire cluster, and using locks and barriers for synchronization.

### History of Shared Memory Systems

- The history of shared memory systems over the last 20+ years shows the space occupied by the efforts to build shared memory systems in hardware and software.
- Software DSM was first thought of in the mid-80s, with systems like Ivy, Clouds Operating System, and similar systems built at UPenn.
- In the early '90s, systems like Munin and TreadMarks were built, followed by Blizzard, Shasta, Cashmere, and Beehive in the later half of the '90s.
- Structured DSM provided a higher-level abstraction than just memory to computations that needed to be built on a cluster. Systems like Linda, Orca, Stampede, and PTS were built in the early to mid-'90s.
- Early hardware shared memory systems like BBN Butterfly and Sequent Symmetry appeared in the market in the mid-'80s, followed by KSR-1, Alewife, and DASH in the early to mid-'90s.
- Commercial versions of distributed shared memory machines like SGI Origin 2000 and SGI Altix were built, with thousands of processors in the latter.
- IBM Bluegene is another example of a shared memory system, and clusters of SMPs have become the workhorses in data centers.
- It is important to reflect on the progress made in shared memory systems and learn about the details of machines built in the past, either in hardware or software.

## Shared Memory Programming

![](https://i.imgur.com/pcKtHIu.png)

- Shared memory programming uses synchronization primitives like locks and barriers to protect data structures so that one thread can exclusively modify the data.
- Mutual exclusion locks and barrier synchronization are popular synchronization primitives used in shared memory programming.
- There are two types of memory accesses that happen in a shared memory program - normal reads and writes to shared data and accesses to synchronization variables used in implementing locks and barriers.
- The operating system or user-level threads library provides mutual exclusion locks or barrier primitives, and in implementing those synchronization primitives, algorithms use reads and writes to shared memory.

### Memory Consistency and Cache Coherence

- Memory consistency model is a contract between the application programmer and the system that answers the "when" question - how soon changes made to a shared memory location by one processor will be visible to other processes that have the same memory location in their respective private caches.
- Cache coherence answers the "how" question - how is the system, i.e., system software plus hardware, implementing the contract of the memory consistency model?
- Cache coherence mechanism ensures that all processes see the changes made to shared memory, commensurate with the memory consistency model.
- In parallel programming, coherence mechanism must fulfill the guarantee made by the memory consistency model to the application programmer.

### Sequential Consistency

![](https://i.imgur.com/7l4Gg7n.png)

- In sequential consistency, memory accesses are expected to happen in textual order on individual processors but the interleaving of memory accesses from different processors is arbitrary.
- The memory model preserves atomicity for individual read-write operations and honors the program order.
- SC memory model doesn't distinguish between data accesses and synchronization accesses.

### SC Memory Model:

![](https://i.imgur.com/MjZGeN3.png)

- SC memory model doesn't know the association between locks and data structures.
- Coherence action is taken on every read-write access, which leads to more overhead and poorer scalability.

###  Typical Parallel Program:

![](https://i.imgur.com/J1llQoD.png)

- A typical parallel program involves getting a lock for accessing data structures and releasing it after the critical section.
- The SC memory model doesn't differentiate between synchronization and data accesses.
- Coherence action is taken on every access even if it's not warranted until the lock is released.

###  Release Consistency:

![](https://i.imgur.com/1CQmKvJ.png)

- Release consistency is a memory consistency model that distinguishes between synchronization and data accesses.
- Every critical section consists of acquire, data accesses governed by the lock, and release.
- Coherence actions prior to the release operation by P1 have to be complete before P2 acquires the same lock.
- Barrier synchronization can also be mapped to acquire and release.

###  RC Memory Model:

![](https://i.imgur.com/ym1Xrc4.png)


- RC memory model distinguishes between normal data accesses and synchronization accesses.
- It initiates coherence actions corresponding to normal data accesses but doesn't block the processors.
- It only takes coherence action when a release synchronization operation is encountered.

### Distributed Shared Memory Example

![](https://i.imgur.com/SVq87tU.png)


- RC memory model allows for parallel modifications to shared data structures
- Program example: one thread modifies structure A while another waits and then uses it
- P2 waits on a condition variable and releases a lock until P1 signals that the modification is done
- Coherence actions are only completed before releasing the lock

### Advantage of RC over SC

- RC memory model allows for overlapping of computation with communication
- Better performance in shared memory machines compared to SC memory model

### Lazy RC

![](https://i.imgur.com/LXs0SJT.png)

- Lazy RC defers coherence actions to the point of lock acquisition rather than lock release
- Overlapping of computation with communication is still possible in the window of time between lock release and lock acquisition

### Eager vs Lazy RC

![](https://i.imgur.com/lctRnu6.png)


- Vanilla RC is the eager release consistent memory model while LRC is the lazy release consistent memory model
- Eager RC broadcasts changes to all processors while Lazy RC only communicates with the necessary processors through point-to-point communication

### Pros and Cons of Lazy and Eager Release Consistency Model

- A system is release consistent if specific operations are performed before ordinary access or release is allowed to perform with respect to any other processor
- Eager release consistency: A processor delays propagating its modification to shared data until it comes to a release.
- Lazy release consistency: The propagation of modifications is postponed until the time of the acquire.
- Lazy release consistency reduces the number of messages and data transferred between processors, which is especially significant for programs that exhibit false sharing and make extensive use of locks.

### Software DSM

![](https://i.imgur.com/vBEaWiw.png)


- In a computational cluster, each node has its private physical memory, and there is no physically shared memory.
- The DSM software implements the consistency model to the programmer.
- DSM software implements sharing and coherence maintenance at the level of pages.
- DSM software provides a global virtual memory abstraction to the application program.
- DSM software handles coherence maintenance by having distributed ownership for the different virtual pages.
- Local physical memories available in each processor host portions of the global virtual memory space in the individual processors commensurate with the access pattern of the application on the different processors.
- The DSM software handles the coherence maintenance of individual pages.
- Early examples of systems that built software DSM include Ivy, Clouds, Mirage, and Munin.
- Single-writer multiple-reader protocol is used where multiple readers can share a page at any point of time, but a single writer is only allowed to have the page at any point of time.
- False sharing can occur where data appears to be shared even though programmatically they are not.
- Page-level granularity and single-writer multiple-reader protocol don't live happily together and will lead to false sharing and ping-ponging of pages.

### LRC with Multi Writer Coherence Protocol

![](https://i.imgur.com/9ipNyv3.png)

- A new coherence protocol is introduced which allows multiple writers to write to the same page while maintaining coherence at the granularity of pages
- The granularity of coherence maintenance is chosen as a page because it matches the operating system's granularity and allows DSM to be integrated with the operating system
- The Treadmarks system uses lazy release consistency (LRC) with multiple writer protocol
- In LRC, the DSM invalidates pages that were modified by the previous lock holder before allowing a new lock holder to modify the same pages
- The DSM software creates diffs of the changes made to pages within a critical section and applies these diffs to the original version of the page when a new lock holder accesses the page
- The DSM software applies all the diffs made by previous lock holders to the original page to create the current version of the page for the new lock holder
- The DSM software brings in the diffs at the point of access to avoid unnecessary communication
- The LRC protocol allows bringing in only what is needed and only invalidating pages that may have been modified
- If multiple processors modify a page under the same lock, the DSM software applies all the diffs made by previous lock holders to the original page to create the current version of the page for the new lock holder
- The DSM software brings in the diffs at the point of access to avoid unnecessary communication
- The DSM software invalidates pages modified by the previous lock holder before allowing a new lock holder to modify the same pages
- The multiple-writer coherence protocol allows multiple users to access different portions of the same page using different locks
- The DSM software only applies the diffs made under the same lock to the original page for the new lock holder
- Multiple threads can modify the same page as long as they use different locks, and the DSM software only applies the diffs made under the same lock to the original page for the new lock holder
- The association between changes made to a page is only specific to the lock governing that critical section

#### Implementation

![](https://i.imgur.com/acchRwm.png)

- When a process or thread tries to write to a page X, the operating system creates a twin for that page and makes the original page writeable by that process.
- When the thread reaches the release point, the DSM software computes the diff between the original and modified versions of the page.
- When the same block governing accesses to the released page is acquired by a different processor, all pages touched in the critical section are invalidated, including X.
- When a processor has a page fault for X, the DSM software knows there is a diff on another node needed to update the page for the current lock acquirer.
- Once the thread in the critical section completes its release operation, the original page is write-protected and the twin is removed.
- If multiple writers are modifying the same page under different locks, it is an application problem and represents a data race.
- TreadMarks implemented this LRC multiple writer coherence protocol on a Unix system.
- The DSM software catches an exception called SIGSEGV when a shared page is accessed by a thread and gets into gear.
- There is space overhead for creating a twin at the point of write and creating a diff data structure at release.
- Garbage collection is used to reduce the space overhead by periodically applying diffs to the original copy of the page and getting rid of them.

### Non Page Based DSM

![](https://i.imgur.com/tq2pE8U.png)


- Non-page based DSM systems do not use granularity of a page for coherence maintenance.
- Library-based approach uses programming framework/library to annotate shared variables, and generates a trap at point of access to contact DSM software for coherence action.
- Structured DSM provides abstractions manipulated using API calls that take coherence actions at the point of call execution.

### Scalability

![](https://i.imgur.com/EfXq8fF.png)


- DSM provides a programming model that looks and feels like a shared memory threads package, but performance does not necessarily scale up as we increase the number of processors in the cluster.
- Overhead increases with the number of processors, and this buildup of overhead happens in true memory multi-processors.

### DSM and Speedup

![](https://i.imgur.com/qxvVk16.png)


- The computation to communication ratio must be high for any hope of speed up with DSM.
- If sharing is too fine-grained, there is no hope of speed up, especially with DSM systems that are only an illusion of shared memory via software.
- Pointer codes may result in increasing overhead for coherence maintenance in DSM in a local area network.

### Distributed Shared Memory Conclusion

- DSM as originally envisioned, that is a threads package for a cluster, is dead.
- Structured DSM, which provides higher-level data abstractions for sharing among threads, is attractive to reduce programming pain for developers of distributed applications on a cluster.

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