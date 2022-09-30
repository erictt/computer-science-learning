# P2L2: Threads and Concurrency 

<!-- toc -->
----

## Process vs. Thread

* A process owns a virtual memory space and OS initialize a PCB to manage the state.
* A thread is also called 
* PCB: single thread process vs multithreaded process
    * <img src="https://i.imgur.com/2uV8di5.jpg" style="width: 600px" />
    * The PCB for multithreaded process is different. In a multi-threaded process, threads share the same code/data/filter, but also have its own registers and stack.

## Benefits of Multithreading

* Parallelization: Speed up the program's execution by spreading the work from one thread/one processor to multiple threads that can execute in parallel on multiple processors.
* Specialization: Give hight priority to tasks that handle more important tasks; Potentially, the thread keep its entire state in the processor cache(hot cache, cache lookups are fast), and the thread can run its task without interruption.
* Why not just write a multiprocess application?
    * Process doesn't share address space and execution context, all of the data have to be allocated memory. Threads share address space and the execution code which makes it more memory-efficient.
    * Inter process communication (IPC) - is more costly than inter thread communication, which consists primarily of reading/writing shared variables.

* Are threads useful on single CPU?
    * Yes, when (t_idle) > 2 * (t_ctx_switch). e.g. disk I/O or network I/O.
        * <img src="https://i.imgur.com/fZQIY5e.jpg" style="width: 300px" />
* Multithreading the OS kernel, support multiple execution contexts, which is particularly useful when we do have multiple CPUs so OS can run threads behalf of the apps and run os-level daemons/drivers on different threads.

## Basic Thread Mechanisms

* Threads can access the same physical memory address, which introduced a data race problem. If threads all access the same address, and make changes, the data will be inconsistent. To avoid the problem, there is a mechanism called mutual exclusion(mutex), which can be used for making the memory access exclusive. And it also offer waiting condition to let threads work with each other.

* Thread data structure: 
    * A thread have thread id, program counter, stack pointer, registers, attributes, etc.
* Create a thread: `fork(proc, args)`(not UNIX fork)
    * When fork is called, a new thread is created/forked from the parent thread.
* Join the thread back to parent thread: `join(thread)` which need to be called on the parent thread
    * when `join` is called, the parent will be blocked until child thread is finished. So watch out if there is a `while(true)` for loop in child thread:D
    * After join returns, the resource associated with child thread will be deallocated.
* Example
    * <img src="https://i.imgur.com/fFq4Hx8.jpg" style="width: 600px" />
    * thread 1 might run before or after the function call `safe_insert(6)`, so there is no guarantee which `safe_insert` will be executed first.

## Mutual Exclusion(mutex)

* To avoid multi threads access the same address at the same time, operating systems support a construct called a **mutex**. **A mutex is like a lock that should be used whenever you access data/state that is shared among threads.** When a thread locks a mutex, it has exclusive access to the shared resource. Other threads attempting to lock the same mutex will fail. 
* How it works:
    * <img src="https://i.imgur.com/dPMqY03.jpg" style="width: 600px" />
    * When T1/T2/T3 attempt to acquire the lock, only one will have the chance to get it.
* There are two different APIs:
    
    ```c
    // 1. lock block
    lock(m) {
        // critical section
    }
    
    // 2. separate function
    lock(m)
    // critical section
    unlock(m)
    ```

## Condition Variable

