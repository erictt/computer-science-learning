# Real-Time and Multimedia

## L10a: TS-Linux

### Introduction

- General purpose operating systems historically catered to throughput-oriented applications, but now there's a growing need for soft real-time guarantees for latency-sensitive applications.
- Time-sensitive Linux is an extension of commodity Linux that addresses providing guarantees for real-time apps in the presence of throughput-oriented apps and bounding performance loss of throughput-oriented apps in the presence of latency-sensitive apps.

### Sources of Latency

<img src="https://i.imgur.com/3pv6SuK.png" style="width: 800px" />

- Time-sensitive apps require quick responses to events, but there are three sources of latency in typical general purpose operating systems: **timer latency**, **preemption latency**, and **scheduler latency**.
- Timer latency comes from the inaccuracy of the timing mechanism due to the granularity of the timing mechanism available in general purpose operating systems.
- Preemption latency happens when the kernel is in the middle of doing something from which it can't be preempted or when the kernel itself is in the middle of handling another higher priority interrupt.
- Scheduler latency prevents an external event from being delivered to the application that's waiting for it because a higher priority task is already in the scheduler's queue.

### Timers Available

<img src="https://i.imgur.com/ji4AzXO.png" style="width: 800px" />

- There are different kinds of timers available in operating systems, such as periodic timers, one-shot timers, and soft timers.
- Periodic timers have periodicity as their pro but have event recognition latency as their con, and their worst-case latency is the periodicity itself.
- One-shot timers are exact timers that can go off exactly when you want the interrupt delivered, but have overhead associated with fielding them.
- Soft timers have reduced overhead since there are no timer interrupts, but there's latency associated with them and an overhead of polling all events to see if any of them have expired.
- Firm timer is a new mechanism proposed in TS Linux that combines the pros of all three types of timers while avoiding their individual cons.

### Firm Timer Design

<img src="https://i.imgur.com/tgang9w.png" style="width: 800px" />

- The firm timer design combines the benefits of one-shot and soft timers.
- The overshoot parameter is a knob used to program the one-shot timer to interrupt at a point after the actual event happened.
- The overshoot window allows the kernel to dispatch expired timers and reprogram the one-shot timer to interrupt at the next event to avoid interrupt overhead.
- The combination of hard and soft timers in the firm timer design reduces the number of one-shot timer interrupts.

#### Implementation

<img src="https://i.imgur.com/gQCCzEL.png" style="width: 800px" />

- The timer-q data structure maintains tasks and their corresponding expiry times in order.
- The APIC hardware, a programmable interrupt controller, is used in modern CPUs for reprogramming one-shot timers with low overhead.
	- The APIC is set by writing a value into a register, which is decremented at each memory bus cycle until it reaches zero and generates an interrupt.
	- Given a 100 MHz memory bus available on a modern machine, a one-shot timer has a theoretical accuracy of 10 nanoseconds.
	- However, in practice, the time needed to field timer interrupts is significantly higher and is the limiting factor for timer accuracy.
- The interrupt handler looks for expired tasks in the timer-q data structure and calls the corresponding callback handlers.
- The firm timer implementation uses an overshoot parameter to avoid fielding one-shot interrupts.
- If the distance between one-shot timers is long, the kernel will use periodic timers instead and dispatch the one-shot event at the preceding periodic timer event.
- The firm timer implementation reduces timer latency by combining one-shot, soft, and periodic timers.

### Reducing Kernel Preemption Latency

- Kernel preemption latency is a source of latency that can be reduced.
- Two approaches to reducing kernel preemption latency are 
	1. **explicitly inserting preemption points in the kernel** 
	2. **allowing preemption of the kernel anytime the kernel is not manipulating shared data structures**
- The lock-breaking preemptible kernel technique, due to Robert Love, combines these two ideas by breaking a long critical section in the kernel into two shorter critical sections: one for manipulating shared data and the other for the rest of the code.
- By breaking up the critical section, it is possible to safely preempt the kernel at certain points and perform tasks such as checking for expired timers.

- TS Linux uses a combination of two principles to reduce scheduling latency: Proportional Period Scheduling and priority scheduling.
- Proportional Period Scheduling allocates each task a fixed proportion of CPU time during each task period T and is adjustable using a feedback control mechanism.
- Priority scheduling is used to avoid priority inversion, which can affect the sensitivity of time-sensitive tasks. TS Linux boosts the priority of a server task to the priority of the requesting task to avoid priority inversion.
- These mechanisms allow TS Linux to have control over how much CPU time is devoted to time-sensitive tasks and ensure that throughput-oriented tasks are able to make forward progress.

