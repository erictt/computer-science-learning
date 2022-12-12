# P3L4: Synchronization Constructs

<!-- toc -->
----

Mutexes and condition variables and any other software synchronization construct requires a lower level support from the hardware in order to guarantee the correctness. Hardware provides this type of low level support via **atomic instructions**.

## Common Synchronization Contructs
### Spinlocks

 It's similar to mutex lock/unlock:
    
```c
spinlock_lock(s);
    // critical sesion
spinlock_unlock(s);
```

The difference is, when lock == busy, the thread that is suspended it's execution at the spinlock_lock() isn't blocked like mutex. Instead, it's spinning. The thread will continue to burn CPU cycles until the lock is free or gets preempted for some reasons.

### Semaphores

It's common sync construct in OS kernels, act like a traffic light to allow the traffic to STOP or GO.
    
* Semaphore is represented via a positive integer number initially, which is the max running threads. If threads arrive at semaphore with 
    * a non-zero value, the semaphore will decrease the value and the thread will process,
    * a zero value, the thread will wait
* when the semaphore is initialized with value: 1, it will be a binary semaphore, act like mutex

POSIX Semaphores([link](http://linux.die.net/man/3/sem_init)):
 
```c
#include <semaphore.h>
    
sem_t sem;
// pshared: flag of whether this semaphore is in a single process or across processes.
sem_init(sem_t *sem, int pshared, int count);  
sem_wait(sem_t *sem);
sem_post(sem_t *sem);
``` 

### Reader/Writer Locks

When specifying synchronization requirements, it is sometimes useful to distinguish among different types of resource access.

For instance, 
- "read" accesses - "never modify" **shared access** lock 
- "write" accesses - "always modify" **exclusive access** lock. 
To cope with this situation, we have **rwlock**s which is similar to mutex, but developers can specify the type of access, and then the lock can behave accordingly.

The primary API([link](https://elixir.bootlin.com/linux/v6.0.3/source/include/linux/rwlock.h))

```c
#include <linux/spinlock.h>

rwlock_t m;
read_lock(m);
    // critical section
read_unlock(m);

write_lock(m);
    // critical section
write_unlock(m);
```
- read/write == share/exclusive

Semantic differences:
* Recursive read lock
    * May differ on how recursively-obtained read locks are unlocked. When unlocking a recursive read lock, some implementations unlock all the recursive locks, while others only unlock the most recently acquired lock.
* Upgrade/downgrade **priority**
    * Allow readers to convert their lock into a writer lock mid-execution, while other implementations do not allow this upgrade.
* Interaction with scheduling policy
    * Block an incoming reader if there is a writer with higher priority waiting

### Monitors

**Monitors** are a <u>higher level synchronization construct</u> that allow us to avoid manually invoking these synchronization operations.

Monitors specify:
* shared resource
* entry procedure for accessing that resource
* possible condition variable used to wake up different types of waiting threads.

When invoking the entry procedure, all of the necessary locking and checking will take place by the monitor behind the scenes. When a thread is done with a shared resource and is exiting the procedure, all of the unlocking and potential signaling is again performed by the monitor behind the scenes.

### More Synchronization Constructs

**Serializers** make it easier to define priorities and also hide the need for explicit signaling and explicit use of condition variables from the programmer.

**Path Expressions** require that a programmer specify a regular expression that captures the correct synchronization behavior. As opposed to using locks, the programmer would specify something like "Many Reads, Single Write", and the runtime will make sure that the way the operations are interleaved satisfies the regular expression.

**Barriers** are like reverse semaphores. While a semaphore allows n threads to proceed before it blocks, a barrier blocks until n threads arrive at the barrier point. Similarly, **Rendezvous Points** also wait for multiple threads to arrive at a particular point in execution.

To further boost scalability and efficiency metrics, there are efforts to achieve concurrency without explicitly locking and waiting. These **wait-free synchronization constructs** are optimistic in the sense that they bet on the fact that there won't be any concurrent writes and that it is safe to allow reads to proceed concurrently. An example of this is **read-copy-update (RCU)** lock that is part of the Linux kernel.

All of these methods require some support from the underlying hardware to atomically make updates to a memory location.

The following lecture will discuss different implementations of spinlocks base on the paper ["The Performance of Spin Lock Alternatives for Shared-Memory Multiprocessors"](https://s3.amazonaws.com/content.udacity-data.com/courses/ud923/references/ud923-anderson-paper.pdf) by Anderson, Thomas E.

Quiz: Does this spinlock implementation correctly guarantee mutual exclusion? is it efficient?

```c
spinlock_init(lock):
    lock = free; // 0 = free, 1 = busy

spinlock_lock(lock):
    spin:
        if (lock == free) {lock = busy;}
        else { goto spin; }

spinlock_unlock(lock):
    lock = free;
```

What if changing the lock part to

```c
spinlock_lock(lock):
    while (lock = busy);
    lock = busy;
```

The answer of both implementations are neither correct, nor efficient. Because we have continuous loop that is spinning as long as the lock is busy which is inefficient. And potentially, when lock is free, all of the waiting threads will set lock to busy at the same time.

So to check the lock and set the lock value atomically, we need hardware support.

## Atomic Instructions

Each type of hardware will support a number of atomic instructions. Some examples include
* `test_and_set`
* `read_and_increment`
* `compare_and_swap`
Each of these operations performs **multi cycle operation**.

Because they are atomic instructions, the hardware guarantees:
- operations will happen atomically
- mutual exclusion - threads on multiple cores cannot perform the atomic operations in parallel
- concurrent attempts to execute an instruction will be queued and performed serially.

To fix the quiz:

```c
spinlock_lock(lock) {
    while(test_and_set(lock) == busy);
}
```

When the first thread arrives, `test_and_set` looks at the value that lock points to. This value will initially be zero. `test_and_set` atomically sets the value to one, and returns zero(*busy* is equal to one). Thus, the first thread can proceed. When subsequent threads arrive, `test_and_set` will look at the value - which is busy - and just return it. Then these threads will spin.

Different platform has different hardware. There may be differences in the efficiencies with which different atomic operations execute on different architectures. We need to check the implementation uses one of the atomic instructions available on the target platform. And also make sure that the software is optimized so that it uses the most efficient atomics on a target platform and uses them in an efficient way.

## Shared Memory Multiprocessors

A multiprocessor system consists of more than one CPU and some memory unit that is accessible to all of these CPUs. That is, the memory component is shared by the CPUs.

<img src="https://i.imgur.com/VDfBtIR.jpg" style="width: 500px" />

In a **bus-based** configuration, the shared bus can only support one memory module at a time. However, it can apply to the multiple memory modules as well.

In the **interconnect-based** configuration, multiple memory references can be in flight at a given moment when each CPU want to access different memory addresses. In bus-based configuration, only one memory access is allow since the CPUs share the same bus.

Shared memory multiprocessors are also referred to as **symmetric multiprocessors(SMPs)**. Each CPU in the SMP platform can have caches to hide latencies for two reasons:
1. The cache is much closer to the CPU
2. Due to the contention amongst the CPUs for accessing shared memory, cache makes it much faster by avoid it.

<img src="https://i.imgur.com/YYwzE91.jpg" style="width: 500px" />

There are different strategy associated with write action:
1. no-write. When CPU need to write, it will bypass cache, and go straight to the memory. And any copy of that memory will be invalidate.
2. write-through.  CPU applies write action to both cache and memory.
3. write-back. CPU writes to cache, and perform the write to memory at some later point in time, perhaps when the particular cache line is evicted. 

## Cache Coherence

To cope with cache coherence, there are two architectures: **non-cache-coherent(NCC) architecture** and **cache-coherent(CC) architecture**. NCC refers to software-based solution, CC refers to hardware-based solution.

In CC, there are two strategies: **write-invalidate(WI)** and **write-update(WU)**.

In WI, the hardware will invalidate all cache entries once one CPU updates its copy. Future references to the invalidated cache entries will have to go through the memory before being re-cached. 

In WU, the hardware will ensure all cache entries are updated once one CPU updated its copy.

In comparison:
1. WI require lower bandwidth because we don't send data to each cache, but only the addresses of the cache for invalidation.
    * If other CPUs don't need the data anytime soon, it's possible to amortize the cost of the coherence traffic over multiple changes. Because the data can be changed multiple times on one CPU before it is needed on another CPU.
2. The advantage of WU is, we have immediate access the updated cache entries. The downside is, the hardware needs to update all caches when any CPU updated the cache.

### Cache Coherence and Atomics

The question is, how to deal with atomic instruction in SMP?

When an atomic instruction is performed against the cached value on one CPU, it is really challenging to know whether or not an atomic instruction will be attempted on the cached value on another CPU. 

One solution is, always bypass caches, and the atomic operations are issued directly to the memory. This way, we enforce a central entry point where all of the references can be ordered and synchronized in a unique manner. 

But the problem is, atomic instructions are gonna take much longer than other instructions since they don't use cache. Not only will they always have to access main memory, but they will also have to contend(竞争) on that memory. Moreover, to guarantee the atomic behavior, we have to generate the coherence traffic to either update or invalidate all cached references regardless of the changes. This is necessary in order to stay on the side of safety and be able to guarantee correctness of the atomic operations.

In summary, atomic instructions on SMP systems are more expensive than on single CPU system because of bus or I/C contention. In addition, atomics in general are more expensive because they bypass the cache and always trigger coherence traffic.

## Spinlock 

### Performance Metrics

1. latency - time to acquire a free lock. ideally immediately execute atomically
2. waiting time(delay) - time to stop spinning and acquire a lock that has been freed. ideally immediately
3. contention - bus/network inter-connection(I/C) traffic. ideally zero
    * By contention, we mean the contention due to the actual atomic memory references as well as the subsequent coherence traffic. 

1 and 3 are conflicted with each other. Because 1 means we want to try to execute the atomic operation asap. As a result, the locking operation will immediately incur an atomic operation which can potentially create some additional contention on the network. 

2 and 3 are conflicted as well. To reduce the waiting time, we need to continuously spin on the lock as long as it's not available. So we can acquire the lock asap.

### Test and Set Spinlock

```c
spinlock_init(lock):
    lock = free; // 0 = free, 1 = busy

spinlock_lock(lock) : // spin
    while(test_and_set(lock) == busy);

spinlock_unlock(lock):
    lock = free;
```

The `test_and_set` instruction is a very common atomic that most hardware platforms support.

**Latency**: minimal (just atomic)
**Delay**: potentially minimal (spinning continuously on the atomic operation)
**Contention**: not so well because processors go to memory on each spin.

With this implementation, even if we have coherent caches, they will be bypassed because we're using an atomic instruction.

### Test and Test and Set Spinlock

The problem with the previous implementation is that all of the CPUs are spinning on the atomic operation. Let's try to separate the test part from the atomic. The intuition is that CPUs can potentially test their cached copy of the lock and only execute the atomic if it detects that its cached copy has changed.

```c
// test (cache), test_and_set (Mm)
// spins on cache (lock == busy)
// atomic if freed (test_and_set)

spinlock_lock(lock):
    while((lock == busy) OR (test_and_set(lock) == busy))
```

This spinlock is referred to as the **test-and-test-and-set spinlock**. It is also called a spin-on-read or spin-on-cached-value spinlock.

**Latency**: slightly worse than the test-and-set lock due to the extra step for checking lock in memory
**Delay**: same as latency due to the extra step.
**Contention**: Depends on our **cache coherence** strategy
* NCC: no different from test-and-set
* CC-WU: improves. only problem is when all caches are updated to free, they will all try to acquire the lock
* CC-WI: horrible. Every single attempt to acquire the lock will generate contention for the memory module and will also create invalidation traffic.
    * One outcome of executing an atomic instruction is that we will trigger the cache coherence strategy regardless of whether or not the value protected by the atomic changes.
    * write-invalidate will invalidate the cached copy. Even if the value hasn't changed, the invalidation will force the CPU to go to main memory to execute the atomic. What this means is that any time another CPU executes an atomic, all of the other CPUs will be invalidated and will have to go to memory.

In an SMP system with N processors, what is the complexity of the memory contention(accesses), relative to N, that will result from releasing a **test_and_test_and_set** spinlock?
* CC-WU: O(N) When lock is released, the `test_and_lock` function will be executed N times because each of the processors in the spin lock will  pass the (lock == busy) and run the next condition.
* CC-WI: O(N^2) When lock is released, the cache on each processor will be invalidated, and they will all fetch the lock status from memory, update their own cache status and invalidate the others' cache. So it will be N^2.

### Spinlock "Delay" Alternatives

Delay after lock release
- Everyone sees lock is free at the same time, but not everyone attempts to acquire it.
- The rationale behind this is to prevent every thread from executing the atomic instruction at the same time.

```c
spinlock_lock(lock):
    while((lock == busy) OR (test_and_set(lock) == busy)) {
        // failed to get lock
        while(lock == busy);
        delay();
    }
```

You can see that all processors waits at the inner while. Once lock == free, they are all gonna delay for a certain time, then go to the outer while. In here, one of the processors will call `test_and_set()` and set the lock to busy, and the others will continue back to the inner while.

**Latency**: ok. We still have to perform a memory reference to bring the lock into the cache, and then another to perform the atomic. However, this is not much different from what we have seen in the past.
**Delay**: Much worse because we add more delay to it.
**Contention**: significantly improved. 
* When the delay expires, the delayed threads will try to re-check the value of the lock, and it's possible that another thread executed the atomic and the delayed threads will see that the lock is busy. If the lock is free, the delayed thread will execute the atomic.
* There will be fewer cases in which threads see a busy lock as free and try to execute an atomic that will not be successful.

An alternative delay-based lock introduces a delay after each memory reference.

```c
spinlock_lock(lock):
    while((lock == busy) OR (test_and_set(lock) == busy)) {
        delay();
    }
```

The main benefit of this is that it works on NCC architectures. Since a thread has to go to main memory on every reference on NCC architectures, introducing an artificial delay great decreases the number of reference the thread has to perform while spinning. 

The problem is, when lock is busy, every spin will have some delay, not just when the lock is free. So it adds more delay to the processors.

#### Picking a Delay

Two strategies for picking the delay: **static delay** and **dynamic delay**.

**Static delay**: base on fixed info, like CPU ID where the process is running.
- it's simple.
- under high load, it will likely spread out all of the atomic references such that there is little or no contention.
- problem is, create unnecessary load under low contention.
    - e.g. one process on CPU 1, the other process on CPU 32, the static delay = ID * 100ms. the second thread has to wait an inordinate amount of time before executing, even though there is no contention.

**Dynamic delay**: each thread take a random delay value from a range of possible delays that increases with the "perceived" contention in the system.
- Under high load, both dynamic and static delays will be sufficient enough to reduce contention within the system.

How to evaluate the number of contentions in the system? Track the number of failed `test_and_set` operations. More fails, more likely a higher degree of contentions.

If we delay after each lock reference, however, our delay grows not only as a function of contention but also as a function of the the length of the critical section. If a thread is executing a large critical section, all spinning threads will be increasing their delays even though the contention in the system hasn't actually increased.

### Queueing Lock

Alternative way to prevent every thread from seeing that the lock has been freed at the same time, aka prevent all threads rushing to acquire the lock simultaneously. The new strategy is called **queueing lock**.

It uses an array of flags with up to `n` elements(n = no. of threads in the system). Each element can have either `has_lock` or `must_wait` flag. In addition, one pointer points to the current lock holder(who has the `has_lock` flag), and another pointer points to the last element of the queue. (remember how to use a fixed-length queue to implement stack?)

Since multiple threads may enter the lock at the same time, it's important to **increment the `queuelast` pointer atomically**. This requires some support for a **read_and_incremement** atomic.

For each thread arriving at the lock, the assigned element of the flags array at the ticket index acts like a private lock. As long as this value is `must_wait`, the thread will have to spin. When the value of the element is becomes `has_lock`, this will signify to the threads that the lock is free and they can attempt to enter their critical section.

When a thread completes a critical section and needs to release the lock, it needs to signal the next thread. Thus `queue[ticket + 1] = has_lock`.

This strategy has two drawbacks:
* First, it requires support for the **read_and_increment** atomic, which is less common that **test_and_set**.
* In addition, this lock requires much more space than other locks. All other locks required a single memory location to track the value of the lock. This lock requires `n` such locations, one for each thread.

#### Queueing Lock Implementation

```c
init:
    flag[0] = has-lock;
    flags[1..p-1] - must-wait;
    queuelast = 0; // global variable

lock:
    myplace = r&inc(queuelast); // get ticket
    // spin
    while(flags[my place % p] == must-wait)
    // now in C.S
    flags[myplace % p] = must-wait;
    
unlock:
    flags[myplace+1 % p] = has-lock;
````

**Latency**: not very efficient. It performs a more complex atomic operation, `read_and_increment` takes more cycles than `test_and_set`.
**Delay**: good. Each lock holder directly signals the next element in the queue that the lock has been freed.
**Contention**: much better than any locks we discussed. The atomic operation is only performed once up front and is not part of the spinning code. The atomic operation and the spinning done with different variables, so cache invalidation on the atomic variable doesn't impact spinning.

In order to realize these contention gains, we must have a cache coherent architecture. Otherwise, spinning must happen on potentially remote memory references. In addition, we have to make sure that every element is on a separated cache line. Otherwise, when we change the value of one element in the array, we will invalidate the entire [cache line](https://open-cas.github.io/cache_line.html), so the processors spinning on other elements will have their caches invalidated.

### Spinlock Performance Comparisons

<img src="https://i.imgur.com/z0SXeYY.jpg" style="width: 600px" />

This figures shows measurements that were gathered from executing a program that had multiple processes. Each process executed a critical section in a loop, one million times. The number of processes in the system was varied such that there was *only one process per processor*.

**Overhead**: how long it would take to execute the number of critical sections. 

Under *high* load, the **queueing lock** performs the best. It is the most scalable; as we add more processors, the overhead does not increase.
The **test_and_test_and_set lock** performs the worst under load. The platform is cache coherent with write-invalidate, and we discussed earlier how this strategy forces O(N^2) memory references to maintain cache coherence.
The spinlock with **static delay** are a little better than the one with **dynamic delay**, since dynamic delay have some measure of randomness and will have more *collisions* than static locks. Also, delaying after every reference is slightly better than delaying after every lock release.

Under *smaller* loads, **test_and_test_and_set** performs pretty well: it has low latency. We can also see that the **dynamic delay** alternatives perform better than the **static delay**. Static delay locks can potentially enforce unnecessarily large delays under small loads, while dynamic delay adjust based on contention.

Under *light* loads, the **queueing lock** performs the worst. This is because of the higher latency inherent to the queueing lock, in the form of the more complex atomic, **read_and_increment**, as well as some additional computation that is required at lock time.

## Terms

* [cache line](https://open-cas.github.io/cache_line.html): A **cache line** is the smallest portion of data that can be mapped into a cache. Every mapped cache line is associated with a **core line**, which is a corresponding region on a **backend storage**. Both the **cache storage** and the backend storage are split into blocks of the size of a cache line, and all the cache mappings are aligned to these blocks. 