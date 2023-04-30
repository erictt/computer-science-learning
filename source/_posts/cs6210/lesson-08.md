# Lesson 08: Failures and Recovery

The goal of this module is to build a system that help the subsystems to survive crashes. To do that, we need to provide persistence support for the subsystems and also make it performant.

## L08a: Lightweight Recoverable Virtual Memory(LRVM)

LRVM is a lightweight runtime library that offer interfaces that allow application to persist the virtual memory to the disk.

### Server Design

![](https://i.imgur.com/0mQV6PV.png)
The LRVM create external data segments to back persistent data structures for the applications
The application can create as many as data segments it wants.

### RVM Primitives

Initialization:
- `initialize(options)`
	- Declares a log segment for aggregating changes made to persistent data structures.
- `map(region, options)`
	- Maps a region of virtual address space to an external data segment.
- `unmap(region)`
	- Decouples a region of virtual address space from its associated external data segment.

Body of server code:
- `begin_transaction(tid, restore_mode)`
	- Signals the RVM runtime that changes will be made to persistent data structures between begin_transaction and end_transaction calls. The restore_mode specifies how to restore the state of the data structures in case of failure.
- `set_range(tid, addr, size)`
	- Being called at the beginning of the transaction. 
	- Specifies a block of memory to modify within the critical section between begin_transaction and end_transaction calls.
- `end_transaction(tid, commit_mode)`
	- Signals the RVM runtime to commit changes made to persistent data structures in the current transaction. The commit_mode specifies how to handle flushing of the redo log to disk.
- `abort_transcation(tid)`
	- Signals the RVM runtime to throw away changes made to persistent data structures in the current transaction.

To reduce log space:
- `flush()`
	- Explicitly flushes the redo log to disk.
- `truncate()`
	- Applies the redo log to the external data segments and truncates the log.

Misc:
- `query_options(region)`
	- Retrieves the options associated with a region of virtual address space.
- `set_options(options)`
	- Sets the options associated with a region of virtual address space.
- `create_log(options, len, mode)`
	- Creates a log segment with specified options, length, and mode.

### How the Server Uses the Primitives

![](https://i.imgur.com/9YbgxG7.png)

1. **Initialization**: At the start of the code, the developer maps the address space of their process to external data segments and specifies the log segment for the code. This is done using the `initialize()`, `map()`, `unmap()`, and `create_log()` primitives.
2. **Begin transaction**: When the developer wants to modify persistent data structures in their code, they begin a transaction using the `begin_transaction()` primitive. They can also specify a restore mode, which tells the system that the transaction will never abort and therefore no undo record needs to be created.
3. **Set range**: Once the transaction has begun, the developer specifies the block of contiguous addresses that they plan to modify in this critical section using the `set_range()` primitive.
4. **Modify data structures**: The developer can then modify in-memory versions of the persistent data structures using normal code.
5. **End transaction**: When the developer is done with the changes, they call `end_transaction()` to commit the transaction. LRVM creates a redo log in memory of the changes that have been made to the persistent data structures.
6. **Flush and sync redo log**: LRVM flushes the redo log to the log segment on the disk synchronously. However, the developer can specify a "no flush" mode in `end_transaction()` to allow the system to commit the transaction without blocking further execution.
7. **Abort transaction**: If the transaction aborts, LRVM restores the original version of the portion of the virtual address space that was modified during the critical section by copying the undo record back into that space.

### Transaction Optimizations

RVM has restricted transaction semantics, which means it doesn't allow nested transactions and doesn't require synchronous I/O for every commit. However, RVM provides opportunities for the developer to optimize the performance of the library for the chosen application.

1. No-restore mode in the begin_transaction call. This mode tells RVN that the transaction starting is not going to abort, so there is no need to create an in-memory undo record. This reduces the amount of work that RVM has to do, and the overhead in performing a transaction is less.
2. No-flush mode in the end_transaction call. This mode tells RVM that there is no need to do a synchronous I/O at the commit point. The application developer takes a chance by using this mode because there is a **window of vulnerability** between end_transaction and the point at which the redo log has been forced to the disk. If there is a system cache within this time, the redo records that were written to in-memory may be lost.

### Implementation

![](https://i.imgur.com/F0Qr7yd.png)


RVM uses a logging strategy called **no undo/redo value logging**, which creates an undo record of the changes that are going to be made to virtual memory but is not a log that is persistent on the disk. The redo log consists of a transaction start and the changes that are made, but **only new value records** of committed transactions are written to the log. This is the reason for forward displacements because we know where to append to the log segment on the disk. Upon commit, the old value records in the virtual memory are replaced with the new value records, which is automatic. Only if you abort, you have to undo the changes. At that point, you have to force the redo log records to the log on the disk.

### Crash Recovery

![](https://i.imgur.com/Ahooon9.png)

Crash recovery consists of RVM first reading the log from tail to head, then constructing an in-memory tree of the latest committed changes for each data segment encountered in the log. The trees are then traversed, applying modifications in them to the corresponding external data segment. Finally, the head and tail location information in the log status block is updated to reflect an empty log. The idempotency of recovery is achieved by delaying this step until all other recovery actions are complete.

### Log Truncation

![](https://i.imgur.com/QJtTzvG.png)

Truncation is the process of reclaiming space allocated to log entries by applying the changes contained in them to the recoverable data segment. Periodic truncation is necessary because log space is finite, and is triggered whenever current log size exceeds a preset fraction of its total size. 

Log truncation has proved to be the hardest part of RVM to implement correctly. To minimize implementation effort, we initially chose to **reuse crash recovery code for truncation**. In this approach, referred to as epoch truncation, the crash recovery procedure described above is applied to an initial part of the log while **concurrent forward processing** occurs in the rest of the log. The figure above depicts the layout of a log while an epoch truncation is in progress.

## L08b: RioVista

There are two orthogonal problems that lead to a system crash. One is **power failure**. The second is **software failure**.

So Rio Vista poses a very interesting rhetorical question. Suppose we postulate that the only source of system crash is software failure.

The authors propose a way to eliminate the heavyweight transaction properties of traditional persistent memory systems while improving performance by **leveraging a battery-backed DRAM to create a persistent file cache**.

### LRVM Revisited

![](https://i.imgur.com/JHriocp.png)
The upshot of LRVM implementation is there are **three copies** of the VM space done by LRVM to manage persistence for recoverable objects.
1. The **original data segment**, which contains the persistent data that is brought into memory and modified during the transaction.
2. The **in-memory undo record**, which is created by LRVM when the application calls the `begin_transaction` primitive. This record contains the old contents of the portion of the memory that the transaction is going to modify.
3. The **redo log record**, which is written out to the disk at the end of the transaction and represents all the changes made to virtual memory within that critical section bound by a `begin_transaction` and end_transaction.

### Rio File Cache

![](https://i.imgur.com/YsZhTki.png)
The Rio File Cache allows for file writes and normal program writes to memory-mapped files to become persistent by definition. This eliminates the need for synchronous writes to the disk and allows for arbitrary delay in writebacks.

### Vista RVM on Top of Rio

![](https://i.imgur.com/BHJzAXL.png)
Vista is an RVM library that has been implemented on top of the Rio file cache. The implementation of RVM using the Rio file cache is similar to LRVM, but it takes advantage of the fact that it is sitting on top of a Rio file cache.

When the data segment is mapped to the virtual memory, this portion of memory becomes persistent because it is contained in the file cache.

At the `begin_transaction` call, a before image is made of the portion of the virtual memory that we intend to modify during this transaction, which serves as the undo log. This undo log is backed up on the file cache and is therefore persistent. 

During the execution of the transaction, normal program writes to the portion of the virtual memory where there are persistent data structures are reflected in the data segment, which is battery-backed. 

At the `end_transaction` call, if the transaction is committed, no work needs to be done other than getting rid of the undo log because all the changes that the application developer intended to be committed to the data segment are already in there. 

On the other hand, if the transaction aborts, the undo record that was created at the beginning of the transaction is used to copy the original image back into the portion of the virtual memory that was modified. 

At the point of `end_transaction` for commit, all that needs to be done by Vista is to get rid of the undo log. There is **no disk I/O involved**, and there is **no redo log** because **we are directly writing into the data segments**.

### Crash Recovery

In the Vista implementation, the data segment is mapped to the virtual memory and is made persistent by definition, and an undo log is created at the begin_transaction call to serve as the undo record in case of transaction abort. 

**At the end_transaction call, if it's a commit, no work needs to be done except to get rid of the undo record,** as all the changes to persistent data structures are already in the data segment. 

If it aborts, the old image is restored back into the virtual memory, and the undo log is discarded. For crash recovery, the old image is recovered from the undo log, which survives crashes because it is in the Rio file cache. 

Vista is simple compared to LRVM because there are **no redo logs and no truncation code**, and it performs significantly better than LRVM due to the absence of disk I/O. 

## L08c: Quicksilver

- the structure of distributed systems today:

![](https://i.imgur.com/nJg7EiJ.png)


Modern distributed systems comprise **user applications** built on **system services** and a **microkernel**. System services handle components like file and web servers, while the microkernel manages processes and resources. This structure promotes extensibility and high performance in various operating system designs.

### Quicksilver System Architecture

![](https://i.imgur.com/qKurR3L.png)
Quicksilver aimed to introduce new services such as window managers and integrate communication into its design. It was the first OS to propose **transactions for recovery management**.

### IPC Fundamental to System Services

**Inter-process communication (IPC)** is crucial to Quicksilver's distributed system, with both synchronous and asynchronous client calls being supported. Quicksilver provides guarantees like **no loss or duplication of requests** and **location transparency for client-server interactions**.

![](https://i.imgur.com/W9pipwG.png)

The kernel manages a data structure called a **service queue**, which is created by a server to handle client requests. When a client makes a request, the kernel informs the server via an **upcall**. The server executes the request, and the **completion goes back into the service queue**, signaling the **kernel** to provide a response to the client.
- At some point, the client needs to perform a **wait** operation on the service queue to indicate that it is ready to receive the response associated with its request. If the server has already processed the request and the response is available in the service queue, the kernel delivers the response to the client. If the response is not yet available, the client will wait until the response comes back.
- **Multiple servers can wait on a service queue**, which means any number of servers can **offer** their services for a particular service queue. The kernel can then choose a server based on their current workload when handling incoming requests.
- **Client-server relationships are interchangeable.** For example, a client may make a call to a file system server, which then acts as a client when making calls to a directory server or a data server. This flexibility allows for more complex interactions between system services.

IPC **guarantees no loss or duplication of requests**, ensuring requests are completed **exactly once**. It also takes care of the **reliability of data transfer**, especially when clients and servers are on remote machines. Furthermore, the **service queue data structure is globally unique**, providing **location transparency** for client-server interactions, meaning clients don't need to know where their requests are being serviced.
- IPC is the primary means of communication between clients and servers in Quicksilver. By integrating the **recovery mechanism** with IPC, the operating system ensures that every client-server interaction using IPC also includes **transactional support** for recovery.

### Bundling Distributed IPC and X Actions

![](https://i.imgur.com/mw32iRm.png)

- Quicksilver bundles IPC with recovery management using lightweight transactions, similar to LRVM.
- IPC calls are tagged with transaction ID.
- A shadow graph structure emerges from client-server interactions, showing the trail of these interactions.
- The transaction tree has a root (owner) and participants.
- Transaction managers on different nodes communicate with no extra overhead, as communication is piggybacked on regular IPC.
- The transaction tree can span multiple nodes or sites.
- Transactions are provided for recovery purposes, and the client-server relationship can traverse multiple nodes, requiring multi-site atomicity for recoverability.

### Transaction Management

![](https://i.imgur.com/Am8bHDT.png)


- Shadowing IPC with transactions is essential for managing resources and recovery.
- The transaction manager at each node manages local resources and coordinates with other transaction managers.
- Shadows transactions enable the operating system to track the state of client-server interactions, allowing for recovery in case of failures.
- The owner of a transaction tree can delegate ownership to another node, which is useful when clients are fragile and may go away.
- Quicksilver handles the heavy lifting of maintaining the transaction tree for recovery purposes.

### Distributed Transaction

![](https://i.imgur.com/ShYcte2.png)


- Transaction managers are responsible for all client-server interactions that touch a particular node.
- The graph structure of the transaction tree helps reduce network communication.
- Brittle nodes in the system, like client nodes, may designate the coordinator to a more robust node like a file server.
- Transaction managers log periodically to persistent store, creating checkpoint records for recoverability reasons.
- Distributed system failures can happen at any point, and transactions are not aborted at the first indication of failure, allowing error reporting to continue and partial failures to be cleaned up when the coordinator initiates termination.

### Commit Initiated by Coordinator

![](https://i.imgur.com/H7XKwFQ.png)

- The transaction tree is activated when the client-server relationship completes its action.
- The coordinator initiates the termination of a transaction, either as a commit or abort, and communicates this to its subordinates.
- Different commit protocols can be used depending on the criticality of states and the nature of breadcrumbs left behind at different sites (e.g., persistent servers may need a two-phase commit protocol, while a window manager may only need a one-phase commit protocol).

### Upshot of Bundling IPC and Recovery


![](https://i.imgur.com/Em1uaQg.png)

- Bundling IPC and recovery management allows services to safely collect breadcrumbs left behind at all touched locations (e.g., memory, file handles, communication handles, windows on display).
- No extra communication is needed for recovery management, as the transaction tree leverages IPC for communication.
- Services can choose recovery management policies and mechanisms based on their specific requirements, with Quicksilver offering a variety of options.

### Implementation Notes

- Log maintenance is essential in Quicksilver for recording and recovering persistent state.
- Transaction managers write log records for persistent state recovery and periodically force in-memory log segments to storage for persistence.
- The frequency of log force impacts performance and can be initiated by applications, but services must be careful in their choice of mechanisms to balance performance and recovery requirements.

### Quicksilver Conclusion

- Quicksilver demonstrates the enduring nature of using transactions for state recovery in operating systems, with ideas finding resurgence in LRVM and other research systems like Texas.
- While commercial operating systems prioritize performance, reliability is often overlooked, leading to potential data loss in system crashes.
- The emergence of storage class memories, which combine DRAM-like latency with non-volatile properties, may lead to a renewed interest in transactions for operating systems in the future.