<img src="https://i.imgur.com/fnRfcDG.png" style="width: 800px" />
<img src="https://i.imgur.com/1NUat25.png" style="width: 800px" />
<img src="https://i.imgur.com/OntEFHp.png" style="width: 800px" />

### Conclusion

- TS-Linux can provide quality of service guarantees for real-time applications running on commodity operating systems such as Linux by addressing the three sources of latency.
- Proportional period scheduling and priority-based scheduling are used to reduce scheduling latency and avoid priority inversion, ensuring that both time-sensitive and throughput-oriented tasks get CPU time.
- The performance evaluation carried out in the paper shows that both objectives are achieved.

## L10b: PTS

### Introduction

- This lesson focuses on middleware for real-time and distributed multimedia applications.
- It builds on the previous lesson's study of an OS scheduler for accurate timing in upper layers of software.

### Programming Paradigms

<img src="https://i.imgur.com/b0fHBvE.png" style="width: 800px" />

- PThreads and sockets are APIs for developing parallel and distributed programs.
- Socket API is low-level and lacks semantic richness for emerging multimedia distributed applications.

### Novel Multimedia Apps


<img src="https://i.imgur.com/JucjLAD.png" style="width: 800px" />

- Sensor-based distributed multimedia applications are computationally intensive and exhibit a control loop going from sensing to actuation in real-time.
- Computational engines such as clusters and clouds may be deployed to cater to the needs of these applications.

### Example - Large Scale Situation Awareness

<img src="https://i.imgur.com/bF6GHTc.png" style="width: 800px" />

### Programming Model for Situation Awareness

<img src="https://i.imgur.com/MI7PLyL.png" style="width: 800px" />

- The objective in Situation Awareness applications is to process streams of data for high-level inferences.
- Video Analytics is in the purview of a domain expert, but systems can come in with programming models to alleviate pain points.
- PTS is an exemplar of a distributed programming system for catering to the needs of Situation Awareness Applications.

### PTS Programming Model

<img src="https://i.imgur.com/Uim23NW.png" style="width: 800px" />

- The PTS programming model is a distributed application with threads and channels as the high-level abstractions.
- The computation graph generated by the PTS programming model looks similar to a UNIX process socket graph.
- The semantics of the channel abstraction is different from the socket abstraction, as the channel holds time sequenced data objects.
- A channel allows many-to-many connections, and a thread can produce or consume data from a channel using the put and get primitives, respectively.
- A channel contains a continuous stream of data with time stamps associated with them, and the programming model allows an application to specify time variables in an abstract way.
- The PTS programming model allows the propagation of temporal causality and correlation of incoming streams, improving the inferencing and hypothesis in situation awareness applications.

### Bundling Streams

<img src="https://i.imgur.com/nM5Bfa9.png" style="width: 800px" />

- The bundling of streams in PTS allows grouping of streams labeled as a group, with an anchor stream and dependent streams.
- The group get primitive allows getting correspondingly timestamped items from all the streams in a given group, reducing the burden of selecting temporally correlated items from individual streams.

### Power of Simplicity

<img src="https://i.imgur.com/oHitOjh.png" style="width: 800px" />

- The power of simplicity is the key for adoption in system design.
- Converting a sequential program for video analytics into a distributed program using PTS is straightforward, by interposing channels between computations and using the get/put primitives.
- The PTS programming model uses threads as computational entities and channels as the means of communication between them.

### PTS Design Principles

<img src="https://i.imgur.com/7cbUtcW.png" style="width: 800px" />

- PTS provides simple abstractions (channel and get/put operations) to manipulate data.
- Channels can be accessed from anywhere in the distributed system and are network-wide unique, similar to UNIX sockets.
- The run-time system and APIs treat time as a first-class entity, allowing for seamless integration of live and historical data.
- PTS allows streams to be persistent under application control.

### Persistent Channel Architecture

<img src="https://i.imgur.com/CE6lmp2.png" style="width: 800px" />

- All computations can be considered as producers or consumers of data, with worker threads reacting to get/put calls.
- The channel architecture has three layers: Live Channel Layer, Interaction Layer, and Backend Layer.
- The Live Channel Layer holds a snapshot of items generated on a channel, and the Garbage Collection trigger moves old data to a garbage list.
- The Persistence Layer handles items that need to be persisted, using a pickling handler function specified by the application.
- The Backend Layer supports different backends for storing channel data, including MySQL, Unix file system, and GPFS.
- All persistence activities happen automatically under the covers.

### Conclusion

- PTS provides a simple programming model for developing live stream analysis applications.
- Time-based distributed data structures for streams, automatic data management, and transparent stream persistence are unique features of the PTS programming model.
- The paper discusses the systems challenges solved by PTS to provide this programming model.