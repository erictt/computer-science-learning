# Lesson 5 - Distributed System


## L05a. Definitions

### What is a Distributed System?

* A Distributed System is a collection of **nodes connected** by a LAN/WAN.
* No physical memory is shared between nodes on a Distributed System. Nodes communicate by sending messages on the network.
* The **communication time/messaging time**  is much larger than the **Event Computation Time** (the time a node takes to complete a process).
    * ![](https://i.imgur.com/lXrR5di.jpg)
    * NOTE how it's calculated. $t_m$ is a->c. $t_e$ is a-b.
* Formal definition from Lamport: A system is distributable if the **message transmission time** $𝑇_𝑚$ is not negligible(可忽略不计的) to the time between events in a **single process** $𝑇_𝑒$.
    

### Distributed System Events Ordering

* Beliefs:
    - Processes are sequential.
    - Send happens before Receive.
* Relationships between events:
    - **Happened Before**: If 𝑎 happened before 𝑏 (𝑎 → 𝑏), then it's either:
        1. 𝑎 is located textually before 𝑏 in the same process.
        2. 𝑎 and 𝑏 are in different processes, and there's a communication event that connects 𝑎 and 𝑏. Transitivity: if 𝑎 → 𝑏 and 𝑏 → 𝑐 then 𝑎 → 𝑐
    - **Concurrent events**: If 𝑎 and 𝑏 are in two different processes and no communication event connects them, then we say that they're concurrent 𝑎 ‖ 𝑏. This is why the “Happened Before” relationship cannot give a complete picture of the system events.

## L05b. Lamport Clocks

### Introduction

* Each node in a distributed system knows:
    - Its own events.
    - Its communication events.
* Lamport's logical clocks:
    - The idea here is that we need to associate a time stamp with each event in the entire distributed system.
    - We'll have a **local clock (counter)** attached to each process. The time stamp would be the counter value.
    - The counter value is **monotonically increasing**.
    - The **time stamp** of communication events will be **either** the counter value of the **sender** process or the **receiver** process **whichever greater**.
* ![](https://i.imgur.com/Lf3VZkE.jpg)
    * In condition 2, d has to be 3, event the previous counter in the process is 0. because the value has to be max counter of incoming message or the counter from local process.

### Logical Clock Conditions

* If we have two events 𝑎 and 𝑏 in the **same process** 𝑖, then $𝐶_𝑖(𝑎) < 𝐶_𝑖(𝑏)$.
* If we have a communication event between event 𝑎 on process 𝑖 and event 𝑑 on process $j$ then:
    - $𝐶_𝑎 < 𝐶_𝑗(𝑑)$
    - $C_j(a) = \max(𝐶_𝑗(𝑎)++ , 𝐶_𝑗)$
* If we have two **concurrent** events 𝑏 and 𝑑, then the **time stamps** will be **arbitrary**.
* This means that Lamport Clocks gives us a **partial order** of all the events happening on the distributed system.
* $c(x) < c(y) \ne x → y$ 

### Lamport Total Order

* If we have two events $𝑎$ process $𝑖$ and $𝑏$ on process $j$, and we can to assert that $𝑎$ is totally ordered ahead of $𝑏$: $(𝑎 ⇒ 𝑏)$ iff
    - $𝐶_𝑖(𝑎) < 𝐶_j(𝑑)$ or
    - $𝐶_𝑖(𝑎) = 𝐶_𝑗(𝑑)$ and $𝑃_𝑖 ≪ 𝑃_j$, where (`≪`) is and arbitrary well-known condition to break the tie (e.g. the greater the process ID the higher the order). 
* Once we get the total order, time stamps are meaningless.

### Distributed Mutual Exclusion (ME) Lock Algorithm

* In a distributed system, we don't have a shared memory to facilitate lock implementation. So we'll use Lamport Clocks to implement a lock.
* Every process will have a queue data structure ordered by the “**Happened Before**” relationship.
* Any process that needs to **acquire the lock** will send a message to all the other processes with its time stamp as the request time.
* Each other process will put the request in its queue, and then acknowledges the request.
* If we have a tie (Two processes sent the same time stamp), we break it by giving priority to the process with higher ID.
* **A process knows that it has the lock if**:
    - Its request is **on top of the queue**.
    - It has **already received acknowledges** from the other processes; or all lock requests from other nodes are later than mine.
    - NOTE that this is being done locally.
* Whenever a process wants to release a lock, it **sends an unlock message** to all other processes.
* When the other processes receive the unlock message, they remove the **process entry** from their queues.
* The algorithm assumptions:
    - Message arrive in order.
    - There's no message loss.
    - The queues are totally ordered.
* Message complexity base on the assumptions above $\text{𝑇𝑜𝑡𝑎𝑙} = 3(𝑁 − 1)$:
    - $𝑁 − 1$ request messages.
    - $𝑁 − 1$ acknowledge messages.
    - $𝑁 − 1$ unlock messages.
* Can we do better?
    - If a process $𝑖$ lock request precedes another process $𝑗$ request in the queue, we can defer the acknowledgement of $𝑖$ and use the unlock message itself as an acknowledgement for $𝑗$.
        - combine with unlock => $2(N-1)$

### Lamport Physical Clock:

* In real world scenarios, the logical clock might be drifting of the real time due to anomalies in the logical clocks.
    - ![](https://i.imgur.com/FLPW4h0.jpg)

* We can say the event $𝑎$ happened before event $𝑏$ in real time $(a \mapsto b)$ if:
    - $C_i(a) < C_j(b)$
    - Physical clock conditions:
        1. PC1: Bound on individual clock drift: $$(\frac{dC_i(t)}{dt} - 1) < \textcolor{red}{k}\ \ \ \ \lor i\ ; (\textcolor{red}{k} \ll 1)$$
        2. PC2: Bound on mutual drift: $$\lor i, j: C_i(t) - C_j(t) < \textcolor{red}{\epsilon}$$
* IPC time and clock drift:
    * <img src="https://i.imgur.com/WYNRswF.jpg" style="width: 400px" />
    * Terms: 
        * mutual clock drift $\epsilon$, 
            * The time difference between the time i think and the time the other think.
        * individual clock drift $k$, 
            * Individual clock drift is what my clock is reading at any point of time and how far off is it from real time.
        * the interprocess communication time $\mu$.
    * Let $\mu$ be the lower bound on IPC, to avoid anomalies when: $a_i\ \text{on}\ P_i \mapsto \textcolor{green}{a_b\ \text{on}\ P_j}$
        1. $C_i(t + \mu) - \textcolor{green}{C_j(t)} > 0$
            - the parity between the interprocess communication time is less than $\mu$
        2. $c_i(t + \mu) - C_j(t) > \textcolor{red}{\mu (1-k)}$
            - individual clock drift is really small comparing to $\mu$
            - difference equation formulation of PC1
    * Using equation 1 and 2, and bound $\epsilon$ on mutual drift: $\textcolor{red}{\mu \ge \epsilon / (1 - k)}$ to avoid anomalies.
    * Real world scenario, target for interprocess communication time > mutual clock drift
        * ![](https://i.imgur.com/D1GfmR9.jpg)
            * $\mu < \epsilon$
        * ![](https://i.imgur.com/ptnh3Hf.jpg)
            * $\mu > \epsilon$

## L05c. Latency Limits

### Introduction

* Network communication is a key factor in determining the performance of a distributed system. Hence, the OS has to reduce the latency for the network services.
* **Latency** vs **Throughput**:
    - Latency is the elapsed time for an event.
    - Throughput is the number of events that can be executed per unit time.
    - Higher bandwidth means higher throughput but doesn't necessarily result in lower latency.
* Overhead on RPC:
    - **Hardware overhead**: How the network controller is interfaced to the CPU. There are two types of network controllers:
        1. DMA(direct memory access): The network controller moves bits of the message from system memory into its private buffer without intervention of the CPU.
        2. The CPU does program I/O to move the bits from the memory into the buffer of the network controller.
            - <img src="https://i.imgur.com/IctbBQw.jpg" style="width: 400px" />
    - **Software overhead**: What the OS takes to prepare the message for transmission.

### RPC Latency

<img src="https://i.imgur.com/mmW40zV.jpg" style="width: 400px" />

* These are the steps needed to perform an RPC:
    1. **Client call**: Setting up the arguments for the procedure call, and makes the call to the kernel. The kernel validates the call, marshals the arguments into a network packet and sets up the controller to do the transmission.
    2. **Controller**: The controller moves the message to its own buffer, and then put it on the bus.
    3. **Time on wire**: Depends on the available bandwidth.
    4. **Interrupt handling**: The message arrives to the server as an interrupt. The **OS** moves the message to the server's controller buffer, and then to the node's memory.
    5. **Server setup to execute the call**: Locating and dispatching the server procedure, unmarshal the arguments from the network packet.
    6. **Server execution**: The server executes the call and sends the results to the client in the same way described above.
    7. **Client setup to receive the results and restart execution**.
* Source of overhead in RPC:
    * Marshaling & Data copying
    * Control transfer
    * Protocol processing

#### Marshaling and Data Copying

* Making an RPC call involves three data copies:
    * ![](https://i.imgur.com/g24aKmd.jpg)
    - First copy: The client stub takes the arguments of the RPC and converts it to an RPC message.
    - Second copy: The kernel has to copy the RPC message from the memory space it resides on to its own buffer.
    - Third copy: The network controller will then copy the RPC message from the kernel buffer to its internal buffer using DMA. This is an unavoidable hardware action.
* The copying overhead is the biggest source of overhead for RPC latency.
* To reduce the number of copies, one of two approaches can be used:
    - Eliminate the stub overhead by **moving the stub from the user space to the kernel** and marshaling directly into the kernel buffer.
    - **Leave the stub in the user space**, but have <u>a shared descriptor between the client stub and the kernel</u>. This descriptor provides information to the kernel about the layout of the arguments on the stack. The kernel these information to create a similar layout in on its space.

#### Control Transfer

![](https://i.imgur.com/BaMWS14.jpg)

* This includes the multiple **context switches** that have to happen to execute an RPC call:
    1. When the client makes an RPC call, it blocks till it receives the results. The kernel makes a context switch to serve another process. This is important to make sure that the client node is not underutilized.
    2. When the call arrives to the server's side, it has to make a context switch from the process it's currently serving to the incoming interrupt (RPC call). This is essentially to the RPC latency.
    3. After executing the call, the server will switch to another process.
    4. When the results arrives at the client's side, the kernel has to switch to serve that client. This is essentially to the RPC latency.
* Only context switch #2 and #4 are critical to the RPC call itself.
* #1 is overlapped with the network communication, meaning it can be done during the communication time. Same as #3. These two context switches are meant to keep the CPU utilized.
    * We can reduce these switches to two by overlapping context switch #1 with #2, and #3 with #4.
* Can we reduce the context switch to 1? if we know that the RPC call will not take much time, then we can spin waiting for the RPC results and don't do context switch on #1 and #4. Then the only context switch we do is #2 for the server to switch to the process to handle the task.

#### Protocol Processing

* Given that we have a **reliable LAN**, the following approaches can be used to reduce latency in transport:
    - Eliminate low level **ACKs**.
    - Using **hardware checksum** for packet integrity.
    - **No client side buffering**. Since the client is blocked, it can resend the call if the message is lost.
    - **Overlap** server side **buffering** with result transmission, and get it out of the critical path of the latency for protocol processing.

## L05d. Active Networks

### Introduction

Note from Computer Network course: https://cs.ericyy.me/cs6250/week-7-software-defined-networking-part-1/index.html#1-active-networks

![](https://i.imgur.com/x6ApgQo.jpg)

* The primary issue once a packet leaves a node in a distributed system is to route the packet reliably and quickly to its destination.
* The intermediate routers have routing tables. The routing table determine, given the packet destination, what the next hub for this packet is. This is done by a simple table lookup.
* We can change this simple lookup to a code execution on the router. This is called **Active Networks**.
* The packets will carry the payload and code to be executed by the router to determine what the next step for this packet is.
* The idea is to make the nodes on the network active by making them look into the message and figure out what to do with it.

### How to implement Active Networks

![](https://i.imgur.com/eFU4WUc.jpg)

* The OS provides **Quality of Service (QoS) APIs** to the application. These APIs will be used by the application to give the OS an idea about the nature of the message.
* The OS uses QoS to synthesize code and creates the packet (IP-header + code + payload) that will be handed to the internet.
* There're two problems with this approach:
    - Changing the protocol stack to handle active networks is not easy.
    - We cannot expect that every node on the internet will be able to execute the code I'm sending.

### Active Node Transfer System (ANTS) Toolkit

![](https://i.imgur.com/0rdsixp.jpg)

* The ANTS Toolkit is an application level package that takes the payload and QoS from the application and create a capsule (ANTS header + payload) that is passed to the protocol stack.
* The protocol stack will create the packet by adding an IP header to the capsule.
* If the receiving node is a normal one, it will just use the IP header to decide where to send the packet.
* If the receiving node is Active, it will process the ANTS header to decide if the packet has to be demultiplexed and sent to different routes.
* Another addition is, with ANTS Toolkit, the core IP network will remain unchanged, and the Active Nodes will **only be added at the edges of the network**.

### ANTS Capsules

![](https://i.imgur.com/IiYNvFF.jpg)

* ANTS header consists of:
    - **Type field**: An MD5 hash of the code to be executed.
    - **Prev field**: The identity of the up-stream node that successfully executed this capsule.
* ANTS APIs:
    - APIs for routing.
    - APIs for manipulating soft store(a k-v store): Soft store is storage that is available in every routing node for personalizing the network flow with respect to the type field. <u>This is the place where we store the code itself</u>.
    - APIs for querying the node to get information about the node and the network.
* Characteristics of the routing program:
    - Easy to program.
    - Easy to debug and maintain.
    - Very quick.

#### Capsule Implementation

![](https://i.imgur.com/w1hdBEI.jpg)

* When a node receives a capsule, one of two possibilities can happen:
    1. If this node had received capsules of this type before:
        - The node probably already has the capsule's code in its soft store by checking the type field(fingerprint).
        - The node will retrieve the code, execute it and proceed.
    2. If this is the first time the node receives a capsule of this type:
        - The node checks the **prev field** and send a **message to the previous node** asking for the code.
        - The previous node retrieves the code from its soft store and sends it to the receiving node.
        - The receiving node computes the fingerprint for the code and **compares it with the type field** to make sure it's the right code.
        - The receiving node executes that code, **store** it in its soft store and proceeds.
        - If the code is not present in the soft store of the previous node, the current node will **drop the capsule**.

### Potential apps

* Protocol independent multicast
* Reliable multicast
* Congestion notification
* Private IP(PIP)
* Anycast

### Pros and Cons of Active Networks

- Pro
    - Flexibility from app perspective
- Cons
    - Protection threats
        - ANTS runtime safety => Java sandboxing
        - Code spoofing => robust fingerprint
        - software integrity => restricted API
    - Resource Management threats
        - At each node => restricted API
        - Flooding the network => Internet already susceptible

The roadblocks to the Active Network vision:

- Need buy in from the router vendors
- ANTS software routing cannot match throughput needed in Internet core.

### Feasibility

- Router makers loath to opening up the network => only feasible at the edge of the network
- Software routing cannot match hardware routing => only feasible at the edge of the network
- Social + psychological reasons
    - hard for user community to accept arbitrary code executing in the public routing fabric

## L05e. Systems from Components

### Introduction

* Hardware design uses a component-based approach to build large and complex hardware systems.
* Using the same approach to build software, reusing software components, will facilitate:
    - Easy testing and optimization.
    - Easy system extension through the addition and deletion of components.
* Possible issues:
    - Might affect the efficiency and performance due to the additional function calls.
    - Could lead to loss of locality.
    - Could lead to unnecessary redundancies.

### Design Cycle

![](https://i.imgur.com/g5z3o54.jpg)

* **Specification**: **IOA**(I/O automata) is used to express abstract specifications of the system at the level of individual components.
    - C-like syntax.
    - Includes a composition operator.
* **Code**: **OCMAL** programming language is used to convert the specification to code that can be executed.
    - **Object** oriented.
    - **Efficient** code similar to C.
    - Good complement to IOA.
* **Optimization**: **NuPrl** framework is used to optimize OCAML code to prepare it for deployment.

### From Specifications to Implementation

![](https://i.imgur.com/LH32b1O.jpg)

* Abstract Behavioral Specifications:
    - Describes the functionality of the sub-systems in terms of requirements using IOA.
    - IOA facilitate proofing of the Abstract Behavioral Specifications against the required properties.
* Concrete Behavioral Specifications: Produced by refining the Abstract Behavioral Specifications.
* Implementation: Translating the Concrete Behavioral Specifications into code using OCAML.

### From Implementation to Optimization

* The unoptimized OCAML code will be converted to unoptimized NuPrl code.
* The unoptimized NuPrl code will be converted to an optimized NuPrl code using the Theorem Prover Framework.
* The optimized NuPrl code will be converted to an optimized OCAML code.

![](https://i.imgur.com/t9MclNm.jpg)

### Synthesizing a TCP-IP Stack

* Specify the **Abstract** Behavioral Specifications and produce the **Concrete** Behavioral Specifications.
* Using an **ensemble suite of micro-protocols** to produce the unoptimized OCAML code.
    * e.g. TCP/IP: flow control, sliding window, encryption, scatter/gather, etc.
* Sources of possible optimization:
    - Explicit memory management instead of implicit garbage collection.
    - Avoid marshaling/unmarshaling across layers.
    - Buffering in parallel with transmission.
    - Header compression.
    - Locality enhancement for common code sequences.
* Using NuPrl:
    - **Static optimization**: A NuPrl expert and an OCAML expert goes through the protocol stack layer by layer and identify optimization possibilities.
    - **Dynamic optimization**: Collapsing multiple layers, if possible, to avoid latency.
        - This is achieved by deriving **common case predicates**(CCP) from the state of the protocol using conditional statements.
        - If the CCP is satisfied, the protocol layers will be bypassed by a generated code for this CCP.
    - ![](https://i.imgur.com/MaDojhz.jpg)

![](https://i.imgur.com/XTCSOpi.jpg)


|   |  2 |  3 |  4 |  5 |  6 |  7 |  8 |
|---|----|----|----|----|----|----|----|
| 2 |  4 |  6 |  8 | 10 | 12 | 14 | 16 |
| 3 |  6 |  9 | 12 | 15 | 18 | 21 | 24 |
| 4 |  8 | 12 | 16 | 20 | 24 | 28 | 32 |
| 5 | 10 | 15 | 20 | 25 | 30 | 35 | 40 |
| 6 | 12 | 18 | 24 | 30 | 36 | 42 | 48 |
| 7 | 14 | 21 | 28 | 35 | 42 | 49 | 56 |
| 8 | 16 | 24 | 32 | 40 | 48 | 56 | 64 |
| 9 | 18 | 27 | 36 | 45 | 54 | 63 | 72 |
|10 | 20 | 30 | 40 | 50 | 60 | 70 | 80 |
|11 | 22 | 33 | 44 | 55 | 66 | 77 | 88 |
|12 | 24 | 36 | 48 | 60 | 72 | 84 | 96 |
