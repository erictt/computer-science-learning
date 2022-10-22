# P3L3: Inter-Process Communication

<!-- toc -->
----

## Inter Process Communication

* **Inter process communication (IPC)** is a set of mechanisms that OS supported for interactions among processes (coordination & communication). The mechanism can be categorized as either **message-based** or **memory-based**.
    * message-based. e.g. sockets, pipes, message queue, etc.
    * memory-based: shared memory, memory mapped files.
* A high-level semantics is RPC, it provides some additional detail as to the protocol(s) that will be used. We will talk about it later.
* One important requirement for IPC is **synchronization primitives**.

## Message Based IPC

* In messaged-based IPC, the operating system is responsible for creating and maintaining the channel that is used to send these messages, i.e. socket/port.
* OS create and maintains a channel, such as buffer, FIFO queue.
* OS provides interface to processes -- port
    * Processes send/write message to a port
    * Other processes recv/read message from a port
* The kernel required to establish communication and perform each IPC operation
* The interaction between process require
    * send: system call + data copy
    * recv: system call + data copy
* In total request-response interaction requires **four user/kernel crossings and four data copying operations**.
* drawback: overheads, too many ops: user/kernel crossing ,and copying data in and out of the kernel
* advantage: simplicity: kernel does channel management and synchronization

### Forms of Message Passing

* Several ways to implement, we will talk about **pipes**, **message queue** and **sockets**.
* Pipes
    * Pipes are characterized by two endpoints, so **only two processes can communicate via a pipe**. There is no notion of a message with pipes; instead, there is just a stream of bytes pushed into the pipe from one process and read from the pipe by the other process.
        * Think about the pipe: `|` in the command line
* Message Queues
    * Messages queues understand the notion of messages that they can deliver. A sending process must submit a properly formatted message to the channel, and then the channel can deliver this message to the receiving process.
    * The OS level functionality regarding message queues includes mechanisms for message priority, custom message scheduling and more.
    * The use of message queues is supported via different APIs in Unix-based systems. Two common APIs are **SysV** and **POSIX**.
* Socket
    * With sockets, processes send and receive messages through the socket interface. The socket API supports **send** and **recv** operations that allow processes to send message buffers in and out of the kernel-level communication buffer.
    * For instance, the socket may be a TCP/IP socket, which means that the entire TCP/IP protocol stack is associated with the socket buffer.

* For message queues, the linux system calls that used for
    * send message to a message queue: `msgsnd`
    * receive messages from a message queue: `msgrcv`
    * perform a message control operation: `msgctl`
    * get a message identifier: `msgget`

## Shared Memory IPC

* In shared memory IPC, processes read and write into a shared memory region. The operating system is involved in establishing the shared memory channel between the processes. What this means is that the OS will map certain physical memory pages into the virtual address spaces of both processes. 
    * The virtual addresses in each process pointing to the shared physical location do not have to be the same. 
    * In addition, the shared physical memory section does not need to be contiguous.
* The benefit of this approach is that once the physical memory is mapped into both address spaces, the operating system is out of the way. System calls are used only in the setup phase.
* Data copies are reduced, but not necessarily avoided. For data to be available to both processes, it needs to explicitly be allocated from the virtual addresses the belong to the shared memory region. If that is not the case, the data within the same address space needs to be copied in and out of the shared memory region.
* Since the shared memory area can be concurrently accessed by both processes, this means that processes must explicitly synchronize their shared memory operations. In addition, it is now the developer's responsibility to handle any protocol-related implementations, which adds to the complexity of the application.
* Unix-based system support two popular shared memory APIs: SysV and POSIX. In addition, shared memory IPC can be established between processes by using a memory-mapped file.

## Copy(messages) vs. Map(shared memory)

* <img src="https://i.imgur.com/svs0b6F.jpg" style="width: 600px" />
* Windows systems leverage this difference. If the data that needs to be transferred is smaller than a certain threshold, the data is copied in and out of a communication channel via a port-like interface. Otherwise the data is mapped into the address space of the target process. This mechanism is called **Local Procedure Calls (LPC).**

## SysV Shared Memory

* The operating systems supports **segments** of shared memory, which don't need to correspond to contiguous physical pages. The operating system treats shared memory as a shared resource using **system wide** policies. That means that there is a limit on the total number of segments and the total size of the shared memory. Currently in Linux the limit is 4000 segments, although in the past it was as few as 6.
* functions for managing shared memory
    * create
        * OS allocates the required amount of physical memory and then it assigns to it a unique key. This key is used to uniquely identify the segment within the operating system. Another other process can refer to this segment using this key.
    * attach
        * OS establishes a valid mapping between the virtual addresses of that process and the physical addresses that back the segment. 
    * detach
        * invalidating the virtual address mappings
    * destroy
        * Once a segment is created, it's essentially a persistent entity until there is an explicit request for it to be destroyed. 

### SysV Shared Memory APIs

* `shmget(shmid, size, flag)` <-- create or open a segment 
    * specify the size of the segment through the size argument, and we can set various flags, like permission flags, with the flag argument.
    * The shmid is the key that references the shared memory segment. This is not created by the operating system, but rather has to be passed to it by the application.
* `ftok(pathname, proj_id)` <-- generate the key
    * This function generates a token based on its arguments. If you pass it the same arguments you will always get the same key. It's basically a hashing function. This is how different processes can agree upon how they will obtain a unique key for the memory segment they wish to share.
