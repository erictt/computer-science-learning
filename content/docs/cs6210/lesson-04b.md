---
weight: 1
title: "Lesson 04b: Parallel Operating System - Part 2"
---

# Lesson 4: Parallel Operating System - Part 2

## Lightweight RPC

### Remote Procedure Call

* Remote Procedure Call (RPC) is the mechanism used to manage communication in client-server operations on distributed systems.
* It’s also efficient to use RPC even when the client and the server are on the same machine:
  * **Safety**: We need to make sure that clients and servers are in different memory spaces. This means that RPC calls will go across different protection domains, which will hinder performance.
  * We need to make RPC across protection domains as efficient as a local procedure call.

### Local Procedure Call(LPC) vs RPC

<img src="https://i.imgur.com/Ohp3NqW.jpg" style="width: 800px" />

* When a local procedure call happens
  * The CPU stops the calling process.
  * The CPU executes the called procedure.
  * Return to normal operation.
  * The **binding and link** of the local procedure call happens at **compile time**.
    * It just hits a `call` or `bl` or some other kind of **brand and link** instruction that sets the program counter to the target address and saves off the address of the next instruction, either on the stack or in a link register. When CPU hits a `ret` or similar instruction, the address of the caller's next instruction will be popped off the stack or out of the link register into the program counter and execution will continue.
      * source: <https://edstem.org/us/courses/32553/discussion/2623222?comment=6004422>
* When a Remote Procedure Call happens:
  * A **trap** is issued to the kernel.
  * The kernel **validates the call** and copies the arguments of the call to the kernel buffers.
  * The kernel **locates the procedure** to be executes and copies the arguments to its address space.
  * The kernel **schedules** the server to run the particular procedure.
  * When the server executes the requests procedure, it returns to the kernel in the same way (**trap** & arguments copy).
  * The **binding** of an RPC can only happens at **runtime**.
  * Overhead = Two traps + two context switches + one procedure execution.
  * NOTE that the data are copied four times: client -> kernel -> server -> kernel -> client
* The copying **overhead** that happens with RPCs is a serious concern, since it happens 4 times with every call.
  * 1st copy: A client stub will copy the arguments from the client stack and serialize it into an RPC packet.
    * Kernel isn't involved in this step.
  * 2nd copy: The kernel will copy the arguments to its buffers.
  * 3rd copy: The kernel will copy the arguments from its buffers to the server domain.
  * 4th copy: The server stub will de-serialize the RPC packet and copy the arguments to the server stack.
  * These four copies are **one-way**, and will be **executed again** to pass the results back from the server to the client.
  * <img src="https://i.imgur.com/Q2X5w1D.jpg" style="width: 800px" />

### Making RPC Cheaper - avoid copy overhead

<img src="https://i.imgur.com/H9dC7JZ.jpg" style="width: 800px" />

* **Binding**: Setting up the relationship between the server and the client in the beginning. It’s a **one-time cost** so it’s OK to leave it as it is.
* The Binding process:
    1. The client calls the entry point procedure of the server, generating a trap in the kernel.
    2. The kernel checks with the server if this client can make calls to the server. Then the server grants permission.
    3. The kernel sets up a Procedure Descriptor (PD) for each procedure provided by servers, with the entry point address, the arguments stack (A-Stack) size, and the allowed number of simultaneous calls from this specific client.
    4. The kernel allocated a buffer shared between the client and the server with the size of the A-Stack (specified by the server). The client and the server can exchange data using this buffer without any intervention from the kernel.
    5. The kernel provides **authentication** to the client in a form of a **Binding Object (BO)**. The client can use this BO to make a call to this specific server in the future without going through the same process. The kernel can find the corresponding server based on the BO.
* **The kernel mediation for the binding happens only one time**.

* Making the actual call:

    <img src="https://i.imgur.com/ezWctT8.jpg" style="width: 800px" />

    1. Passing arguments between the client and the server **through the A-Stack** can **only be by value**, not by reference, since the client and server don’t have access to each other’s address space.
        * Note this is not serialization and deserialization, but only a data structure shared by both client and server.
    2. The stub procedure **copies** the arguments from the client memory space into the A-Stack.
    3. The client presented the BO to the kernel (trap) and blocks on the kernel’s response.
    4. At this point, the client will be blocked waiting for the call to be executed. The kernel can use the client thread for executing the procedure on the server’s domain.
    5. The kernel validates the BO and **allocates an execution stack (E-Stack)** for the server to use it **for its own execution**.
    6. The server stub **copies the arguments from the A-Stack to the E-Stack**.
    7. After finishing execution, the server stub **will copy the results from the E-Stack to the A- Stack**.
    8. The server traps the kernel, and everything will be done reversely to return to the client.

