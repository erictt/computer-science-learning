## OMSCS 6210 Spring 2023 Test 3 Prep


## Internet-scale computing

### 1. (11 points)(Giant-scale services)

Assume you are the developer responsible for deploying ChatGPT. Assume that the underlying ML model used by ChatGPT needs a total of 800 GB memory for storing the model parameters. The model can be decomposed into 8 GB slices that can be run in a pipelined manner. The data center you are deploying ChatGPT offers machines with a fixed 8 GB of memory, and you have profiled each slice to take 1 ms of execution time. Assume zero communication cost to convey the results from one slice of model execution to the next.

a. [2 points] You now want to deploy this model to support 1 million requests per sec. How many minimum machines will you need?

1 pipeline needs 100 nodes(100 * 8GB = 800GB)
each request take 1 ms of execution, each pipeline can take 1000 requests / sec.
To support 1 million requests/sec, we need 1000 pipelines
So 100 nodes * 1000 clusters = 100,000 nodes

b. [2 points] What is the latency incurred by the user for each query?
	Answer with justification if you can reduce the latency by employing more machines per query.

The model works as a pipeline, each slice takes 1ms. Since each node has a fixed 8 GB memory, we require 100 steps to accomplish a single task, which is 100ms.
Adding more machines doesn't reduce the latency as each pipeline requires 100ms.

c. [2 points] Calculate the throughput if one node in the whole fleet fails.

Assuming we have 100K nodes, one node fails in one of the pipelines. This will cut off the entire pipeline, which leads to only 999 pipelines available. So the throughput will be 999K requests/sec.

d. [2 points] Calculate the throughput if two nodes fail.

There are two possibilities:
1. Two nodes work for the same slice.  The throughput will be reduced to 998K
2. Two nodes works for different slice. The throughput is the same as `c`,  which is 999K

e. [3 points] The model gets updated. The updated model has to be deployed in the servers. Discuss pros and cons of each of the strategies (fast, rolling, big-flip) for doing the update.

Fast (cold upgrade): 
	Pro: Fastest upgrade, comparing to the other strategies.
	Con: The entire service will be unreachable during the upgrade.

Rolling (1 pipeline at a time): 
	Pro: The service only loses 1/1000 capacity during the upgrade.
	Con: It takes 1000x times to fully complete the upgrade comparing to fast upgrade.

Big-flip (50/50): 
	Pro: Faster than Rolling, and also offers continuous services during the upgrade.
	Con: The service's throughput will be reduced to half of the capacity during the upgrade.


### 2. (10 points)(Map-reduce)

A map-reduce application consists of:
- 30 shards of data to be processed
- 10 distinct outputs to be produced
- CPU time to execute a map function: $T_m$
- CPU time to execute a reduce function: $T_r$
- I/O time to write the intermediate result by a mapper: $T_i$
- RPC time to fetch an intermediate result by a reducer: $T_{rpc}$
- I/O time to write out the result by a reducer: $T_f$

The Map-reduce infrastructure includes asynchronous RPC, allowing a reducer to fetch the intermediate results in parallel from the mappers. The map-reduce infrastructure uses 10 threads for the map function and 5 threads for the reduce function. Ignoring scheduling overheads by the infrastructure, compute the total execution time for the above application. (Show your work for partial credit)

1. 30 shards assign to 10 map threads => $3 * (T_m + T_i)$ for processing all map tasks
2. 10 distinct outputs assign to 5 reduce threads => $2 * (T_{rpc} + T_r)$ for processing the reduce tasks. This assumes that the 30 RPC calls are being done in parallel. Each reduce only needs $T_{rpc}$ to retrieve all the data.
3. Write all results to disk, each reduce thread will need to handle 2 tasks. To write out all the results, we need $2 * T_f$ 

In total: $3 * (T_m + T_i) + 2 * (T_{rpc} + T_r) + 2 * T_f$


### 3. (8 points)(CDN–Coral)

a.[3 points] Why is Coral called an overlay network? Give another example of an overlay network.

An overlay network is a virtual network built on top of the physical network with 1-1 mapping. Coral is a content delivery network that map the node ID to the physical IP.

One example is that IP over LAN. The IP is an overlay on the MAC address of the computer, used for external network communication with others in the local/world-wide network.

b.[5 points] Key-based routing in Coral Given below is a routing table for Coral, where the source node 9 (src) is trying to reach the destination node 1 (dst).
Entries in the second row show the XOR distance from the source (src) to a node that is currently reachable (i.e., src has a valid IP-address for that node). Entries in the third row show how the routing table evolved after the first iteration of key-based routing.