* `shmat(shmid, addr, flags)` <-- attach the shared memory segment
    * The programmer has an option to provide the virtual addresses to which the segment should be mapped, using the addr argument. If NULL is passed, the operating system will choose some suitable addresses.
    * The returned virtual memory address can be interpreted in various ways, so it is the programmer's responsibility to cast the address to that memory region to the appropriate type.
* `shmdt(shmid)` <-- detach a segment
    * This call invalidates the virtual to physical mappings associated with this shared segment.
* `shmctl(shmid, cmd, buf)`
    * To send commands to the operating system in reference to the shared memory segment.
    * If we specify IPC_RMID as the cmd, we can destroy the segment.
* more detail: https://tldp.org/LDP/lpg/node21.html

### POSIX Shared Memory API

* The POSIX shared memory standard doesn't use segments, but files. They are not "real" files that live in a filesystem that are used elsewhere by the operating system. Instead they are files that live in the **tmpfs** filesystem. 
* Since shared memory segments are now referenced by a file descriptor, there is no longer a need for the key generation process.
* The functions:
    * created/opened:  `shm_open()`.
    * attach/detach shared memory: `mmap()` and `munmap()`
    * destroy a shared memory region: `shm_unlink()`
    * remove file descriptor from the address space of the process: `shm_close()`, not destroy
* https://man7.org/linux/man-pages/man7/shm_overview.7.html

### Shared Memory and Sync

* Shared memory has the same situation we encountered in multithreaded environments -- synchronization.
* Couple of options for handling inter-process synchronization:
    1. mechanism supported by process threading library (PThread)
    2. OS-supported IPC for synchronization
* Either method must coordinate
    * number of concurrent accesses to shared segment (i.e. mutexes)
    * when data is available and ready for consmption(i.e. signals)
    * [mq_notify()](https://man7.org/linux/man-pages/man3/mq_notify.3.html) and [sem_wait()](https://man7.org/linux/man-pages/man3/sem_wait.3.html)  in Linux

#### PThreads Sync for IPC

* The property of the mutex or the condition variable when they are created is whether or not that synchronization variable is private to a process or shared amongst processes.
* The keyword for this is **PTHREAD_PROCESS_SHARED**. If we specify this in the attribute structs that are passed to mutex/condition variable initialization we will ensure that our synchronization variables will be visible across processes.
* One very important thing is that these data structures for the synchronization construct are allocated from the shared memory region must be visible to both processes!
* <img src="https://i.imgur.com/zK6k5Je.jpg" style="width: 600px" />
* To create the shared memory segment, we first need to create our **segment identifier**. We do this with `ftok`, passing `arg[0]` which is the pathname for the program executable as well as some integer parameter. We pass this **id** into `shmget`, where we specify a **segment size of 1KB** and also pass in some flags.
* Using the segment id, we attach the segment with `shmat`, which returns a shared memory address - which we assign to `shm_address` here. `shm_address` is the **virtual address** in this process's address space that points to the physically shared memory.
* Then we cast that address to the datatype of the struct we defined - `shm_data_struct_t`. This struct has two fields. 
    * One field is the actual buffer of information, the data. 
    * The other component is the mutex. In this example, the mutex will control access to the data.
* To actually create the mutex, we first have to create the `mutexattr` struct. Once we create this struct, we can set the pshared attribute with **PTHREAD_PROCESS_SHARED**. Then we initialize the mutex with that data structure, using the pointer to the mutex inside the struct that lives in the shared memory region.
* This set of operations will properly allocate and initialize a mutex that is shared amongst processes.

#### Sync for Other IPC

* Pthreads isn't necessarily always supported on every platform. Sometimes, we can rely on other means of synchronization in those cases, such as **message queues** and **semaphores**.
* Message queues. Implement mutual exclusion via send/recv operations.
    * For example, process A can write to the data in shared memory and then send a "ready" message into the queue. Process B can receive the msg, read the data, and send an "ok" message back.
* Semaphores are an OS support synchronization construct and a binary semaphore can have two states, 0 or 1. 
    * When a semaphore has a value of 0, the process will be blocked. If the semaphore has a value of 1, the process will decrement the value (to 0) and will proceed.

#### IPC Command Line Tools

* Linux provided some command line utilities for using IPC in general.
    * `ipcs` -> list all IPC facilities
        * `-m` display info on shared memory IPC only
    * `ipcrm` -> delete IPC facility
        * `-m [shmid]` deletes shm segment with given id

## Shared Memory Design Considerations

* Consider
    * different APIs/mechanisms for synchronization
    * OS provides shared memory, and is out of the way
    * data passing/sync protocols are up to the programmer
* Ask
    * How many segments you need?
        * 1 large segment -> manager for allocating/freeing memory from shared segment
        * multiple segments, one for each pairwise communication
            * use pool of segments to avoid creating in the middle of execution
            * use a queue of segment ids  to manage the segments for communicating among processes
                * or via some other mechanism like message queue.
    * How large  the segment it should be?
        * if you know the size up front like static size, you can set up the segment size == data size
        * if want to support arbitrary messages sizes that are potentially much larger than the segment size, 
            * One option is to transfer the data in rounds. The sending process sends the message in chunks, and the receiving process reads in those chunks and saves them somewhere until the entire message is received. In this case, the programmer will need to include some protocol to track the progress of the data movement through the shared memory region.