---
weight: 1
title: "P2L5: Thread Performance Considerations"
---

# P2L5: Thread Performance Considerations

<!-- toc -->
----

## Which Threading Model Is Better?

* Depends on the matrix we used to evaluate.
* review the [quiz](/cs6200/p2l2-threads-and-concurrency/#quiz)
* <img src="https://i.imgur.com/g0QGBWU.jpg" style="width: 600px" />

## Are Threads Useful?

* Threads are useful because:
    1. parallelization: speed up the execution.
    2. specialization: hot cache
    3. efficiency. lower memory requirements and are cheaper to synchronize
        1. Threads are useful even on a single CPU because they allow us to hide latency of I/O operations.
* How to measure things are useful?
  * a matrix multiply application: raw execution time
  * web service application: throughput(requests/s) or response time
  * hardware chip: overall utilization increase
  * for any these matrix, we might care: average value or max/min value, or a certain percentage.
  * To evaluate or determine whether things are useful, it is important to determine the properties that we care. We can such properties **matrices**.

### Performance Metrics

* There are lots of useful matrices. we have discussed:
  * execution time, throughput, request time, CPU utilization
* Some others:
  * wait time: how long a job waited to start executing.
  * platform efficiency: how well resources are utilized.
  * performance per dollar/watt
  * **percentage of SLA violation**:
* In summary we want measurable quantities that obtained from
  * experiments with real software deployment, real machines, real workload.
  * these experimental settings are **testbed**.

* So are threads useful?
  * It depends.

## Multi Process Vs. Multi Threaded

* Take a web server as an example:
  * <img src="https://i.imgur.com/D4jTsAL.jpg" style="width: 200px" />
    1. client/browser send request
    2. web server accept request
    3. server processing steps
    4. respond by sending file
* Note that some work are CPU complexity like parse request/computer header, and some other are IO operations like accept connection, read/find file.

* Multi Process Web Server: spawn multiple processes and run it in each process.
  * Benefits:
    * Simple.
    * Each request is handled in a new process with its own address space: there is no need for any (explicit) synchronization code.
  * Downside:
    * it require higher memory footprint, which can hurt the performance.
    * pay higher cost to context switch since processes don't share states due to IPC constrains
    * it's difficult to have multiple process listening on a specific port.
* Multi-threaded Web Server: single process, with multiple threads, achieving concurrency within a single address space.
  * we can adapt the boss-worker mode, or have a pipeline setup.
  * benefits:
    * have a shared address space, shared state,
    * a cheap user level context switch.
    * Memory requirements are lighter, since we have a lot of shared information across all threads in the process.
  * Downside:
    * not a simple implementation. Multithreaded programs require explicit application level synchronization code, which can add to the overall complexity of the application.
    * a multithreaded approach depends on underlying operating system level support for threads, although this is less of an issue now than it was in the past.

## Event-Driven Model

* <img src="https://i.imgur.com/RhtrFlu.jpg" style="width: 400px" />
* Event-driven model is composed with two parts:
  * event dispatcher
    * work as a state machine of external events => call handler(jump to the code)
    * accept any of these types of notifications and based on the notification type invoke the right handler.
  * event handlers, such accept connection, read request, etc.
    * If the handler needs to block (i.e. making an I/O request), the handler will initiate the blocking operation and immediately pass control back to the dispatch loop.
* It works in a **single address space**, a **single process** and a **single thread of control**.
* How to achieve **concurrency** with only **one** thread?
  * In the event driven model, the processing of multiple requests are **interleaved within a single execution context**.
  * Consider we have a request, and it went through all events, and at some point block on send data back to the client. In the meantime, two requests come in. The fist one is blocking on disk I/O, and second one is waiting on receiving data from client. At this point, all requests are waiting. Later on, each of them will be processed.
  * Even we only have one thread, we still handling the requests simultaneously.
* Why does this work?
  * On 1 CPU, threads hide latency.
    * it make sense to do context switch if (t_idle > 2 * t_ctx_switch)
    * but if (t_idle == 0) context switch just waste cycles.
  * In the event driven model, a request will be processed exactly until a wait is necessary, at which point the execution context will switch to servicing another request.
  * In a multiple CPUs situation, we can still benefit from the model. Each CPU could host a single event-driven process, and multiple requests could be worked on concurrently within that process.
  * Gotcha: It is important to have mechanisms that will steer the right set of events to the right CPU.

* How does this work?
  * First of all, both sockets and files are represented by **file descriptors**. An event in the context of the web server is an input on any of the file descriptors associated with it.
  * So how to know which file descriptors have input?
    * system call `select()`: scan a range of file descriptors, and return the first one that have input. Another alternative is the `poll()` system call.
    * both system calls have to scan through a potentially large list of file descriptors, and it's likely only few have input, which wastes lots of time.
    * A more recent system call is `epoll()`, which eliminates some of the problems that select and poll have.
  * The benefits of the event driven model mainly come from the design as a single address space with a single flow of control. As a result, the overheads are lower. There is a smaller memory footprint, and no need for context switching or synchronization.

### Helper Threads And Processes

* In the many-to-one ULT:KLT model, a ULT might blocks the entire process because the KLT is not aware of the threads in ULT. The event-driven model has the same issue.
* One way to solve this is to use **asynchronous I/O operations**. The asynchronous system call allows the the process/thread continue execution and check the result later by obtaining the relevant info from the stack and either return the result somewhere, or call the caller with callback function.
* Asynchronous needs a multithreaded kernel, so the caller and asynchronous call can leave on different threads, and not block each other.

* What if asynchronous I/O calls are not available?
  * Run **helper** functions on other threads/processes.
  * <img src="https://i.imgur.com/e5fUTcZ.jpg" style="width: 400px" />
  * When the handler needs to initiate an I/O operation that can block, the handler passes the call to the operation to a **helper**, and returns to the event dispatcher. The helper will be the one that handles the blocking I/O operation and interact with the dispatcher as necessary.
  * Two models are used in this situation:
    * Asymmetric Multi-Process Event-Driven Model or AMPED.
    * The multithreaded equivalent acronym is AMTED.
  * The benefits from these models:
    * resolves portability limitation of basic event-driven model
    * smaller footprint that regular worker thread
  * Downside are:
    * applicability to certain classes of applications
    * there are some complexities surrounding events routing on multi-CPU systems.

## Flash: Event-Driven Web Server

* Flash is an event-driven webserver(**AMPED**) with **asymmetric helper processes**
  * helpers used for disk reads (mostly)
  * pipes used for communication from helpers to dispatcher
  * helper reads file in memory(via mmap)
  * dispatcher checks (via **mincore**) if pages are in memory to decide to call "local" handler or helper
* Additional optimizations from Flash is application-level caching (data and computation)
  * For instance, every request has an associated pathname, and we need to look up the file given the pathname. That lookup will compute some result, which we can cache so we do not have to perform the same computation again.

## Apache Web Server

* <img src="https://i.imgur.com/LkdkVSo.jpg" style="width: 400px" />
* The core component provides core services like accepting requests, issuing responses, and managing concurrency. The various modules are mounted in a pipeline and extend the functionality of the basic server behavior.
* The flow of control is similar to event-driven model, but it's a combination of multiprocess and multithreaded model, which implements a multithreaded boss/workers configuration with a dynamic thread pool.
* The number of processes can also be dynamically adjusted.

## Experimental Methodology

* Setting up performance comparisons
  * Define comparison points: What systems are you comparing?
  * Define inputs: What workload will be used?
  * Define matrices: How will you measure performance?
* Flash: What systems are you comparing?
  * a multiprocess, single threaded implementation
  * a multithreaded implementation using the boss/workers pattern
  * a single process event-driven (SPED) implementation
  * Zeus (SPED implementation with two processes)
  * Apache (multiprocess at the time)
* Flash: What workload will be used?
  * Goal:
    * realistic request workload -> distribution of web pages accesses over time
    * controlled, reproducible workload -> trace-based (from real web servers)
  * Workload used:
    * CS Web Server trace(Rice Univ.)
    * Owlnet trace(Rice Univ.)
    * Synthetic workload
* Flash: How will you measure performance?
  * Matrices:
    * Bandwidth (bytes/second) -> total number of bytes transferred / total amount of time took to transfer the bytes
    * Connection Rate (requests/second) -> total client connections / total amount of time passed
  * Both of these metrics were evaluated as a function of file size(x-axis), because:
    * with larger file size, the connection cost can be amortized => higher bandwidth
    * however, with larger file size, causes more work per connection, aka lower connection rate.

## Experimental Results

* Best Case Numbers
  * Synthetic load: N requests for the same file(after first request, the file will be cached, the following requests will be faster)
  * Bandwidth measurement:
    * bandwidth = N * file size(bytes) / total time
    * file size: 0 - 200 KB -> vary work per request
  * Result:
    * <img src="https://i.imgur.com/vIuuN6v.jpg" style="width: 300px" />
    * All of the implementations had similar results, with bandwidth increasing sharply with file size initially before plateauing.
    * SPED has the best performance.
    * Flash has slightly lower performance, because it performs the extra check for memory presence.
    * Zeus has an anomaly, where it drops in performance after a threshold of around 125Kb.
    * The performance of the multithreaded/multiprocess implementations are lower because of the extra synchronization requirements and the cost of context switching.
    * Apache has the lowest performance because it has no optimizations.

* CS Trace & Owlnet Trace
  * <img src="https://i.imgur.com/1i0i5RF.jpg" style="width: 300px" />
  * Owlnet Trace
    * Flash and SPED are the best, followed by MT/MP and then Apache.
    * The reason for this trend is because the owl trace is very small, so most of the requests can be serviced from the cache. However, not everything can be serviced from cache, so sometimes blocking I/O is required. In this case, SPED will block, but Flash will not because it has helpers. This helps explain why Flash's performance is slightly higher than the SPED implementation.
  * CS Trace
    * The CS trace is a much larger trace, which means that most requests are not serviced from the cache.Since the SPED implementation does not support asynchronous I/O the performance drops significantly. The multithreaded implementation does better than the multiprocess implementation because it has a smaller memory footprint (more memory available to cache files) and is able to synchronize more quickly/cheaply.
    * Flash performs the best. It has the smallest memory footprint, which means it has the most memory available for caching files. As a result, fewer requests will require blocking I/O requests, which further speeds everything up. In addition, since everything occurs in the same address space, there is no need for explicit synchronization.
* Impact of Optimizations in Flash
  * <img src="https://i.imgur.com/nAUmcEe.jpg" style="width: 300px" />
  * Fully optimized flash having the highest connection rate at a given file size.

* Summary of Performance Results
  * When data is in cache:
    * SPED >> AMPED Flash: because unnecessary test for memory presence
    * SPED and AMPED Flash >> MT/MP: sync and context switching overhead
  * With disk-bound workload
    * AMPED Flash >> SPED: because blocks become no async I/O
    * AMPED Flash >> MT/MP: because more memory efficient and less context switching

## Advice on Designing Experiments

* Understand the purpose of relevant experiments.
  * Take web server experiment as an example. The clients care about response time, the operators when runs the server care about throughput. So there are several possible goals:
    * +response time, +throughput => great!
    * +response time => acceptable
    * +response time, -throughput => maybe useful
    * maintain response time when request rate increase
  * The goals are to gain some insight into both the metrics and the configuration our experiments.
* Picking the right metrics
  * use "standard" metrics with broader audience
  * the matrices needs to answer why/what/who questions
    * client performance -> response time, timedout requests, etc.
    * operator costs -> throughput, costs
* Picking the right configuration space
  * Think what you can choose:
    * System resources:
      * hardware(CPU, memory) & software(# of threads, queue size, etc)
    * Workload
      * webserver: request rate, # of concurrent requests, file size, access pattern
  * Now pick
    * choose a subset of configuration parameters
    * pick range for each variable factor
    * pick relevant workload
    * include best/worst case scenarios

## Advice on Running Experiments

* Run test cases N times
* Compute metrics
* Represent results
* **Draw a conclusion!**

## Papers

* ["Flash: An Efficient and Portable Web Server"](https://s3.amazonaws.com/content.udacity-data.com/courses/ud923/references/ud923-pai-paper.pdf) by Pai