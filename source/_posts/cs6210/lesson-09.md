# Lecture 09: Internet Computing

<!--
## Instruction
You are a teach assistant of the course of advanced operating system. This is the lecture of Internet Computing, which teaches Giant Scale Services, MapReduce, Content Delivery Networks. I will ask you a sequence of questions regarding the course. Use bullet points to answer all questions accurately, don't make up anything. And also make your answer easy to understand and easy to review. Provide more details if necessary.
## End of Instruction
-->

## L09a: Giant Scale Services

### Introduction

- This lecture focuses on managing large data centers and internet scale computing.
- This lecture addresses systems issues in managing large data centers, programming big data applications, and disseminating content on the web in a scalable manner.
- This lecture builds on previous lessons to harden distributed systems issues and handle scale on the order of thousands of processes and failures.

### Generic Service Model of Giant Scale Services

<img src="https://i.imgur.com/mZmtQ2W.png" style="width: 800px" />

- The web portal example used in the module is Gmail, a popular email service provided by Google.
- The architecture within a site typically consists of thousands of servers, all interconnected through a high-bandwidth communication backplane, and connected to data stores to process incoming client requests.
- The servers may optionally use a backplane that allows them to talk to one another for servicing any particular request, which helps to distribute the load evenly.
- The load manager plays a crucial role in ensuring that the client traffic is balanced among all the servers, and no server is overloaded, which would cause the service to slow down or fail.
- In addition to load balancing, the load manager also monitors the state of the servers and shields incoming client requests from any partial failures that may happen internally within a particular site.
- The load manager typically uses various algorithms and techniques to balance the load, such as round-robin, least-connections, or IP hashing.
- Embarrassingly parallel refers to the fact that the incoming client requests are all independent of one another and can be handled in parallel as long as there is enough server capacity to meet all the incoming requests. This is a characteristic of most giant scale services.

### Clusters as Workhorses

<img src="https://i.imgur.com/0XOda7V.png" style="width: 800px" />


- Computational clusters are the workhorses of giant scale services and are employed in modern data centers.
- Each node in the cluster may itself be an SMP, and the advantages of structuring computational resources as a cluster of machines includes absolute scalability, cost and performance control, and incremental scalability.
- Computational clusters offer incremental scalability by adding more nodes to the cluster to increase performance, or scaling back when the volume of requests decreases.

### Load Management Choices

<img src="https://i.imgur.com/DmJCSlP.png" style="width: 800px" />


- Load management can be done at any of the seven layers of the OSI reference model, with higher layers offering more functionality in terms of dealing with server failures and directing incoming client requests.
- Load managers operating at the transport level or higher can dynamically isolate down server nodes from the external world, have service-specific front end nodes, and co-opt client devices in load management.

### Load Management at Network Level

- Load management at the network level is done using round-robin DNS servers, which assign different IP addresses corresponding to different servers to incoming client requests for good load balance.
- The assumption in this model is that all servers are identical and that data is fully replicated, so any incoming request can be sent to any server, and the data needed to satisfy the request is available.
- The advantage of using round-robin DNS servers is good load balance, but the disadvantage is that it cannot hide down server nodes from the external world.

### DQ principle

<img src="https://i.imgur.com/6kVTPLF.png" style="width: 800px" />


- The DQ principle is used to manage incoming client requests and the data set available for handling those requests on a server.
	- The server has all the data required for dealing with incoming client queries, called the full data set ($D_f$).
	- The offered load to the server is called $Q_0$, which is the amount of requests hitting the server per unit time.
	- The **yield** (Q) is the ratio of completed requests($Q_c$) to the offered load($Q_0$), and ideally should be one, but may be less than one if the server is not able to deal with the offered load entirely.
	- The *available data set for processing each query*($D_v$) may be less than the full data set due to failures of some data servers or the load on the server, and is called the **harvest** ($D = \frac{D_v}{D_f}$).
- The product $D \cdot Q$, representing the data server query and the rate of query coming into the server, is a constant for a given server capacity.
- To increase the number of clients being served, the harvest can be decreased while keeping the yield the same.
- To give the complete data that is needed for serving a query, the yield can be decreased while keeping the harvest constant.
- DQ represents a system constant for the server's capacity, and the system administrator can choose to sacrifice yield for harvest or harvest for yield.
- For network-bound applications, DQ is much more intuitive than traditional measures like **I/O operations per second (IOOPS)**.
- **Uptime** is another metric that system administrators use, but it is not very intuitive for giant-scale services because if there are no queries during the **mean-time-to-repair (MTTR)**, then the uptime is not a good measure of how well a server is performing.
- The DQ principle is powerful in advising the system administrator on how to architect the system, including how much to replicate, how much to partition the data set, and how to gracefully degrade the servers when the volume of incoming traffic increases beyond a server capacity.

