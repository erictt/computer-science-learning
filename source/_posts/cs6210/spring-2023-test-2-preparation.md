# OMSCS 6210 Spring 2023 Test 2

## Distributed Systems 

### I. Lamport’s Logical Clock 

A. [2 points] Lamport’s logical clock is an intellectually appealing  strategy for maintaining the state of communicating processes in a  distributed system. What is deficient about logical clocks that  necessitates the physical clock formalism by Lamport in the same  paper? 

- **Lack** mechanisms to **synchronize** processes with respect to physical time. 
- `happen-before` **doesn't guarantee** that the assigned timestamps will be consistent with actual **real-time order**.

B. [4 points] Assume a system where clocks on nodes do not drift and  the network communication time is constant. Do we still need a  Lamport’s clock to determine “happened before” relations? Explain. 
 
Yes. 

1. Even with no drift clock and network issue, the **clock synchronization** among multiple nodes is still hard to achieve. Besides, the time for processing events varies, which leaves uncertainties to the event orders. <-- NTP
2. Physical locks can't **differentiate events that occur in a rapid succession**. As a result, the events with close timestamps might be incorrectly ordered.
3. Lamport's logical clocks can help establish partial orders for concurrent events based on **causal relationships**, which cannot be achieved using physical clocks alone.

### II. Lamport’s ME Algorithm 

A. [5 points] Construct a simple ordering of events involving two  processes (P1 and P2) where Lamport’s algorithm violates mutual  exclusion, where P2 acquires mutex when it has already been acquired  by P1. 

Give your answer in the form of a sequence of one of the following  events. Show the state of the queues at P1 and P2 wherever  necessary, and clearly indicate which messages were delivered out of  order. 

• SEND LOCK/ACK/UNLOCK P1 -> P2 (P1 sends lock/ack/unlock to P2) 
• RECV LOCK/ACK/UNLOCK P1 -> P2 (P2 receives lock/ack/unlock  sent by P1) 
• ACQUIRE P1 (P1 acquires lock) 

--