![](https://i.imgur.com/eLH5T5v.png)

(i) [2 points] Which node did "src" make an RPC call to in the first iteration to get the new entries in the third row? Why?

Node 5. The key-based routing reduce ~half of the distance to the destination.

(ii) [2 points] Which node will "src" make the next RPC call? Why?

Node 3. The same reason as before, it takes half of the distance to the destination.

(iii) [1 point] How many hops does it take "src" to reach "dst"? List the nodes visited by "src" in getting to "dst".

4 (9->5, 5->3, 3->0, 0->1)


## Real-time and Multimedia

### 4. (10 points)(TS-Linux)

a. [2 points] What is the priority inversion problem and how can it be handled in a Linux-like OS that uses priority-based scheduling?

The priority inversion problem occurs when a higher-priority task is blocked by a lower-priority task that is currently running, often due to the lower-priority task servicing a request from a higher-priority one.

The problem can be handled by temporarily boosting the priority of the lower-priority task to match the priority of the higher-priority task during the service time, preventing preemption by intermediate-priority tasks.

b. [2 points] Proportional period scheduling in TS-Linux allocates to a requesting task a desired proportion (Q) of the CPU in each period (T - a scheduling parameter). What problem is this aiming to solve?

It's aiming to solve the problem of allocating CPU resources to time-sensitive tasks while **ensuring that other tasks also get the opportunity to run**. By allowing tasks to request a specific proportion of CPU time within a given time quantum, the scheduler can perform admission control to check if the requested proportion can be satisfied without overcommitting CPU resources, thus providing temporal protection and improving scheduling accuracy.

c. [6 points] A video game running on top of TS-Linux is using the one-shot timer. It has it programmed to go off every 300 microseconds to update some internal state of the game. It uses an overshoot parameter of 30 microseconds. At 290 microseconds since the last firing of the one-shot timer there is an external interrupt (lower in priority compared to timer events) into TS- Linux. List the steps taken by TS-Linux upon getting this interrupt (concise bullets, please).

1. TS-Linux acknowledges the external interrupt since it is lower in priority compared to time events.
2. The interrupt is serviced, and the system continues executing the current task.
3. At 300 microseconds, the one-shot timer goes off.
4. TS-Linux checks for expires timers, including the video game's timer.
5. The video game's timer event is dispatched and handled.
6. If necessary, the one-shot timer is reprogrammed for the next 300-microsecond interval.
7. The system returns to executing the video game and other tasks as per their priorities and scheduling.


### 5. (8 points)(PTS)

a. [6 points] Your friend is developing a multi-modal live-streaming application that is represented using a pipelined graph of tasks. Give three reasons why you would advise your friend to choose PTS rather than using Unix sockets and processes.

1. Time as a first-class entity: PTS allows for time manipulation within the application, making it easier to handle time-sensitive data, which is essential in a live-streaming application.
2. Seamless handling of live and historical data: PTS allows for integration of live and historical data, simplifying data management and access for the application.
3. Persistent streams under application control: PTS enables the continuous production and persistence of data, ensuring that the data is available for processing and retrieval as needed.

b. [2 points] Assume a PTS Channel ch1 has items with timestamps 25, 50, 75, 100.

Consider the following PTS code sequence by a thread T1:
```c
<item, ts> = Get(ch1, “now”);//returns latest item from channel 1
Digest = Process(item);
<some code> // code to process item just gotten
Put (ch2, Digest, ts+25); //put digest with timestamp ts+25
```

What is the timestamp associated with the above put operation?

The latest item has a timestamp 100, and the Put operation adds 25 to the timestamp, so the timestamp associated with the Put operation is 125.

## Failures and Recovery

### 6. (10 points)(Quicksilver)

In Quicksilver, consider a client is contacting a file server for opening and writing to a file. For this, the file server contacts a directory server for creating the file (which maps filenames to “pointers” to file’s data), and a data server for writing to a disk block (which allocates data blocks on disk and writes bytes to them).

![](https://i.imgur.com/ttawWh5.png)


1. [2 points] Describe at least one scenario in which this client's request fails. What are the breadcrumbs that could be left behind due to such a failure?

For example, the client crashes during the interaction with the file server, directory server, or data server. The breadcrumbs that could be left behind due to such a failure include allocated memory that hasn't been reclaimed, file handles, communication handles, and possible partially written data on the data server.

2. In the above scenario, assume that the client closes the file after writing to it. The coordinator for the shadow transaction tree that represents this client-server interaction is the client node.
	1. [2 points] In the absence of any failures, what will happen upon the "close" call by the client?
		1. When the client closes the file, the coordinator of the shadow transaction tree will initiate a commit process. This involves sending commit requests to the participating nodes(file server, directory server, and data server) and receiving their votes. If all the votes are positive, the coordinator will finalize the commit, and the temporary resources will be cleaned up.
	2. [2 points] Suppose a 1-phase commit is used instead of 2-phase commit. Describe a failure scenario that may leave the system in an inconsistent state.
		1. A failure scenario that may leave the system in an inconsistent state is when the client successfully writes to the data server but fails to update the directory server before crashing. In this case, the file's data is written to the disk, but the directory server doesn't have the correct pointer to the file's data, leaving the system inconsistent.
	3. [2 points]Explain why a 2-phase commit will NOT leave the system in an inconsistent state for the failure scenario you described above.
		1. During the first phase, the coordinator will send vote requests to all participating nodes(file server, directory server, and data server). If any of the nodes do not respond positively or crash during the process, the coordinator will not proceed with the commit and will instead initiate an abort process. This ensures that the system remains consistent even in the face of failures.
3. [2 points] Suppose the file server is built to serve numerous clients at the same time, and talks to multiple data servers(each managing a single disk, for example). What would be the advantage of the file server making non-blocking IPC calls to data servers, as opposed to blocking IPC calls?
	1. The file server can continue processing other client requests while waiting for the responses from the data servers. This allows for better concurrency and higher overall throughput, as the file server does not have to wait for one data server to complete its task before moving on to the next request.

### 7. (6 points)(LRVM)

a. [3 points] How does the “no restore” mode in begin-transaction help in improving the performance of a server written on top of LRVM?

It eliminates the need to restore the data segments to their original state in case of an abort, which avoided the data copy on set-range.

b. [3 points] During crash recovery, the redo log is applied to the data segments to bring the server to a consistent state prior to the crash. LRVM chooses to apply the log to the affected data segments starting from the tail of the log rather than the head. Why?

This allows LRVM to avoid applying redundant updates that have already been applied previously. By starting from the tail of the log, LRVM can skip over updates that have already been applied, reducing the amount of work required during recovery and improving the overall performance of the system.

### 8. (6points)(RioVista)


a.[3 points] Your friend John argues that a battery backed file cache such as Rio provides the exact same functionality and benefits as the end transaction in LRVM with the no-flush mode. Would you agree with his argument? State why or why not.

I would not entirely agree with John's argument. While a battery-backed file cache like Rio does provide some benefits similar to the end transaction in LRVM with no-flush mode, they are not the same in terms of functionality.

Rio uses a battery-backed cache to store data in memory, allowing for faster data access and ensuring data durability in case of a system crash. However, it does not provide the same level of transactional guarantees and atomicity that LRVM with no-flush mode offers. LRVM allows applications to manage persistent memory as if it were a regular volatile memory, providing atomicity through transactions. The no-flush mode in LRVM ensures that changes made within a transaction are committed to stable storage only at the end of the transaction, reducing the number of disk flushes.

b.[3 points] In RioVista, consider a transaction that completes successfully. List the number of copies of the persistent data structures that happen in the following table:

| What is copied? | Where is it copied to? | Lifetime of the copy |
| --------------- | ---------------------- | -------------------- |
| The before image copy of the address range that was modified, in the state it was at the very start of the transaction | The undo log region of memory, which is mapped to an undo log region in the file cache. |  Starts when set-range is called. Lives until the transaction is committed, at which point it is discarded.|


## Security

### 9. (10 points)(Security principles, AFS)

Throw back to the 80's. You are one of the designers of AFS. You choose to implement AFS using ONLY a public-key encryption system. Note: Symmetric key (i.e., private-key) encryption should NOT be used for any of the client-server interactions.

Answer the following questions:

a. [2 points] A new user joins the system. What all needs to happen in the system to give the new user the same rights and privileges as existing users?

My idea is similar to mTLS, the server will send the pub key to the client upon the auth process. 
Then the client(Vinus) generates a public/private key pair and send the public key along with the username/password to the server, and the message is encrypted with server's public key. 

b. [2 points] With your implementation, when a user logs in to "virtue", what should happen?

c. [2 points] In your implementation of the system, when a request comes from a client, how will the server know the identity of the client to enable decryption of the message?

d. [2 points] In your implementation of the system, when a reply comes from the server, how will "virtue" know how to decrypt the message?

e. [2 points] A student graduates and his privileges to AFS have to be revoked. What all needs to happen in the system to ensure that the student has no access to the system?