# RT and Multimedia

## L10a: TS-Linux

1.  TS-Linux Introduction:

-   General purpose operating systems historically catered to throughput-oriented applications, but now there's a growing need for soft real-time guarantees for latency-sensitive applications.
-   Time-sensitive Linux is an extension of commodity Linux that addresses providing guarantees for real-time apps in the presence of throughput-oriented apps and bounding performance loss of throughput-oriented apps in the presence of latency-sensitive apps.
-   This module discusses approaches to address these questions.

2.  Sources of Latency:

![](https://i.imgur.com/3pv6SuK.png)


-   Time-sensitive apps require quick responses to events, but there are three sources of latency in typical general purpose operating systems: timer latency, preemption latency, and scheduler latency.
-   Timer latency comes from the inaccuracy of the timing mechanism due to the granularity of the timing mechanism available in general purpose operating systems.
-   Preemption latency happens when the kernel is in the middle of doing something from which it can't be preempted or when the kernel itself is in the middle of handling another higher priority interrupt.
-   Scheduler latency prevents an external event from being delivered to the application that's waiting for it because a higher priority task is already in the scheduler's queue.

3.  Timers Available

![](https://i.imgur.com/ji4AzXO.png)


-   There are different kinds of timers available in operating systems, such as periodic timers, one-shot timers, and soft timers.
-   Periodic timers have periodicity as their pro but have event recognition latency as their con, and their worst-case latency is the periodicity itself.
-   One-shot timers are exact timers that can go off exactly when you want the interrupt delivered but have overhead associated with fielding them.
-   Soft timers have reduced overhead since there are no timer interrupts, but there's latency associated with them and an overhead of polling all events to see if any of them have expired.
-   Firm timer is a new mechanism proposed in TS Linux that combines the pros of all three types of timers while avoiding their individual cons.

![](https://i.imgur.com/n9WS96G.png)


Section 4: Firm Timer Design

![](https://i.imgur.com/tgang9w.png)

-   The firm timer design combines the benefits of one-shot and soft timers.
-   The overshoot parameter is a knob used to program the one-shot timer to interrupt at a point after the actual event happened.
-   The overshoot window allows the kernel to dispatch expired timers and reprogram the one-shot timer to interrupt at the next event to avoid interrupt overhead.
-   The combination of hard and soft timers in the firm timer design reduces the number of one-shot timer interrupts.

Section 5: Firm Timer Implementation

![](https://i.imgur.com/gQCCzEL.png)

-   The timer-q data structure maintains tasks and their corresponding expiry times in order.
-   The APIC hardware, a programmable interrupt controller, is used in modern CPUs for reprogramming one-shot timers with low overhead.
-   The interrupt handler looks for expired tasks in the timer-q data structure and calls the corresponding callback handlers.
-   The firm timer implementation uses an overshoot parameter to avoid fielding one-shot interrupts.
-   If the distance between one-shot timers is long, the kernel will use periodic timers instead and dispatch the one-shot event at the preceding periodic timer event.
-   The firm timer implementation reduces timer latency by combining one-shot, soft, and periodic timers.

Section 6: Reducing Kernel Preemption Latency

![](https://i.imgur.com/WwVdkoF.png)

-   Kernel preemption latency is a source of latency that can be reduced.
![](https://i.imgur.com/fnRfcDG.png)
![](https://i.imgur.com/1NUat25.png)
![](https://i.imgur.com/OntEFHp.png)


-   Two approaches to reducing kernel preemption latency are explicitly inserting preemption points in the kernel and allowing preemption of the kernel anytime the kernel is not manipulating shared data structures.
-   The lock-breaking preemptible kernel combines these two approaches by breaking long critical sections into two sections: manipulating shared data and other code, allowing the kernel to be preempted safely and enabling checking for expired timers.
![](https://i.imgur.com/kbkZ7Yj.png)

Section 7: TS-Linux Conclusion

-   TS-Linux can provide quality of service guarantees for real-time applications running on commodity operating systems such as Linux by addressing the three sources of latency.
-   Proportional period scheduling and priority-based scheduling are used to reduce scheduling latency and avoid priority inversion, ensuring that both time-sensitive and throughput-oriented tasks get CPU time.
-   The performance evaluation carried out in the paper shows that both objectives are achieved.

## L10b: PTS

1.  PTS Introduction:

-   This lesson focuses on middleware for real-time and distributed multimedia applications.
-   It builds on the previous lesson's study of an OS scheduler for accurate timing in upper layers of software.

2.  Programming Paradigms:

![](https://i.imgur.com/b0fHBvE.png)

-   PThreads and sockets are APIs for developing parallel and distributed programs.
-   Socket API is low-level and lacks semantic richness for emerging multimedia distributed applications.

3.  Novel Multimedia Apps:

![](https://i.imgur.com/JucjLAD.png)

-   Sensor-based distributed multimedia applications are computationally intensive and exhibit a control loop going from sensing to actuation in real-time.
-   Computational engines such as clusters and clouds may be deployed to cater to the needs of these applications.

4.  Example - Large Scale Situation Awareness:

![](https://i.imgur.com/bF6GHTc.png)

-   Large-scale situation awareness applications require pruning sensor streams and avoiding false positives and negatives.
-   The programming infrastructure needs to facilitate time-sensitive data and provide the right level of abstractions for simplicity.

5.  Programming Model for Situation Awareness:

![](https://i.imgur.com/MI7PLyL.png)

-   The objective in Situation Awareness applications is to process streams of data for high-level inferences.
-   Video Analytics is in the purview of a domain expert, but systems can come in with programming models to alleviate pain points.
-   PTS is an exemplar of a distributed programming system for catering to the needs of Situation Awareness Applications.

Section 6: PTS Programming Model

![](https://i.imgur.com/Uim23NW.png)

-   The PTS programming model is a distributed application with threads and channels as the high-level abstractions.
-   The computation graph generated by the PTS programming model looks similar to a UNIX process socket graph.
-   The semantics of the channel abstraction is different from the socket abstraction, as the channel holds time sequenced data objects.
-   A channel allows many-to-many connections, and a thread can produce or consume data from a channel using the put and get primitives, respectively.
-   A channel contains a continuous stream of data with time stamps associated with them, and the programming model allows an application to specify time variables in an abstract way.
-   The PTS programming model allows the propagation of temporal causality and correlation of incoming streams, improving the inferencing and hypothesis in situation awareness applications.

Section 7: Bundling Streams

![](https://i.imgur.com/nM5Bfa9.png)

-   The bundling of streams in PTS allows grouping of streams labeled as a group, with an anchor stream and dependent streams.
-   The group get primitive allows getting correspondingly timestamped items from all the streams in a given group, reducing the burden of selecting temporally correlated items from individual streams.

Section 8: Power of Simplicity

![](https://i.imgur.com/oHitOjh.png)

-   The power of simplicity is the key for adoption in system design.
-   Converting a sequential program for video analytics into a distributed program using PTS is straightforward, by interposing channels between computations and using the get/put primitives.
-   The PTS programming model uses threads as computational entities and channels as the means of communication between them.

Section 9: PTS Design Principles

![](https://i.imgur.com/7cbUtcW.png)

-   PTS provides simple abstractions (channel and get/put operations) to manipulate data.
-   Channels can be accessed from anywhere in the distributed system and are network-wide unique, similar to UNIX sockets.
-   The run-time system and APIs treat time as a first-class entity, allowing for seamless integration of live and historical data.
-   PTS allows streams to be persistent under application control.

Section 10: Persistent Channel Architecture

![](https://i.imgur.com/CE6lmp2.png)

-   All computations can be considered as producers or consumers of data, with worker threads reacting to get/put calls.
-   The channel architecture has three layers: Live Channel Layer, Interaction Layer, and Backend Layer.
-   The Live Channel Layer holds a snapshot of items generated on a channel, and the Garbage Collection trigger moves old data to a garbage list.
-   The Persistence Layer handles items that need to be persisted, using a pickling handler function specified by the application.
-   The Backend Layer supports different backends for storing channel data, including MySQL, Unix file system, and GPFS.
-   All persistence activities happen automatically under the covers.

Section 11: PTS Conclusion

-   PTS provides a simple programming model for developing live stream analysis applications.
-   Time-based distributed data structures for streams, automatic data management, and transparent stream persistence are unique features of the PTS programming model.
-   The paper discusses the systems challenges solved by PTS to provide this programming model.