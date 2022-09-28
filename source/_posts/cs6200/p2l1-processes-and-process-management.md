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

----

Note from book: Operating Systems Three Easy Pieces by Remzi H Arpaci-Dusseau, Andrea C Arpaci-Dusseau

## Scheduler -- choose what to run

* **Scheduling Metrics** 
    1. turnaround time -- $T_{\text{turnaround}} = T_{\text{complete}} - T_{\text{arrives}}$

* Some assumptions about the "workload"(the set of processes that OS needs to run) to simplify the problem:
    1) all jobs(processes) arrive at once
    2) just use CPU (no I/O)
    3) running time of each job is known
* Algorithm #1: FIFO
    * Base on the assumption, if we have three jobs: A, B, C, and each takes 10s, then the average turnaround time = $\frac{10+20+30}{3} = 20s$
    * if B needs 100s, then the average turnaround time = $\frac{10+110+120}{3} = 110s$.
    * The problem here is called **convoy effect**, a short job was queued behind a heavyweight job.
* Algorithm #2: SJF(Short Job First)
    * This solves the convoy effect problem because A and B get to run at first, the turnaround time = $\frac{10+20+120}{3} = 50s$.
    * What if we relex the assumption #1, and job A and C come after 10s?
        * $T = \frac{100+(110-10)+(120-10)}{3} = 103.33s$
* Algorithm #3: STCF(Shortest Time-to-Complietion First
    * In this case, even A and C come later after 10s, the CPU will switch to them immediately after they jump in. So, $T = \frac{(120-0)+(20-10)+(30-10)}{3} = 50s$.

* A New Metric for later algorithm comparison: **Response Time** $T_{\text{response}} = T_{\text{firstrun}} - T_{\text{arrival}}$ 

* Algorithm #4: Round Robin
    * each job gets to run for a **time slice** alternatively.
    * Then:
        * the average of turnaround time of RR is $\frac{28+30+110}{3}=56s$
        * And the average of response time of RR is $\frac{0+1+2}{3} = 1s$ but SJC is $\frac{0+100+110}{3}=70s$ and STCF is $\frac{0+10+20}{3}=10s$ 
* Summarize:
    * two types of schedulers:
        * SJF, STCF: good turnaround time, bad response time.
        * RR: good response time, bad turnaround time.
    * And still haven't relexed assumptions: 2, 3

### Scheduling - Multi-level Feedback Queue (MLFQ)

* No assumptions, aka: 1) don't know job length; 2) do I/O as well; 3) workload can be interactive or long-running as background jobs.
    * interactive jobs are short-running and may frequently relinquish the CPU
* Used in Windows and Unix(not Linux)
* Definition of MLFQ:
    * Create a number of distinct queues, each assigned a different priority level.
    * At any given time, a job can only be on one queue.
    * Use priority to decide which job should run at a given time: a job with higher priority is chosen to run.
        * If more than one on the same priority, use round-robin to run them alternatively.
* Rules:
    * Rule 1: If Priority(A) > Priority(B), A runs (B doesn’t).
    * Rule 2: If Priority(A) = Priority(B), A & B run in RR.
    * Rule 3: When a job enters the system, it is placed at the highest priority (the topmost queue).
    * Rule 4: Once a job uses up its time allotment at a given level (regardless of how many times it has given up the CPU), its priority is reduced (i.e., it moves down one queue).
        * e.g. the time slice in Queue 8 is 10ms, and job A only spent 3ms and starts to wait for an I/O. In this case, the job stays in Queue 8 until the I/O gets back and A consumes the entire 10ms before moving it to next level.
    * Rule 5: After some time period S, move all the jobs in the system to the topmost queue.
        * This is to avoid the problem of **starvation**: too many interactive jobs consumed all CPU times and the long-running jobs never recieve any CPU time.

### Scheduling - Proportional Share

* Propotional share means: a scheduler trys to guarantee that each job obtain a certain percentage of CPU time. There are three approaches: **lottery scheduling**, **stride scheduling**, and **the Completely Fair Scheduler (CFS)** of Linux.

