# P2L2: Threads and Concurrency 

// it RELEASE mutex!!
Wait(mutex,cond) {
    release mutex and go on wait queue
    ...
    remove from queue, re-acquire mutex
    exit the wait operation
}

That's the reason in lock, it use **while**, not **if**
Lock(m) {
    while (my_list.not_full()) // this while will be run by multiple consumer threads, **if** can't guarantee access to m once the condition is signaled. The list can change before the consumer gets access again.
        Wait(m, list_full);
    my_list.print_and_remove_all();
}

common mistakes

## Mutual Exclusion(mutex)

### Spriout
### Deadlock

## Kernel VS User-level Threads

one-to-one model
many-to-one model
many-to-many model


### Multithreading Patterns

* Boss/Workers Pattern
    * boss: assign work to workers
    * workers: performs entire task

    Throughput of the system limited by boss thread => must keep boss efficient
    Throughput = 1 / t 