# Week 5 - Router Design and Algorithms Part 1

<!-- toc -->
----

## What's Inside a Router?

* The main job of a router is to **implement the forwarding plane functions and the control plane functions**.
* **Forwarding (or switching) function** on the data plane:
    * This is the router’s action to transfer a packet from an input link interface to the appropriate output link interface. Forwarding occurs at very **short timescales** (typically a few nanoseconds) and is typically **implemented in hardware**.     
    * <img src="https://i.imgur.com/MqPYOfB.png" style="width: 600px" />

    * <img src="https://i.imgur.com/TCJCRcx.png" style="width: 600px" />
* Input ports:
    * The input ports perform several functionalities.
        1. If we look at the figure from left to right, the first function is to physically terminate the incoming links to the router. 
        2. Second, the data link processing unit decapsulates the packets. 
        3. Finally, and most importantly, the input ports perform the lookup function. At this point, the input ports consult the forwarding table to ensure that each packet is forwarded to the appropriate output port through the switch fabric.
            * NOTE: Regardless of the routing protocol, **packet forwarding is based on the destination address alone**, no need for the source address.**[Quiz]**
* Switching fabric:
    * Simply put, the switching fabric moves the packets from input to output ports, and it makes the connections between the input and the output ports. There are three types of switching fabrics: memory, bus, and crossbar. 
* Output ports:
    * An important function of the output ports is to **receive and queue the packets** from the switching fabric and then send them over to the outgoing link.
* <img src="https://i.imgur.com/7Mihqg7.png" style="width: 600px" />
* Router’s control plane functions:
    * By control plane functions, we refer to implementing the **routing protocols**, maintaining the **routing tables**, computing the **forwarding table**. All these functions are implemented in software in the routing processor, or as we will see in the SDN chapter, these functions could be implemented by a remote controller.
    * <img src="https://i.imgur.com/lTIj39W.png" style="width: 600px" />

## Router Architecture

* <img src="https://i.imgur.com/vfsfnbO.png" style="width: 600px" />
* A router has input links and output links, and its main task is to switch a packet from an input link to the appropriate output link based on the destination address. We note that in this figure, the input/output links are shown separately but often they are put together. 

* Now let's look at what happens when a packet arrives at an input link. First, let's take a look at the **most time-sensitive tasks**: lookup, switching, and scheduling. 
* **Lookup**: When a packet arrives at the input link,  the router looks at the destination IP address and determines the output link by looking at the **forwarding table (or Forwarding Information Base or FIB)**. The FIB provides a mapping between destination prefixes and output links. 
    * The routers use **the longest prefix matching algorithms** to resolve any disambiguities. We will see these algorithms soon. Also, some routers offer a more specific and complex type of lookup, called packet classification, where the lookup is based on destination or source IP addresses, port, and other criteria.
* **Switching**: After lookup, the switching system takes over to transfer the packet from the input link to the output link. Modern fast routers use **crossbar switches** for this task. Although scheduling the switch (matching available inputs with outputs) is difficult because multiple inputs may want to send packets to the same output. 
* **Queuing**: After the packet has been switched to a specific output, it will need to be queued (if the link is congested). The queue may be as simple as **First-In-First-Out (FIFO)**, or it may be more **complex (e.g., weighted fair queuing)** to provide delay guarantees or fair bandwidth allocation.  

* Now, let's look at some less time-sensitive tasks that take place in the router. 

* **Header validation and checksum**: The router checks the packet's version number, decrements the time-to-live (TTL) field, and recalculates the header checksum. 
    * Note this happens on the Data plane[Quiz].
* **Route processing**: The routers build their forwarding tables using routing protocols such as RIP, OSPF, and BGP. **These protocols are implemented in the routing processors**. 
* **Protocol Processing**: The routers need to implement the following protocols to implement their functions:
    * **Simple Network Management Protocol (SNMP)** for a set of counters for remote inspection
    * **TCP and UDP** for remote communication with the router
    * **Internet Control Message Protocol (ICMP)** for sending error messages, e.g., when time-to-live (TTL) time is exceeded

## Different Types of Switching

