---
weight: 1
title: "Lesson 01: Internet Architecture"
---

# Lesson 1: Internet Architecture

<!-- toc -->
----

## The OSI Model(7 layers) vs The Traditional Model(5 layers)

* <img src="https://i.imgur.com/BE8yWY4.jpg" style="width:600px" />
* In the traditional model, the application, presentation, and session layers are combined into a single layer, and this combined layer is called the application layer. **The interface between the application layer and the transport layer are the sockets.** It is up to the application developer to design the functionality of the overall application.

### the OSI design

* **application layer**: multiple protocols. e.g. http, smtp, ftp, etc.
* **presentation layer**: intermdediate role of formatting info. e.g. format video stream, translate integers from big endian to little endian format.
* **session layer**: manage different transport streams belong to the same session between end-user application process. e.g. tie together audio and video stream.
* **transport layer**: two protocols: TCP and UDP.
  * TCP: guaranteed delivery of the application-layer messages, flow control, congestion-control, etc.
  * UDP: connetionless best-effort to the applicaiton.
* **network layer**: moving **datagrams** from one Internet host to another. Two protocols: IP and routing.
  * IP: define the fields in datagram and the method soruce/dest hosts interact with intermediate routers.
  * Routing protocols: define the routes that datagrams flow from source to dest
* **data link layer**: move the **frames**(packets of information) from one node to the next. protocol examples: Ethernet, PPP, WIFI.
* **physical layer**: actual hardware. transfer bits within a frame between two nodes. e.g.  twisted-pair copper wire, coaxial cable, and single-mode fiber optics.

## Encapsulation and De-encapsulation

* <img src="https://i.imgur.com/uLuBH5F.jpg" style="width:600px" />
* From the source, each layer encapsulates the message and add its own header to create transport-layer segment/datagram/frame. Then the message will be decapsulated and re-encapsulated at the switch/router for deciding where the message should go. At last the message will be decapsulated at the destination.

## The end-to-end (e2e) principle

* definition: specific application-level functions usually cannot, and preferably should not be built into the lower levels of the system at the core of the network.
* the network core should be **simple and minimal**, while the **end systems** should carry the intelligence.
  * The error correction on data link layer doesn't violate, because the entire error correction function can be implemented at the same layer.

### Violations of the End-to-End Principle

* Cases where this principle needs to be violated.
    1. firewalls and traffic filters.
        * monitor the network traffic, either allow traffic to go through or drop traffic flagged as malicious.
    2. Network Address Translation (NAT) Boxes is the mediator that take care of the communication between the hosts on the private network and the hosts on the public Internet. e.g. our home router.
        * <img src="https://i.imgur.com/zC7ltM3.jpg" style="width:500px" />
        * **The translation table** provides a mapping between the public-facing IP address/ports and the IP addresses/ports that belong to hosts inside the private network.
            * <img src="https://i.imgur.com/29DCQlU.png" style="width:500px" />
        * Why NAT boxes violate e2e principle?
            * The hosts behind NAT are not globally addressable or routable. Not possible for hosts on the public Internet to initiate connections to these devices.
            * Workaround:
                * STUN: enables hosts to discover NATs and the public IP address and port number that  the NAT has allocated for the applications for.
                * UDP hole punching: bidirectional UDP connections between hosts behind NATs.

## The Hourglass Shape of Internet Architecture

* In brief, IP has been a crucial layer for the whole internet architecture, which resembled the hourglass shape of the layered Internet:
  * <img src="https://i.imgur.com/DvtgDuY.jpg" style="width:300px" />
* A model called the Evolutionary Architecture model helped to understand the evolution in a quantitative manner. The main idea is, if we introduce another protocol to replace IP, and it's powerful enough to compete IP, eventually it will become the new critical path. This change won't widen the waist of the hourglass. A network architect should try to design the functionality of each layer consisting several protocols that offer largely **non-overlapping but general** services, so that they **do not compete** with each other.

## Interconnecting Hosts and Networks

Internet is a network of networks:

