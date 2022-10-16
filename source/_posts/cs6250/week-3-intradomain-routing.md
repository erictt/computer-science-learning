#  Lesson 3: Intradomain Routing

<!-- toc -->
----

This lecture, we learn about the protocols that enable data to travel over a "good" path from the source to the destination within a single administrative domain.

* Network-layer functions:
    * **forwarding**: move packets from router’s input to appropriate router output. <-- data plane
    * **routing**: move packets from router’s input to appropriate router output. <-- control plane 
* Two approaches to structuring network control plane:
    * **per-router control (traditional) <-- this lesson focus on**
        * Individual routing algorithm components in each and every router interact in the control plane
        * <img src="https://i.imgur.com/FjdfGIk.jpg" style="width: 500px" />
    * logically centralized control (software defined networking)
        * Remote controller computes, installs forwarding tables in routers
        * <img src="https://i.imgur.com/1nAAdMr.jpg" style="width: 500px" />

* Two Types of Routing Domain
    * **Intradomain routing** (Interior Gateway Protocols (IGPs)): routers that belong to the same administrative domain <-- this lesson focus on
    * **Interdomain routing**: Routers belong to different administrative domains

## Routing Protocols

* Goal: determine the "good" paths(equivalently, routes), from sending hosts to receiving host, through network of routers
    * path: sequence of routers packets traverse from given initial source host to final destination host
    * “good”: least “cost”, “fastest”, “least congested”
    * routing: a “top-10” networking challenge!
* What could weights on the graph edges represent in these diagrams, when we are seeking the least-cost path between two nodes? [Quiz]
    * Length of the cable
    * Time delay to traverse the link
    * Monetary cost
    * Link capacity
    * Current load on the link
* Routing algorithm classification
    * <img src="https://i.imgur.com/WjPJvy3.jpg" style="width: 500px" />

* Notation
    * **u** source node.
    * **v** every other node.
    * **D(v)** cost of the current least cost path from u to v.
    * **p(v)** the previous node along the current least cost path from u to v.
    * **c(u, v)** (or $c_{u, v}$) the cost from u to directly attached neighbor v
    * **N'** subset of nodes along the current least-cost path from u-v.

### The Link-state Algorithm