* Lottery scheduling
    * Each process are assigned certain amount of **tickets**, and the scheduler randomly picks a number, and the process holding the number gets scheduled.
        
        ```
        // counter: used to track if we’ve found the winner yet int counter = 0;
        // winner: use some call to a random number generator to // get a value, between 0 and the total # of tickets int winner = getrandom(0, totaltickets);
        // current: use this to walk through the list of jobs node_t * current = head; while (current) {
        counter = counter + current->tickets;
        if (counter > winner)
            break; // found the winner
        current = current->next; } // ’current’ is the winner: schedule it...
        ```

        * <img src="https://i.imgur.com/GHp42Lz.jpg" style="width:500px" />

    * Question 1: how many tickets should we assign to each process?
        * The shares are base on users. For example, we have two Users A and B, A has jobs: A1, A2, B has one job: B1. And the total tickets are 100, then A1 and A2 gets 25 each, and B1 gets 50.
    * Question 2: How to calculate the fairness?
        * use **unfaireness metric U**. Assuming two jobs both needs 10s to finish and A finished in 10, and B finished in 20. Then $U=\frac{10}{20} = 0.5$. Our goal is to achieve `U=1`.

* Stride scheduling - a deterministic fair-share scheduler
    * Each job in the system has a **stride**, which is inverse in proportion to the number of tickets it has. The scheduler then uses the stride and **pass** to determine which process should run next.
    * The basic idea is simple: at any given time, pick the process to run that has the **lowest pass value** so far; when you run a process, increment its **pass counter** by its stride.
    * For example, A, B and C have 100, 50 and 250 tickets. Devided 10,000 by each's stride value, we gets: A: 100, B: 200, C: 40. Then decide which to run as:
        * <img src="https://i.imgur.com/8tYgG78.jpg" style="width:400px" />
        * A B and C all start at 0, so pick A at first. when reaching 100, run B and C in a sequence. Then C has the minimum pass value, the scheduler runs C until it reach 120, then switch to A.

* The Completely Fair Scheduler (CFS) of Linux
    * Fairly divide a CPU evenly among all competing processes. It does so through a simple counting-based technique known as **virtual runtime** (**vruntime**): the amount of time the process has spent on the processor.
    * Several main configs that the scheduler used:
        * **sched_latency**: The scheduler period is a period of time during which all runnable tasks should be allowed to run at least once. a typical value is 48ms, so if there are 4 processes, the per-process time slice is 12ms.
        * **min_granularity**: the minimum time slice of a process. usually 6ms. so if there are more than 8 processes, each will have at least 6ms time slice.
        * **weighting(niceness)**: enable control over process priority. CFS maps the **nice** value of each process to a weight, as shown here:

            ```
            static const int prio_to_weight[40] = { 
                / * -20 * / 88761, 71755, 56483, 46273, 36291, 
                / * -15 * / 29154, 23254, 18705, 14949, 11916, 
                / * -10 * / 9548, 7620, 6100, 4904, 3906, 
                / * -5 * / 3121, 2501, 1991, 1586, 1277, 
                / * 0 * / 1024, 820, 655, 526, 423, 
                / * 5 * / 335, 272, 215, 172, 137, 
                / * 10 * / 110, 87, 70, 56, 45, 
                / * 15 * / 36, 29, 23, 18, 15,
            };
            ```
            
            * $\text{time}\_\text{slice}_k = \frac{\text{weight}_k}{\sum_{0}^{n-1}\text{weight}_i} \cdot  \text{sched}\_\text{latency}$ 
            * To improve the efficiency, the scheduler uses [Red-Black Trees](https://cs.ericyy.me/algorithms-1/week-5/index.html#red-black-bsts) with the **vruntime** values of each process and run the **min-vrumtime** process at each time and push it back to the tree after the time slice.
    * What about I/O and sleeping process?
        * if the process gone for sleeping for a long time, when it wakes up, it might monopolize the CPU for a long time. To avoid this, CFS sets the vruntime of that job to the minimum value that found in the tree.