* The switching fabric is the brain of the router, as it performs the main task to switch (or forward) the packets from an input port to an outport port. Let's look at the ways that this can be accomplished:
    * **Switching via memory**: Input/Output ports operate as I/O devices in an operating system, controlled by the routing processor. When an input port receives a packet, it sends **an interrupt** to the routing processor, and the packet is **copied to the processor's memory**. Then the processor extracts the destination address and **looks into the forward table** to **find the output port**, and finally, the packet is **copied into that output's port buffer**.
        * <img src="https://i.imgur.com/nmHwtcE.png" style="width: 600px" />

    * **Switching via bus**: In this case, the routing processor does not intervene as we saw the switching via memory. When an input port receives a new packet, it **puts an internal header** that designates the output port, and it s**ends the packet to the shared bus**. Then **all the output ports will receive the packet, but only the designated one will keep it**. When the packet arrives at the designated output port, the internal header is removed from the packet. **Only one packet** can **cross the bus** at a given time, so the **speed of the bus limits the speed of the router**. 
        * <img src="https://i.imgur.com/C66HMkK.png" style="width: 600px" />

    * **Switching via interconnection network**: A **crossbar switch** is an interconnection network that connects N input ports to N output ports using 2N buses. Horizontal buses meet the vertical buses at crosspoints controlled by the switching fabric. For example, let's suppose that a packet arrives at port A that will need to be forwarded to output port Y, the switching fabric closes the crosspoint where the two buses intersect so that port A can send the packets onto the bus, and then the packet can only be picked up by output port Y. **Crossbar network can carry multiple packets**[Quiz](Only this switching method) at the same time, **as long as they are using different input and output ports**. For example, packets can go from A-to-Y and B-to-X simultaneously. 
        * <img src="https://i.imgur.com/i3V2I9I.png" style="width: 600px" />

## Challenges that the router faces

* The fundamental problems that a router faces revolve around:
    1. **Bandwidth and Internet population scaling**: These scaling issues are caused by:
        * An increasing number of devices that connect to the Internet,
        * Increasing volumes of network traffic due to new applications, and
        * New technologies such as optical links that can accommodate higher volumes of traffic. 
    2. **Services at high speeds**: New applications require services such as protection against delays in the presence of congestion and protection during attacks or failures. But offering these services at very high speeds is a challenge for routers. 
* To understand why let’s look at the bottlenecks that routers face in more detail:
    * <img src="https://i.imgur.com/7bg6KKN.png" style="width: 600px" />
* **Longest prefix matching**: As we have seen in previous topics, routers need to look up a packet’s destination address to forward it. The increasing number of Internet hosts and networks has made it **impossible for routers to have explicit entries for all possible destinations**. So instead, routers group destinations into prefixes. But then, routers run into the problem of more complex algorithms for efficient longest prefix matching. 
* **Service differentiation**: Routers can also offer service differentiation which means different quality-of-service (or security guarantees) to different packets. In turn, this **requires the routers to classify packets based on more complex criteria beyond destination**. For example, they can include source or applications/services associated with the packet. 
* **Switching limitations**: As we have seen, a fundamental operation of routers is to switch packets from input ports to output ports. A way to deal with high-speed traffic is to **use parallelism by crossbar switching**. But at high speeds, this comes with its problems and limitations (e.g., head of line blocking).  
* **Bottlenecks about services**: Providing performance guarantees (quality of service) at high speeds is nontrivial, as is providing support for new services such as measurements or security guarantees.

### Prefix-Match Lookups

* The Internet continues to grow in terms of networks (AS numbers) and IP addresses. As a result, one of the challenges that a router faces is the scalability problem. One way to help with the scalability problem is to **“group” multiple IP addresses by the same prefix**. 
* different ways to denote prefix:
    1. **Dot decimal**
        * Example of the 16-bit prefix: 132.234
        * The binary form of the first octet: 10000100
        * Binary of the second octet: 11101010
        * The binary prefix of 132.234: 1000010011101010*
            * The * indicates wildcard character to say that the remaining bits do not matter.
    2. **Slash notation**
        * Standard notation: A/L (where A=Address, L=Length)
            * Example: 132.238.0.0/16
        * Here, 16 denotes that only the first 16 bits are relevant for prefixing.  
    3. **Masking**
        * We can use a mask instead of the prefix length. 
            * Example: The prefix 123.234.0.0/16 is written as 123.234.0.0 with a mask 255.255.0.0
        * The mask 255.255.0.0 denotes that only the first 16 bits are important. 

