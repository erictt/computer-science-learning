# Virtualizing the CPU

* What are the goals for virtualization?
    * Efficiency
    * Security
        * processes should be isolated from each other

## The Abstraction: The Process

* What changes when a program runs?
    * registers (program counter, general purpose) // [what are registers?](https://www.learncomputerscienceonline.com/what-are-cpu-registers/)
    * I/O (disk, network)
    * memory(address space)
        * techincally, it's virtual memory.

## How to virtualize CPUs?

* The goal is to run N processes "at once" even we have M CPUs(N > M)

* Two key concepts:
    * Mechanisms: low-level methods or protocols that ensure processes running alternatively. e.g. **context switch**, which gives the OS the ability to stop one program and run another.
        * **Time sharing** is a basic technique used by an OS to share a resource. By allowing the resource to be used for a little while by one entity, and then a little while by another, and so forth.
    * Policies: on top of the mechanisms, policies are algorithms for making some kind of decision of which program to run within the OS.

* One example to explain the details: Assume we have one CPU and one process, then the procedure will be: 1) OS boot up; 2) Switch to program P; 3) program P exit and switch to OS;
    * The problems are:
        1. what if P wants to do something restricted? e.g. reading a file that it's not supposed to read.
        2. what if OS wants to stop P and run another program?
        3. what if P does something slow? e.g. disk I/O or network I/O
    * Solotions:
        * Problme 1: use a bit(0 and 1) to indicate the `mode of operation` (user mode or kernel mode)
            * application runs on user mode with limited access, and OS runs on kernel mode with no restriction. The mode switching procedure is called **trap instruction**.
            * There are lots of **system calls** like open(), read() and close() which require the CPU to switch to kernel mode to perform.
                * C has the same functions like open(), read(), but they are hidden inside the system call.
            * A complete example of the switching is:
                1) OS boot up and set up the **trap handler** and then switch to user mode to run program(this is called **return-from-trap**)
                2) The program runs in user mode and switch to kernel mode(this is called **trap**) to utilize system calls, and **return-from-trap** later on, then **exit()** eventually.
            * this whole mechanism is called **limited direct execution**
        * Problem 2: a **timer interrupt** is programmed in the CPU that interrupt processes every x ms, and a pre-conﬁgured **interrupt handler** in the OS runs.
            * The OS has a **scheduler** to decide what's the next step and execute a **context switch**. 
                * A context switch is conceptually simple: all the OS has to do is save a few register values for the currently-executing process (onto its kernel stack, for example) and restore a few for the soon-to-be-executing process (from its kernel stack).
        * Problem 3: Use process states. e.g. when a process initiated an I/O request to a disk, it becomes **blocked** and thus some other process can use the processor. Here are the other states:
        * <img src="https://i.imgur.com/tgM8fmf.jpg" style="width:400px" />
        * Running: a process is running
        * Ready: a process is ready, but OS has chosen not to run it at the moment
        * Blocked: waiting for other events to be finished. e.g. I/O request to disk or network.

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

* A New Metric for later algorithm comparison: **Response Time** $T_{\text{response}} = T_{\text{firstrun}} − T_{\text{arrival}}$ 

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
            * $\text{time_slice}_k = \frac{\text{weight}_k}{\sum_{0}^{n-1}\text{weight}_i} \cdot  \text{sched_latency}$

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
            
            * To improve the efficiency, the scheduler uses [Red-Black Trees](https://cs.ericyy.me/algorithms-1/week-5/index.html#red-black-bsts) with the vruntime values of each process to run the min-vrumtime process.
    * What about I/O and sleeping process?
        * if the process gone for sleeping for a long time, when it wakes up, it might monopolize the CPU for a long time. To avoid this, CFS sets the vruntime of that job to the minimum value that found in the tree.