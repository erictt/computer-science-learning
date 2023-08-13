---
weight: 1
title: "P2L4: Thread Design Considerations"
---

# P2L4: Thread Design Considerations

<!-- toc -->
----

## Kernel Vs. User Level Threads

* [A review of the concept](/cs6200/p2l2-threads-and-concurrency/#kernel-level-threads-vs-user-level-threads)
  * <img src="https://i.imgur.com/n6mauOA.jpg" style="width: 600px" />

## Thread Related Data Structures

### Single CPU

* A process is described by its process control block, which contains:
  * virtual address mapping
  * stack
  * registers
* If the process links in a **user-level threading**(ULT) library, the library will maintain a user-level thread data structure, which contains:
  * user-level thread id
  * user-level registers
  * thread stack
* If we want the multiple kernel-level threads associated with the threads in the process, the PCB needs to be duplicated for each kernel-level thread. To avoid the duplication, we can split the PCB into smaller data structures:
  * The PCB only keep the virtual address mapping,
  * The **kernel-level thread**(KLT) keeps the stack and register
  * <img src="https://i.imgur.com/tAsXGwj.jpg" style="width: 600px" />

### At Scale

* In a multiple processes situation, there will be multiple ULT, PCB and KLT. To cope with this, the system need to maintain the relationships: ULT <-> PCB, PCB <-> KLT. And if the system has multiple CPU, we also need to maintain the relationship: CPU <-> KLT.
* <img src="https://i.imgur.com/rl1hSer.jpg" style="width: 600px" />
* For each process, we need to track the kernel level threads that execute on behalf the process, and the for each kernel level thread, we need to track of the processes on whose behalf we execute.
* When kernel itself is multithreaded, we can have multiple kernel-level threads supporting a single user-level process. When kernel needs to schedule/context switch among kernel-level threads that belong to diff processes, it can quickly determine the KLT point to diff PCB.

### Hard and Light Process State

* When the operating system context switches between two kernel level threads that belong to the process, there is information relevant to both threads in the process control block, and also information that is only relevant to each thread.
* Information relevant to all threads includes the virtual address mapping, while information relevant to each thread specifically can include things like signals or system call arguments. When context switching among the two kernel level threads, we want to preserve some portion of the PCB and swap out the rest.
* We can split up the information in the PCB into **hard process state** which is <u>relevant for all user level threads</u> in a given process and **light process state** that is <u>only relevant for a subset of user level threads</u> associated with a particular kernel level thread.
* <img src="https://i.imgur.com/Xp5tefH.jpg" style="width: 600px" />

### Rationale For Data Structures

* Single control block:
  * large continuous data structure
  * private for each entity (even though some information can be shared)
  * saved and restored in entirety on each context switch
  * updates may be challenging
* Multiple data structures:
  * smaller data structures
  * easier to share
  * save and restore only what needs to change on context switch
  * user-level library only needs to update a portion of the state for customized behavior

## Data Structures in Solaris 2.0(OS)

* The Solaris OS is intended for multiple CPU and multi-threads. Each kernel-level thread has a lightweight process data structure associated with it, called **lightweight process(LWP)**, which represents the virtual CPUs onto which the user-level threads are scheduled. And the kernel-level scheduler is responsible for scheduling the kernel-level threads onto physical CPU.

### User Level Structures

* From paper: ["Implementing Lightweight Threads"](https://s3.amazonaws.com/content.udacity-data.com/courses/ud923/references/ud923-stein-shah-paper.pdf) by Stein and Shah
  * not POSIX threads, but similar
* When a thread is created, the library returns a thread id(tid). This id is **not a direct pointer to** the thread data structure but is rather an index into an array of thread pointers. the reason for that is, if there is a problem with the thread, the value at the index can change to -1 instead of the pointer just pointing to some corrupt memory.
* The thread data structure:
  * <img src="https://i.imgur.com/GTGvRgH.jpg" style="width: 300px" />
* To avoid one thread overrun its boundary and overwrite the data for the next thread, we create a red zone for separating the threads. **Red zone** is a portion of the address space that is not allocated. If a thread tries to write to a red zone, the operating system causes a fault.

### Kernel Level Structures

* <img src="https://i.imgur.com/9UGSnpT.jpg" style="width: 400px" />
* Data structures in details
  * Process:
    * list of kernel level threads
    * virtual address space
    * user credentials
    * signal handlers
  * **light-weight process (LWP)**:
    * user level registers
    * system call arguments
    * resource usage info
    * signal masks
  * Kernel-level thread(KLT):
    * kernel-level registers
    * stack pointer
    * scheduling info
    * pointers to associated LWPs, and CPU structures
  * CPU:
    * current thread
    * list of kernel level threads
    * dispatching & interrupt handling information

* LWP contains data that is relevant for some subset of the user threads in a given process, which is similar to the data contained in the ULT, but the LWP is visible to the kernel. When the kernel needs to make scheduling decisions, they can look at the LWP to help make decisions.
* The KLT has information about an execution context that is always needed. There are operating system services (for example, scheduler) that need to access information about a thread even when the thread is not active. As a result, **the information in the kernel level thread is not swappable**. The LWP data does not have to be present when a process is not running, so its data can be swapped out.

## Thread Management Interaction

* The Solaris **user thread library** life cycle.
  * <img src="https://i.imgur.com/idV7KLN.png" style="width: 500px" />
* Why kernel-level threads and user-level threads need to interact with each other?
  * Consider a process with four user threads, and a kernel with two threads. At a given time, the process require the level of concurrency to two. It always happens that two of its threads are blocking on, i.e. I/O, and the other two threads are executing.
  * Consider the scenario where the two user level threads that are scheduled on the kernel level threads happen to be the two that block. The kernel level threads block as well. This means that the whole process is blocked, even though there are user level threads that can make progress. The user threads have no way to know that the kernel threads are about to block, and has no way to decide before this event occurs.
  * It would be helpful if the kernel can **signal** the user-level library before blocking, and the user-level library could potentially request more kernel-level threads, or allocate one kernel thread to  other threads that can be executed immediately.

### Visibility in Between

* The kernel sees:
  * Kernel-level threads
  * CPUs
  * Kernel-level scheduler
* The user-level library sees:
  * User-level threads
  * Available kernel-level threads

* A case of invisibility:
  * In a many-to-many case, if a user level thread acquires a lock while running on top of a kernel level thread and that kernel level thread gets preempted, the user level library scheduler will cycle through the remaining user level threads and try to schedule them. If they need the lock, none will be able to execute and time will be wasted until the thread holding the lock is scheduled again.
    * The **user level library** makes schedule changes kernel not aware of such as changing the ULT/KLT mapping; The kernel is also unaware of the data structure the user-level threads use such as mutex variable, wait queues.
  * The one-to-one model helps address some of these issues because the kernel-level threads are aware of the state the of the user-level threads.
* How/When does the user-level library run?
  * The process jumps to the user level library scheduler when:
    * ULTs explicitly yield
    * Timer set by the by UL library expires
    * ULTs call library functions like lock/unlock
    * Blocked threads become runnable
  * UL library scheduler
    * runs on ULT operations
    * runs on signal from timer or kernel

### Issue On Multiple CPUs

* In a multi CPU system, the kernel level threads that support a process may be running concurrently on multiple CPUs. We may have a situation where the user level library that is operating in the context of one thread on one CPU needs to somehow impact what is running on another CPU.
* For example, there are three threads in one process : T1, T2, T3, and the thread priority is T3 > T2 > T1. The process is running on a two CPU, two threads OS.
  * Currently, T2 is holding the mutex and is executing on one CPU. T3 wants the mutex and is currently blocking. T1 is running on the other CPU. At some point, T2 releases the mutex, and T3 becomes runnable. Since T3 has higher priority than T1, we want to preempt T1.
  * We can't directly modify the registers of CPU, so we need to **send a signal from the context of one thread on one CPU to the context of the other thread on the other CPU**, to tell the other CPU to execute the library code locally, so that the proper scheduling decisions can be made.

### Synchronization Related Issues

* In a multi-CPU situation, T2 needs acquire a mutex that is locked by T1. Usually, we put T2 into the mutex queue, and wait for execution. But if T1 takes a short time to release the mutex, schedule T2 to one CPU and waste several CPU cycles might be a better idea.
* Mutexes which sometimes block and sometimes spin are called **adaptive mutex**. These only make sense on multiprocessor systems, since we only want to spin if the owner of the mutex is currently executing in parallel to us.

#### Destroy threads

* Instead of destroying threads right away once it's not used, we
  * put it on a "death row"
  * periodically destroyed by reaper thread
  * otherwise thread structures/stacks are reused.

## Interrupts and Signals

* **Interrupts** are events that are generated **externally** by components(hardware) other than the CPU to which the interrupt is delivered. Interrupts are notifications that **some external event has occurred**.
  * Components may deliver interrupts: I/O devices, Timers, Other CPUs
    * For example, when a user-level application tries to perform a illegal task using the hardware, the kernel is notified via an interrupt.
  * Interrupts varies on different physical platforms
  * Interrupts appear asynchronously.
* **Signals** are events that are triggered by the CPU and the software running on it. e.g. `SIGKILL`
  * which signals can occur depend on the OS
  * Signals can appear both **synchronously** and **asynchronously**.
  * Signals can occur in direct response to an action taken by a CPU, or they can manifest similar to interrupts.
* Signal/Interrupt Similarities
  * Both have a unique identifier, values depend on the hardware or OS.
  * Both can be **masked**. An interrupt can be masked on a **per-CPU basis** and a signal can be masked on a **per-process basis**.
    * **A mask is used to disable or delay the notification** of an incoming interrupt or signal.
  * If the mask indicates that the corresponding interrupt or signal is enabled, the incoming notification will trigger the corresponding **handler**.
  * **Interrupt handlers** are specified for the entire system by the OS. **Signal handlers** are set on a per-process basis, by the process itself.
* Differences
  * For interrupts, the kernel has an **interrupt table** which jumps to a particular subroutine depending on the interrupt type.
  * For signals, the process likewise has a **signal handler** which selectively enables certain signals using a thread-speciﬁc **signal mask**. The kernel calls the handler if the mask allows (i.e. has the bit set) the signal.

### Interrupt Handling

* The interrupt interrupts the execution of the thread that was executing on top of the CPU. The CPU looks up the interrupt number in a table and executes the handler routine that the interrupt maps. The interrupt number maps to the starting address of the handling routine, and the program counter can be set to point to that address to start handling the interrupt.
* Which interrupts can occur depends on the hardware of the platform and how the interrupts are handled depends on the operating system running on the platform.
* <img src="https://i.imgur.com/GCKytqS.jpg" style="width: 500px" />

### Signal Handling

* Signals are different from interrupts in that signals originate from the CPU. For example, if a process tries to access memory that not allocated, a SIGSEGV signal will be generated.
* For each process, the OS maintains a mapping where the keys correspond to the signal number. Here is a list of signals from POSIX: [signal.h](https://pubs.opengroup.org/onlinepubs/9699919799/)
* The default signal responses from the OS includes: Terminate, Ignore, Terminate and Core Dump, Stop or Continue (from stopped)
* For most signals, processes can install its custom handling routine, usually through a system call like **signal()** or **sigaction()** although there are **some signals which cannot be caught**.
* synchronous signals include:
  * SIGSEGV
  * SIGFPE (divide by zero)
  * SIGKILL (from one process to another)
* asynchronous signals include:
  * SIGKILL (as the receiver)
  * SIGALARM (timeout from timer expiration)

### Why Disable Interrupts or Signals? Avoid Deadlock

* Interrupts and signals are handled in the context of the thread being interrupted/signaled. This means that they are handled on the thread's stack, which can cause certain issues.
* When a thread handles a signal, the program counter of the thread will point to the first address of the handler. The stack pointer will remain the same, meaning that whatever the thread was doing before being interrupted will still be on the stack.
* If the handling code needs to access some shared state that can be used by other threads in the system, we will have to use mutexes. If the thread which is being interrupted had already locked the mutex before being interrupted, we are in a **deadlock**. The thread can't unlock its mutex until the handler returns, but the handler can't return until it locks the mutex.
* A simple solution is keep handler code simple, like not acquire mutex, but it's too restrictive.
* A better solution is to use **interrupt/signal masks** which allow us dynamically enable/disable whether the handling code can interrupt the executing mutex.
  * The mask is a sequence of bits where each bits represents a specific interrupt or signal with value 0/1.
  * When event occur, the handler will check the mask to decide whether pending or proceed.
    * Once the interrupt/signal is pending, others interrupts/signals might also become pending. Typically the handling routine will only be executed once, so if we want to ensure a signal handling routine is executed more than once, it is not sufficient to generate the signal more than once.
* **When masks disable interrupt/signal**
  * Interrupt masks are per CPU. If the mask disables interrupt, the hardware interrupt routing mechanism will not deliver interrupt to CPU
  * Signal masks are per execution context (ULT on top of KLT). If a mask disables a signal, the kernel will see this and will not interrupt the corresponding execution context.
* Interrupts on Multicore Systems
  * On a multi CPU system, the interrupt routing logic will direct the interrupt to any CPU that at that moment in time has that interrupt enabled. One strategy is to enable interrupts on just one CPU, which will allow avoiding any of the overheads or perturbations related to interrupt handling on any of the other cores. The net effect will be improved performance.
* Two Types of Signals
    1. **One-shot signals** refer to signals that will only interrupt once. This means that from the perspective of the user level thread, n signals will look exactly like one signal. One-shot signals must also be explicitly re-enabled every time.
    2. **Real-Time Signals** refer to signals that will interrupt as many times are they are raised. If n signals occur, the handler will be called n times.

### Interrupts as a Separated Threads

* To avoid the deadlock situation we covered before regards to handler code trying to lock a mutex that the thread had already locked, one way from the Sun thread paper is, to allow interrupts to become full-fledged threads, and execute independently.
  * <img src="https://i.imgur.com/ZMnIWlm.jpg" style="width: 600px" />
  * In this case, when the handler is blocked, it still has its own context/stack, and can remain blocked. And the main thread can continue to work, and eventually unlock the mutex so the handler will be free to execute.
  * However dynamic thread creation is expensive! The decision described in Solaris system is
    * if handler doesn't lock -> execute on interrupted thread's stack
    * if handler can block -> turn into real thread
  * One way to optimize it is
    * pre-create & pre-initialize thread structures for interrupt routines.

### Interrupts: Top Vs. Bottom Half

* When an interrupt is handled in a different thread, we no longer have to disable handling in the thread that may be interrupted. Since the deadlock situation can no longer occur, we don't need to add any special logic to our main thread.
* However the interrupt/signal work can divided to two parts:
  * **top half**: handling in the context of the main thread. this half needs to be fast, non-blocking, and min-amount of processing
  * **bottom half**: allows arbitrary complexity
  * <img src="https://i.imgur.com/TSsadeE.jpg" style="width: 600px" />

### Performance of Threads as Interrupts

* The overhead of performing the necessary checks and potentially creating a new thread in the case of an interrupt adds about 40 SPARC instructions to each interrupt handling operation.
* As a result, it is no longer necessary to disable a signal before locking a mutex and re-enable the signal after releasing the mutex, which saves about 12 instructions per mutex.
* Since mutex lock/unlocks occur much more frequently than interrupts, the net instruction count is decreased when using the interrupt as threads strategy.

### Threads and Signal Handling

* The enable/disable happens at the user-level threads, and the signal triggered at at the kernel-level. It results an inconsistency between the ULT and KLT.
  * <img src="https://i.imgur.com/pgzPGpL.jpg" style="width: 600px" />
* **Degree concurrency** is used by the $m × n$ model in Solaris to control the amount of multiplexing from ULTs to LWPs (and thus KLTs).

* Let's look at four cases:

1. ULT mask = 1 and KLT mask = 1
    * This won't be a problem since they are the same
2. ULT mask = 0 & KLT mask = 1 & another ULT mask = 1
    * <img src="https://i.imgur.com/efTtBcf.jpg" style="width: 400px" />
    * The**threading library** has a **signal handler's table** that indicates the signal and corresponding handler function. The **library handling routine** can see the masks of the user level threads.
        * e.g. the table: `SIGNAL-N: handler-N-start-addr`
    * In this case, when a signal occurs at the kernel level, the KLT calls the **threading library provided handler**. The library handling routine knows that one thread can't handle the signal, but the other can. It invoke the library scheduler and make ULT that has mask enabled running on KLT so that signal can be handled.
3. ULT mask = 0 & KLT mask = 1 & another ULT mask = 1 & KLT mask = 1
    * <img src="https://i.imgur.com/5b85iL7.jpg" style="width: 400px" />
    * In the case where a signal is generated by a kernel level thread that is executing on behalf of a user level thread which does not have the bit enabled, the threading library will know that it cannot pass the signal to this particular user thread.
    * What it can do, is send a **directed signal** down to the kernel level thread associated with the user level thread that has the bit enabled. This will cause that kernel level thread to raise the same signal, which will be handled again by the user level library and dispatched to the user level thread that has the bit enabled.
4. All ULT masks = 0 & all KLT masks = 1, the kernel think the ULKs can handle all signal, but none of them can.
    * <img src="https://i.imgur.com/ksK2AMG.jpg" style="width: 400px" />
    * When the signal occurs, the kernel interrupts the execution of whichever thread is currently executing atop it. The library handling routine kicks in and sees that no threads that it manages can handle this particular signal.
    * Then, the thread library will make a system call requesting to disable the signal mask on the particular kernel level thread. We can't change other ULTs that associated with KLTs that running on the other CPUs.
    * Then the threading library will reissue the signal for entire process again. The OS will find the other threads in the process and all of the masks associated with the KLTs will be disabled via system call.
    * When any of the ULT re-enable the mask, the threading lib will make a system call, and tell the kernel level thread to enable the particular signal mask.

* The algorithm above is optimized for the common cases, because:
  * Signals occur much less frequently than does the need to update the signal mask.
  * Updates of the signal mask are cheap. They occur at the user level and avoid system calls.
  * Signal handling becomes more expensive - as system calls may be needed to correct discrepancies - but they occur less frequently so the added cost is acceptable.

## Tasks in Linux

* The main abstraction that Linux uses to represent an execution context is called a **task**. A task is essentially the **execution context of a kernel level thread**. A single-threaded process will have one task, and a multithreaded process will have many tasks.
* Key elements in task structure([complete](https://elixir.bootlin.com/linux/v5.17/source/include/linux/sched.h#L728)):

    ```c
    struct task_struct {
        // ...
        // if it'a single-thread process, the task id = process id, 
        // if multi-thread, each task has it's own identifier which will be held in the pid(process ID)
        // and the pid is also the first task id
        pid_t pid; 
        pit_t tgid; // task group id // TODO i'm confused. is this the same as pid?
        int prio;
        volatile long state;
        struct mm_struct *mm;
        struct files_struct *files;
        struct list_head tasks; // head of the list of tasks
        int on_cpu;
        cpumask_t cpus_allowed;
        // ...
    }
    ```

* Task creation: clone
  * to create a new task, the ops in linux is called `clone`. here is the function:
    * `clone(function, stack_ptr, sharing_flags, args)`
    * very similar to pthread, and also take an argument: `sharing_flags`
  * The sharing flag:
    * <img src="https://i.imgur.com/3nLBkdk.jpg" style="width: 600px" />
    * If it's not set, the child will not share anything with the parent.
* Linux thread model
  * **Native POSIX Thread Library(NPTL)**: **1-1 Model** aka, a kernel level task for each user level thread.
    * It replaced the earlier implementation of **LinuxThreds**(M:M Model), has similar issues as  Solaris OS.
  * In NPTL, **the kernel sees every user level thread.** This is acceptable because kernel trapping has become much cheaper, so user/kernel crossings are much more affordable.
  * Also, modern platforms have more memory - removing the constraints to keep the number of kernel threads as small as possible.
* The benefits got from 1:1 model:
  * **Scheduling.** With 1:1 threads, there is <u>no longer any need for user-level scheduling</u> because the kernel sees all threads and their priorities can be refined to allow scheduler to optimize things appropriately.
  * **Synchronization.** With 1:1 threads, there is <u>no more management of signal masks</u>. The kernel thread will deliver signals to its user thread if the mask is enabled.
  * **Signaling.** With 1:1 threads, <u>User threads can be woken up immediately once a mutex is freed, rather than needing to traverse through a user-level threading library that relies on global synchronization primitives</u>. Furthermore, blocking operations(like waiting on a lock) are trivial to recognize, and deadlocks can be avoided because the kernel sees all primitives.
  * **light-weight processes aren’t necessary** because all of the data for a thread is stored within the thread itself; any shared data across threads is stored in their PCB.