* Results of using an A-Stack:

    1. Using an A-Stack reduces the number of copies from four to two.
    2. The two copies happen in the client or server user space above the kernel.
        1. called marshal and unmarshal

  * <img src="https://i.imgur.com/Lnx96rS.jpg" style="width: 800px" />

* Even with this trick, we still have the overhead associated with the context switch itself:

    1. The client trap.
    2. Switching the protection domain.
    3. The server trap.
    4. Loss of locality (implicit).

### RPC on SMP

<img src="https://i.imgur.com/hcon3SR.jpg" style="width: 800px" />

* On a multiprocessor system, we can reduce context switching overhead by caching domains on idle processors. This keeps the caches warm (no TLB invalidation).
* When a call is made, the kernel checks for a processor idling in the context of the server domain. If one is found, **the kernel exchanges the processors of the calling and the idling threads**. Then, the called server procedure can execute on that processor without requiring a context switch. Same can be done on return from the call.
* Keeping the caches warm reduces the loss of locality.
* If the same server is serving multiple clients, the kernel can **pre-load the same server on multiple CPUs** to be able to simultaneously serve multiple clients.

## Scheduling

### Introduction

* How should the scheduler choose the next thread to run on the CPU?
  * First come first serve.
  * Highest static priority.
  * Highest dynamic priority.
  * Thread whose memory contents are in the CPU cache.

* Memory Hierarchy Refresher
  * L1 cache: 1-2 cycles
  * L2 cache: ~10 cycles
  * ...
  * Memory: ~100 cycles

* Cache Affinity Scheduling

<img src="https://i.imgur.com/oCPxxYT.jpg" style="width: 800px" />

* If a thread T1 is running on a particular CPU P1, it’s recommended to run the next call of that thread on the same CPU. The reason behind this is that T1 is likely to find its working set in the caches of P1, which in turn saves time.
  * <u>This can be inefficient if another thread T2 polluted the cache of P1</u> between the two calls of T1.

### Scheduling Policies

* First come first serve (FCFS):
  * The CPU scheduling depends on the order of arrival of the threads.
  * This policy ignores affinity in favor of fairness.
* Fixed processor (Thread-centric):
  * For the first run of a thread, the scheduler will pick a CPU, and will always attach this thread to that CPU.
  * Selecting the processors might be scheduled by a load balancer depend on the CPU load.
* Last processor (Thread-centric):
  * Each CPU will pick the same thread that used to run on it in the last operation cycle.
  * The reason for this is it's likely that the process will find its cache on that processor.
  * This policy favors affinity.
* Minimum Intervening (MI) (Processor-centric):
  * We will save the **affinity** of each thread with respect to every processor.
  * A thread T1 affinity will be saved in the form of an affinity index representing the number of threads that ran on the CPU between T1’s different calls. **The smaller the index the higher the affinity**.
  * Whenever a processor is free, it will pick the thread with the highest affinity to its cache.
  * **Limited** Minimum Intervening: If a lot of processors are running on the system, **keep only the affinity of the top few processors**.
* Minimum Intervening + queue (Processor-centric):
  * This policy will take into consideration not only the affinity index, but also how many threads are in the queue of the CPU when making the scheduling decision.
  * affinity size + length of the queue

In Summary

* <img src="https://i.imgur.com/dW3pKYs.jpg" style="width: 800px" />

### Implementation Issues

* The operating system should maintain a global queue containing all the threads that is available to all the CPUs. This queue will become very huge if the system has a lot of threads.
* To solve this issue, the OS would maintain local policy-based queues for every processor.
* A thread’s position in the queue will be determined by its priority.
* Thread priority = Base priority + thread age + affinity.
* If a specific processor ran out of threads, it will pull some threads from other processors.

### Performance

* **Throughput**: How many threads get executed and completed per unit time.
  * -> System centric.
* **Response time**: When a thread is started, how long it takes to complete execution.
  * -> User centric.
* **Variance**: Does the response time vary by time?
  * -> User centric.
  * When picking a scheduling policy, you need to pay attention to the load on each CPU.
  * In order to boost performance, a CPU might choose to stay idle till the thread with the **highest affinity** becomes available.
  * But when cpu load is heavy, fixed processor might be better than cache affinity, since the cache might gets

### Cache Aware Scheduling

<img src="https://i.imgur.com/6fAbXJU.jpg" style="width: 800px" />

