**OMSCS 6210 Spring 2023 Test 2 (120 min Canvas Quiz) 


L5c not on the list

L6a nucleus 

L7a Data Structures

L7b

Distributed Systems 

I. Lamport’s Logical Clock 

A. [2 points] Lamport’s logical clock is an intellectually appealing  strategy for maintaining the state of communicating processes in a  distributed system. What is deficient about logical clocks that  necessitates the physical clock formalism by Lamport in the same  paper? 

B. [4 points] Assume a system where clocks on nodes do not drift and  the network communication time is constant. Do we still need a  Lamport’s clock to determine “happened before” relations? Explain. 

II. Lamport’s ME Algorithm 

A. [5 points] Construct a simple ordering of events involving two  processes (P1 and P2) where Lamport’s algorithm violates mutual  exclusion, where P2 acquires mutex when it has already been acquired  by P1. 

Give your answer in the form of a sequence of one of the following  events. Show the state of the queues at P1 and P2 wherever  necessary, and clearly indicate which messages were delivered out of  order. 

• SEND LOCK/ACK/UNLOCK P1 -> P2 (P1 sends lock/ack/unlock to P2) 
• RECV LOCK/ACK/UNLOCK P1 -> P2 (P2 receives lock/ack/unlock  sent by P1) 
• ACQUIRE P1 (P1 acquires lock) 

--
SEND LOCK P1 -> P2 
SEND LOCK P2 -> P1

RECV LOCK P1 -> P2 
RECV LOCK P2 -> P1

SEND ACK P2 -> P1
SEND ACK P1 -> P2

ACQUIRE P1
SEND UNLOCK P1 -> P2
ACQUIRE P2
SEND UNLOCK P1 -> P2


B. [3 points] Construct a simple example of a sequence of events involving two processes P1 and P2, where “progress” is violated,  that is, in a situation where the mutex previously held by P1 has  been released, but P2 is not able to acquire it. 

Use the format shown in part (A) for the sequence of events, and  clearly indicate which message was lost. 

C. [2 points] The correctness of the basic Lamport's ME algorithm  depends on no message loss. You want to relax this requirement and  yet assure correctness. How would you do it? 

D. [2 points] Your co-worker asserts that for the correctness of the  basic Lamport's ME algorithm, messages from a given process P1 to  all other processes in the entire distributed system must arrive in  the order in which they are sent from P1. Is she right? You should  justify your answer with an explanation.

III. Latency Reduction in RPC 

A. [2 points] Thekkath and Levy suggest using a shared descriptor  between the client stub and the kernel for marshalling arguments  during an RPC call. Your friend argues that this does not result in  reducing the copying overhead of an RPC call. How would you counter  her argument? 

B. [4 points] Consider the following control transfers involved in an  RPC call. 

