# P3L1 : Scheduling [WIP]

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

    * ![](https://i.imgur.com/J1Qwqim.jpg)

    * In this case, we assumed we know the execution time. But it's not realistic. What we can do is, generate heuristics base on the similar jobs in the past.
        * It can base on a single task, or base on the average execution time for n past tasks **(windowed average)**.
* Priority
    * This means we run the tasks base on their **priority levels**, and run the highest priority task next(preemption)
    * ![](https://i.imgur.com/22Dl6io.jpg)

    * This algorithm might causes **starvation**, in which a low priority task never gets executed due to high priority tasks keep jumping in.
        * The solution is **priority aging**, so priority = f(actual priority, time spent in runqueue) so if a job's priority will increase as it stays in the runqueue for long enough.

#### Priority Inversion

* ![](https://i.imgur.com/b9JScO5.jpg)


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
    * ![](https://i.imgur.com/8cscM2e.jpg)

    * For metrics, 
        * the throughput stays the same, 
        * the average wait and average completion time are close to SJF, but no need for priority knowledge of execution times, which was said was unfeasible in a real system.
* The downside of timeslicing is the overhead. We have exaggerated in our graphs that there is no latency between tasks, but this is not the case. In real case, we have to interrupt the running task, execute the scheduler, and context switch to the new task. **Even when there is only one task, the scheduler sill needs to run at the timeslice intervals.** 
    * Consider this, our throughput will be lower than 0.25, and avg. wait and avg. comp. will be higher.

### How Long Should a Timeslice Be

* Depends on whether the tasks are CPU bounded or I/O bounded.

#### CPU Bound Timeslice Length

* ![](https://i.imgur.com/eOrJGaQ.jpg)

#### I/O Bound Timeslice Length

* ![](https://i.imgur.com/NZx7FCP.jpg)

### Summarizing Timeslice Length

* CPU bound tasks prefer longer timeslices
    * limits the number of context switching overheads
    * keep CPU utilization and throughput high
* I/O bound tasks prefer short timeslices
    * I/O bound tasks can issue I/O earlier
    * keeps CPU and device utilization high
    * better user-perceived performance - wait time is low

## Runqueue Data Structure

Linux O(1) Scheduler
Linux CFS Scheduler
Scheduling on Multiprocessors
Hyperthreading
Scheduling for Hyperthreading Platforms
CPU Bound or Memory Bound
Scheduling with Hardware Counters
CPI Experiment Results


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