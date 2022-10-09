# P2L1: Processes and Process Management

<!-- toc -->

----

## What is a Process

* First of all, OS manages hardware on behalf of applications. **Process** is a state of a program that is loaded in memory and executing. Comparing to **application**, as a **static entity**, which is a program that stored on disk, process is an **active entity**.

* A process in memory:

    * <img src="https://i.imgur.com/4Le9TjY.jpg" style="width: 200px" />
    * type of state:
        * text and data:
            * static state when process first loads
        * heap
            * dynamically created during execution
        * stack
            * grows and shrinks when executing functions with LIFO stategy

### Address Space 
    
* Process uses virtual addresses for locating the process in memory. The OS maps the **virtual addresses** to **physical addresses**(DRAM) location in phlysical memory by using **page tables**.
* Once the memory is out of space, the OS dynamically decides which addresses should be located in physical memory or **swapped** to disk.

* Some explanations about memory types:
    * Stack
        * is allocated and deallocated by the compiler **implicitly**, also called automatic memory. it's used to keep track of where the program is
            * e.g. `void func() { int x; }` // declares an integer on the desk, will be deallocated when function returns.
    * Heap
        * all allocations and deallocations are explicitly handled by programmers.
            * e.g. 
            
                ```
                void func() {
                    int *x = (int *) malloc(sizeof(int));
                    ...
                    free(x);
                }
                ```
            
                * **int *x**: the complier make room for the pointer
                * **malloc()**: requests spcae for an integer on the **heap**, return either the address of the integer or NULL if fails.
                    * notice if you print out the size of x: `printf("%d\n", sizeof(x));`, it's gonna be the size of pointer, not the integer.
                * **free()**: free the heap memory.


### Process Execution State

* As any given time, CPU needs to know the instruction sequence the programing is. The CPU uses **program counter**(PC) to register the state.
* Another state defined what a process is doing is **stack**. And the top of the stack is defined *stack pointer** which reperents the last executing code of the program due to LIFO. 
* To maintain all of the info of every process, the OS maintain a **process control block(PCB)**

* [what are registers?](https://www.learncomputerscienceonline.com/what-are-cpu-registers/)

### Pcroess Control Block

* A process control block is a data structure that OS maintained for every process. It contains:
    * process state
    * process number
    * process counter <-- change frequently
    * CPU registers
    * memory limits
    * CPU scheduling info
* PCB is crated when process is created, certain fields updates when process state changes.
* How PCB is Used
    * The CPU only runs a process for a period of time, and then switch to another one, and back and forth. For every switch, the OS needs to store the PCB in memory when executing another process and resume the state once the CPU runs it again.
    * The Switch action is called **context switch**.
* Context switch is expensive, it requires store and reload cache from memory and continue the process. So the OS needs to be wise on this.
* There are direct costs: the number of CPU cycles requried to load and store a new PCB to/from memory; indirect costs: if the data is cached in L1/2/3 cache, it's called **Hot Cahe**, very fast to retrieve. But from time to time, the process might be swapped out from cache, and to load it again, the cache is **cold** and require more cycles to fetch from memory.

### Life Cycle

* Process States
    * <img src="https://i.imgur.com/0pQ5F7Z.jpg" style="width: 500px" />
    * new: allocates/initializes the PCB for this process. 
* Process Creation - two mechanisms
    * fork
        * OS creates a new PCB for the child, and then will copy the exact same values from the parent PCB into the child PCB. Both processes will continue executing with the exact same state at the instruction immediately following the fork.
    * exec
        * OS loads a new program. The child's PCB will now point to values that describe this new program. The program counter of the child will now point to the first instruction of the new program.
* The parent of all processes in UNIX-based OS is `init`.

### CPU Scheduler

* Lots of processes in the ready queue, the **scheduler** needs to decide **which one** will be dispatched to run and **how long**.
* The OS needs to:
    * preempt: interrupt and save current context
    * schedule: run scheduler to choose next process
    * dispatch: dispatch process/switch into its context
* How long should a process run for?
    * The goal is, not to do context switch too frequently but also fair.
    * There are lots of algorithem implemented to make the decision.

### I/O

* When a process makes an I/O request, the operating system will deliver that request, and move the process to the I/O queue for that particular I/O device. The process will remain in the queue until the request is responded to, after which the process will move back to a ready state (or might immediately be scheduled on the CPU).
* <img src="https://i.imgur.com/GsD803O.jpg" style="width: 500px" />

### Process Interaction

* For example, web server need to accesss database to read data and return the client.
* This is called Inter-Process Communication(IPC):
    * Transfer data/info between address spaces
    * Maintain protection and isolation
    * Provide flexibility and performance
* Two implementations:
    * Message-passing IPC:
        * The OS provides communication channle, like share buffers.
        * The process write(send)/read(recv) message to/from **channels**
        * Positive: OS manages the work
        * Downside: Overheads. Every information has be copied to channel and to another process
        * <img src="https://i.imgur.com/WPrAVtZ.jpg" style="width: 300px" />

    * Shared Memory IPC
        * OS establishes a share channel and maps it into each process address space
        * Process directly read/write from the momroy
        * Positive: OS is out of hte way
        * Downside: developers need to implement the code
        * <img src="https://i.imgur.com/lgu76Xu.jpg" style="width: 300px" />
* Does Shared Memory performa better than message passing communication?
    * It depends. Although, it doesn't require data copy, the actual memory mapping is expensive.

