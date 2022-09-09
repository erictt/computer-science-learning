# Introduction

[toc]

## What is the Internet?

* A network of networks
    * <img src="https://i.imgur.com/IXBYnsb.jpg" style="width:500px" />

* In Internet, all devices are called **hosts** or **end systems**. End systems are connected together by a network of **communication links** and **packet switches**. The links are made up of different types of physical media, including copper, fiber, etc. Different links can transmit data at different rates. **Transmisssion rate** measured in bits/second. The data sending in between end systems called **packets**.
* End systems access the Internet through **Internet Service Providers(ISPs)**, which provide a vareity of types of network accesss to the end systems.
* Internet standards are developed by the Internet Engineering Task Force (IETF) [IETF 2020]. The IETF standards documents are called **requests for comments (RFCs)**.
* A **protocol** defines the format and the order of messages exchanged between two or more communicating entities, as well as the actions taken on the transmission and/or receipt of a message or other event.

## How we access the network?

1. cable-based access
    * <img src="https://i.imgur.com/Y0ZYH7i.jpg" style="width:400px" />
    * **Frequency Division Multiplexing (FDM)**: different channels transmitted in different frequency bands
    * network of cable, fiber attaches homes to ISP router
    * Ethernet: wired access at 100Mbps, 1Gbps, 10Gbps 

2. wireless access
    * Wireless local area networks (WLANs)
        * typically within or around building (~100 ft)
        * 802.11b/g/n (WiFi): 11, 54, 450 Mbps transmission rate
        * Additionally, ac/ax: 1300 Mbps and 10Gbps
        * https://www.signalboosters.com/blog/ieee-802.11-standards-explained-802.11abgnacax/

* How host-sending function work?
    * the host breaks the application messages into small chunks, known as **packets**, of length **L** bits, and transmits the packet into access network at **transmission rate R** (aka link bandwidth)
        * packet transmission delay = time needed to transmit L-bit packet into link = $\frac{L\text{(bits)}}{R\text{(bits/sec)}}$

* What physical media are used for data transmission?
    * **Twisted pair(TP)**
        * two insulated copper wires
            * Category 5: 100 Mbps, 1Gbps Ethernet
            * Cat 6: 10 Gbps Ethernet
    * Coaxial cable
        * two concentric copper conductors, limited bandwidth: 100 Mbps
    * **Fiber optic cable**
        * glass fiber carrying light pulses, each pulse a bit
        * high-speed(10-100Gbps), low error rate
    * The others:
        * wireless radio
        * WiFi
        * 4G/5G
        * Bluetooth
        * terrestrial microwave
        * satellite


## How data are transfered in the Internet?

* Two key functions:
    * **Packet switching/forwarding**
        * hosts break application-layer messages into packets and forwards them from one router to another
    * **Routing**
        * determine source-destination pathes takens by packets base on routing algorithms
* Packet-switching: **store-and-forward**
    * packet transmission delay: takes **L/R** seconds to transmit **L-bit** packet into link at **R** bps
        * e.g. L = 10Kbits; R = 100 Mbps, one-hoe transmission delay = 0.1m/sec
    * store-and-forward: entire packet must arrive(will explain why must have entire packet later) at router before it can be transmmitted on next link
* Packet-switching: **queueing**
    * <img src="https://i.imgur.com/da9IqzA.jpg" style="width:500px" />
    * **Packet queuing and loss**: if arrival rate (in bps) to link exceeds transmission rate (bps) of link for some period of time:
        * packets will queue, waiting to be transmitted on output link 
        * packets can be dropped (lost) if memory (buffer) in router fills up
* Alternative to packet switching: **circuit switching**
    * end-end resources allocated to, reserved for “call” between source and destination. Commonly used in traditional telephone networks
    * <img src="https://i.imgur.com/1uOr4TL.jpg" style="width:300px" />
    * in diagram above, each link has four circuits. Call gets 2nd circuit in top link and 1st circuit in right link. There is no sharing among the circuits which guaranteed the performance of each circuit.
    * Frequency Division Multiplexing (FDM) vs Time Division Multiplexing (TDM)
        * FDM: optical, electromagnetic frequencies divided into (narrow) frequency bands
        * TDM: time divided into slots
        * <img src="https://i.imgur.com/budDdjN.jpg" style="width:300px" />

* Internet sturcture
    * <img src="https://i.imgur.com/qbmSenx.jpg" style="width:600px" />
    * <img src="https://i.imgur.com/ZeBxteW.jpg" style="width:500px" />
    * At “center”: small # of well-connected large networks
        * “tier-1” commercial ISPs (e.g., Level 3, Sprint, AT&T, NTT), national & international coverage 
        * content provider networks (e.g., Google, Facebook): private network that connects its data centers to Internet, often bypassing tier-1, regional ISPs

## How do packet delay and loss occur?

* How data are transmitted:
    * <img src="https://i.imgur.com/qpU1Gfy.jpg" style="width:500px" />
* Packet delay: $d_{\text{nodal}} = d_{\text{proc}} + d_{\text{queue}} + d_{\text{trans}} +  d_{\text{prop}}$
    1. $d_{\text{proc}}$ **nodal processing**
        * check bit errors
        * determine output link
        * typically < microsecs
    * $d_{\text{queue}}$: **queueing delay**
        * time waiting at output link for transmission 
        * depends on congestion level of router
    * $d_{\text{trans}}$: **transmission delay**
        * L: packet length (bits) 
        * R: link transmission rate (bps)
        * $d_{\text{trans}} = L/R$
    * $d_{\text{prop}}$: **propagation delay**
        * d: length of physical link
        * s: propagation speed (~2x108 m/sec)
        * $d_{\text{prop}} = d/s$
* Packet loss
    * <img src="https://i.imgur.com/AIUCKjo.jpg" style="width:300px" />
* How to calculate the **throughput** from sender to receiver?
    * Two ways to measure: 
        * instantaneous: rate at given point in time
        * average: rate over longer period of time
    * <img src="https://i.imgur.com/UuXSLZB.jpg" style="width:300px" />
    * per-connection end-end throughput: min(Rc,Rs,R/10)

## What are the Protocol Layers and Their Service Models?

* Layers:
    * **application**: **application-layer message**, supporting applications like:
        * HTTP, IMAP, SMTP, DNS
    * **transport**: process data transfer
        * TCP, UDP
        * the **segment** this layers added is used for error-detection and also make sure the message is unchanged
    * **network**: routing of **datagrams** from source to destination
        * IP, routing protocols
        * This layer adds end system addresses in the datagram.
    * **link**: data transfer between neighboring network elements
        * Ethernet, 802.11 (WiFi), PPP
        * This layer has two types of fields: header and payload, the payload is typically a packet from the layer above.
    * **physical**: bits “on the wire”


* From the source, each layer **encapsulates** the message and add its own header to create transport-layer **segment/datagram/frame**. Then the message will be decapsulated and re-encapsulated at the switch/router for deciding where the message should go. At last the message will be decapsulated at the destination.
