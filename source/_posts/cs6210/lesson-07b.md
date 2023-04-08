# Lesson 7: Distributed Subsystems - Distributed Shared Memory

Can we make the cluster appear like a shared memory machine?

## Introduction

- Distributed Shared Memory (DSM) is a **software implementation** that provides the illusion of shared memory to applications in a distributed system.
- DSM allows exploiting remote memories in a cluster to make it appear as a shared memory machine, simplifying application development.
- DSM works by creating an operating system abstraction that provides the illusion of shared memory to applications, even though nodes in the local area network do not physically share memory.

## Cluster as a Parallel Machine 

### Sequential Program

<img src="https://i.imgur.com/2o38mhX.png" style="width: 800px" />

- To exploit a cluster starting from a sequential program, one possibility is automatic parallelization, which means writing a sequential program and letting a tool identify opportunities for parallelism and map it to the cluster.
- Automatic parallelization is an example of implicitly parallel programming, where the program is not written explicitly in parallel but the tool identifies opportunities for parallelism and maps it to the cluster.
- High Performance **Fortran** is an example of a programming language that does automatic parallelization, where the user uses directives for distribution of data and computation.
- Automatic parallelization works well for certain classes of programs called data parallel programs, where the data accesses are fairly static and determinable at compile time.

### Message Passing

<img src="https://i.imgur.com/tPeuuQC.png" style="width: 800px" />

- The other way to exploit a cluster is to write the program as a truly parallel program, where the application programmer thinks about the application and writes the program explicitly in parallel.
- There are two styles of explicitly parallel programs: **message passing** style and **shared memory** style.
- The message passing style is true to the physical nature of the cluster, where every processor has its private memory and cannot directly access the memory of another processor. It uses a message passing library that provides primitives for application threads to do sends and receives to peers executing on other nodes of the cluster.
- Examples of message passing libraries include MPI, PVM, and CLF from Digital Equipment Corporation, and many scientific applications running on large scale clusters use this style of programming using MPI as the message passing fabric.
- The downside to the message-passing style of programming is that it is difficult to program, as it requires the programmer to think in terms of coordinating the activities of different processes by explicitly sending and receiving messages from their peers, which is a radical change of thinking in terms of how to structure a program.

### DSM

<img src="https://i.imgur.com/MZj30m5.png" style="width: 800px" />

- The DSM abstraction is a way of giving the illusion to the application programmer that all the memory in the entire cluster is shared, even though it is not physically shared.
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

<img src="https://i.imgur.com/pcKtHIu.png" style="width: 800px" />

- Shared memory programming uses synchronization primitives like locks and barriers to protect data structures so that one thread can exclusively modify the data.
- **Mutual exclusion locks and barrier** synchronization are popular synchronization primitives used in shared memory programming.
- There are two types of memory accesses that happen in a shared memory program:
	1. Normal reads and writes to shared data;
	2. Accesses to synchronization variables used in implementing locks and barriers.
- The operating system or user-level threads library provides mutual exclusion locks or barrier primitives, and in implementing those synchronization primitives, algorithms use reads and writes to shared memory.

### Memory Consistency and Cache Coherence

- **Memory consistency** model is a contract between the application programmer and the system that answers when **the changes made to a shared memory location by one processor** will be **visible to other processes** that share the same memory location in their respective private caches. It deals with the ordering and visibility of memory operations (like read, write, and atomic operations) across different processors or cores in a multiprocessor system.
- **Cache coherence** addresses the problem that arises when multiprocessors have their own **private caches**. When a shared memory location that is cached by other processors, it can lead to inconsistent data across the caches. Cache coherence ensures all caches have a consistent view of the shared memory.
- In parallel programming, the coherence mechanism must fulfill the guarantee made by the **memory consistency model to the application programmer**.

### Sequential Consistency

<img src="https://i.imgur.com/7l4Gg7n.png" style="width: 800px" />

- In sequential consistency, memory accesses are expected to happen in textual order on individual processors, but the interleaving of memory accesses from different processors is arbitrary.
- The memory model preserves atomicity for individual read-write operations and honors the program order.
- SC memory model **doesn't distinguish between data accesses and synchronization accesses**.

#### SC Memory Model

<img src="https://i.imgur.com/MjZGeN3.png" style="width: 800px" />

