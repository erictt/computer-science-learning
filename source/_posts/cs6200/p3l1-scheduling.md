# P3L1 : Scheduling

<!-- toc -->
----

## Overview

* The CPU scheduler
    * decides how and when the processes (and their threads) access the shared CPUs.
    * schedules tasks running on both user level and kernel level.
* The CPU scheduler choose one of the ready tasks to run on CPU, and it runs when
    * CPU becomes idle
    * new task becomes ready
    * timeslice expired timeout
* Once the thread is dispatched on CPU, the CPU will do all of the jobs: context switch, enter user mode, set PC, and go.
* The questions are:
    * which task should be selected? -> schedule policy/algorithm
    * how is this done? -> depends on runqueue data structure

## Scheduling Algorithm

### Run To Completion

* **Run To Completion** scheduling assumes that once a task is assigned to a CPU, it will run on that CPU until it is finished.
* Initial assumptions:
    * group of tasks/jobs
    * known execution times
    * no preemption
    * single CPU
* common metrics we use for measuring the performance of the algorithms:
    * throughput
    * average job completion time
    * average job wait time
    * CPU utilization
* Let's compare two implementations:
    * **First Come First Serve (FCFS)**, schedule the tasks in the order of arrival.
        * e.g. T1(1s), T2(10s), T3(1s), arriving order: T1 - T2 - T3
        * average completion time is (1s + 11s + 12s) / 3 = 8s. 
        * average wait time is (0s + 1s + 11s) / 3 = 4s.
    * **Shortest Job First (SJF)**, schedule the order base on their execution time.
        * e.g. T1(1s), T2(10s), T3(1s), arriving at the same time
        * the execution order will be: T1 -> T3 -> T2

### Preemptive

* Preemptive means the job can be interrupted after it's execution started.

* SJF + Preempt
    * T2 arrives at 0s, T1 and T3 arrives at 2s, so T2 should be preempted

    * <img src="https://i.imgur.com/J1Qwqim.jpg" style="width: 400px" />

    * In this case, we assumed we know the execution time. But it's not realistic. What we can do is, generate heuristics base on the similar jobs in the past.
        * It can base on a single task, or base on the average execution time for n past tasks **(windowed average)**.
* Priority
    * This means we run the tasks base on their **priority levels**, and run the highest priority task next(preemption)
    * <img src="https://i.imgur.com/22Dl6io.jpg" style="width: 400px" />

    * This algorithm might causes **starvation**, in which a low priority task never gets executed due to high priority tasks keep jumping in.
        * The solution is **priority aging**, so priority = f(actual priority, time spent in runqueue) so if a job's priority will increase as it stays in the runqueue for long enough.

#### Priority Inversion

* <img src="https://i.imgur.com/b9JScO5.jpg" style="width: 600px" />


### Round Robin Scheduling

* each task gets to run for a **time slice** alternatively.
    * similar to FCFS, we pick up the first available task from the queue
    * each task runs a certain amount of time, or
        * the task yield if it waits on I/O
    * This algorithm can work with priorities(including preemption) as well.

## Timesharing and Timeslices

* **Timeslice** = maximum amount of uninterrupted time given to a task
    * also called **time quantum**
* task may run less than timeslice time, if
    * the task has to wait on I/O, synchronization. The task will be placed on a queue and preempted.
    * higher priority task becomes runnable before the lower priority task's timeslice has expired.
* using timeslices allows for the tasks to be interleaved. And it's also the only way to achieve timesharing of the CPU for the CPU bound tasks.
    * I/O tasks are not critical though.
* e.g.
    * <img src="https://i.imgur.com/8cscM2e.jpg" style="width: 600px" />

    * For metrics, 
        * the throughput stays the same, 
        * the average wait and average completion time are close to SJF, but no need for priority knowledge of execution times, which was said was unfeasible in a real system.
* The downside of timeslicing is the overhead. We have exaggerated in our graphs that there is no latency between tasks, but this is not the case. In real case, we have to interrupt the running task, execute the scheduler, and context switch to the new task. **Even when there is only one task, the scheduler sill needs to run at the timeslice intervals.** 
    * Consider this, our throughput will be lower than 0.25, and avg. wait and avg. comp. will be higher.