#### Replication vs Partitioning

<img src="https://i.imgur.com/4lfmAdl.png" style="width: 800px" />

- System administrators have the choice to replicate or partition data in a server's data store and computational resources.
- Replicating data means every data server has the full corpus of data needed to serve a request, and failures can be redirected to another live server with full access to the same data repository.
- Partitioning data means end partitions of the full corpus of data can become unavailable if some service fails, leading to a decrease in harvest.
- DQ is independent of replication or partitioning so long as incoming requests are network-bound and assuming processing incoming requests is not disk-bound.
- Replication beyond a certain point is important because users would prefer complete data, while searches may be okay with incomplete data.

#### Graceful Degradation

<img src="https://i.imgur.com/XfUMKgn.png" style="width: 800px" />

- DQ defines the total system capacity, which is a constant. If a server reaches its limit in terms of DQ, we have a choice of gracefully degrading the service from the point of view of the client.
- One option is to keep the harvest the same, which means that the fidelity of the answers returned by the server is constant, but the yield Q comes down.
- Another option is to keep the yield Q constant, but decrease the harvest, which means that the fidelity of the results returned to the users is less than 100%.
- System providers can use strategies such as cost-based admission control, priority or value-based admission control, or reducing data freshness to manage saturation.
- These choices allow the system administrator to make decisions about how they affect the harvest, yield, and uptime of the server.

#### Online Evolution and Growth

<img src="https://i.imgur.com/VjbFQX7.png" style="width: 800px" />

- The DQ principle can be used to measure the loss of service during upgrades, and there are three upgrade strategies that can be employed:
	- Fast reboot: All servers are brought down at once, upgraded, and then turned back on. This results in complete loss of service for the entire upgrade duration.
	- Rolling upgrade: Servers are upgraded one at a time, resulting in no complete loss of service, but there is a DQ loss every time a server is upgraded.
	- Big flip: Half of the servers are brought down at once, upgraded, and then turned back on, followed by the other half. This results in 50% capacity service during the upgrade duration.
- Regardless of the strategy used, there is always a DQ loss that cannot be hidden from users. The system administrator has to make informed decisions on how to minimize this loss during upgrades, and the DQ principle can help in making these decisions.

### Conclusion

- Giant scale services are network bound, not disk I/O bound.
- The DQ principle helps optimize service and plan for graceful degradation during various scenarios.

## L09b: MapReduce

### Introduction

<img src="https://i.imgur.com/uh0tUTR.png" style="width: 800px" />

- MapReduce is a programming environment for dealing with big data applications.
- The input to MapReduce is considered as a set of records identified by a key-value pair.
- The MapReduce framework requires two user-defined functions: **map** and **reduce**.
- Both map and reduce functions take key-value pairs as inputs and produce key-value pairs as outputs.
- The map function looks for unique names in the corpus of documents and outputs the number of times each name occurs in a file.
- The reduce function aggregates the values from the map function and outputs the total number of occurrences for each unique name.
- The programming environment handles the plumbing between the output of the map function and input of the reduce function, as well as other details such as the number of mapper and reducer instances required.

### Why MapReduce

<img src="https://i.imgur.com/6QszE4y.png" style="width: 800px" />

- Many processing steps in giant-scale services are expressible as MapReduce, such as seat availability searches, website frequency analysis, word indexing, and page ranking.
- These applications are embarrassingly parallel and work on big datasets, making them ideal for taking advantage of the computation resources in a data center.
- Domain expertise in the form of map and reduce functions is required from the app developer, but the programming system handles the heavy lifting such as instantiating mappers and reducers and data movement.

### Heavy Lifting Done by the Runtime

<img src="https://i.imgur.com/789SyjC.png" style="width: 800px" />

- The programming library splits the input key-value pairs into M splits and spawns a master and worker threads for map and reduce functions.
- The master assigns worker threads for mapping and reducing functions.
- In the map phase, each worker thread reads its assigned split, parses the input, and applies the user-defined map function.
- Intermediate key value pairs produced by the mapper are buffered in memory and periodically written to files.
- In the reduce phase, the worker pulls data from all mappers' intermediate results on their local disks using RPC.
- The programming framework sorts the input data set and calls the user-supplied reduce function for each key with the set of intermediate values.
- Each reduce function writes to the final output file specific to the partition it is responsible for.
- The master manages the available machines to handle the M input data sets and the R reduce splits.
- The user only needs to write the map and reduce functions, and the framework handles the rest.

### Issues to be handled by the Runtime