- SC memory model *doesn't know the association between locks and data structures*.
- *Coherence action is taken on every read-write access*, which leads to more overhead and poorer scalability.

###  Typical Parallel Program

<img src="https://i.imgur.com/J1llQoD.png" style="width: 800px" />

- A typical parallel program involves getting a lock for accessing data structures and releasing it after the critical section.
- **Coherence action is taken on every access**, even if it's not warranted until the lock is released.

###  Release Consistency(RC)

<img src="https://i.imgur.com/1CQmKvJ.png" style="width: 800px" />

- Release consistency is a memory consistency model that distinguishes between synchronization and data accesses.
- Every critical section consists of acquire, data accesses governed by the lock, and release.
- Coherence actions prior to the release operation by P1 have to be complete before P2 acquires the same lock.
- **Barrier synchronization can also be mapped** to acquire and release.

####  RC Memory Model

<img src="https://i.imgur.com/ym1Xrc4.png" style="width: 800px" />


- It initiates coherence actions corresponding to normal data accesses, but doesn't block the processors.
- It **only takes coherence action when a release synchronization operation** is encountered.

### Distributed Shared Memory Example

<img src="https://i.imgur.com/SVq87tU.png" style="width: 800px" />


- RC memory model allows for parallel modifications to shared data structures
- Program example: one thread modifies structure A while another waits and then uses it
- P2 waits on a condition variable and releases a lock until P1 signals that the modification is done
- Coherence actions are only completed before releasing the lock

### Advantage of RC over SC

- RC memory model allows for overlapping of computation with communication
- Better performance in shared memory machines compared to SC memory model

### Lazy RC

<img src="https://i.imgur.com/LXs0SJT.png" style="width: 800px" />

- Lazy RC **defers coherence actions** to the point of lock **acquisition** rather than lock release
- Overlapping of computation with communication is still possible in the window of time between lock release and lock acquisition

### Eager vs Lazy RC

<img src="https://i.imgur.com/lctRnu6.png" style="width: 800px" />


- Vanilla RC is the eager release consistent memory model while LRC is the lazy release consistent memory model
- Eager RC broadcasts changes to all processors while Lazy RC only communicates with the necessary processors through point-to-point communication

### Pros and Cons of Lazy and Eager Release Consistency Model

- A system is release consistent if specific operations are performed before ordinary access or release is allowed to perform with respect to any other processor
- Eager release consistency: A processor delays propagating its modification to shared data until it comes to a release.
- Lazy release consistency: The propagation of modifications is postponed until the time of the acquire.
- Lazy release consistency **reduces the number of messages and data transferred** between processors, which is especially **significant for** programs that *exhibit false sharing and make extensive use of locks*.

### Software DSM


<img src="https://i.imgur.com/NabK1PU.png" style="width: 500px" />

Software DSM is a way to implement the illusion of a global shared memory in a computational cluster where each node has its own private physical memory. The software has to implement the consistency model to the programmer, as there is no physically shared memory. In a tightly coupled multiprocessor, coherence is maintained at individual memory access level by the hardware. However, in a cluster, this **fine-grain** of maintaining coherence at individual memory access level leads to too much **overhead**.

To implement software DSM, **the granularity of coherence maintenance is at the level of a page**. The global virtual memory abstraction is provided to the application program running on the cluster, which views the entire cluster as a globally shared virtual memory. Under the cover, **the DSM software partition the global address space into chunks that are managed individually on the nodes of the different processors of the cluster**.

The DSM software maintains coherence by having **distributed ownership for the different virtual pages** that constitute this global virtual address space. The ownership responsibility is split into individual processors, which are responsible for **keeping complete coherence information for that particular page** and **taking the coherence actions** commensurate with that page.

The DSM software implements the global virtual memory abstraction and knows exactly who to contact as the owner of the page to get the current copy of the page. When there is a page fault, the DSM software communicates with the operating system to handle it, contacts the owner of the page, and asks for the current copy of the page. The owner sends the page to the node that is requesting it, and the page is put into the physical memory, and the VM manager updates the page table for the thread to resume its execution.

