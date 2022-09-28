# P2L2: Threads and Concurrency 

<!-- toc -->
----

## Process vs. Thread

* A process owns a virtual memory space and OS initialize a PCB to manage the state.
* A thread is also called 
* PCB: single thread process vs multithreaded process
    * ![](/images/16642403768260.jpg)
    * Tthe PCB for multithreaded process is different. In a multi-threaded process, threads share the same code/data/filter, but also have its own registers and stack.

## Benefits of Multithreading

* Parallelization: Speed up the program's execution by spreading the work from one thread/one processor to multiple threads that can execute in parallel on multiple processors.
* Specialization: Give hight priority to tasks that handle more important tasks; Potentially, the thread keep its entire state in the processor cache(hot cache, cache lookups are fast), and the thread can run its task without interruption.
* Why not just write a multiprocess application?
    * Process doesn't share address space and execution context, all of the data have to be allocated memory. Threads share address space and the execution code which makes it more memory-efficient.
    * Inter process communication (IPC) - is more costly than inter thread communication, which consists primarily of reading/writing shared variables.

* Are threads useful on single CPU?
    * Yes, when (t_idle) > 2 * (t_ctx_switch). e.g. disk I/O or network I/O.
        * ![](/images/16643240276439.jpg)
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
    * ![](/images/16643255661268.jpg)
    * thread 1 might run before or after the function call `safe_insert(6)`, so there is no guarantee which `safe_insert` will be executed first.

## Mutual Exclusion(mutex)

* To avoid multi threads access the same address at the same time, operating systems support a construct called a **mutex**. **A mutex is like a lock that should be used whenever you access data/state that is shared among threads.** When a thread locks a mutex, it has exclusive access to the shared resource. Other threads attempting to lock the same mutex will fail. 
* How it works:
    * ![](/images/16643260382048.jpg)
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
    * ![](/images/16643265308844.jpg)
    * The problem is that the consumer shouldn't keep running check whether the list is full but gets notified once it's full. This is when `Condition` is useful.
* ![](/images/16643276891817.jpg)
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
    * ![](/images/16643300159714.jpg)
* Here are some pseudocodes for the second approach:
    * ![](/images/16643309225383.jpg)
    * The `writer_phase` is used in `reader_thread` for signaling the writer thread.
    * The `reader_phase` is used in `writer_thread` for signaling the writer thread.
    * The `resource_counter` is a **proxy variable** that reflects the state that the current resource is in. Instead of controlling updates to the shared state, we can instead control access to this proxy variable. As long as any update to the shared state is first reflected in an update to the proxy variable, we can ensure that our state is accessed via the policies we wish to enforce.
    * Notice the order of `Broadcast(read_phase); Signal(write_phase);`, it prefer readers than writer.
* Critical Section Structure of the code:
    * ![](/images/16643309746929.jpg)
    * Both of the writer and readers follow the structure:
        * ![](/images/16643310156604.jpg)
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

* This is a problem that 
wake up is not necessary, the threads need to wait again

Deadlocks

## Kernel Vs. User-Level Threads

* Multithreading Models
    * One-to-One Model
    * Many-to-One Model
    * Many-to-Many Model
* Scope of Multithreading

## Multithreading Patterns

* Boss/Workers Pattern
    * boss: assign work to workers
    * workers: perform entire task

    Throughput of the system limited by boss thread => must keep boss efficient
    Throughput = 1 / t 

* Pipeline Pattern
* Layered Pattern