SEND LOCK P1 -> P2 (P1 sends lock request to P2)  
- P1: [P1:T1]  
- P2: []  
SEND LOCK P2 -> P1 (P2 sends lock request to P1)  
- P1: [P1:T1]  
- P2: [P2:T2]  
RECV LOCK P2 -> P1 (P1 receives lock request from P2, later lock request enough for acquire)  
- P1: [P1:T1,P2:T2]  
- P2: [P2:T2]  
ACQUIRE P1 (P1 acquires lock)  
SEND ACK P1 -> P2 (P1 sends ACK that it received P2 lock request)  
- P1: [P1:T1,P2:T2]  
- P2: [P2:T2]  
RECV ACK P1 -> P2 (P2 receives ack sent by P1 OUT OF ORDER, P2 thinks it has lock, it should have received P1's Lock request first)  
ACQUIRE P2 (P2 acquires lock)  
- P1: [P1:T1,P2:T2]  
- P2: [P2:T2]  
RECV LOCK P1 -> P2

B. [3 points] Construct a simple example of a sequence of events involving two processes P1 and P2, where “progress” is violated,  that is, in a situation where the mutex previously held by P1 has  been released, but P2 is not able to acquire it. 

Use the format shown in part (A) for the sequence of events, and  clearly indicate which message was lost. 

SEND LOCK P1 -> P2
SEND LOCK P2 -> P1
SEND ACK P2-> P1
SEND ACK P1-> P2
ACQUIRE P1
SEND UNLOCK P1->P2 (got lost)

C. [2 points] The correctness of the basic Lamport's ME algorithm  depends on no message loss. You want to relax this requirement and  yet assure correctness. How would you do it? 

So we still have message in order and queues are in total order.

Make it as TCP protocol-like, when receiving a message bump the SEQ number and send a ACK. If the SEQ is missed, ask for a resend.

D. [2 points] Your co-worker asserts that for the correctness of the  basic Lamport's ME algorithm, messages from a given process P1 to  all other processes in the entire distributed system must arrive in  the order in which they are sent from P1. Is she right? You should  justify your answer with an explanation.

She is right. If messages arrive out of order, the `happens-before` relation may be violated, leading to **incorrect order of lock requests** in the queue.

### III. Latency Reduction in RPC 

A. [2 points] Thekkath and Levy suggest using a shared descriptor  between the client stub and the kernel for marshalling arguments  during an RPC call. Your friend argues that this does not result in  reducing the copying overhead of an RPC call. How would you counter  her argument? 

In the traditional RPC mechanism, the client stub marshals the arguments into a buffer, which is then copied into kernel space which costs significant overhead. By sharing the same descriptor, the copy from user space to kernel space can be eliminated.

B. [4 points] Consider the following control transfers involved in an  RPC call. 

![](https://lh4.googleusercontent.com/jV3e22BqOf9vlb9zpw7dSCxlyxUhVGvIkDhEvjwJ5j_rBiFMfIa_CEIRpby2HVGaXsklsmlODOOxHNsXh1VSEwR6seJYUSmOOc2OumJ30RgGynJJ4yE4H0en-dmH-aQFSBMXzmTElvqruHHcQM-9SbY)

Out of these, identify the ones that are in the critical path. Why are  the identified calls considered in the critical path while others are  not? 

There are two paths are considered critical. One is when the call arrivals on the server, it needs to do context switch from other processes to serve the incoming calls. The other one is, when the results arrive to the client, the client needs to do context switch to handle the response.

C. [4 points] You have designed an RPC system which has the following  parameters: 

• T: Message transmission time in either direction for sending the  arguments of the call or receiving the results (includes protocol  processing, time on the wire, and interrupt processing)  

• CSc = 3T: Context switch time at the client node 

• CSs= T: Context switch time at the server node 

You notice from the logs that the server procedure execution time is  bimodal: it takes T units of time mostly but occasionally 20T units  of time. 

How would you optimize the latency for RPC calls for this client server interaction? 

In a normal route, the request takes 4T(1T on the wire, 1T for server to do context switch, 1T for execution, 1T for transfer back to client) to get back. So in my design, the client will do context switch if it doesn't get a response from the server.

### IV. Active Networks 

A. In an Active Network, we expect the intermediate routers to execute  code by looking at the “type” field of the capsule present in the  incoming packet. For a “type” that it has not seen before, it  requests the code from the node present in the “prev” field.

1. [2 points] Is it possible for the “prev” node to not have the code  corresponding to the “type” of the incoming packet? Explain why. 

Yes, each router only has a limited size of soft store, the code might be discarded from its cache because its cache eviction policies. 

3. [2 points] Given that the active store uses LRU to replace items  from it, why would the “prev” node NOT have the code corresponding  to the “type” field? 

In a very intense network, the request to `prev` node might get delayed, and the code gets evicted before the request arrives.

4. [2 points] How is this situation handled in Active Networks? Why? 

The router will drop the packet if it can't find the code in its own cache or the prev node's cache. We rely on higher level protocol to handle the situation, e.g. re-transmit the packet.

## Distributed Objects and Middleware 

### V. Spring OS

A. [2 points] What purpose does the memory object abstraction serve in  the virtual memory subsystem of the Spring Kernel? 

- Memory object abstraction allows multiple memory regions to **share the same memory objects**.
- It also allows the virtual memory manager to **handle various types of backing storage for memory regions**, the virtual memory can be associated with backing files or swap space on disk, etc.

B. [2 points] Your co-worker argues that Spring Kernel’s memory  management does not offer any extensibility features. How would you  counter that argument? 

- VMM enables extensibility by using **memory object as an abstraction layer**, which allows virtual memory regions to be associated with various backing storage. 
- By using **external pagers** for managing the memory objects, it allows implementing different policies and algorithms for memory management.

### VI. EJB 

A. [6 points] You have a startup to implement a portal for airline  reservations. The clients come to you over an insecure wide-area  network. These are the objectives which are your “secret sauce” for  the startup:  

• You want to exploit parallelism across independent client request • You want to exploit parallelism within each client request  

• You want to protect your business logic from being exposed to the  wide-area Internet  

You are planning to use EJB for meeting these objectives. Your N-tier  solution has a Web container, an EJB container, and a Database server.  To meet the design objectives: 

1. [2 points] What functionalities would you put into the Web container  (that interfaces with the client browsers)?  

3. [4 points] What functionalities would you put into the EJB  container? Justify

There are two components we need to allocate: **presentation logic**, **business logic**. The entity bean can be separated from the business logic to get better performance & scalability.  
  
In this question, we can put the presentation logic into web container to have parallelism across independent client requests. And put business logic into the EJB container for protection to the business logic.  
  
We also need to separate the **Entity Bean** with the business logic so the requests within a client can be executed in parallel.

### VII. Java RMI 

A. [4 points] Java RMI evolved from the Spring Subcontract mechanism.  Name one similarity and one difference in the implementation of the  two systems. 

S: Both use interfaces to hide the implementation and communication details
D: RMI exploits the semantics of JAVA for marshalling and unmarshalling while subcontract use IDL to be language independent.

B. [2 points] Java allows object references to be passed as parameters  during object invocation. What is the difference in parameter  passing (when a local object reference is passed as a 
parameter)  while invoking a remote object using Java RMI? 

The difference is, the passing machanims for remote object is value/result, meaning a copy of the object is sent to the invoked method. In contrast, local objects pass a pure reference.

## Distributed Subsystems 

### VIII. GMS 

A. [2 points] Is it possible for a page X to be present in the "local"  part of two nodes N1 and N2 at the same time? If yes, explain how. 

Yes, the pages in local can be shared among multiple nodes. When it happens, the page will be copied over to the others' local for accessing.

B. [4 points] N1 faults on page X; N1's global part is empty; N2 has  the oldest page in the entire cluster in its global part; the missing page X is not in cluster memory. List the steps that will  ensue to service this page fault. 

1. N1 sends its LRU page to N2's global part
2. N2 swap out its LRU page and store the page from N1 
3. N1 bring in the page X from disk into its local memory.

C. [8 points] Assume that we have a set of Nodes N1, N2 and N3 in a  Global Memory System. The previous epoch of the geriatrics algorithm  has just ended. Now each of the nodes send age information for each  of their Local and Global pages to the initiator. The age  information sent by each node is shown below: 

Node N1: [LP1: 5, LP2: 7, LP3: 4, GP1: 11, GP2: 2] 

Node N2: [LP1: 1, LP2: 8, GP1: 3, GP2: 3, GP3: 9] 

Node N3: [LP1: 13, LP2: 15, LP3: 4, LP4: 1, LP5: 10] 

The integers corresponding to each page denote its age (a page with  age 10 is older than a page with age 5) 

We choose the parameter for Max Page replacement M = 6 (assume that  the parameter T for epoch duration does not play a role here)

1. [6 points] List down the response sent by the initiator to each  of the nodes while clearly stating what each section of the  response means. [Hint: each “weight” field in the response must  be denoted as a percentage value or as a ratio] 

The oldest pages are 15, 13, 11, 10, 9, 8

{MinAge 8, (W1 = 1/6, W2 = 2/6, W3 = 3/6)}

3. [2 point] Which node is selected as the initiator in the next  epoch? Why? 

N3, because it has the highest weight, hence it is the least active node.

### IX. DSM

A. [6 points] Consider a page-based software DSM system that implements  a single-writer multiple-reader coherence protocol. A process P on  Node N1 wants to write to page X. The page X is present in N1 but  it is marked read-only. Node N3 is the owner of page X which is  currently read-shared by nodes N1, N2, and N3. List the steps  involved in handling this situation to allow process P to be able to  write to page X. 

1. When process P on Node N1 attempts to write to the page X, a page fault occurs. The DSM software communicates with the OS to handle the page fault.
2. The DSM software on N1 determines the current owner of the page X which is N3.
3. N1 send a write permission request to N3.
4. N3 send invalidation messages to the nodes that have read-shared copies.
5. N2 and N3 acknowledge the invalidation requests.
6. N3 update the page X as write-exclusive for N1 and inform N1.
7. N1 acknowledge the update and continue the work of process P. 

### X. DFS 

A. [4 points] Consider the xFS file system.  
- Node Nf is the manager node for a file F1 
- Assume that coherence is maintained at the granularity of individual  files 
- F1 is currently read-shared by nodes N1, N2, and N3 

The following events happen: 

- Time T1: Node N1 attempts to write to file Nf 
- Time T2: Node N2 attempts to read the file Nf 

1. [2 points] List the actions that would take place at time T1 

1. N1 send a request to Nf the metadata manager for write access to F1,
2. Nf lookup the metadata and find the N1, N2, and N2 are sharing the file. It sends invalidation messages to N2 and N3.
3. Upon receiving the acknowledgements, Nf update cache consistency information to indicate the new owner and give write permission to N1.
4. Once N1 owns the file, it will proceed with writing to file F1.

2. [2 points] List the actions that would take place at time T2.

1. N2 send read access request to Nf
2. Nf check the status of file F1, and revoke the ownership of N1
3. N1 stopped writing and flush the changes to storage.
4. N1 forward the data to the new client for N2.
5. N2 proceeds with read to the file F1.

 B. [2 points]  Why do file systems procrastinate writing a file to stable storage as  soon as the process that is doing the write closes the file? 
 
To improve disk I/O and solve the small write problem

C. [2 points] In xFS, what purpose does the “log segment” data structure of the file  system serve? 

Log segment is an append-only data structure, which improves write performance and allow more efficient, continuous disk access. It also minimizes disk seek operations and provide better write throughput.

D. [2 points] Distinguish between static and dynamic metadata  management.

Static: metadata allocation and distribution are predetermined. It simplifies metadata management and lookup. But potentially, it has load imbalance and limited scalability problem.

Dynamic: metadata can be reassigned to different nodes based on factors such as load, access patterns, or system changes. It offers better load balancing, and better scalability. But also introduces complexities in metadata lookup and management.

## Missing

L5e
L6a nucleus 
L7a Data Structures
L7b eager RC vs lazy RC