* What is the need for variable length prefixes?
    * In the earlier days of the Internet, we used an IP addressing model based on classes (fixed-length prefixes). With the rapid exhaustion of IP addresses, in 1993, the Classless Internet Domain Routing (CIDR) came into effect. CIDR essentially assigns IP addresses using arbitrary-length prefixes. CIDR has helped to decrease the router table size, but at the same time, it introduced us to a new problem: longest-matching-prefix lookup.
* Why do we need (better) lookup algorithms?
    * The table shows the consequence (inference) that motivates and impacts the design of prefix lookup algorithms for every observation. The four takeaway observations are:
        * Measurement studies on network traffic had shown a large number of concurrent flows of short duration. This already large number has only been increasing, and as a consequence, caching solutions will not work efficiently. 
        * The important element of any lookup operation is how fast it is done (lookup speed). A large part of the cost of computation for lookup is accessing memory.
        * An unstable routing protocol may adversely impact the update time in the table: add, delete or replace a prefix. Inefficient routing protocols increase this value up to additional milliseconds.
        * A vital trade-off is memory usage. We can use expensive fast memory (cache in software, SRAM in hardware) or cheaper but slower memory (e.g., DRAM, SDRAM).
        * <img src="https://i.imgur.com/j1ZijS8.png" style="width: 600px" />


## Unibit Tries

* To start our discussion on prefix matching algorithms, we will use an example prefix database with nine prefixes, as shown below.
    * <img src="https://i.imgur.com/JWDUCpL.png" style="width: 600px" />
* One of the simplest techniques for prefix lookup is the unibit trie. For the example database we have, the figure below shows a unibit trie: 
    * <img src="https://i.imgur.com/DitB6n2.png" style="width: 600px" />
* Every node has a 0 or 1 pointer. Starting with the root, 0-pointer points to a subtrie for all prefixes that begin with 0, and similarly, 1-pointer points to a subtrie for all prefixes that start with 1. Moving forward similarly, we construct more subtries by allocating the remaining bits of the prefix.
* When we do prefix matching, we follow the path from the root node down to the trie. So let’s take an example from the above table and see how we can do prefix matching in the unibit trie. For example:
    1. Assume we are doing the longest prefix match for P1=101* (from our prefix database). We start at the root node and trace a 1-pointer to the right, then a 0-pointer to the left, and then a 1-pointer to the right.
    2. For P7=100000*, we start at the root node and trace a 1-pointer to the right, then five 0-pointers on the left.
* These are the steps we follow to perform a prefix match:
    1. We begin the search for a longest prefix match by tracing the trie path.
    2. We continue the search until we fail (no match or an empty pointer)
    3. When our search fails, the last known successful prefix traced in the path is our match and our returned value.
* Two final notes on the unibit trie:
    1. If a prefix is a substring of another prefix, **the smaller string is stored in the path to the longer (more specific prefix)**. For example, P4 = 1* is a substring of P2 = 111*, and thus P4 is stored inside a node towards the path to P2.
    2. **One-way branches**. **There may be nodes that only contain one pointer**. For example, let’s consider the prefix P3 = 11001. After we match 110 we will be expecting to match 01. But in our prefix database, we don’t have any prefixes that share more than the first 3 bits with P3. So if we had such nodes represented in our trie, we would have nodes with only one pointer. The nodes with only one pointer each are called one-way branches. For efficiency, **we compress these one-way branches to a single text string with 2 bits (shown as node P9).**


## Multibit Tries

* Why do we need multibit tries?
    * While a **unibit trie** is very efficient and offers advantages such as fast lookup and easier updates, its most significant problem is the number of memory accesses required to perform a lookup. For 32 bit addresses, we can see that looking up the address in a unibit trie might require 32 memory accesses, in the worst case. Assuming a 60 nsec latency, the worst-case search time is 1.92 microseconds. This could be very inefficient in high-speed links. 
    * Instead, we can implement lookups using a stride. **The stride is the number of bits that we check at each step**[Quiz].  
    * So an alternative to unibit tries are the **multibit tries**. A multibit trie is a trie where each node has 2^k children, where k is the stride. Next, we will see that we can have two flavors of multibit tries: **fixed-length stride** tries and **variable-length stride** tries.
    * A multibit trie is shorter than a unibit trie representing the same prefix database and requires fewer memory accesses to perform a lookup.[Quiz]