### How Long Should a Timeslice Be

* Depends on whether the tasks are CPU bounded or I/O bounded.

#### CPU Bound Timeslice Length

* <img src="https://i.imgur.com/eOrJGaQ.jpg" style="width: 600px" />

#### I/O Bound Timeslice Length

* <img src="https://i.imgur.com/NZx7FCP.jpg" style="width: 600px" />

### Summarizing Timeslice Length

* CPU bound tasks prefer longer timeslices
    * limits the number of context switching overheads
    * keep CPU utilization and throughput high
* I/O bound tasks prefer short timeslices
    * I/O bound tasks can issue I/O earlier
    * keeps CPU and device utilization high
    * better user-perceived performance - wait time is low

## Runqueue Data Structure

* Runqueue is either implemented with multiple queues or a tree. The data structure is designed to help scheduler to determine which task to run next easily. 
* For example,  we want I/O and CPU bound tasks to have different timeslice values. We can either
    1. use the same runqueue, and check the type of tasks
    2. use two different data structures.
* Common way for the example, is to build a multi-queue data structure. Each queue associated with different timeslice values:
    * <img src="https://i.imgur.com/u4Kh5jg.jpg" style="width: 500px" />
    * The I/O intensive tasks are assigned to the queue with shorter timeslices, The CPU intensive tasks are assigned to the queue that has infinite timeslice but lowest priority.
    * The benefits with this design are:
        * timeslicing benefits for I/O bound tasks,
        * timeslicing overheads avoided for CPU bound tasks.
    * To determine whether a task is CPU or I/O intensive, we can use history based heuristics. However, it won't help with the new tasks or the tasks with dynamic behaviors.
    * To fix the problem, we can initially put every new tasks into the the queue with top priority. If the task yields before timeslice expire, then it stay in the queue, otherwise, move it down to next queue with lower priority, and keep going until it gets pushed into the last queue.
    * The resulted data structure is called **Multi-Level Feedback Queue(MLFQ)**, which is a group of queues that associated with different scheduling policies. The data structure provides feedback to tasks and help to adjust the tasks in different levels.

### Linux O(1) Scheduler

* The Linux O(1) scheduler add/select tasks in constant time. It's a preemptive, priority-based scheduler, with 140 priority levels. level:0-99 are real-time tasks, level: 100-139 are timesharing tasks. The default value for a user process is 120, and can be adjusted with the **nice value**: (-20 - 19).
    * <img src="https://i.imgur.com/hngR40I.jpg" style="width: 400px" />

* The O(1) scheduler use the same ideas as the MLFQ scheduler. It sets up **different timeslice values to different priorities**(smallest for low priority, highest for high priority), and **use feedback to adjust the tasks** in the future.
    * The feedback for the task is depends on how long the task spend on sleep(waiting/idling). 
        * longer sleep -> interactive -> priority -5 (boost),
        * smaller sleep -> compute-intensive -> priority+5(lowered)
* The scheduler is implemented with two arrays: **active** and **expired**.
    * <img src="https://i.imgur.com/mo2lVrN.jpg" style="width: 400px" />
    * The active list is the primary one that the scheduler uses to select the next task to run. Once the task runs, it will be put on expired array. And the two arrays will be swapped when the active array is empty.
* The problem of O(1) scheduler is, the task could wait unpredictable amount of time to be scheduled. Because the task will not get a chance to run again until all other tasks in the active queue have been executed.
    * Meaning it doesn't work well with the applications that have **realtime/interactive needs**, like gaming, video streaming, etc.
    * Plus, it doesn't offer fairness guarantees as well -> a task should be able to run for an amount of time that is relative to it's priority.

### Linux CFS Scheduler