An early example of systems that built software DSM includes Ivy, Clouds, Mirage, and Munin. They used coherence maintenance at the granularity of an individual page and a single-writer multiple-reader protocol. However, **the single-writer multiple-reader protocol has the potential for false sharing,** which is the problem of data appearing to be shared even though programmatically they are not. The page-based coherence maintenance and the single-writer multiple-reader protocol do not live happily together and can lead to false sharing and ping-ponging of the pages due to the false sharing among the threads of the application across the entire network.

### LRC with Multi Writer Coherence Protocol

<img src="https://i.imgur.com/9ipNyv3.png" style="width: 800px" />

- The goal of the **multiple writer coherence protocol** is to maintain coherence information at the granularity of pages, so the DSM can be integrated with the operating system.
- Multiple writer coherence allows multiple writers to write to the same page, recognizing that an application programmer may have packed lots of different data structures within the same page.
- The coherence protocol used in this system is LRC, which defers consistency traffic until the point of access.
- When a processor acquires a lock and makes modifications, the DSM software creates a diff of the changes made to the pages within the critical section.
- When another processor requests the same lock, the DSM software invalidates the pages modified by the previous lock holder, based on the diffs stored by the DSM software.
- If a processor tries to access an invalidated page, the DSM software retrieves the original page and diffs from the previous lock holder and applies them to create the current version of the page for the new lock holder.
- If multiple processors modify the same page, the DSM software applies all the diffs in order to create the current version of the page.
- LRC allows the DSM software to bring in only the data that the new lock holder needs, deferring the retrieval of diffs until the point of access.
- The DSM software can extend this protocol to any number of processors that may have made modifications to the same pages under the provision of the lock.

#### Implementation

<img src="https://i.imgur.com/acchRwm.png" style="width: 800px" />

- When a process or thread attempts to write to a page X, the operating system creates a twin for that page and makes the original page writeable by the process.
- At the release point, the DSM software calculates the diff between the original and modified versions of the page, storing it in a diff data structure.
- When a different processor acquires the same lock governing the released page, all pages touched in the previous critical section, including X, are invalidated. If there is a page fault for X, the DSM software retrieves the necessary diff from another node to update the page for the current lock acquirer.
- After the thread in the critical section completes its release operation, the original page is write-protected, and the twin is deleted to free up the physical memory that was allocated for it.
- In case multiple writers are modifying the same page under different locks, it represents an application problem and a data race that should not be there if the application is constructed correctly.
- The LRC multiple writer coherence protocol was implemented on a Unix system by TreadMarks. When a thread accesses a shared page, the DSM software catches the SIGSEGV exception to take appropriate action.
- There is a **space overhead** for creating a twin at the point of write and creating a diff data structure at release.
- **Garbage collection is used to reduce the space overhead** by periodically applying diffs to the original copy of the page and getting rid of them.

### Non Page Based DSM

<img src="https://i.imgur.com/tq2pE8U.png" style="width: 800px" />


- The library-based approach uses a programming framework/library to annotate shared variables, causing a trap at the point of access to contact the DSM software, which can take coherence actions. This approach eliminates false sharing possible in page-based systems and single write or cache coherence protocols. Systems that use this approach include Shasta and Beehive.
- The structured DSM approach provides abstractions at the level of meaningful application structures, using API calls to execute semantics and take coherence actions. Examples of systems that use this approach include Linda, Orca, Stampede, Stampede RT, and PTS.

### Scalability

<img src="https://i.imgur.com/EfXq8fF.png" style="width: 800px" />


- DSM provides a programming model that looks and feels like a shared memory threads package, but performance does not necessarily scale up as we increase the number of processors in the cluster.
- Overhead increases with the number of processors, and this buildup of overhead happens in true memory multi-processors.

### DSM and Speedup

<img src="https://i.imgur.com/qxvVk16.png" style="width: 800px" />


- The computation to communication ratio must be high for any hope of speed up with DSM.
- If sharing is too fine-grained, there is no hope of speed up, especially with DSM systems that are only an illusion of shared memory via software.
- Pointer codes may result in increasing overhead for coherence maintenance in DSM in a local area network.

### Distributed Shared Memory Conclusion

- DSM as originally envisioned, that is a threads package for a cluster, is dead.
- Structured DSM, which provides higher-level data abstractions for sharing among threads, is attractive to reduce programming pain for developers of distributed applications on a cluster.