* In a modern multicore system, we have multiple cores on a single processor, and the cores themselves are HW multi-threaded (switching between the core’s threads based on latency).
* We need to make sure that all the threads on a specific core can find their contents on either the core’s L1 cache, or at most the L2 cache.
* For each core, the OS schedules some cache frugal(节俭的) threads along with some cache hungry threads. This ensures that the amount of cache needed by all threads is less than the total size of the last level cache of the CPU (e.g. L2).
  * cache frugal thread: require less cache
  * cache hungry thread: require more cache
* Determining if a thread is cache frugal or hungry can be done through **system profiling** (additional overhead).

## Shared Memory Multiprocessor OS

### Challenges of Parallel Systems

<img src="https://i.imgur.com/Sgir3KV.jpg" style="width: 800px" />
* ICN - Inter-connection Network

* The big size of the system results in bottlenecks for the global data structures.
* The memory latency is huge due to faster processors and more complex controllers.
* **A non-uniform memory access (NUMA) architecture**: Connecting all the nodes in the system through an Inter-connecting Network. The large distance between accessing processors and the target memory results in lower performance.
* **Deep memory hierarchy** (Multi-cache).
* **False sharing**: Sometimes the cache hierarchy (large cache lines) makes the memory addresses touched by different threads on different cores to be on the same cache block. This gives the illusion that these addresses are shared (without programmatic sharing). This particularly happens on modern processors because they tend to have larger cache blocks.
  * e.g. An array of 4 integers, and 4 threads are updating the corresponding integer matching with their IDs. Technically they don't share data, but the array is still shared among four threads because the array is in the same cache line. We can avoid this by forcing each element of the array to be in different cache line so they don't share anything. But it's too much work for developers to think of.
  * <https://www.youtube.com/watch?v=OuzYICZUthM&list=PLLX-Q6B8xqZ8n8bwjGdzBJ25X2utwnoEG&index=7>

### OS Design Principles

<img src="https://i.imgur.com/kdOcyoH.jpg" style="width: 800px" />

* Exploit **affinity of caches** when taking scheduling decisions.
* Pay attention to **locality**.
* **Limit the amount of sharing** of data structures to reduce contention.

### Page Fault Service

<img src="https://i.imgur.com/9QWTKYu.jpg" style="width: 800px" />

* A page fault service consists of:
  * TLB and Page Table lookup: This is thread specific and can be done in parallel.
  * Locating the data on disk and moving it to the page frame, then updating the Page Table: This is a bottleneck because these are OS functions and have to be done in series.
  * TLB update: This is processor specific and can be done in parallel.
* There’re two scenarios in parallel OSs:
  * Multi-process workload: If each thread is running independently on a specific CPU, we’ll have distinct page tables and hence no serialization.
  * Multi-threaded workload: If the address space is shared between different threads, then the page tables and TLB will be shared as well. In this scenario, the OS should ensure that no or minimum serialization happens.
* **Principles for Scalable Structures in Parallel OS**
  * Determine functionally needs of each service.
  * To **ensure concurrent executions** of services, **minimize shared** data structures.
    * Less sharing -> more scalable
  * **Replicate/Partition data structures that have to be shared** to reduce locking, meaning more concurrency.

### Tornado OS

* Tornado uses an **object-oriented** approach, where <u>every virtual and physical resource in the system is represented by an independent object</u>. This ensures locality and independence for all resources.
* Trusted Object: Tornado uses a single object reference for all the OS parts.
* This single object reference, however, is translated into different physical representations.
* Degree of clustering (replicating a specific object):
  * Implementer choice.
        1. Single representation.
        2. One representation per core.
        3. One representation per CPU.
        4. One representation per group of CPUs.
  * The consistency of these representations is **maintained through Protected Procedure Calls**.
  * Don't use the hardware coherence. Because the hardware cache coherence might cause overhead replicate it to all CPUs. Therefore, you have to worry about keeping these copies consistent with one another.
* Traditional Structure
  * <img src="https://i.imgur.com/Er7qdWN.jpg" style="width: 800px" />

