---
weight: 1
title: "Lesson 04a: Parallel Operating System - Part 1"
---

# Lesson 4: Parallel Operating System - Part 1

## Shared Memory Machine Model

* Dance Hall Architecture:
  * <img src="https://i.imgur.com/GdC11HY.jpg" style="width: 800px" />

  * CPUs on one side of the interconnection network, and memory on the other side.
  * The entire memory space is accessible from any CPU.
* Symmetric Multiprocessor (SMP) Architecture:
  * <img src="https://i.imgur.com/ClBtjah.jpg" style="width: 800px" />

  * <u>The CPUs are connected to the memory via a system bus</u>.
  * The access time from any CPU to the memory is the same.
  * Each CPU is equipped with a private cache.
* Distributed Shared Memory (DSM) Architecture:
  * <img src="https://i.imgur.com/AEcXzsz.jpg" style="width: 800px" />

  * Each CPU has a piece of memory connected to it to facilitate faster access.
  * Each CPU can access other memory spaces through the interconnection network.
  * Each CPU is equipped with a private cache.

### Memory Consistency Model

* A Memory Consistency Model formulates what can be expected from the system.
* **Sequential Consistency (SC)**:
  * **Program order:** Memory accesses from each process are ordered.
  * **Arbitrary interleaving**: The interaction between processes in terms of memory accesses is arbitrary.

### Cache Coherence

To deal with the cache problem is multiprocessor situation. The goal is to avoid overhead and expect performance increase as the number of processors increase. Despite of the strategies we have below, the best solution is do not share memory since it can avoid cache coherence issue.

* <img src="https://i.imgur.com/RYDjUFm.jpg" style="width: 800px" />

* How the system implements the Memory Consistency Model in the presence of private caches.
* **Non-cache-coherent (NCC)** multiprocessor: This model grants a shared memory space to all the CPUs, while **leaving the private cache coherence issue to software**.
* **Cache-coherent (CC)** multiprocessor:
  * **Write-invalidate**: Whenever a CPU writes to a memory location in its cache that happens to be fetched by other CPUs, the HW broadcasts a message on the system bus to invalidate other CPUs’ caches.
  * **Write-update**: Whenever a CPU writes to a memory location in its cache that happens to be fetched by other CPUs, the HW broadcasts an update on the system bus to replicate this change on other CPUs’ caches.

## Synchronization

### Basic Synchronization Primitives

* Lock:
  * A primitive to protect shared data structure in multi-threaded operations.
  * Types of locks:
        1. **Mutual exclusion**: Can be used by one thread at a time (e.g. protect a data structure while writing to it).
        2. **Shared lock**: Allows multiple threads to access the data at the same time (e.g. Multiple threads reading the same data at the same time, while preventing the modification of this data).
* **Barrier synchronization**:
  * A primitive to ensure that multiple threads reached a particular point in terms of computations.
    * Like a reverse from a semaphore, will block all threads until n threads arrive at this point.
  * It blocks threads that reach this point until the other threads (those that use the same barrier) reach the same point, and then all threads can continue execution.
  * The access time from any CPU to the memory is the same.

### Atomic Operations

* If we have a lock (e.g. global variable) that is shared between multiple threads, each thread will need to execute read/write operations to acquire/release this lock. This read/write operation is called atomic.
* Read/write operations are **atomic**, but checking/blocking/acquiring the lock is not atomic. This can cause problems while acquiring/releasing the lock. SO we need a new **semantic atomic instruction** to use with the lock to ensure thread-safe.
* Atomic RMW (Read – Modify – Write) instructions:
  * **Test-and-set**: Takes a specific memory location as an argument, **returns its current value** and **sets it to one**.
  * **Fetch-and-increment**: Takes a specific memory location as an argument, returns its current value and **increments it by one, or any given value**.
  * These instructions called in general “**Fetch-and- 𝜙** [fi:]”, where 𝜙 is any given operation.

### Scalability Issues with Synchronization

* **Latency**: The overhead of acquiring/releasing the lock.
  * The lock is being used, how long can i acquire it. It's the time spent by a thread in acquiring the lock.
* **Waiting time**: How long to wait till a thread can acquire the lock.
  * It depends on what these threads are doing with this lock.
  * For instance, if this thread acquires this lock, and then it is modifying the data for a long time before releasing it, and if another thread comes along and wants the team lock, it's going to wait for a long time.
* **Contention**: If there’re multiple threads spinning on a specific lock, we expect an overhead on the system bus. This overhead increases time consumed from the point a thread releases that lock to the point it’s acquired by another thread.
  * Threads compete to acquire the lock simultaneously.

