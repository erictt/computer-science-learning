# Internet Architecture

[TOC]

## The OSI Model(7 layers) vs The Traditional Model(5 layers)

* ![](/images/16616192098783.jpg)
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

* ![](/images/16616205278614.jpg)
* From the source, each layer encapsulates the message and add its own header to create transport-layer segment/datagram/frame. Then the message will be decapsulated and re-encapsulated at the switch/router for deciding where the message should go. At last the message will be decapsulated at the destination.

## The end-to-end (e2e) principle

* definition: specific application-level functions usually cannot, and preferably should not be built into the lower levels of the system at the core of the network. 
* the network core should be **simple and minimal**, while the **end systems** should carry the intelligence. 
    * The error correction on data link layer doesn't violate, because the entire error correction function can be implemented at the same layer.

### Violations of the End-to-End Principle 

* Cases where this principle needs to be violated. 
    1. firewalls and traffic filters. 
        * monitor the network traffic, either allow traffic to go through or drop traffic flagged as malicious.
    2. Network Address Translation (NAT) Boxes
        * Is the intermediate that take care of the communication between the hosts on the private network and the hosts on the public Internet. e.g. our home router.
            * ![](/images/16616228397008.jpg)
        * ![](/images/16616228486990.png)
            * **The translation table** provides a mapping between the public-facing IP address/ports and the IP addresses/ports that belong to hosts inside the private network.
        * Why NAT boxes violate e2e pinciple?
            * The hosts behind NAT are not globally addressable or routable. Not possible for hosts on the public Internet to initiate connections to these devices.
            * Workaround: 
                * STUN: enables hosts to discover NATs and the public IP address and port number that  the NAT has allocated for the applications for.
                * UDP hole punching: bidirectional UDP connections between hosts behind NATs.

## Interconnecting Hosts and Networks

Internet is a network of networks:

<img src="https://i.imgur.com/IXBYnsb.jpg" style="width:500px" />

The ways connectiing:

* Layer 1(physical layer): Repeaters and Hubs. Forward digital signals to connect different Ethernet segments.
* Layer 2(data link layer): Bridges and Layer2-Switches. not directly connected, based on MAC addresses. The limitaion is the finite bandwidth of the outputs.
* Layer 3(network layer): Routers and Layer3-Switches.

## Bridges & Switches

* A **bridge** is a **device** with multiple inputs/outputs which transfers frames from one to another (or multiple) outputs, used to connect two or more local area networks. 
    * A **learning bridge** learns, populates and maintains, a forwarding table. It only forward the frame that needs to be forward.

* how does the bridge learn? When the bridge receives any frame this is a “learning opportunity” to know which hosts are reachable through which ports. Because the bridge can view the port over which a frame arrives and the source host.