* Base on [Dijkstra's Algorithm](https://www.programiz.com/dsa/dijkstra-algorithm).
* Specs
    * **centralized**: network topology, link costs known to all nodes
        * accomplished via “link state broadcast” 
        * all nodes have same info
    * computes least cost paths from one node (“source”) to all other nodes
        * gives **forwarding table** for that node
    * iterative: after k iterations, know least cost path to k destinations

* Algorithm
    * <img src="https://i.imgur.com/msB5AAM.jpg" style="width: 500px" />

    * The key is **in the loop, select the node with the least cost from the previous iteration**.
    * Note that the edge is weighted, e.g.
        * <img src="https://i.imgur.com/jTYnBJ4.png" style="width: 500px" />
* Computational Complexity
    * each iteration, loop `-1` elements. By the end, it's $n + (n-1) + (n-2) + ... + 1 = n(n-1)/2 \approx n^2$ 
    * more efficient implementations possible: $O(n\log{n})$
* message complexity: 
    * each router must broadcast its link state information to other n routers 
    * efficient (and interesting!) broadcast algorithms: **O(n)** link crossings to disseminate a broadcast message from one source
    * each router’s message crosses **O(n)** links: overall message complexity: **O(n^2)**


### The Distance-vector Algorithm

* Base on [Bellman-Ford algorithm](https://www.programiz.com/dsa/bellman-ford-algorithm). Each node maintains its own distance vector, with the costs to reach every other node in the network. Then, from time to time, each node sends its own distance vector to its neighbor nodes. The neighbor nodes in turn, receive that distance vector and they use it to update their own distance vectors.
* How is the vector update is happening? Each node x updates its own distance vector using the Bellman Ford equation: **Dx(y) = minv{c(x,v) + Dv(y)}** for each destination node y in the network. A node x, computes the least cost to reach destination node y, by considering the options that it has to reach y through each of its neighbor v. So node x considers the cost to reach neighbor v, and then it adds the least cost from that neighbor v to the final destination y. It calculates that quantity over all neighbors v and it takes the minimum.
* Psudocode: 
    * <img src="https://i.imgur.com/YcqJO6H.png" style="width: 500px" />
* Now, let’s see an example of the distance vector routing algorithm. Let’s consider the three node network shown here:
    * <img src="https://i.imgur.com/dljYM5y.png" style="width: 500px" />
* In the first iteration, each node has its own view of the network, which is represented by an individual table. Every row in the table is the distance vector of each node. Node x has it’s own table, and the same is true for nodes y and z. We note that in the first iteration, node x does not have any information about y or z’s distance vectors, thus these values are set to infinity.
* In the second iteration, the nodes exchange their distance vectors and they update their individual views of the network. 
* Node x computes its new distance vector, using the Bellman Ford equation for every destination node y and z. For each destination, node x compares the cost to reach that destination through a neighbor node.     
    * `dx(y) = min{c(x,y) + dy(y), c(x,z)+dz(y) } = min{2+0, 7+1} = 2`
    * `dx(z) = min{c(x,y) + dy(z), c(x,z)+dz(z) } = min{2+1, 7+0} = 3`
* At the same time, node x receives the distance vectors from y and z from the first iteration. So it updates its table to reflect its view of the network accordingly. 
* Nodes y and z repeat the same steps to update their own tables.
    * <img src="https://i.imgur.com/l9Hl51P.png" style="width: 500px" />
* In the third iteration, the nodes process the distance vectors received from the previous iteration (if they have changed), and they repeat the same calculations. Finally, each node has its own routing table.
    * <img src="https://i.imgur.com/K9lLEvf.png" style="width: 500px" />
* Finally, at this point, there are no further updates sent from the nodes. Thus, the nodes are not doing any further calculations on their distance vectors. The nodes enter a waiting mode, until there is a change in the link costs. 


#### The count-to-infinity problem

* <img src="https://i.imgur.com/JrFpvsN.png" style="width: 500px" />

* Let’s assume that the cost of link y-x changed from 4 to 60. 
    * At t0 y detects that cost has changed, now it will update its distance vector thinking that it can still reach x through z with a total cost of 5+1=6
    * At t1, we have a routing loop, where z thinks it can reach x through y and y thinks it can reach x through z. This will be causing the packets to be bouncing back and forth between y and z until their tables change. 
    * z and y keep updating each other about their new cost to reach x. For example, y computes its new cost to be 6, and then informs z. Then z computes its new cost to be 7, and then informs y, and so on. 
* This back and forth continues for a total of 44 iterations, at which point z computes its cost to be larger than 50, and that point it will prefer to reach x directly rather than through y. 
* This link cost change took a long time to propagate among the nodes of the network. This is known as the **count-to-infinity problem**. 

#### Solution to the count-to-infinity problem: Poison reverse

* since z reaches x through y, z will advertise to y that the distance to x is infinity (Dz(x)=infinity). However z knows that this is not true and Dz(x)=5. z tells this lie to y, as long as it knows that it can reach to x via y. Since y assumes that z has no path to x except via y, it will never send packets to x via z. 
* So z poisons the path from z to y. 
* Things change when the cost from x to y changes to 60. y will update its table and send packet to x directly with cost Dy(x)=60. It will inform z about its new cost to x, after this update is received. Then z will immediately shift its route to x to be via the direct (z,x) link at cost 50. Since there is a new path to x, z will inform y that Dz(x)=50.
* When y receives this update from z, y will update Dy(x)=51=c(y,z)+Dz(x). 
* Since z is now on least cost path of y to reach x, y poisons the reverse path from z to x. Y tells z that Dy(x)=inf, even though y knows that Dy(x)=51. 
* This technique will solve the problem with 2 nodes, however poisoned reverse will not solve a general count to infinity problem involving 3 or more nodes that are not directly connected.

## Internet Approach to scalable routing

Aggregate routers into regions known as “**autonomous systems**” (AS) (a.k.a. “domains”)

* **intra-AS (aka “intra-domain”)**: routing among within same AS (“network”)
    * all routers in AS must run same intra-domain protocol
    * routers in different AS can run different intra-domain routing protocols
    * gateway router: at “edge” of its own AS, has link(s) to router(s) in other AS’es
* **inter-AS (aka “inter-domain”)**: routing among AS’es
    * gateways perform inter-domain routing (as well as intra-domain routing)

*  Common Intra-AS Routing Protocols
    *  RIP: Routing Information Protocol [RFC 1723]
        * classic DV: DVs exchanged every 30 secs
        * no longer widely used
    * OSPF: Open Shortest Path First  [RFC 2328]
        * link-state routing
        * IS-IS protocol (ISO standard, not RFC standard) essentially same as OSPF

### Routing Information Protocol(RIP)

* **The RIP is based on the Distance Vector protocol.**

* The first version of RIP, released as a part of the BSD version of Unix, uses hop count as a metric (i.e. assumes link cost as 1). The metric for choosing a path could be shortest distance, lowest cost, or a load-balanced path. In RIP, routing updates are exchanged between neighbors periodically, using a RIP response message, as opposed to distance vectors in the DV protocols. These messages, called **RIP advertisements**, contain information about sender’s distances to destination subnets.
* Let’s look at a simple RIP example to illustrate how it works. The figure below shows a portion of the network. Here, A, B, C and D denote the routers and w, x, y and z denote the subnet masks.
    * <img src="https://i.imgur.com/qYLrL7Y.jpg" style="width: 500px" />
* Each router maintains a routing table, which contains its own distance vector as well as the router's forwarding table. If we have a look at the routing table of Router D, we will see that it has three columns: destination subnet, identification of the next router along the shortest path to the destination, and the number of hops to get to the destination along the shortest path. A routing table will have one row for each subnet in the **AS** (**AS = Autonomous Systems**, which will be discussed in more detail in Lesson 4).
    * <img src="https://i.imgur.com/36Oq2xl.jpg" style="width: 500px" />
* For this example, the table in the above figure indicates that to send a datagram from router D to destination subnet w, the datagram should first be forwarded to neighboring router A; the table also indicates that destination subnet w is two hops away along the shortest path. Now if router D receives from router A the advertisement (the routing table information of router A) shown in the figure below it merges the advertisement with the old routing table.
    * <img src="https://i.imgur.com/8HWXozX.jpg" style="width: 500px" />
* In particular, router D learns that there is now a path through router A to subnet z that is shorter than the path through router B. Therefore, router D updates its table to account for the new shortest path. The updated routing table is shown in the figure below. As the Distance Vector algorithm is in the process of converging or as new links or routers are getting added to the AS, the shortest path is changing.
    * <img src="https://i.imgur.com/837fX25.png" style="width: 500px" />

* Each node maintains a RIP Table (Routing Table), which will have one row for each subnet in the AS. RIP version 2 allows subnet entries to be aggregated using route aggregation techniques.
* If a router does not hear from its neighbor at least once every 180 seconds, that neighbor is considered to be no longer reachable (broken link). In this case, the local routing table is modified, and changes are propagated. Routers send request and response messages over UDP, using port number 520, which is layered on top of network-layer IP protocol. RIP is actually implemented as an application-level process. 
* Some of the challenges with RIP include updating routes, reducing convergence time, and avoiding loops/count-to-infinity problems.


### Open Shortest Path First (OSPF)

It's a routing protocol that uses a **link-state routing algorithm** to find the best path between the source and the destination router. OSPF was introduced as an advancement of the RIP Protocol, operating in upper-tier ISPs. It is a link-state protocol that uses flooding of link-state information and a Dijkstra least-cost path algorithm.

A link-state routing algorithm is a dynamic routing algorithm in which each router shares knowledge of its neighbors with every other router in the network. The network topology built as a result can be viewed as a directed graph with preset weights for each edge assigned by the administrator.

* **Hierarchy**
    * Two-level hierarchy: local area, backbone.
        * link-state advertisements flooded only in area, or backbone
        * each node has detailed area topology; only knows direction to reach other destinations
    * <img src="https://i.imgur.com/MpgwIMY.jpg" style="width: 500px" />
    * Each area runs its own OSPF link-state routing algorithm, with each router in an area broadcasting its link-state to all other routers in that area. Within each area, one or more **area border routers** are responsible for routing packets outside the area. 
    * Exactly one OSPF area in the AS is configured to be the **backbone area**. The primary role of the backbone area is to route traffic between the other areas in the AS. The backbone always contains all area border routers in the AS and may contain non-border routers as well. 
    * For packets routing between two different areas, it is required that the packet be sent through an **area border router**, **through the backbone**, and then to the area border router within the destination area before finally reaching the destination.
* **Operation**
    * First, a graph (topological map) of the entire AS is constructed. Then, considering itself as the root node, each router computes the shortest-path tree to all subnets by running Djikstra's algorithm locally. The link costs have been pre-configured by a network administrator. The administrator has a variety of choices while configuring the link costs. For instance, he may choose to set them to be inversely proportional to link capacity, or set them all to one. Given a set of link weights, OSPF provides the mechanisms for determining least-cost path routing. 
    * Whenever there is a change in a link's state, the router broadcasts routing information to all other routers in the AS, not just to its neighboring routers. It also periodically broadcasts a link's state even if its state hasn't changed. 
* **Link State Advertisements**
    * Every router within a domain that operates on OSPF uses **Link State Advertisements (LSAs)**. LSA communicates the router's local routing topology to all other local routers in the same OSPF area. In practice, LSA is used for building a database (called the link state database) containing all the link states. LSAs are typically flooded to every router in the domain. This helps form a consistent network topology view. Any change in the topology requires corresponding changes in LSAs.
* **The refresh rate for LSAs**
    * OSPF typically has a refresh rate for LSAs, which has a default period of 30 minutes. If a link comes alive before this refresh period is reached, the routers connected to that link ensure LSA flooding. Since the flooding process can happen multiple times, every router receives multiple copies of refreshes or changes - and stores the first received LSA change as new and the subsequent ones as duplicates.

#### Processing OSPF Messages in the Router

<img src="https://i.imgur.com/qjpQLy4.jpg" style="width: 500px" />

* Let’s begin with a simple model of a router given in the figure above. The router consists of a route processor (which is the main processing unit) and interface cards that receive data packets which are forwarded via a switching fabric. Let us break down router processing in a few steps:
* Initially, the LS update packets which contain LSAs from a neighboring router reaches the current router’s OSPF (which is the route processor). This is the first trigger for the route processor. As the LS Updates reach the router, a consistent view of the topology is being formed and this information is stored in the link-state database. Entries of LSAs correspond to the topology which is actually visible from the current router. 
* Using this information from the link-state database, the current router calculates the shortest path using shortest path first (SPF) algorithm. The result of this step is fed to the Forwarding Information Base (FIB)
* The information in the FIB is used when a data packet arrives at an interface card of the router, where the next hop for the packet is decided and its forwarded to the outgoing interface card.
 

To further understand OSPF processing, let's look at the following flow chart and view it in time slices (T1, T2, …, T7).

<img src="https://i.imgur.com/NCy0UrE.png" style="width: 500px" />
<img src="https://i.imgur.com/FEcOnST.png" style="width: 500px" />

## Hot Potato Routing

* In large networks, routers rely both on interdomain and intradomain routing protocols to route the traffic. 
* The routers within the network use the intradomain routing protocols to find the best path to route the traffic within the network. In case when the final destination of the traffic is outside the network, then the traffic will travel towards the networks exit (egress points) before leaving the network. In some cases there are multiple egress points that the routers can choose from. These egress points (routers) can be equally good in the sense that they offer similarly good external paths to the final destination.
* In this case, hot potato routing is a technique/practice of choosing a path within the network, by **choosing the closest egress point based on intradomain path cost** (Interior Gateway Protocol/IGP cost)[Quiz].

## An Example Traffic Engineering Framework[Optional]

* It involves three main components: **measure**, **model** and **control** as shown in the below figure:
    * <img src="https://i.imgur.com/lSY8uGJ.jpg" style="width: 500px" />
    

* **Measure**: The efficient assignment of link weights depends on the real time view of the network state which includes:
    * the operational routers and links,
    * the link capacity and IGP parameters configuration.
* The status of the network elements can be obtained using **Simple Network Management Protocol (SNMP)** **polling** or via SNMP **traps**. The link capacity and the IGP parameters can be gathered from the configuration data of the routers or external databases that enable the provisioning of the network elements. Furthermore, a software router could act as **an IGP route monitor** by participating in OSPF/IS-IS with operational routers and reporting real time topology information. 
* In addition to the current network state, the network operator also requires an estimate of the traffic in the network that can be acquired either by prior history or by using the following measurement techniques: 
    1. Directly from the SNMP Management Information Bases (MIBs) 
    2. By combining packet-level measurements at the network edge using the information in routing tables 
    3. Network tomography which involves observing the aggregate load on the links along with the routing data 
    4. Direct observation of the traffic using new packet sampling techniques   

* **Model**: This involves predicting the traffic flow through the network based on the IGP configuration. The best path between two routers is selected by calculating the shortest path between them when all the links belong to the same OSPF/IS-IS area. In case of large networks consisting of multiple OSPF/IS-IS areas, the path selection among routers in different areas is dependent on the summary information passed across the area boundaries. If there are multiple shortest paths between two routers, it is leveraged for load balancing by splitting the traffic almost evenly over these paths. 
* The routing model thus aims to compute a set of paths between each pair of routers, with each path representing the fraction of traffic that passes through each link. The volume of traffic on a link can now be estimated by combining the output of the routing model and the estimated traffic demands. 

* **Control**: The new link weights are applied on the affected routers by connecting to the router using telnet or ssh. The exact commands are dependent on the operating systems of the router. These updates may be automated or done manually depending on the size of the network. 
* Once a router receives a weight change, it updates its link-state database and floods the newly updated value to the entire network. On receiving the updated value, each router in turn updates its link-state database, recomputes the shortest paths and updates affected entries in its forwarding table.  Similar to when there is a topology change or a failure, this involves a transition period where there is a slightly inconsistent view of the shortest path for few destinations. Although the convergence after a weight change is faster than a failure scenario (as there is no delay in detecting a failure), it still involves a transient period in the network. Hence, understandably, changing the link weights is not done frequently and only done in scenarios where there is new hardware, equipment failures or changes in traffic demands.