### Spinlocks

* [Notes from CS6200](https://cs.ericyy.me/cs6200/p3l4-synchronization-constructs/index.html#test-and-test-and-set-spinlock)

#### Naive Spinlock

* (**spin on test-and-set**): A thread that is waiting for a lock to be released will spin on the lock **(infinitely execute test-and-set)** till it’s released. This type has three issues:
* **Too much contention**: Each waiting processor accesses the shared flag as frequent as possible using expensive Fetch-and- 𝜙 operation.
* **Doesn’t exploit caches**.
* **Disrupts useful work**.

#### Caching Spinlock

* (**spin on read**): On a cache-coherent system, the threads that are waiting for a lock to be released can spin on the cached value of the lock. This removes the contention from the communication network. The problem with this type is once the lock is released, all the spinning threads will try to execute test-and-set to acquire the lock, which produces a huge amount of network traffic.

#### Spinlock with delay

* Whenever a lock is released, each pending processor will wait for a specified delay time before trying to acquire the lock.
* Each processor will have its own delay.
* In some situations, the lock isn’t blocking a lot of threads and can be acquired immediately without causing much contention. <u>To avoid unnecessary delays in this case, we can use dynamic delays.</u> When the lock is released, the processor waits for a certain amount of time, and then tries to acquire the lock. If the lock was not acquired during this delay, this means that is has high contention, then the processor will double its delay time(exponential backoff).
* <img src="https://i.imgur.com/QWD4xhm.jpg" style="width: 800px" />
* In comparison, the second implementation doesn't use cache. So if the processors are non-cache coherent multi-processor, this algorithm will still work.
* <u>If there's a lot of contention, then the static assignment of delay may be better than the dynamic exponential backoff.</u> But in general, any kind of delay or any kind of procrastination will help a lock algorithm better than the naive spin lock that we talked about.

#### Ticket lock

* <u>ensure fairness.</u> This lock structure maintains data fields to determine which thread has the lock now (**now_serving**), and which one should acquire the lock next (**next_ticket**).
* <img src="https://i.imgur.com/GX6Nn6d.jpg" style="width: 800px" />

* If a processor wants to acquire the look, it executes (fetch-and-increment) on the next_ticket field. Then waits till the now_serving value of the lock is equal to the ticket value of the processor.
* This structure ensures fairness between processors. Each thread gets a chance to acquire the lock.
* The processor releases the lock by incrementing now_serving.
* It adds overhead to the network for maintaining the lock information.

#### Array-based Queuing Lock (Anderson)

The ONLY atomic instruction: **fetch-and-inc(queuelast);**

<img src="https://i.imgur.com/vYzeXjl.jpg" style="width: 800px" />

* The thread that is releasing the lock will signal another pending thread to acquire the lock.
* The lock maintains two data structures:
    1. A circular queue of flags, where each processor either has the lock (**has_lock**) or waiting for it to be released (**must_wait**).
    2. A “queue_last” variable to specify the **next free spot** in the queue.
* The pending thread will spin on its position in the queue till it can jump to (has_lock) and acquire the lock.
* When a thread is releasing the lock, it will signal the next thread in the queue, by setting the next position in the flags array to (has_lock).
* Advantages:
  * There’s only one atomic operation a thread has to execute to acquire the lock.
  * The lock is fair. It maintains the order of requests.
  * The spin position of each processor (must_wait) ensures independence between different threads.
  * Whenever a lock is released, exactly one thread is signaled to acquire the lock. This decreases contention.
* Disadvantage:
  * **The size of the queue will depend on the number of processors.** Since the lock maintains a **STATIC** data structure, it must create a structure that can accommodate for the worst-case scenario (all processors are waiting for the lock). If we have a large-scale multi-processing system, this can be a problem (high space complexity).

#### Linked List-based Queuing Lock (MCS Lock)

* To avoid the space complexity of the Array-based Queuing Lock, a linked list can be used as a representation for the queue, so the size of the queue will be exactly equal to the dynamic sharing of the lock.
  * This means that the size of the queue will be equal to the number of processors that are actually using the queue right now, not all the processors in the system.
* The lock data structure is a **dummy node** and will be the initial node of the linked list.
* Each thread gets a node with two fields:
  * **got_it**: To indicate that the thread acquired the lock (locally accessible to the processor).
  * **next**: To point to the next thread in the queue.
* Whenever a new thread wants to join the queue, it will execute an atomic operation (**fetch-and-store(L, me)**):
    1. It change the “next” pointer in the last node to point to itself.
    2. Set the “next” pointer of its node to null.
    3. Spin on its “got_it” field.
    4. <img src="https://i.imgur.com/aja7H5D.jpg" style="width: 800px" />
* When a thread releases the lock, it should remove itself from the list and signal the next thread. If there’s no thread waiting for the lock, the releasing thread should set the “next” pointer to null.
  * <img src="https://i.imgur.com/UZPW9w4.jpg" style="width: 800px" />
* A problem can arise if a new thread tries to acquire the lock at the same time the releasing thread sets the pointer to null. A race condition will happen.
  * This is a **corner case** that `me` think it's the last request.
* To avoid this issue, the releasing thread should do a **comp-and-swap(L, me, nil)** atomic operation. It checks if the last requester pointer is still pointing at itself and if yes it sets the pointer to null.
  * So in the instruction, it compares first two arguments: last and me, if the same, set L to the third argument: nil.
    * the instruction returns true if the swap succeeded. Otherwise won't do the swap and return false.
    * When it return false, **me** is gonna **spin** on `me`'s next pointer == null to wait for the next pointer to become not null. Once it's not null, `me` is gonna signal the successor that he gets the lock.
  * TODO: Look into the code to get a better understanding.
  * <img src="https://i.imgur.com/Lt2xucv.jpg" style="width: 800px" />

* Advantages:
  * Guarantees FIFO **ordering** of lock acquisitions. <-- Fair
  * Processors **spin** on locally-accessed flags only. <-- Unique
  * The space complexity of this data structure is proportional to the number of requesters to the lock at any point of time. <-- Dynamic
  * Works well on cache-coherent or non-cache-coherent systems.
* Disadvantage:
  * If the processor only has **test and set** instruction, then an exponential backoff algorithm would be a good bet for scalability, because you need to implement these two instructions.

### Summary

<img src="https://i.imgur.com/mdiNl1D.jpg" style="width: 800px" />
- Spin:
    - pvt: spin on private variable
    - sh: spin on shared variable
- RMW ops pre CS:
    - How many ops of RMW are required for a lock.
    - Depends on the amount of contention except for Anderson and MCS, which has two fixed numbers.

## Barrier Synchronization

### Centralized Counting Barrier

* We have a counter that is initialized by the number of threads 𝑁 to be synchronized.
* Once a thread arrives to the barrier, it atomically decrements the counter, and spins on it till it becomes zero.
* The last thread to arrive will decrement the counter. Now the counter is zero, so that thread will reset the counter to its initial value 𝑁, so that it can be used for the next barrier.
* A problem can arise if one of the threads races to the next barrier before the counter is reset to its initial value 𝑁. This thread will directly go through the barrier.
  * To solve this problem, we add another spin loop so that the threads will wait for the counter to become zero, then wait again till it becomes 𝑁.
  * <img src="https://i.imgur.com/Gve4a02.jpg" style="width: 800px" />
  * Question: when all threads reach the second `while`, what if one of the thread update the N to N-1, and some other threads are still haven't do the `count == N` check yet? It might cause some threads stuck forever.

### Sense Reversing Barrier

To reduce the spin from 2 to 1.

* In a Counting Barrier we have two spin loops for each thread. One waits for the counter to become zero, and the other one waits for the counter to become 𝑁.
* To avoid having two loops, we add another variable “**sense**” that is shared between all the threads to be synchronized.
* This variable will be true for the current barrier, and false for all the other barriers.
* This way we can determine which barrier we’re in at any particular point of time.
* Whenever a thread arrives at the barrier, it decrements the counter and spins on “sense” reversal.
* The last thread will reset the counter to 𝑁 and reverses the “sense” variable.
* The problem with this technique is that we have two shared variables between all the threads, which decreases the possibilities for scalability (More sharing → Less scalability).
* <img src="https://i.imgur.com/bWPVE0l.jpg" style="width: 800px" />

### Tree Barrier

To reduce the contention among all of the threads, only the nodes that rise up to the parent spin on the locksence.

* Instead of having a single pair of “count” and “lock_sense” variables shared between 𝑁 threads, we will have a pair of variables for each 𝐾 number of threads, where 𝐾 < 𝑁.
* Processors are divided into groups. Each group is assigned to a tree leaf.
* When a thread arrives to the barrier, it decrements the **counter** and spins on **lock_sense**.
* The last thread of the leaf will arrive and decrement the counter to zero. Then it checks if it has a “parent”, if yes it decrements the counter of its parent and spins on the parent’s **lock_sense**.
* This operation is executed recursively until the last thread arrives to the barrier.
* The last thread will decrement the counter at the root of the tree to zero, which indicates that everyone arrived. This thread will then reset the counter to 𝑁 and reverse the root’s **lock_sense** flag.
* All the threads till the bottom of the true will wake up **recursively**.
  * <img src="https://i.imgur.com/9nhLaFD.jpg" style="width: 800px" />
* This allows for higher scalability since the amount of sharing is relatively small.
* Disadvantages:
  * The spin location is not static for each thread. It depends on the time the thread arrives to the barrier.
    * Meaning p0 and p1 both have a chance to move up to spin.
  * If you have a **huge number of threads**, the tree will grow too deep and will results in **contention** on the system.
  * On a non-cache-coherent system, a thread might need to **modify/spin on a variable in a remote memory**, which adds **contention** to the system.

### MCS Tree Barrier (4-Ary arrival)

To minimize contention, MCS tree implements the barrier with two trees: arrival tree and wakeup tree. Both offers static positions for the nodes.

* This is a modified Tree Barrier where each node is allowed to have at most 4 children.
* Each node has two data structure:
  * **HaveChildren**: Indicates if the node is a parent or not, and how many children it has if any.
  * **ChildNotReady**: Each child thread has a unique spot in the parent’s ChildNotReady structure to signal the arrival of that child thread. These spots are statically determined.
* Whenever a thread arrives to the barrier, it sets it’s spot in the parent’s ChildNotReady structure to True. The thread spins on the arrival of its own children if it has any.
* A 4-Ary tree facilitates the best performance.
* In a cache-coherent system, it can be arranged so that all the ChildNotReady structure can be packed in one word, so the parent processor just spins on a single memory location.
  * <img src="https://i.imgur.com/GvwNrG9.jpg" style="width: 800px" />

* Although the **arrival tree** is a 4-Ary tree as shown in the above figure, the **wakeup tree** is a binary tree.
* Each thread has a **ChildPointer** that can be used to signal the child to wake up.
  * <img src="https://i.imgur.com/JIHnMQZ.jpg" style="width: 800px" />

* key takeaway:
  * the wakeup tree is binary.
  * The arrival tree is 4-ary.
  * The **static locations** associated with each processor, both in the arrival tree and the wakeup tree

### Tournament Barrier

* The barrier is represented by a tournament data structure (binary tree) with 𝑁 players and $\log_2N$ rounds.
* The **winning thread of each round is predetermined**. This allows the spin locations to be static.
  * E.g. P0 is the winner and it spins to wait for P1 to arrive.
* Tournament Barriers don’t need a Fetch-and- 𝜙 operation.
* Tournament Barriers works even if the system doesn’t have a shared memory, where threads can only **communicate through message passing** (No shared memory → Cluster machine).
  * If you have NCC NUMA machine, it is possible to locate the spin location in the memory that is very close to P0 P2 P4 and P6 respectively.
* <img src="https://i.imgur.com/AwZcmUz.jpg" style="width: 800px" />

* The main difference is that in the tournament barrier, the spin locations are statically determined, whereas in the tree barrier we saw that the spin locations are dynamically determined based on who arrives at a particular node in the barrier in the tree in that algorithm.
* Another important difference between the tournament barrier and the tree barrier is that there is no need for a **fetch and phi** operation.
* The amount of communication in the tournament barrier in terms of all the notation is exactly similar to the tree barrier it is $O(\log{N})$.

### Dissemination Barrier

* In each round $𝑘$, whenever a processor $𝑃_𝑖$ arrives at the barrier, it will signal processor $P_{i+2^k \cdot mod(N)}$ This creates a cyclic communication order between the processors.
  * For easier understanding, the formula can be interpreted as:
    * Round 0, each process send message to the 2^0 neighbor.
    * Round 1, each process send message to the 2^1 neighbor, aka, p0 -> p2, p1 -> p3, and so on.
    * Round 2, each process send message to the 2^2 neighbor, aka, p0 -> p4, p1 -> p(5%5=0), and so on.
* A Dissemination Barrier would need ⌈$\log_2N$⌉ rounds for all the processors to wake up.
* Spin locations are statically determined.
* <img src="https://i.imgur.com/lWKudKa.jpg" style="width: 800px" />

## So far

* Spin algorithms:
  * test-and-set
  * test-and-set with cacahe
  * test-and-set with delay
  * ticket
  * queue
* Barrier algorithms:
  * Counter
  * Tree
  * MCS Tree
  * Tornament
  * Dissemination
* Parallel Architectures: ? When?
  * Cache Coherence shared-memory multiprocessors
  * Cache Coherence non-unified memory access
  * Non-cache coherence non-unified memory access
  * Multiprocessor clusters.