* Objectization of Memory Management:
  * The Address Space will be represented by the “Process Object”, which will be shared by all the threads executing on the CPU.
  * The Address space will be broken into regions:
    * → Each region will be backed by a “File Cache Manager – FCM” on the File System.
  * Another DRAM object will represent the Page Frame Manager, which is responsible for serving page frames for threads.
  * Another object called “Cached Object Representation – COR” will handle page I/O.
  * Whenever a thread incurs a page fault:
        1. The Process Object will decide which region this page fault fall into, given the virtual page number.
        2. The Region Object will contact the File Cache Manager.
        3. The FCM will contact the DRAM Object to get the physical page frame.
        4. The FCM will pass the file and offset to COR, which will pull the data from the desk into the DRAM’s page frame.
        5. FCM indicates to the Region Object that the physical page frame has been populated.
        6. The region Object will go through the Process Object to update the TLB.
  * <img src="https://i.imgur.com/siuC4YU.jpg" style="width: 800px" />

  * Objectization decisions:
        1. The Process Object can be one per CPU, since the TLB is one per CPU.
        2. The Region Object should be one per group of CPUs.
        3. The FCM should be one per group of CPUs.
        4. COR should have a single representation.
        5. DRAM Object can be one per physical memory.
  * Advantage of clustered object: Same object reference on all nodes. We can have different replications of the same object, which decreases data structures locking.
* Implementation of Clustered Object:
  * <img src="https://i.imgur.com/SyBCNM1.jpg" style="width: 800px" />
  * <img src="https://i.imgur.com/zSkTVfY.jpg" style="width: 800px" />

  * How object reference works in each CPU? Each CPU has:
    * → **Translation Table**: Maps a object reference to a representation in memory.
    * → **Miss Handling Table**: If the object reference is not present in the Translation Table, the Miss Handling Table maps the object reference to Object Miss Handler that decides if this object reference should point to an already existing representation or a new representation should be created. Then, it maps this object reference to its representation and installs the mapping in the Translation Table.
    * → **Global Miss Handler**: If the Object Miss Handler is not local, a Global Miss Handler will be used. Every node has a Global Miss Handler, and it knows the partitioning of the Miss Handling Table. If an object reference is presented to the Global Miss Handler, it will resolve the location of the required replica, installs it locally, and populates the Translation Table.
  * **Non-Hierarchical Locking and Existence Guarantee**:
    * → **Hierarchical Locking**: Whenever a thread is trying to execute a page fault, it locks the Process Object, the Region Object, the FCM, and the COR. This approach kills concurrency.
    * → One way to resolve this is to use an **Existence Guarantee** and a **Reference Count** on the Process Object.
      * // TODO The Reference Count increase every time there is a new thread is referring it
  * **Dynamic Memory Allocation**:
    * → Tornado OS breaks up the Heap space into multiple portions, each of which will be located on the physical memory of a specific node. That allows for scalable implementation of DMA.
    * → This also prevents false sharing across nodes.
  * **Inter-Process Communication – IPC**:
    * → IPC is realized by Protected Procedure Calls (PPCs).
      * → If the communication is on the same processor, no context switch happens.
      * → If the communication is between different processors, full context switch happens.
        * When you modify one replica, you have to make a particular procedure called the other replicas to deflect the other changes that you made In the first replica. So all of these are things that are happening under the cover.
* Tornado OS summary:
  * Object oriented design for scalability.
  * Multiple implementations of OS objects.
  * Optimize for common case.
    * page fault handing vs region destruction
      * region destruction happens less frequently
  * No hierarchical locking.
  * Limited sharing of OS data structures.

### Corey OS

The main principle in structuring an operating system for a shared memory multiprocessor is to limit sharing kernel data structures, which both limits concurrency and increases contention.

* **Address Ranges**: Similar to Tornado’s region concept. The difference is, instead of hiding the regions details from the application, on Corey, the address ranges are exposed to application so that it optimizes execution based on current thread accesses.
* **Shares**: A facility to be used by any process to communicate to the OS that the process will not share a specific data structure it’s currently using.
* Dedicated cores for kernel activities.

### Cellular Disco

* The **Cellular Disco** project explored the possibility of decreasing the virtualization overhead. The idea is to place a virtual layer between the guest OS and the I/O HW.

<img src="https://i.imgur.com/p2oO7iL.jpg" style="width: 800px" />

<img src="https://i.imgur.com/pr3jXUg.jpg" style="width: 800px" />

* Steps in handling I/O

  * CD runs as a multi-threaded kernel process on top of the host OS(Irix in this case)

    1. I/O request to CD: check permission; rewrite interrupt vectors
    2. CD forwards the request to the dormant host OS
    3. Host kernel issues the appropriate I/O request(3)
        * After Irix initiates the I/O request, control returns to CD
        * puts the host kernel back into the dormant state
    4. Upon I/O completion the hardware raises an interrupt
    5. CD reactivates dormant host, making it look as if the I/O interrupt had just been posted
        * Allows host to properly do any cleanup of I/O completion
    6. Finally, CD posts a virtual interrupt to the virtual machine to notify it of the completion of its I/O request