* As a replacement for the O(1) scheduler, the CFS scheduler was introduced to solve the problem O(1) scheduler has.
* CFS uses a [read-black tree](/algorithms-1/week-5/index.html#red-black-bsts) as the runqueue data structure.
    * <img src="https://i.imgur.com/m2zvO5A.jpg" style="width: 400px" />
        * Red-black tree is self-balancing trees
* Tasks are ordered in the tree **based on the amount of time that they spent running on the CPU**, a quantity known as **vruntime** (virtual runtime). CFS tracks this virtual runtime in a nanosecond granularity.
* This runqueue has the property that for a given node, all nodes to the left have lower vruntimes and therefore need to be scheduled sooner, while all nodes to the right, have larger vruntimes and therefore can wait longer.
* The CFS algorithm always schedules the task with the least amount of vruntime in the system, which is typically the leftmost node of the tree. Periodically, CFS will increment the vruntime of the task that is currently executing on the CPU, at which point it will compare this vruntime with the vruntime of the leftmost task in the tree. If the currently running task has a smaller vruntime than the leftmost node, it will keep running; otherwise, it will be preempted in favor of the leftmost node, and will be inserted appropriately back into the tree.
* CFS changes the effective rate at which the task's virtual time progresses. For lower priority tasks, time passes more quickly. There virtual run time value progresses faster. And therefore, they will lose their CPU more quickly. On the contrary, for the high priority tasks, time passes more slowly.
* Performance of CFS:
    * select task: O(1)
    * add task: O(logN)

## Scheduling on Multiprocessors

*  **multiprocessors vs multicores**
    *  Multiprocessors means there are multiple CPUs. Each CPU has its own private L1/L2 and LL(last-level)  cache which may or may not be shared among the CPUs. Although the system memory(DRAM) is shared.
    *  Multicore means each CPU has multiple internal cores. Each core has it's own private L1/L2 cache. The CPU as a whole shares LLC(last-level cache). DRAM is shared as well.
    * The performance of processes/threads is highly dependent on the amount of execution state that is present in the **CPU cache** or **memory**.
        * The goal is to schedule the thread onto the same CPU that it has executed before because it's likely that the CPU cache is hot. This is called **cache affinity**.
    * To achieve cache affinity, we want to keep tasks on the same CPU as much as possible. To do so, we maintain a **hierarchical scheduling architecture** which has a load balancing component that dividing the tasks into CPUs. Each CPU has its own scheduler with its own runqueue and responsible for scheduling tasks on that CPU exclusively.
    * To load balance across CPUs, we look at the length of each of the runqueue, and also rebalance the queues when a CPU is idle.
    * In addition to having multiple processors, it is possible to have **multiple memory** nodes. The CPUs and the memory nodes will be connected via some physical interconnect.  In most configurations it is common that a memory node will be closer to a socket of multiple processors, which means that access to this memory node from those processors is faster than accessing some remote memory node. We call these: **non-uniform memory access (NUMA)** platforms.
        * From a scheduling perspective, what makes sense is to keep tasks on the CPU closest to the memory node where their state is, in order to maximize the speed of memory access. We refer to this as **NUMA-aware scheduling**.

### Hyperthreading

* The reason we have to context switch among threads is because the CPU only has one set of registers to describe an execution context. Over time, hardware architects have realized they can hide some of the latency associated with context switching. One of the ways that this has been achieved is to have CPUs with multiple sets of registers where each set of registers can describe the context of a separate thread. One term is to refer this is **hyperthreading**.
    * Also called:
        * hardware multithreading
        * chip multithreading (CMT)
        * simultaneous multithreading **(SMT)**
    * In hyperthreading, we have multiple hardware-supported execution context, one CPU. So the context switch is really fast.
* Modern platforms often support two hardware threads, though some high performance platforms may support up to eight. Modern systems allow for hyperthreading to be enabled/disabled at boot time, as there are tradeoffs to this approach. If hyperthreading is enabled, each of these hardware contexts appears to the scheduler as an entity upon which it can schedule tasks.
* Another feature that hyperthreading has is, **hide memory access latency**, because
    * SMT ctx_switch is in order of cycles(O(cyles)), but memory load is in order of 100 cycles(O(100 cycles)).
* What kinds of threads should be co-scheduled on hardware threads?
    * ["Chip Multithreading Systems Need a New Operating System Scheduler" by Fedorova, Alexandra, et. al.](https://s3.amazonaws.com/content.udacity-data.com/courses/ud923/references/ud923-fedorova-paper.pdf)

### Scheduling for Hyperthreading Platforms

* Lets first make some assumptions:
    1. thread can issue instruction on every single cycle
        * max **instruction-per-cycle(IPC)** = 1: **CPU bound** thread will be able to maximize the **IPC** matrix.
    2. memory access = 4 cycles
        * a **memory bound** thread will experience some idle cycles while it is waiting for the memory access to return.
    3. hardware switching instantaneous
    4. SMT with 2 hardware threads
* Now compare different scenarios:
    1. <img src="https://i.imgur.com/hfj0Wg3.jpg" style="width: 400px" />
        
        * threads "interfere" each other,
        * "contend" for CPU pipeline resources
        * performance for each task degrades by 2x
        * memory is idle
    
    2. <img src="https://i.imgur.com/KSjqhq8.jpg" style="width: 400px" />
    
        * CPU idle, waste CPU cycles
    
    3. <img src="https://i.imgur.com/Ir847Rb.jpg" style="width: 400px" />
    
        * mix of CPU and memory-intensive threads
            * avoid/limit contention of processor pipeline
            * all components (CPU and memory) well utilized  
 
### How do tell a thread is CPU bound or memory bound? 

* Previously, we used sleep time to determine a process is interactive or CPU intensive. But it won't work for two reasons:
    * The thread is not really sleeping when it is waiting on memory access. It is waiting at some stage in the processor pipeline, not on some software queue.
    * To keep track of the sleep time we were using software methods and that is too slow at this level. The context switch takes on the order of cycles, so we need to be able to make our decision on what to run very quickly.
* We need some hardware-level information in order to help make our decision.
* Most modern platforms contain **hardware counters** that get updated as the processor executes and keep information about various aspects of execution, like
    * L1, L2 … LLC cache misses
    * Instructions Per Cycle (IPC) metrics
    * Power/Energy usage data
* Tools  for accessing these hardware counters, such as oprofile, linux perf tool.
* So how can hardware counters help us make scheduling decisions?
    * With hardware counters, we can (g)estimate what kind of resource(CPU or memory) a thread needs.  The scheduler can use this information to pick a good mix of the threads that are available in the runqueue to schedule in the system so that all of the components of the system are well utilized and the threads interfere with each other as little as possible.
    * For example, a thread scheduler can look at the number of LLC misses - a metric stored by the hardware counter - and determine that if this number is great enough then the thread is most likely memory bound.
* Even though different hardware counters provide different metrics, schedulers can still make informed decisions from them. 
    * Schedulers often look at multiple counters across the CPU and can rely on models that have built for a specific platform and that have been trained using some well-understood workloads.

### Scheduling with Hardware Counters

* Fedorova speculates that a more concrete metric to help determine if a thread is CPU bound or memory bound is **cycles per instruction (CPI)**. A memory bound thread will take a lot of cycles to complete an instruction; therefore, it has a high CPI. A CPU bound thread will have a CPI of 1 (or some low number) as it can complete an instruction every cycle (or close to every cycle).
* Given that there is no CPI counter on the processor that Fedorova uses - and computing something like 1 / IPC would require unacceptable software intervention - she uses a simulator.
* Testbed: 4 cores x 4-way SMT, total 16 hardware contexts
* Workload: CPI of 1, 6, 11, 16
    * 1 will be most CPU-intensive, 16: most memory-intensive
    *  4 threads of each kind
* Use IPC as the metric. The overall workload, max IPC = 4
* <img src="https://i.imgur.com/HZJlgUR.png" style="width: 600px" />
* CPI Experiment Results
    * <img src="https://i.imgur.com/WBkCwSw.jpg" style="width: 400px" />
    * With mixed CPI => processor pipeline well utilized => high IPC
    * With same CPI => contention on some cores; wasted cycles on other cores
    * So mixed CPI is good.
* Another question is, is this simulation realistic? The answer is no. Fedorova profiled a number of applications from several respected benchmark suites and computed the CPI values, and got:
    * <img src="https://i.imgur.com/HqCft2O.jpg" style="width: 600px" />
    * You can see most of the values are cluttered together around 2.5-4.5. Since CPI isn't very different across applications, it may not  be the most instructive metric to inform scheduling decisions.
* Post Mortem / The key takeways
    * resource contention in SMTs for processor pipeline
    * hardware counters can be used to characterize workload
    * schedulers should be aware of resource contention, not just load balancing
* PS: LLC usage would have been a better choice.

## ----


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