![](https://lh4.googleusercontent.com/jV3e22BqOf9vlb9zpw7dSCxlyxUhVGvIkDhEvjwJ5j_rBiFMfIa_CEIRpby2HVGaXsklsmlODOOxHNsXh1VSEwR6seJYUSmOOc2OumJ30RgGynJJ4yE4H0en-dmH-aQFSBMXzmTElvqruHHcQM-9SbY)

Out of these, identify the ones that are in the critical path. Why are  the identified calls considered in the critical path while others are  not? 

C. [4 points] You have designed an RPC system which has the following  parameters: 

• T: Message transmission time in either direction for sending the  arguments of the call or receiving the results (includes protocol  processing, time on the wire, and interrupt processing)  

• CSc = 3T: Context switch time at the client node 

• CSs= T: Context switch time at the server node 

You notice from the logs that the server procedure execution time is  bimodal: it takes T units of time mostly but occasionally 20T units  of time. 

How would you optimize the latency for RPC calls for this client server interaction? 

IV. Active Networks 

A. In an Active Network, we expect the intermediate routers to execute  code by looking at the “type” field of the capsule present in the  incoming packet. For a “type” that it has not seen before, it  requests the code from the node present in the “prev” field.

1. [2 points] Is it possible for the “prev” node to not have the code  corresponding to the “type” of the incoming packet? Explain why. 

2. [2 points] Given that the active store uses LRU to replace items  from it, why would the “prev” node NOT have the code corresponding  to the “type” field? 

3. [2 points] How is this situation handled in Active Networks? Why? 

Distributed Objects and Middleware 

V. Spring OS 

A. [2 points] What purpose does the memory object abstraction serve in  the virtual memory subsystem of the Spring Kernel? 

B. [2 points] Your co-worker argues that Spring Kernel’s memory  management does not offer any extensibility features. How would you  counter that argument? 

- Though the Virtual Machine Manager(VMM) in the Spring OS is responsible for actions such as mapping, sharing, protection and caching of local memory, they rely on external paging objects for paging and coherency operations.  
- This functionality of paging and coherency can be implemented as a service outside the microkernel, thus offering extensibility.

VI. EJB 

A. [6 points] You have a startup to implement a portal for airline  reservations. The clients come to you over an insecure wide-area  network. These are the objectives which are your “secret sauce” for  the startup:  

• You want to exploit parallelism across independent client request • You want to exploit parallelism within each client request  

• You want to protect your business logic from being exposed to the  wide-area Internet  

You are planning to use EJB for meeting these objectives. Your N-tier  solution has a Web container, an EJB container, and a Database server.  To meet the design objectives: 

1. [2 points] What functionalities would you put into the Web container  (that interfaces with the client browsers)?  

2. [4 points] What functionalities would you put into the EJB  container? Justify

There are two components we need to allocate: presentation logic, business logic. The entity bean can be separated from the business logic to get better performance & scalability.  
  
In this question, we can put the presentation logic into web container to have parallelism across independent client requests. And put business logic into the EJB container for protection to the business logic.  
  
We also need to separate the Entity Bean with the business logic so the requests within a client can be executed in parallel.

VII. Java RMI 

A. [4 points] Java RMI evolved from the Spring Subcontract mechanism.  Name one similarity and one difference in the implementation of the  two systems. 

S: Both use interfaces to hide the implementation and communication details
D: RMI exploits the semantics of JAVA for marshalling and unmarshalling while subcontract use IDL to be language indenpendent.

B. [2 points] Java allows object references to be passed as parameters  during object invocation. What is the difference in parameter  passing (when a local object reference is passed as a 
parameter)  while invoking a remote object using Java RMI? 

The difference is, the passing machanims for remote object is value/result, meaning a copy of the object is sent to the invoked method. In contrast, local objects pass a pure reference.

Distributed Subsystems 

VIII. GMS 

A. [2 points] Is it possible for a page X to be present in the "local"  part of two nodes N1 and N2 at the same time? If yes, explain how. 

Yes, the pages in local can be shared among multiple nodes. When it happens, the page will be copied over to the others' local for accessing.

B. [4 points] N1 faults on page X; N1's global part is empty; N2 has  the oldest page in the entire cluster in its global part; the missing page X is not in cluster memory. List the steps that will  ensue to service this page fault. 

1. N1 expend its local memory.
2. N1 bring the page X from disk into its local memory.

C. [8 points] Assume that we have a set of Nodes N1, N2 and N3 in a  Global Memory System. The previous epoch of the geriatrics algorithm  has just ended. Now each of the nodes send age information for each  of their Local and Global pages to the initiator. The age  information sent by each node is shown below: 

Node N1: [LP1: 5, LP2: 7, LP3: 4, GP1: 11, GP2: 2] 

Node N2: [LP1: 1, LP2: 8, GP1: 3, GP2: 3, GP3: 9] 

Node N3: [LP1: 13, LP2: 15, LP3: 4, LP4: 1, LP5: 10] 

The integers corresponding to each page denote its age (a page with  age 10 is older than a page with age 5) 

We choose the parameter for Max Page replacement M = 6 (assume that  the parameter T for epoch duration does not play a role here)

1. [6 points] List down the response sent by the initiator to each  of the nodes while clearly stating what each section of the  response means. [Hint: each “weight” field in the response must  be denoted as a percentage value or as a ratio] 

oldest pages are 15, 13, 11, 10, 9, 8

{MinAge 8, (W1 = 1/6, W2 = 2/6, W3 = 3/6)}

3. [2 point] Which node is selected as the initiator in the next  epoch? Why? 

N3, because it has the highest weight, hense least active node.

IX. DSM 

A. [6 points] Consider a page-based software DSM system that implements  a single-writer multiple-reader coherence protocol. A process P on  Node N1 wants to write to page X. The page X is present in N1 but  it is marked read-only. Node N3 is the owner of page X which is  currently read-shared by nodes N1, N2, and N3. List the steps  involved in handling this situation to allow process P to be able to  write to page X. 

1. When process P on Node N1 attempts to write to page X, a page fault will be triggered.
2. N1 sends a write request to N3 for write permission to page X.
3. N3 sends invalidation messages to N2 to invalidate shared copies, and invalidate its own copy.
4. N2 acknowledges the message.
5. N3 update permission of page X to read-write for N1.
6. Process P resume execution.

X. DFS 

A. [4 points] Consider the xFS file system.  

- Node Nf is the manager node for a file F1 

- Assume that coherence is maintained at the granularity of individual  files 

- F1 is currently read-shared by nodes N1, N2, and N3 

The following events happen: 

- Time T1: Node N1 attempts to write to file Nf 

- Time T2: Node N2 attempts to read the file Nf 

1. [2 points] List the actions that would take place at time T1 2. [2 points] List the actions that would take place at time T2.

 B. [2 points]  

Why do file systems procrastinate writing a file to stable storage as  soon as the process that is doing the write closes the file? 

C. [2 points] 

In xFS, what purpose does the “log segment” data structure of the file  system serve? 

D. [2 points] Distinguish between static and dynamic metadata  management.**