* Let's take a look at a producer and consumer example. This is the pseudocode. It has three pieces:
    * main: create 10 producer threads, and 1 consumer thread
    * producers: lock the mutex, and insert one id (note, it's `my_list->insert`
    * consumer: lock the mutex, clean up the list if it's full, otherwise it wait and try again.
    * <img src="https://i.imgur.com/MwtnqbF.jpg" style="width: 600px" />
    * The problem is that the consumer shouldn't keep running check whether the list is full but gets notified once it's full. This is when `Condition` is useful.
* <img src="https://i.imgur.com/s70WRi3.jpg" style="width: 600px" />
* In the image above, the `Wait` is a condition function that being called for waiting for the condition `list_full` and `Signal` is used for notifying another thread that the condition `list_full` is met.

* Condition Variable API
    1. Wait(mutex, cond)
        1. mutex is automatically released & re-acquried on wait
    2. Signal(cond)
        1. notify only one thread waiting on condition
    3. Broadcast(cond)
        1. notify all waiting threds
* What happened in the wait function?

    ```
    Wait(mutex,cond) {
        // atomically release mutex 
        // and go on wait queue
        
        // wait ...
        
        // remove from the wait queue
        // re-acquire mutex
        // exit the wait operation
    }
    ```
    
    * Notice that the mutex is **RELEASED** once the thread goes to the wait stage.

* The Quiz: Instead of `while`, why did we not simply use 'if'?
    
    ```
    Lock(m) {
        while (my_list.not_full()) 
            Wait(m, list_full);
        my_list.print_and_remove_all();
    } // unlock
    ```
    
    * `while` can support multiple consumer threads;
        * if it's `if`. When multiple threads get into the wait condition, and they all get notified the condition. They will acquire the lock one by one and execute `my_list.print_and_remove_all();` regardless it's full or not. The list can change before any consumers access it. `while` can guarantee that `my_list.print_and_remove_all();` only being called when it's full.
    * `if` cannot guarantee access to m once the condition is signaled;

## Readers/Writer Problem

* **Read/write problem**: some subset of threads that want to read from shared state, and one thread that wants to write to shared state.
* To solve the problem,
    * one way is to use two counters: one for read_counter, the other for writer_counter, so
        * when read_counter == 0 and writer_counter == 0, read is ok, writer is ok.
        * when read_counter > 0 read is ok
        * when writer_counter == 1, neither read nor write.
    * the other way is to use one counter: `resource_counter` to indicate resource usage situation: 0: free, -1: 1 writer, >0: multiple readers
    * <img src="https://i.imgur.com/MOquvBQ.jpg" style="width: 600px" />
* Here are some pseudocodes for the second approach:
    * <img src="https://i.imgur.com/iI4hMCg.jpg" style="width: 600px" />
    * The `writer_phase` is used in `reader_thread` for signaling the writer thread.
    * The `reader_phase` is used in `writer_thread` for signaling the writer thread.
    * The `resource_counter` is a **proxy variable** that reflects the state that the current resource is in. Instead of controlling updates to the shared state, we can instead control access to this proxy variable. As long as any update to the shared state is first reflected in an update to the proxy variable, we can ensure that our state is accessed via the policies we wish to enforce.
    * Notice the order of `Broadcast(read_phase); Signal(write_phase);`, it prefer readers than writer.
* Critical Section Structure of the code:
    * <img src="https://i.imgur.com/41K52U2.jpg" style="width: 600px" />
    * Both of the writer and readers follow the structure:
        * <img src="https://i.imgur.com/0z9HTAV.jpg" style="width: 600px" />
    * This implementation allows dealing complex situation that mutex doesn't support, like one writer/multiple writer.

## Avoiding Common Pitfalls

* keep track of mutex/cond. variables used with a shared resource.
    * e.g. add comments on the mutex
* check that you're always using lock/unlock
* using a single mutex to access a single resource!
* check that you're signaling correct condition
* check that you are not using signal when broadcast is needed
    * only 1 thread will proceed... remaining threads will continue to wait.
* ask do you need priority guarantee.

### Spurious Wake-ups

* <img src="https://i.imgur.com/TYMYMGj.jpg" style="width: 600px" />

* This is a problem doesn't necessary affect correctness but may impact performance.
* The root cause is that boardcast() and signal() been called inside the lock, and when the reader was signaled, the writer might still holds the lock. Then the reader will switch from the read_phase wait lock to the counter_mutex lock and doesn't do anything useful, but wasted several context switch from the CPU.
* Let's see some examples:
    * <img src="https://i.imgur.com/euhZ4v2.jpg" style="width: 600px" />

    * Put the broadcast and signal outside of the lock block will solve the spurious wake-up issue for the writer, but we can't put the `signal(writer_phase)` outside the lock because we can't continue to access the protected resource: `if(counter_resource == 0)` out of the lock.

### Deadlocks

* Def: when two or more competing threads are waiting on each other to complete, but none of them ever do.
* E.g. the lock m_A and m_B created a **cycle**
    * T1 -> lock(m_A) -> lock(m_B) -> foo1(A, B)
    * T2 -> lock(m_B) -> lock(m_A) -> foo2(A, B)
    * 
* How to avoid:
    * fine-grained locking. Always unlock A before locking B
    * Use mega lock to lock all resources. It's useful for some cases, but it's too restrictive, and limited parallelism.
    * **maintain lock order,** every thread needs to acquire m_A at first, then m_B.
        * This is the most common solution.
* In summary, A cycle in the wait graph is **necessary** and **sufficient** for a deadlock to occur.
    * edges from thread waiting on a resource to thread owning a resource
* What can we do?
    * deadlock prevention
        * Each time a thread is about to acquire a mutex, we can check to see if that operation will cause a deadlock. This can be expensive.
    * Deadlock detection & recovery rollback
        * We can accomplish this through analysis of the wait graph and trying to determine whether any cycles have occurred. This is still an expensive operation as it requires us to have a rollback strategy in the event that we need to recover.
    * Ostrich algorithm. Simply do nothing, and reboot the system if the system goes wrong.

## Kernel-Level Threads Vs. User-Level Threads

* **Kernel level threads** imply that the operating system itself is **multithreaded**. Kernel level threads are visible to the kernel and are managed by kernel level components like the **kernel level scheduler**. The operating system scheduler will determine how these threads will be mapped onto the underlying physical CPU(s) and which ones will execute at any given point.
* Some kernel level threads may exist to support user level applications, while other kernel level threads may exist just to run **operating system level services**, like daemons for instance.
* At the user level, the processes themselves are multithreaded and these are the user level threads. **For a user level thread to actually execute, it must first be associated with a kernel level thread, and then the OS level scheduler must schedule that kernel level thread on the CPU.**

### Multithreading Models

* One-to-One Model
    * each user level thread associated with one kernel thread.
    * Advantages:
        * OS understands the needs of the threads, like I/O blocking
    * Disadvantages:
        * Expensive, must go to kernel and do the system call.
        * Rely/Limited on the mechanisms and policies supported by the kernel.
* Many-to-One Model
    * All user level threads for a process associated with one kernel thread.
    * Advantages:
        * Everything is done at the user level, which frees us from being reliant on the OS limits and policies.
    * Disadvantage:
        * OS loses its insight into application needs. If the **user-level library** scheduled a blocking operation like I/O, the kernel level thread will see the thread is blocked and end up blocking the entire process.
* Many-to-Many Model
    * some user threads to have a many-to-one relationship, the other have one-to-one.
    * Advantage:
        * The kernel is aware that the process is multithreaded since it has assigned multiple kernel level threads to the process. 
        * Some threads can be scheduled to any kernel-level threads, which is called **unbound** thread. If a user-level thread is mapping to a kernel level thread permanently, it's called **bound** thread.
    * Disadvantage:
        * requires extra coordination between user-level and kernel-level management.

### Scope of Multithreading

* The questions is whether the threads inside a process is visible to kernel or not. 
    * If not, it's called **process scope**, and the **user level library** manage the threads for the given process it linked to, the OS/Kernel can't see them, and will  probably allocate the CPU relative to the total amount of user threads evenly. 
    * If yes, it's called **system scope**, and the **OS-level thread managers**(e.g. CPU scheduler) will be aware of the amount of threads in the process and allocates the threads by the total amount of threads.
* e.g. A has 6 threads, B has 3 threads. 
    * if they are in the process scope, 50% of the kernel threads will be allocated to A, 50% to B.
    * if they are in the system scope, the total 9 threads will be evenly allocated into all kernel threads.

## Multithreading Patterns

### Boss/Workers Pattern

* boss: assign work to workers | workers: perform entire task
* throughput of the system limited by boss thread => must keep boss efficient
    * throughput = 1 / boss_time_pre_task 
* Different ways boss assign works
    1. directly signaling specific workers
        * Boss needs to do some extra work to track every worker's status.
        * Workers don't need to synchronize with the others
    2. establish a queue between the boss and the workers
        * boss is a producer, and the workers are consumers
        * boss doesn't need to know the process detail in the worker
        * worker takes job from the queue from the top and process it
        * synchronization is required, need to maintain a concurrent queue so only one worker can retrieve from it.
* For the second approach, the queue filling up is dependent primarily on **the number of workers**. So how many? 
    1. create on demand. inefficient, the cost of creating thread is significant.
    2. more common ways: create a fix-sized pool of workers. Can be increased when high demands.
* One downside of second approach:
    * **locality**. Boss doesn't keep the status of any workers, not aware of whether the task is simple or not.
    * One solution to this is, **worker variants**. Use a subset of workers to work on the same specific works. Since the jobs are the same, the state is likely be present in hot cache, aka better performance.
    
### Pipeline Pattern

* The overall task is divided into subtasks and each of the subtasks are assigned a different thread. each of the subtasks might have different amount of threads.
* The throughput of the pipeline will be dependent on the weakest link in the pipeline; that is, the task that takes the longest amount of time to complete.
* The best way to pass work between these stages is a shared buffer base communication between stages. That means the thread for stage one will put its completed work on a buffer that the thread from stage two will read from and so on.
* A key benefit of this approach is specialization and locality, which can lead to more efficiency, as state required for subsequent similar jobs is likely to be present in CPU caches.
* A downside of this approach is that it is difficult to keep the pipeline balanced over time. When the input rate changes, or the resources at a given stage are exhausted, rebalancing may be required.

### Layered Pattern

* Similar to pipeline pattern. instead of putting each task into a thread, this approach groups similar tasks into a "layer" and the threads assigned to the layer can work on the group of subtasks.
* A benefit of this approach is that we can have specialization while being less fine-grained than the pipeline pattern. However it's not suit for all applications.

### Quiz

* For a 6-step toy order application, and 6 threads. We have two solutions:
    1. a boss-workers solution
        1. a worker process a toy order in 120ms
    2. a pipeline solution, 
        1. each of the 6 steps take 20ms
* How long will it take for these solutions to complete 10 and 11 orders?
    * boss-worker (10): 240ms
    * boss-worker (11): 360ms
        * Note that, one of threads is boss, 5 are workers
    * pipeline (10): 300ms
        * how to calculate?
            * Once the first job is popped, that's 120ms. Then every 20ms, there is another one finished. So:
                * 120 + 9 * 20 = 300ms
    * pipeline (11): 320ms