<img src="https://i.imgur.com/IXBYnsb.jpg" style="width:500px" />

The ways they connect:

* Layer 1(physical layer): Repeaters and Hubs. Forward digital signals to connect different Ethernet segments.
* Layer 2(data link layer): Bridges and Layer2-Switches. not directly connected, based on MAC addresses. The limitation is the finite bandwidth of the outputs.
* Layer 3(network layer): Routers and Layer3-Switches.

## Bridges

* A **bridge** is a **device** with multiple inputs/outputs which transfers frames from one to another (or multiple) outputs, used to connect two or more local area networks(at the data link layer).
  * A **learning bridge** learns, populates and maintains, a forwarding table. It only forward the frame that needs to be forward.

* how does the bridge learn? When the bridge receives any frame this is a “learning opportunity” to know which hosts are reachable through which ports. Because the bridge can view the port over which a frame arrives and the source host.

### The looping problem in bridges

* how does the looping problem exist? two possible reasons:
    1) each bridge doesn't know the entire configuration of the network, it's possible the fragment will be froward back to itself;
    2) more likely, the loops are built in purpose of redundancy in case of failure.
* how to solve it? **The spanning tree algorithm**. The algorithm is used to build a network topology that has no loops and reaches all LANs in the local network. In practice, it is by removing ports from the topology that the extended LAN is reduced to an acyclic tree. The algorithm can help to prevent broadcast storms[Quiz].
  * The figure below shows the final state of the spanning tree. In this example, B1 is the root bridge, since it has the smallest ID. Notice that both B3 and B5 are connected to LAN A, but B5 is the designated bridge since it is closer to the root. Similarly, both B5 and B7 are connected to LAN B, but in this case B5 is the designated bridge since it has the smaller ID; both are an equal distance from B1.
    * <img src="https://i.imgur.com/5UDqRVT.jpg" style="width:500px" />
    * Note that the root node is not always in the center, the network administrators can configure the switch ID to have a specific spanning tree[Quiz]. And the inactive links will not be forwarded traffic, but still reachable for future updates[Quiz].
    * For more details: <https://www.sciencedirect.com/topics/computer-science/spanning-tree-algorithm>

### Comparing to other network connecting devices

* **Repeaters and Hubs**: They operate on the physical layer **(L1)**, as they **receive and forward digital signals** to connect different Ethernet segments. They provide connectivity between hosts that are directly connected **(in the same network)**. The advantage is that they are simple and inexpensive devices, and they can be arranged in a hierarchy. Unfortunately, hosts that are connected through these devices belong to the same **collision domain**, meaning that they compete for access to the same link.
  * **Repeater**: sometimes can regenerates signals bit-by-bit when the signal is week.

* **Bridges and Layer2-Switches**: These devices can enable **communication between hosts that are not directly connected**. They operate on the data link layer **(L2)** **based on MAC addresses**. They receive packets and they forward them to reach the appropriate destination. A limitation is the finite bandwidth of the outputs. If the arrival rate of the traffic is higher than the capacity of the outputs then **packets are temporarily stored in buffers**. But if the buffer space gets full, then this can lead to **packet drops**.
  * **Bridge**: mainly used to segment a network to allow a large network size. Also has filtering capability.
  * **Layer2-Switch**: acts as a multiport bridge in the network. It provides the bridging functionality with greater efficiency. It does not forward packets that have errors and forward good packets selectively to the correct port only.
* **Routers and Layer3-Switches**: These are devices that operate on Layer 3. We will talk more about these devices and the routing protocols in the upcoming lectures.
  * **Router** normally connect LANs and WANs together and have a dynamically updating routing table based on which they make decisions on routing the data packets.

* refers:
  * <https://afteracademy.com/blog/what-are-routers-hubs-switches-bridges>
  * <https://www.tutorialspoint.com/network-devices-hub-repeater-bridge-switch-router-gateways-and-brouter>
  * <https://www.geeksforgeeks.org/network-devices-hub-repeater-bridge-switch-router-gateways/>
