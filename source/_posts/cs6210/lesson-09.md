# Lecture 09: Internet Computing

<!--
## Instruction
You are a teach assistant of the course of advanced operating system. This is the lecture of Internet Computing, which teaches Giant Scale Services, MapReduce, Content Delivery Networks. I will ask you a sequence of questions regarding the course. Use bullet points to answer all questions accurately, don't make up anything. And also make your answer easy to understand and easy to review. Provide more details if necessary.
## End of Instruction
-->

## L09a: Giant Scale Services

### Introduction

-   The module focuses on managing large data centers and internet scale computing.
-   The module addresses systems issues in managing large data centers, programming big data applications, and disseminating content on the web in a scalable manner.
-   The module builds on previous lessons to harden distributed systems issues and handle scale on the order of thousands of processes and failures.
-   Failures are inevitable, and the module will address how to handle them.

### Generic Service Model of Giant Scale Services

![](https://i.imgur.com/mZmtQ2W.png)

-   The web portal example used in the module is Gmail, a popular email service provided by Google.
-   The architecture within a site typically consists of thousands of servers, all interconnected through a high-bandwidth communication backplane, and connected to data stores to process incoming client requests.
-   The servers may optionally use a backplane that allows them to talk to one another for servicing any particular request, which helps to distribute the load evenly.
-   The load manager plays a crucial role in ensuring that the client traffic is balanced among all the servers, and no server is overloaded, which would cause the service to slow down or fail.
-   In addition to load balancing, the load manager also monitors the state of the servers and shields incoming client requests from any partial failures that may happen internally within a particular site.
-   The load manager typically uses various algorithms and techniques to balance the load, such as round-robin, least-connections, or IP hashing.
-   Embarrassingly parallel refers to the fact that the incoming client requests are all independent of one another and can be handled in parallel as long as there is enough server capacity to meet all the incoming requests. This is a characteristic of most giant scale services.

5.  Clusters as Workhorses

![](https://i.imgur.com/0XOda7V.png)


-   Computational clusters are the workhorses of giant scale services and are employed in modern data centers.
-   Each node in the cluster may itself be an SMP, and the advantages of structuring computational resources as a cluster of machines includes absolute scalability, cost and performance control, and incremental scalability.
-   Computational clusters offer incremental scalability by adding more nodes to the cluster to increase performance, or scaling back when the volume of requests decreases.

7.  Load Management Choices:

![](https://i.imgur.com/DmJCSlP.png)


-   Load management can be done at any of the seven layers of the OSI reference model, with higher layers offering more functionality in terms of dealing with server failures and directing incoming client requests.
-   Load managers operating at the transport level or higher can dynamically isolate down server nodes from the external world, have service-specific front end nodes, and co-opt client devices in load management.

8.  Load Management at Network Level:

-   Load management at the network level is done using round-robin DNS servers, which assign different IP addresses corresponding to different servers to incoming client requests for good load balance.
-   The assumption in this model is that all servers are identical and that data is fully replicated, so any incoming request can be sent to any server, and the data needed to satisfy the request is available.
-   The advantage of using round-robin DNS servers is good load balance, but the disadvantage is that it cannot hide down server nodes from the external world.

### DQ principle

![](https://i.imgur.com/6kVTPLF.png)


-   The DQ principle is used to manage incoming client requests and the data set available for handling those requests on a server.
-   The server has all the data required for dealing with incoming client queries, called the full data set (Df).
-   The offered load to the server is called Q0, which is the amount of requests hitting the server per unit time.
-   The yield (Q) is the ratio of completed requests to the offered load, and ideally should be one, but may be less than one if the server is not able to deal with the offered load entirely.
-   The available data set for processing each query may be less than the full data set due to failures of some data servers or the load on the server, and is called the harvest (Dv/Df).
-   The product DQ, representing the data server query and the rate of query coming into the server, is a constant for a given server capacity.
-   To increase the number of clients being served, the harvest can be decreased while keeping the yield the same.
-   To give the complete data that is needed for serving a query, the yield can be decreased while keeping the harvest constant.
-   DQ represents a system constant for the server's capacity, and the system administrator can choose to sacrifice yield for harvest or harvest for yield.
-   For network-bound applications, DQ is much more intuitive than traditional measures like I/O operations per second (IOOPS).
-   Uptime is another metric that system administrators use, but it is not very intuitive for giant-scale services because if there are no queries during the mean-time-to-repair (MTTR), then the uptime is not a good measure of how well a server is performing.
-   The DQ principle is powerful in advising the system administrator on how to architect the system, including how much to replicate, how much to partition the data set, and how to gracefully degrade the servers when the volume of incoming traffic increases beyond a server capacity.

![](https://i.imgur.com/4lfmAdl.png)
![](https://i.imgur.com/XfUMKgn.png)


Section 12: Online Evolution and Growth

![](https://i.imgur.com/VjbFQX7.png)

-   Services are continuously evolving, requiring upgrades to servers in data centers.
-   Fast reboot involves bringing down all servers at once to upgrade, resulting in complete loss of service for the duration of upgrade.
-   Rolling upgrade involves upgrading servers one at a time, resulting in service availability but with periodic DQ loss.
-   Big flip involves bringing down half the nodes at once to upgrade, resulting in 50% service availability for the duration of upgrade.
-   DQ loss is a constant, and system administrators have a choice in how they dish out the loss to the user community.

Section 13: Online Evolution and Growth (cont)

-   The DQ principle helps system designers optimize for yield or harvest for a given system capacity.
-   It also helps in coming up with explicit policies for graceful degradation of services during server failure, load saturation, or planned upgrades.

Section 14: Giant Scale Services Conclusion

-   Giant scale services are network bound, not disk I/O bound.
-   The DQ principle helps optimize service and plan for graceful degradation during various scenarios.

## L09b: MapReduce

1.  MapReduce Introduction:

-   Big data refers to large data sets that take a long time to compute.
-   Applications that work on big data need to exploit parallelism available in data centers.
-   Programming in the large requires parallelizing an application across many machines and handling data distribution and failure handling.

2.  MapReduce:

![](https://i.imgur.com/uh0tUTR.png)

-   MapReduce is a programming environment for dealing with big data applications.
-   The input to MapReduce is considered as a set of records identified by a key-value pair.
-   The MapReduce framework requires two user-defined functions: map and reduce.
-   Both map and reduce functions take key-value pairs as inputs and produce key-value pairs as outputs.
-   The example of finding specific names of individuals in a corpus of documents is used to explain the MapReduce framework.
-   The map function looks for unique names in the corpus of documents and outputs the number of times each name occurs in a file.
-   The reduce function aggregates the values from the map function and outputs the total number of occurrences for each unique name.
-   The programming environment handles the plumbing between the output of the map function and input of the reduce function, as well as other details such as the number of mapper and reducer instances required.

Section 3: Why MapReduce

![](https://i.imgur.com/6QszE4y.png)

-   MapReduce is a programming framework for big data applications.
-   Many processing steps in giant-scale services are expressible as MapReduce, such as seat availability searches, website frequency analysis, word indexing, and page ranking.
-   These applications are embarrassingly parallel and work on big datasets, making them ideal for taking advantage of the computation resources in a data center.
-   Domain expertise in the form of map and reduce functions is required from the app developer, but the programming system handles the heavy lifting such as instantiating mappers and reducers and data movement.

Section 4: Heavy Lifting Done by the Runtime

![](https://i.imgur.com/789SyjC.png)

-   The programming library splits the input key-value pairs into M splits and spawns a master and worker threads for map and reduce functions.
-   Mappers are assigned to worker threads and produce intermediate key-value pairs that are buffered in memory and periodically written to local disks.
-   Reducers are assigned to worker threads based on the number of unique keys specified by the app developer and pull data from all mappers using remote read.
-   Once all reducers have completed their work, the map reduce computation is complete.

Section 5: Heavy Lifting Done by the Runtime (cont)

-   The programming framework sorts input data from mappers and calls the user-supplied reduce function for each key with intermediate values.
-   Each reduce function writes to a final output file for its partition and notifies the master when it's done.
-   The master manages available resources to handle m and R splits and assigns workers to handle each split.

Section 6: Issues to be handled by the Runtime

-   Runtime system manages and map_reduce computation.
-   Master data structures include location of files created by mappers and namespace of files created by mappers.
-   Scoreboard keeps track of mappers and reducers currently assigned to work on different splits.
-   Fault tolerance is important, as a mapper may not respond in a timely manner, and master may assume it's dead and restart on a different node.
-   Locality management ensures that the working set of computations fits in the closest level of the memory hierarchy of a process.
-   Task granularity is important for good load balance of computational resources.
-   Programming framework offers several refinements to the basic model, such as overriding the partitioning function and combining function for mapping and reduce functions.

Section 7: MapReduce Conclusion

-   The power of MapReduce is its simplicity.
-   The domain expert only needs to write the Map and Reduce functions for their application.
-   The runtime system manages all the heavy lifting under the covers.

## L09c: Content Delivery Networks

Introduction

-   The internet and World Wide Web provide vast amounts of information to users.
-   Content creation happens both by individuals and businesses like CNN, BBC, and NBC.
-   This section will focus on content delivery networks (CDNs) and how information is stored and distributed.
-   Previous sections focused on the server end of giant scale services, data organization, and programming models for big data.
-   CDNs deal with the issue of scale in distributing information worldwide to users.

Summary of Section 3: DHT Introduction
![](https://i.imgur.com/6reJ4A9.png)

-   Content distribution networks allow for the distribution and storage of content on the internet
-   Key-value pairs are used to identify unique content and the location of the node where the content is stored
-   DHT, or distributed hash table, is a distributed solution to store key-value pairs on the internet
-   DHT uses a key-space namespace and node-space namespace to create unique signatures for content and IP addresses
-   The API for manipulating the DHT data structure includes putkey and getkey functions

Summary of Section 4: DHT Details
![](https://i.imgur.com/1BGPiiw.png)

-   DHT deals with the key-space namespace and node-space namespace
-   The key-space namespace is managed by generating a unique key for content using an algorithm like SHA-1
-   The node-space namespace is managed by creating an SHA-1 hash of IP addresses of nodes that want to share content
-   The objective of DHT is to store a key in a node ID that is very close to the key
-   The API for manipulating DHT includes putkey and getkey functions

Certainly! Here are some additional details on the topics covered in each section:

3.  DHT:

-   Content distribution networks (CDNs) are used to distribute user-generated content to others on the internet.
-   To distribute content, a content hash is created to ensure uniqueness of the content and is paired with the node ID of the computer where the content is stored.
-   The key-value pair is then stored in a distributed hash table (DHT), which is a distributed solution for storing key-value pairs so that they can be discovered by others.
-   The DHT works by storing key-value pairs on nodes whose IDs are close enough to the key itself.
-   The API for manipulating the DHT data structure includes putkey (to store a key-value pair) and getkey (to retrieve a value associated with a key-value pair).

4.  DHT Details:

-   The DHT manages two namespaces: the key-space namespace and the node-space namespace.
-   Content is disseminated using a unique key generated by an algorithm like SHA-1, which creates a 160-bit key.
-   Node IDs are created using the same algorithm, such as encoding IP addresses into a 160-bit node ID.
-   The objective is to store a key in a node ID such that the key is very close to the node ID, and the API for manipulating the DHT includes putkey and getkey.

5.  CDN (An Overlay Network):
![](https://i.imgur.com/7HqjOFt.png)

-   A CDN is an example of an overlay network, which is a virtual network on top of the physical network.
-   Overlay networks are used at the user level to map virtual addresses to IP addresses for sending messages.
-   User-level routing tables are constructed by exchanging mapping information between friends to discover one another and send messages.
-   Overlay networks allow content to be shared and distributed among a set of users who have exchanged information with one another.

6.  Overlay Networks in General:

-   Overlay networks are a general principle and exist at the operating system level, such as the IP network overlaying the local area network.
-   IP addresses translate to MAC addresses to traverse the local area network to reach the destination.
-   CDN is an overlay on top of TCP/IP, and a node ID maps to an IP address for sending messages.

7.  DHT and CDNs:
![](https://i.imgur.com/dOBg47Z.png)

-   DHT is an implementation vehicle for CDNs to populate the routing table at the user level.
-   Put operation is used for placement of key-value pairs, and get operation is used for retrieval of a value associated with a key-value pair.
-   The construction of the routing table involves storing key-value pairs on nodes and using the put and get operations to retrieve them.

Summary of section 8:
![](https://i.imgur.com/WApbZ7g.png)

-   The traditional approach for constructing a distributed hash table involves a greedy algorithm where a key value is placed in a node that is very close to the key, and when retrieving a key, the algorithm looks for the node closest to the key.
-   Routing tables at each node in the system only list the nodes that can be communicated with directly.
-   If a node is not in the routing table, the algorithm goes to a node that is close enough to the desired node, hoping that it will know how to communicate with the desired node.
-   The goal of the greedy approach is to get to the desired destination as quickly as possible with the minimum number of hops.

Summary of section 9:
![](https://i.imgur.com/L6CacoJ.png)

-   The greedy approach leads to a metadata server overload problem where a node that is closest to a key value pair becomes congested with traffic from puts and gets.
-   This creates a tree saturation problem where nodes in close proximity to the congested node also become congested.
-   If content becomes popular, there is also an origin server overload problem where the server hosting the content becomes inundated with download requests.
-   A content distribution network can solve the origin server overload problem by automatically mirroring content at geo-local sites and dynamically routing requests to the closest mirror.
-   However, this solution is expensive and not accessible to individual content providers.
-   The Coral System is a solution that democratizes content distribution and addresses both the metadata server overload and origin server overload problems.

Summary of section 10:
![](https://i.imgur.com/dvhuL4n.png)

-   The first solution to the origin server overload problem is to use a web proxy, but it is not suitable for dynamic content.
-   Content distribution networks solve the origin server overload problem but are expensive and not accessible to individual content providers.
-   The Coral System is a solution that democratizes content distribution and addresses both the metadata server overload and origin server overload problems.

11.  Greedy Approach Leads to Tree Saturation:
![](https://i.imgur.com/sP84B76.png)

-   The greedy approach of constructing a DHT leads to tree saturation which happens at the node that maps to a lot of clustered keys.
-   The coral approach avoids tree saturation by not being greedy and not necessarily storing the key K in the node N with an ID equal to K.
-   The Coral DHT implements a sloppy DHT that spreads metadata overload so that no single node in the democratic process of helping one another is saturated.
-   The distance between the source and the destination in Coral key-based routing is computed by XORing the bit patterns of the node IDs for the source and the destination.

12.  Key-Based Routing:
![](https://i.imgur.com/aVjeEY8.png)

-   The greedy approach is to get as close to the desired destination in the node ID namespace and ask a nearby node if it has a way of getting to the desired destination.
-   The objective in the greedy approach is reaching the destination with the fewest number of hops.
-   The Coral key-based routing slowly progresses towards the desired destination by going to some node that is half the distance to the destination in the node ID namespace in each hop.

13.  Coral Key-Based Routing:
![](https://i.imgur.com/IBcnqUd.png)

-   The Coral key-based routing reduces the distance by approximately half in each hop and avoids being greedy to avoid congestion and tree saturation.
-   The distance between the source and the destination is computed by XORing the bit patterns of the node IDs for the source and the destination.
-   In each hop, the Coral key-based routing goes to some node that is half the distance to the destination in the node ID namespace.

14.  Key-Based Routing in Coral:
![](https://i.imgur.com/zKcI0Q5.png)

-   In Coral key-based routing, the table is populated with the XOR distance of each node that is directly reachable from the source to the desired destination.
-   In each hop, the distance to the destination is reduced by half by going to a node that is approximately half the distance to the destination in the node ID namespace.
-   In each hop, the node may not have a direct way to reach the desired node, and a nearby node is contacted to obtain information on nodes that are close enough to the desired destination.

Section 15: Coral Sloppy DHT - Put Operation
![](https://i.imgur.com/x6q3TsB.png)

-   The primitives available in Coral for manipulating the sloppy DHT are put and get operations.
-   The put operation takes two parameters: Key and value.
-   Key is the content hash, and value is the node ID of the proxy with the content for that key.
-   Put can be initiated by the origin server or a node that wants to serve as a proxy.
-   The result of doing the put operation is to store this key value in some metadata server.
-   We need to place this key value in an appropriate node based on space and time metrics.
-   Full state means a particular node is already storing l values for a key.
-   Loaded is stating how many requests per unit time a node is willing to entertain for a particular key.
-   The Coral key-based routing algorithm reduces the distance by half to find the appropriate node to place the key.
-   We ask each node along the way if it is loaded or full, and if it is, we retract our steps and choose an appropriate node.
-   The Coral put operation chooses an appropriate node that is neither full nor loaded to entertain requests for retrieving the particular key value pair.

Section 16: Coral Sloppy DHT (cont) - Get Operation
![](https://i.imgur.com/5UOslTS.png)

-   The get operation works similarly to the put operation.
-   We go to a node that is half the distance to the key we are looking for.
-   If the content is popular, then multiple proxies may have gotten the key value pair.
-   They may have put their own node IDs as a potential node for the content.
-   Our metadata server may not necessarily have to be the destination which exactly matches that key.

Section 17: Coral in Action

-   Coral allows for user-generated content to be distributed in a democratic fashion.
-   The load for serving as a metadata server and content server can get naturally distributed.
-   Naomi creates a unique signature for her content and uses Coral to put it out on the internet.
-   Jacques uses Coral to get the content by following the key-based routing algorithm and ends up at David's computer.
-   Jacques serves as a proxy for the content and puts a new key value pair in the system.
-   Kamal also uses Coral to get the content and ends up getting it from Jacques, who serves as a proxy.
-   The metadata server load is distributed and the origin server is not stressed.

Section 18: Content Delivery Networks Conclusion

-   Coral offers a participatory approach to democratize content generation, storage, and distribution.
-   Commercial CDNs like Akamai contractually mirror content for customers and deploy their own mirrors to deal with increases in requests.
-   Lesson module on Internet Scale Computing is complete.