### Prefix Expansion

* Consider a prefix such as 101* (length 3) and a stride length of 2 bits. If we search in 2-bit lengths, we will miss out on prefixes like 101*. To combat this, we use a strategy called **controlled prefix expansion**, where we expand a given prefix to more prefixes. We ensure that the expanded prefix is a multiple of the chosen stride length. At the same time, we remove all lengths that are not multiples of the chosen stride length. We end up with a new database of prefixes, **which may be larger (in terms of the actual number of prefixes) but with fewer lengths.** So, the expansion gives us more speed with an increased cost of the database size.
* In the figure below, we have expanded our original database of prefixes while considering a stride length of three. Initially, we had five different prefix lengths (1, 3, 4, 5, and 6), but now we have more prefixes but only two lengths (3 and 6).  
* For example, we substitute (expand) P3 = 11001* with 110010* and 110011*. 
* When we expand our prefixes, there may be a collision, i.e., when an expanded prefix collides with an existing prefix. In that case, that expanded prefix gets dropped. For example, in the figure, we see that the fourth expansion of P6=1000* collides with P7 and thus gets removed.
* <img src="https://i.imgur.com/eZ1rpOS.png" style="width: 600px" />

### Multibit tries: Fixed-Stride

* We introduced multibit tries in the previous section. Here, we will look at a specific example of a fixed-stride trie of length 3. Every node has 3 bits. 
* We are using the same database of prefixes as in the previous section. We can see that the prefixes (P1, P2, P3, P5, P6, P7, P8, and P9) are all represented in the expanded trie. 
* Some key points to note here:
    1. Every element in a trie represents two pieces of information: a pointer and a prefix value.
    2. The prefix search moves ahead with the preset length in n-bits (3 in this case) 
    3. When the path is traced by a pointer, we remember the last matched prefix (if any).
    4. **Our search ends when an empty pointer is met**. At that time, we **return the last matched prefix as our final prefix match**.
* <img src="https://i.imgur.com/VDG8AAy.jpg" style="width: 600px" />
* Example: We consider an address A, which starts with 001. The search for A starts with the 001 entry at the root node of the trie. Since there is no outgoing pointer, the search terminates here and returns P5. Whereas if we search for 100000, the search will terminate with P7.

### Multibit Tries: Variable Stride

* Why do we need variable strides? 
    * In this topic, we will discuss a more flexible version of the algorithm, which offers us a **variable number of strides**. With this scheme, we can examine a different number of bits every time.
    * We encode the stride of the trie node using a pointer to the node. The root node stays as is (in the previous scheme).  
    * We note that the rightmost node still needs to examine 3 bits because of P7. 
    * But at the leftmost node needs only to examine 2 bits because P3 has 5 bits in total. So we can rewrite the leftmost node as in the figure below. 
    * So now we have four fewer entries than our fixed stride scheme. So by varying the strides, we could **make our prefix database smaller and optimize for memory**.
    * <img src="https://i.imgur.com/V0hcd12.jpg" style="width: 600px" />
* Some **key points** about variable stride:
    1. Every node can have a different number of bits to be explored.
    2. The optimizations to the stride length for each node are all done to **save trie memory and the least memory accesses**.
    3. An optimum variable stride is selected by using dynamic programming

* Note that, in either fixed length or variable stride tires, the prefix in each node in the trie should have the **same length**.[Quiz]

## Quiz

* <img src="https://i.imgur.com/EncB0xD.jpg" style="width: 500px" />
* Questions:
    1. why n1 is none?
    2. why n6/n7/n11/n17 is none?
* Notice this is NOT a question asking a prefix lookup but constructing the variable-length multibit trie. So we must do the controlled prefix expansion to find which prefix (mapped to a letter for simplicity) goes in each node in the trie. The nodes with no prefix occur when there is no associated prefix in the expanded prefix database. For example, n7 is none because 0101 is not in the expanded prefix database. 
