# Lesson 7b: Distributed Subsystems - Distributed Shared Memory

Can we make the cluster appear like a shared memory machine?

## Introduction

- Distributed Shared Memory (DSM) is a software implementation that provides the illusion of shared memory to applications in a distributed system.
- DSM allows exploiting remote memories in a cluster to make it appear as a shared memory machine, simplifying application development.
- DSM works by creating an operating system abstraction that provides the illusion of shared memory to applications, even though nodes in the local area network do not physically share memory.

## Cluster as a Parallel Machine 

### Sequential Program

<img src="https://i.imgur.com/2o38mhX.png" style="width: 800px" />

- To exploit a cluster starting from a sequential program, one possibility is automatic parallelization, which means writing a sequential program and letting a tool identify opportunities for parallelism and map it to the cluster.
- Automatic parallelization is an example of implicitly parallel programming, where the program is not written explicitly in parallel but the tool identifies opportunities for parallelism and maps it to the cluster.
- High Performance Fortran is an example of a programming language that does automatic parallelization, where the user uses directives for distribution of data and computation.
- Automatic parallelization works well for certain classes of programs called data parallel programs, where the data accesses are fairly static and determinable at compile time.

### Message Passing

<img src="https://i.imgur.com/tPeuuQC.png" style="width: 800px" />

- The other way to exploit a cluster is to write the program as a truly parallel program, or explicitly parallel program, where the application programmer thinks about the application and writes the program explicitly in parallel.
- There are two styles of explicitly parallel programs: message passing style and shared memory style.
- The message passing style of explicitly parallel program is true to the physical nature of the cluster, where every processor has its private memory and cannot directly access the memory of another processor. It uses a message passing library that provides primitives for application threads to do sends and receives to peers executing on other nodes of the cluster.
- Examples of message passing libraries include MPI, PVM, and CLF from Digital Equipment Corporation, and many scientific applications running on large scale clusters use this style of programming using MPI as the message passing fabric.
- The downside to the message-passing style of programming is that it is difficult to program, as it requires the programmer to think in terms of coordinating the activities on different processes by explicitly sending and receiving messages from their peers, which is a radical change of thinking in terms of how to structure a program.

### DSM

<img src="https://i.imgur.com/MZj30m5.png" style="width: 800px" />

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

<img src="https://i.imgur.com/pcKtHIu.png" style="width: 800px" />

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

<img src="https://i.imgur.com/7l4Gg7n.png" style="width: 800px" />

- In sequential consistency, memory accesses are expected to happen in textual order on individual processors but the interleaving of memory accesses from different processors is arbitrary.
- The memory model preserves atomicity for individual read-write operations and honors the program order.
- SC memory model doesn't distinguish between data accesses and synchronization accesses.

### SC Memory Model:

<img src="https://i.imgur.com/MjZGeN3.png" style="width: 800px" />

- SC memory model doesn't know the association between locks and data structures.
- Coherence action is taken on every read-write access, which leads to more overhead and poorer scalability.

###  Typical Parallel Program:

<img src="https://i.imgur.com/J1llQoD.png" style="width: 800px" />

- A typical parallel program involves getting a lock for accessing data structures and releasing it after the critical section.
- The SC memory model doesn't differentiate between synchronization and data accesses.
- Coherence action is taken on every access even if it's not warranted until the lock is released.

###  Release Consistency:

<img src="https://i.imgur.com/1CQmKvJ.png" style="width: 800px" />

- Release consistency is a memory consistency model that distinguishes between synchronization and data accesses.
- Every critical section consists of acquire, data accesses governed by the lock, and release.
- Coherence actions prior to the release operation by P1 have to be complete before P2 acquires the same lock.
- Barrier synchronization can also be mapped to acquire and release.

###  RC Memory Model:

<img src="https://i.imgur.com/ym1Xrc4.png" style="width: 800px" />


- RC memory model distinguishes between normal data accesses and synchronization accesses.
- It initiates coherence actions corresponding to normal data accesses but doesn't block the processors.
- It only takes coherence action when a release synchronization operation is encountered.

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

- Lazy RC defers coherence actions to the point of lock acquisition rather than lock release
- Overlapping of computation with communication is still possible in the window of time between lock release and lock acquisition

### Eager vs Lazy RC

<img src="https://i.imgur.com/lctRnu6.png" style="width: 800px" />


- Vanilla RC is the eager release consistent memory model while LRC is the lazy release consistent memory model
- Eager RC broadcasts changes to all processors while Lazy RC only communicates with the necessary processors through point-to-point communication

### Pros and Cons of Lazy and Eager Release Consistency Model

- A system is release consistent if specific operations are performed before ordinary access or release is allowed to perform with respect to any other processor
- Eager release consistency: A processor delays propagating its modification to shared data until it comes to a release.
- Lazy release consistency: The propagation of modifications is postponed until the time of the acquire.
- Lazy release consistency reduces the number of messages and data transferred between processors, which is especially significant for programs that exhibit false sharing and make extensive use of locks.

### Software DSM

<img src="https://i.imgur.com/vBEaWiw.png" style="width: 800px" />


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

<img src="https://i.imgur.com/9ipNyv3.png" style="width: 800px" />

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

<img src="https://i.imgur.com/acchRwm.png" style="width: 800px" />

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

<img src="https://i.imgur.com/tq2pE8U.png" style="width: 800px" />


- Non-page based DSM systems do not use granularity of a page for coherence maintenance.
- Library-based approach uses programming framework/library to annotate shared variables, and generates a trap at point of access to contact DSM software for coherence action.
- Structured DSM provides abstractions manipulated using API calls that take coherence actions at the point of call execution.

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