- The runtime system needs to manage and MapReduce computation.
- The master data structures keep track of the location of files created by completed mappers and a scoreboard of mappers and reducers assigned to work on different splits.
- Fault tolerance is important in case an instance of a map function does not respond in a timely manner, the master may assume that it's dead and restart it on a different node of the cluster.
- The locality management system ensures that the working set of computations fit in the closest level of the memory hierarchy of a process.
- Task granularity is an important issue, and it's the responsibility of the programming framework to come up with the right task granularity so that there can be good load balance of the computational resources.
- The user can override the partitioning function with their own partitioning function if they think that will result in a better way of organizing the data.
- Combining functions may also be incorporated in writing mapping and reduce functions.
- The map and reduce functions need to be item potent for the fault tolerance model of the programming environment to work correctly.
- The programming framework offers bells and whistles for getting status information and logs.

### Conclusion

- The power of MapReduce is its simplicity.
- The domain expert only needs to write the Map and Reduce functions for their application.
- The runtime system manages all the heavy lifting under the covers.

## L09c: Content Delivery Networks

### Introduction

- The internet and World Wide Web provide vast amounts of information to users.
- Content creation happens both by individuals and businesses like CNN, BBC, and NBC.
- This section will focus on content delivery networks (CDNs) and how information is stored and distributed.

### DHT 

#### Introduction
<img src="https://i.imgur.com/6reJ4A9.png" style="width: 800px" />

- DHT stands for Distributed Hash Table, which is a decentralized and scalable system used for storing and retrieving data in a peer-to-peer (P2P) network. In a DHT, each node in the network is responsible for storing a portion of the overall data. The data is stored as key-value pairs, and the keys are hashed to determine which node in the network will be responsible for storing that particular key-value pair.
- DHTs allow for efficient data retrieval and storage, as well as load balancing across the network, since each node is responsible for only a small portion of the data. Additionally, DHTs are fault-tolerant, since data is replicated across multiple nodes, and if one node fails, another node can take over its responsibilities.
- The API for manipulating the DHT data structure includes **putkey** (to store a key-value pair) and **getkey** (to retrieve a value associated with a key-value pair).

#### Details
<img src="https://i.imgur.com/1BGPiiw.png" style="width: 800px" />

Distributed Hash Table (DHT) deals with two namespaces, namely the key-space namespace and the node-space namespace.

- **The key-space namespace** is managed by generating a unique key for the content using an algorithm like SHA-1, which generates a 160-bit key that ensures no collision occurs, even if different content uses the same algorithm to generate the key.
- **The node-space namespace** is created by using an SHA-1 hash of IP addresses of nodes that want to share content. These IP addresses are encoded into a 160-bit NodeID using the same algorithmic technique used to generate keys.

The objective is to store a key in a NodeID such that the key is very close to the NodeID. Ideally, the key should be exactly equal to the NodeID, but it's not always possible to guarantee that the hash values will be the same.

The API for manipulating the distributed hash table data structure includes putkey and getkey methods. 

- The putkey method takes two arguments, the key and the value, where the value can be any associated content such as an IP address. 
- The getkey method takes one argument, the key, and returns the value associated with that key-value pair.

### CDN (An Overlay Network)

<img src="https://i.imgur.com/7HqjOFt.png" style="width: 800px" />

- A CDN is an example of an overlay network, which is a virtual network on top of the physical network.
- Overlay networks are used at the user level to map virtual addresses to IP addresses for sending messages.
- User-level routing tables are constructed by exchanging mapping information between friends to discover one another and send messages.
- Overlay networks allow content to be shared and distributed among a set of users who have exchanged information with one another.

### Overlay Networks in General

- Overlay networks are a general principle and exist at the operating system level, such as the IP network overlaying the local area network.
- IP addresses translate to MAC addresses to traverse the local area network to reach the destination.
- CDN is an overlay on top of TCP/IP, and a node ID maps to an IP address for sending messages.

### DHT and CDNs

<img src="https://i.imgur.com/dOBg47Z.png" style="width: 800px" />

- DHT is an implementation vehicle for CDNs to populate the routing table at the user level.
- Put operation is used for placement of key-value pairs, and get operation is used for retrieval of a value associated with a key-value pair.
- The construction of the routing table involves storing key-value pairs on nodes and using the put and get operations to retrieve them.

### Traditional(Greedy) Approach

<img src="https://i.imgur.com/WApbZ7g.png" style="width: 800px" />

- The traditional approach for constructing a distributed hash table involves a greedy algorithm where a key value is placed in a node that is very close to the key. When retrieving a key, the algorithm looks for the node closest to the key.
- Routing tables at each node in the system only list the nodes that can be communicated with directly.
- If a node is not in the routing table, the algorithm goes to a node that is close enough to the desired node, hoping that it will know how to communicate with the desired node.
- The goal of the greedy approach is to get to the desired destination as quickly as possible with the minimum number of hops.

### The Problems of Greedy Approach

- The greedy approach leads to a **metadata server overload** problem, where a node that is closest to a key value pair becomes congested with traffic from puts and gets.
	- <img src="https://i.imgur.com/L6CacoJ.png" style="width: 800px" />
- This also creates a **tree saturation** problem, where nodes in proximity to the congested node also become congested.
	- <img src="https://i.imgur.com/sP84B76.png" style="width: 800px" />
- If content becomes popular, there is also an **origin server overload** problem, where the server hosting the content becomes inundated with download requests.
	- <img src="https://i.imgur.com/rMJT7Me.png" style="width: 800px" />

- A content distribution network can solve the origin server overload problem by automatically mirroring content at geo-local sites and dynamically routing requests to the closest mirror.
- However, this solution is expensive and not accessible to individual content providers.
- The Coral System is a solution that democratizes content distribution and addresses both the metadata server overload and origin server overload problems.
- The coral approach avoids tree saturation by not being greedy and not necessarily storing the key K in the node N with an ID equal to K.
- The Coral DHT implements a sloppy DHT that spreads metadata overload so that no single node in the democratic process of helping one another is saturated.
- The distance between the source and the destination in Coral key-based routing is computed by XORing the bit patterns of the node IDs for the source and the destination.
	- **XOR distance** represents the distance between the two nodes in the overlay network space. The larger the XOR value, the farther apart the two nodes are in the network.

### Key-Based Routing

<img src="https://i.imgur.com/aVjeEY8.png" style="width: 800px" />

- The greedy approach is to get as close to the desired destination in the node ID namespace and ask a nearby node if it has a way of getting to the desired destination.
- The objective in the greedy approach is reaching the destination with the fewest number of hops.

#### Key-Based Routing in Coral

<img src="https://i.imgur.com/IBcnqUd.png" style="width: 800px" />

- The Coral key-based routing reduces the distance by approximately half in each hop and avoids being greedy to avoid congestion and tree saturation.
- In each hop, the Coral key-based routing goes to some node that is half the distance to the destination in the node ID namespace. 
- If the node does not have a direct way to reach the desired node, and a nearby node is contacted to obtain information on nodes that are close enough to the desired destination.

<img src="https://i.imgur.com/zKcI0Q5.png" style="width: 800px" />

### Coral Sloppy DHT 

The primitives available in Coral for manipulating the sloppy DHT are put and get operations.

#### Put Operation

<img src="https://i.imgur.com/x6q3TsB.png" style="width: 800px" />

- The put operation takes two parameters: key and value.
	- Key is the content hash, and value is the node ID of the proxy with the content for that key.
- Put can be initiated by the origin server or a node that wants to serve as a proxy.
- The result of doing the put operation is to store this key value in some metadata server.
- We need to place this key value in an appropriate node based on space and time metrics.
- **Full** state means a particular node is already storing l values for a key.
- **Loaded** is stating how many requests per unit time a node is willing to entertain for a particular key.
- The Coral key-based routing algorithm reduces the distance by half to find the appropriate node to place the key.
- We ask each node along the way if it is loaded or full, and if it is, we retract our steps and choose an appropriate node.
- The Coral put operation chooses an appropriate node that is neither full nor loaded to entertain requests for retrieving the particular key value pair.

#### Get Operation
<img src="https://i.imgur.com/5UOslTS.png" style="width: 800px" />

- The get operation works similarly to the put operation.
- We go to a node that is half the distance to the key we are looking for.
- If the content is popular, then multiple proxies may have gotten the key value pair.
- They may have put their own node IDs as a potential node for the content.
- Our metadata server may not necessarily have to be the destination which exactly matches that key.

#### Coral in Action

- Coral allows for user-generated content to be distributed in a democratic fashion.
- The load for serving as a metadata server and content server can get naturally distributed.
- Let's say, Naomi creates a unique signature for her content and uses Coral to put it out on the internet.
	- <img src="https://i.imgur.com/qPpZi7u.png" style="width: 800px" />

- Jacques uses Coral to get the content by following the key-based routing algorithm and ends up at David's computer.
	- <img src="https://i.imgur.com/DIWu4Y9.png" style="width: 800px" />

- Jacques serves as a proxy for the content and puts a new key value pair in the system.
	- <img src="https://i.imgur.com/wTgwlKd.png" style="width: 800px" />

- Kamal also uses Coral to get the content and ends up getting it from Jacques, who serves as a proxy.
	- <img src="https://i.imgur.com/6uhBtdH.png" style="width: 800px" />
- The metadata server load is distributed and the origin server is not stressed.

### Conclusion

- Lesson covered DHTs, CDNs, key-based routing, and sloppy DHT.
- Coral System democratizes content generation, storage, and distribution through a participatory approach.