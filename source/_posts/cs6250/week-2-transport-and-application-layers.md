
# Lesson 2 : Transport and Application Layers

<!-- toc -->
----

## Introduction

* Transport layer provides a logical end-to-end transport between two endpoints:
    * <img src="https://i.imgur.com/Iacof30.jpg" style="width:500px" />
* Relationship between transport and network layer
    * Transport layer encapsulate the message from application layer with an additional header, which is called **segment**, and send to the the receiving host via routes/bridges/switches/etc.
* Transport layer allows application assuming a standard set of functionalities like packets delivery guarantee, data integrity, etc.

## Multiplexing

* **Multiplexing** is an ability for a host to run multiple application to use the network simultaneously. The transport layer use additional identifiers known as ports. Each application binds itself to a uniquie port number by opening sockets and listening for data from remote connection.

### Connection Oriented and Connectionless Multiplexing and Demultiplexing

* <img src="https://i.imgur.com/mVT8Gmq.jpg" style="width:500px" />

* Consider the scenario shown in the figure above, which includes three hosts running an application. A receiving host that receives an incoming transport layer segment will forward it to the appropriate socket. The receiving host identifies the appropriate socket by examining a set of fields in the segment. 
* The job of delivering the data included in the transport-layer segment to the appropriate socket, as defined in the segment fields, is called **demultiplexing**. 
    * Going up to application layer.
* Similarly, the sending host will need to gather data from different sockets and encapsulate each data chunk with header information (that will later be used in demultiplexing) to create segments, and then forward the segments to the network layer. We refer to this job as **multiplexing**. 
    * Going downstream with extra header(Encapsulate the mssage)

## Connectionless and Connection-Oriented Service

### Connectionless Service(UDP)

* The identifier of a UDP socket is a **two-tuple** that consists of **a destination IP address and a destination port number**. 
* Consider two hosts, A and B, which are running two processes at UDP ports a and b, respectively. Suppose that Host A sends data to Host B. The transport layer in Host A creates a transport-layer segment by the application data, the source port, and the destination port; and forwards the segment to the network layer. In turn, the network layer encapsulates the segment into a network-layer datagram and sends it to Host B with best-effort delivery. Then Host B identifies the correct socket by looking at the field of destination port, then use the info to demultiplex.
* <img src="https://i.imgur.com/48WMNml.jpg" style="width:500px" />
* <img src="https://i.imgur.com/WQ9esiM.jpg" style="width:500px" />
* Advantage of UDP:
    * no congestion control or similar mechanisms. no connection management overhead. which make it faster than TCP.

#### Checksum(an error checking mechanism):

* it's a basic error checking since there is no guarantee for link-by-link reliability. The UDP sender adds the bits of the source port, the destination port, and the packet length. It performs a 1's complement on the sum (all 0s are turned to 1 and all 1s are turned to 0s), which is the value of the checksum. The receiver adds all the four 16-bit words (including the checksum). The result should be all 1's unless an error has occurred. 

* Steps of checksum(https://www.youtube.com/watch?v=AtVWnyDDaDI):
    1. Break the original message into `k` number of blocks with `n` bits in each block
    2. Sum all the `k` data blocks
    3. Add the carry to the sum, if any.
    4. Do 1's complement to the sum(reverse the sum).
* Performance of checksum
    * The checksum detects all errors involving an odd number of bits.
    * In detects mosts erros involving an even number of bits.
    * If one or more bits of a segment are damaged and the correspoding bit or bits of oppsote value is a second segment are also damaged, the sums of those columns will not change and the receiver will not detect the error.
* UDP checksum calculation https://stackoverflow.com/questions/1480580/udp-checksum-calculation
* How is a 1s complement checksum useful for error detection? https://stackoverflow.com/questions/5607978/how-is-a-1s-complement-checksum-useful-for-error-detection

### Connection-Oriented Service(TCP)

* <img src="https://i.imgur.com/1h1pQVl.png" style="width:500px" />
* The identifier for a TCP socket is a four-tuple that consists of the **source IP, source port, destination IP, and destination port**. 
* Let’s consider the example of a TCP client-server as shown in the figure above. 
    * The TCP server has a listening socket that waits for connection requests coming from TCP clients. A TCP client creates a socket and sends a connection request, which is a TCP segment that has a source port number chosen by the client, a destination port number 12000, and a special connection-establishment bit set in the TCP header. 
    * Finally, the TCP server receives the connection request, and the server creates a socket that is identified by the four-tuple source IP, source port, destination IP, and destination port. 
    * The server uses this socket identifier to demultiplex incoming data and forward them to this socket. Now, the TCP connection is established and the client and server can send and receive data between one another.    

* an example connection establishment.
    * <img src="https://i.imgur.com/nIodUGD.png" style="width:500px" />
* Why don't UDP/TCP use process IDs rather than defin port numbers?
    * Process IDs are specific to OS, therefore use process IDs make the protocol dependent to OS. Also a process should can set up multiple channels.
* How a single port used for creating multiple conenctions with client?
    * Because TCP is identified by a 4-tuple(source IP, source port, dest IP, dest port). When binding socket with TCP, it uses the 4-tuple. So a server creates different sockets for multiple sockets that binded with the same IP/port.
    * https://stackoverflow.com/questions/11129212/tcp-can-two-different-sockets-share-a-port#:~:text=Thanks%20%3AD&text=%40premktiw%3A%20Yes%2C%20multiple%20client,local%2Bremote%20pairs%20are%20unique.

## The TCP Three-Way Handshake

* Step 1: The TCP client sends a special segment (containing no data) with the SYN bit set to 1. The client also generates an initial sequence number (**client_isn**) and includes it in this special TCP SYN segment.
* Step 2: The server, upon receiving this packet, allocates the required resources for the connection and sends back the special "connection-granted" segment which we call SYNACK segment. This packet has the SYN bit set to 1, the acknowledgement field of the TCP segment header set to **client_isn+1**, and a randomly chosen initial sequence number (**server_isn**) for the server.  
* Step 3: When the client receives the SYNACK segment, it also allocates buffer and resources for the connection and sends an acknowledgment with SYN bit set to 0.

* <img src="https://i.imgur.com/rqDwUPE.png" style="width:500px" />

### Connection Teardown

* Step 1: When the client wants to end the connection, it sends a segment with FIN bit set to 1 to the server.
* Step 2: The server acknowledges that it has received the connection closing request and is now working on closing the connection.
* Step 3: The server then sends a segment with FIN bit set to 1, indicating that connection is closed.
* Step 4: The client sends an ACK for it to the server. It also waits for sometime to resend this acknowledgment in case the first ACK segment is lost.
* <img src="https://i.imgur.com/3kzN0XX.png" style="width:500px" />

## Reliable Transmission

* TCP guarantees in-order delivery of the application-layer data without any loss or corruption. How to achieve? Below are various methods that can be implemented.

* ARQ(Automatic Repeat Request)
    *  If the sender does not receive an acknowledgment within a given period of time, the sender can assume the packet is lost and resend it. 
* Stop and Wait ARP
    * The sender to send a packet and wait for its acknowledgment from the receiver, then resend if timeout.
    * Typically the timeout value is a function of the estimated **round trip time (RTT)** of the connection. 
    * one of the ways for improvement of this method is send at most N unacknowledged packets, which referred as window size.
    * another one is called **Go-back-N**. The receiver can simply discard any out-of-order received packets.
        * <img src="https://i.imgur.com/6KlIECw.png" style="width:500px" />

### Selective ACKing

* The sender **retransmits only those packets that it suspects were received in error**. Then, the receiver would acknowledge a correctly received packet even if it is not in order. The out-of-order packets are buffered until any missing packets have been received, at which point the batch of the packets can be delivered to the application layer. 
* Note that, even in this case, TCP would need to use a **timeout** as there is a possibility of ACKs getting lost in the network. 
* In addition to using a timeout to detect loss of packets, TCP also uses **duplicate acknowledgments as a means to detect packet loss**. A duplicate ACK is an additional acknowledgment of a segment for which the sender has already received acknowledgment earlier. When the sender receives 3 duplicate ACKs for a packet, it considers the packet to be lost and will retransmit it instead of waiting for the timeout. This is known as fast retransmit. For example, in the figure below, once the sender receives 3 duplicate ACKs, it will retransmit packet 7 without waiting for a timeout.
* <img src="https://i.imgur.com/2dSE05y.png" style="width:500px" />

## Transmission Control

### Flow control

* The goal is to control the Transmission Rate to Protect the Receiver buffer.
    * Consider hosts A and B. The sender A maintain a variable **receive window(rwnd) = RcvBuffer - [LastByteRcvd - LastByteRead]**
        * **LastByteRead**: the number of the last bytes in the data stream read from the buffer by the application process in B
        * **LastByteRcvd**: the number of the last bytes in the data stream that has arrived from the network and has been placed in the receive buffer at B
    * <img src="https://i.imgur.com/kHW8UYr.png" style="width:500px" />
    * The receiver advertises the value **rwnd** in every segment/ACK it sends back to the sender. The sender also keeps track of two variables, **LastByteSent** and **LastByteAcked**. 
    * To not overflow the receiver’s buffer, the sender must ensure that the maximum number of unacknowledged bytes it sends is no more than the **rwnd**. Thus we need
        * **LastByteSent – LastByteAcked  <= rwnd**
    * **Caveat**: if receiver inform sender that rwnd is 0, and the sender stop sending message, then sender will never know new buffer space is available. TCP resolves this by sending segments of size 1 byte even after **rwnd = 0**.

### Congestion control

* The goal is to control the transmission rate to protect the network from congestion.
* Congestion control means to avoid the tramsmission rate of a set of senders greater than the capacity of receiver.
* Desired properties:
    * **efficiency**. go high throughput.
    * **fairness**. either every flow has equal bandwidth or other policies.
    * **low delay**. packets get stored in the buffer and wait for a long queue get delivered need to be avoid.
    * **fast convergence**. The idea here is that a flow should converge to its fair allocation fast. Fast convergence is crucial since a typical network’s workload is composed of many short flows and few long flows. If the convergence to fair share is not fast enough, the network will still be unfair for these short flows.
* Two approaches:
    * **network-assisted congestion control**. Rely on network layer, use ICMP souce quench to notify the source that the network is congested. but even ICMP packets can be lost under severe congestion.
    * **implement end-to-end congestion control**(TCP use) the hosts infer congestion from the network behavior and adapt the transmission rate. Congestion control is a primitive provided in the transport layer, whereas routers operate at the network layer. Therefore, the feature resides in the end nodes with no support from the network. 
        * Note that this is no longer true as certain routers in the modern networks can provide explicit feedback to the end-host by using protocols such as [ECN](https://en.wikipedia.org/wiki/Explicit_Congestion_Notification) and [QCN](https://web.stanford.edu/~balaji/presentations/au-prabhakar-qcn-description.pdf).  
* How a host infers congestion? via signs of congestion:
    * **packet delay**. As the network becomes congested, the queues in the router buffers build-up, leading to increased packet delays. Thus, an increase in the round trip time, which can be estimated based on ACKs, can indicate congestion in the network. However, it turns out that packet delays in a network tend to be variable, making delay-based congestion inference quite tricky. 
    * **packet loss**. As the network gets congested, routers start dropping packets. Note that packets can also be lost due to other reasons such as routing errors, hardware failure, time-to-live (TTL) expiry, error in the links, or flow control problems, although it is rare. 
* The earliest implementation of TCP used packet loss as a signal for congestion. This is mainly because TCP already detected and handled packet losses to provide reliability.

* **How Does a TCP Sender Limit the Sending Rate?**
    * TCP congestion control was introduced so that each source can do the following:
        * First, determine the network's available capacity.
        * Then, choose how many packets to send without adding to the network's congestion level.
    * Each source uses ACKs as a packing mechanism. If the receiving host received a packet sent earlier, it would release more packets into the network.
    * TCP uses a **congestion window(cwnd)** similar to the **receive window(rwnd)** used for flow control. It represents the **maximum number of unacknowledged data** that a sending host can have in transit (sent but not yet acknowledged).
    * TCP uses a **probe-and-adapt approach** in adapting the congestion window. Under normal conditions, TCP increases the congestion window trying to achieve the available throughput. Once it detects congestion, the congestion window is decreased.
    * In the end, the number of unacknowledged data that a sender can have is the minimum of the congestion window and the receive window. 
        * **LastByteSent – LastByteAcked <= min{cwnd, rwnd}**
    * In a nutshell, a TCP sender cannot send faster than the slowest component, which is either the network or the receiving host.

## Congestion Control at TCP - AIMD     

* TCP decreases the window when the level of congestion goes up, and it increases the window when the level of congestion goes down. We refer to this combined mechanism as **additive increase/multiplicative decrease (AIMD)**.    

### Additive Increase (AI)

* The connection starts with a constant initial window, typically 2, and increases it additively. The idea behind additive increase is to increase the window by one packet every RTT (Round Trip Time). So, in the additive increase part of the AIMD, every time the sending host successfully sends a CongestionWindow (**cwnd**) number of packets it adds 1 to **cwnd**. 
* Also, in practice, this increase in AIMD happens incrementally. TCP does not wait for ACKs of all the packets from the previous RTT. Instead, it increases the congestion window size as soon as each ACK arrives. In bytes, this increment is a portion of the **MSS (Maximum Segment Size)**. 
* `Increment = MSS × (MSS / CongestionWindow)`
* `CongestionWindow += Increment`
* <img src="https://i.imgur.com/IytxuUe.png" style="width:500px" />

### Multiplicative Decrease (MD)

* Once TCP detects congestion, it reduces the rate at which the sender transmits. So, when the TCP sender detects that a loss event has occurred, then it sets **cwnd** to half of its previous value. This decrease of the **cwnd** for each timeout corresponds to the **“multiplicative decrease”** part of AIMD. For example, suppose the **cwnd** is currently set to 16 packets. If a loss is detected, then cwnd is set to 8. Further losses would result in the **cwnd** to be reduced to 4, and then to 2, and then to 1. The value of **cwnd** cannot be reduced further than a value of 1 packet.
* TCP continually increases and decreases the congestion window throughout the lifetime of the connection. If we plot **cwnd** with respect to time, we observe that it follows a sawtooth pattern as shown in the figure:
* <img src="https://i.imgur.com/I4g6waG.png" style="width:500px" />

### AIAD - MIMD - MIAD

* Would all thse polices conver? If so, what's the diff from AIMD?
    * https://inst.eecs.berkeley.edu/~ee122/fa08/notes/19-TCPAdvancedx6.pdf

### TCP Reno

* There are different implementations of TCP that use variations to control congestion and maximize bandwidth usage. 
* For example, **TCP Reno** uses two types of loss events as a signal of congestion.
    * The first is **triple duplicate ACKs** and is considered to be mild congestion. In this case, the congestion window is reduced to half of the original congestion window.
    * The second is **timeout**, i.e. when no ACK is received within a specified amount of time. It is considered a more severe form of congestion, and the congestion window is reset to the initial window size. 
    * <img src="https://i.imgur.com/WD3dhRx.png" style="width:500px" />
* Lastly, "**probing**" refers to the fact that **a TCP sender increases its transmission rate to probe for the rate** at which congestion onset begins, backs off from that rate, and then begins probing again to see if the congestion onset rate has changed. 

### Slow start in TCP

* When we have a new connection that starts from a cold start, the sending host can take much longer to increase the congestion window by using AIMD. So for a new connection, we need a mechanism that can rapidly increase the congestion window from a cold start. 
* To handle this, TCP Reno has a **slow start phase** where the congestion window is increased exponentially instead of linearly, as in the case of AIMD. Once the congestion window becomes more than a threshold, often called the **slow start threshold**, it starts using AIMD. 
* <img src="https://i.imgur.com/9jxB0II.png" style="width:500px" />
* <img src="https://i.imgur.com/Skm8mvO.png" style="width:500px" />
* Slow start is called “slow” start despite using an exponential increase because, in the beginning, it sends only one packet and starts doubling it after each RTT. Thus, it is slower than starting with a large window. 

* Finally, we note that there is one more scenario where slow start kicks in: __when a connection dies while waiting for a timeout to occur__. This happens when the source has sent enough data as allowed by the flow control mechanism of TCP but times out while waiting for the ACK. Thus, the source will eventually receive a cumulative ACK to reopen the connection. Then, instead of sending the available window size worth of packets at once, it will use the slow start mechanism.

* In this case, the source will have a fair idea about the congestion window from the last time it had a packet loss. It will now use this information as the “target” value to avoid packet loss in the future. This target value is stored in a temporary variable, **CongestionThreshold**. Now, the source performs slow start by doubling the number of packets after each RTT until the value of **cwnd** reaches the congestion threshold (a knee point). After this point, it increases the window by 1 (additive increase) each RTT until it experiences packet loss (cliff point). After which, it multiplicatively decreases the window.
* <img src="https://i.imgur.com/tpHmIkv.jpg" style="width:800px" />


### TCP Fairness

* The goal is to get the throughput achieved for each link to fall somewhere near the intersection of the **equal bandwidth share line** and the **full bandwidth utilization line**, as shown in the graph below:
    * <img src="https://i.imgur.com/ADBvj7v.png" style="width:500px" />
* At point A in the above graph, the total utilized bandwidth is less than capacity R, so no loss can occur at this point. Therefore, both the connection will increase their window size. Thus, the utilized bandwidth's sum will grow, and the graph will move towards B.
* At point B, as the total transmission rate is more than capacity R, both connections may start having packet loss. As a result, they will decrease their window size to half and move towards point C.
* At point C, the total throughput is again less than R, so both connections will increase their window size to move towards point D and will experience packet loss at D, and so on.
* Thus, using AIMD leads to fairness in bandwidth sharing.

#### cases that TCP is not fair

* , connections with smaller RTT values would increase their congestion window faster than those with longer RTT values.
* a single application uses multiple parallel TCP connections.

## TCP CUBIC

* To make TCP more efficient under high bandwidth delay product networks, **TCP CUBIC** is one of the improvements that implemented in Linux kernel.
* Let us see what happens when TCP experiences a triple duplicate ACK, say at window=Wmax. This could be because of congestion in the network. To maintain TCP-fairness, it uses a multiplicative decrease and reduces the window to half. Let us call this Wmin. 
* Now, we know that the optimal window size would be in between Wmin and Wmax  and closer to Wmax. So, instead of increasing the window size by 1, it is okay to increase the window size aggressively in the beginning. Once the W approaches closer to Wmax, it is wise to increase it slowly because that is where we detected a packet loss last time. Assuming no loss is detected this time around Wmax, we keep on increasing the window a little bit. If there is no loss still, it could be that the previous loss was due to a transient congestion or non-congestion related event. Therefore, it is okay to increase the window size with higher values now. 
    * <img src="https://i.imgur.com/ISc6Z8N.png" style="width:500px" />

* This window growth idea is approximated in TCP CUBIC using a cubic function. Here is the exact function it uses for the window growth:
    * $$W(t) = C(t-K)^3 + W_{max}$$

* Here, Wmax is the window when the packet loss was detected. Here C is a scaling constant, and K is the time period that the above function takes to increase W to Wmax when there is no further loss event and is calculated by using the following equation:
    * $$K = \sqrt[3]{\frac{W_{max}B}{C}}$$

* It is important to note that time here is the time elapsed since the last loss event instead of the usual ACK-based timer used in TCP Reno. This also makes TCP CUBIC RTT-fair. 
    * The window growth depends **only on the time between two consecutive congestion events**. One congestion event is the time when TCP undergoes fast recovery. This feature allows CUBIC flows competing in the same bottleneck to have approximately the same window size independent of their RTTs, achiveing good RTT-fairness.

### The TCP Protocol: TCP Throughput    

* With AIMD, the congestion window increases by 1 packet every RTT. When loss is detected, the `cwnd` is cut in half.
* We have a simple model that predicts the throughput for a TCP connection.
* Assume p = the probability loss, and network delivers 1 out of every p consecutive packets, followed by a single packet loss.
    * <img src="https://i.imgur.com/u29aqEh.png" style="width:500px" />
* Because the congestion window(`cwnd`) size increase a constant rate of 1 packet for every RTT, the height of the sawtooth is W/2, the width of the base is W/2, which corresponds to W/2 round trips, or RTT * W/2.
* The number of packets sent in one cycle is the area under the sawtooth. Therefore, the total number of packets sent is:
    * $(\frac{W}{2})^2 + \frac{1}{2}(\frac{W}{2})^2 = \frac{3}{8}W^2$
* As stated in our assumptions about our lossy network, it delivers 1/p packets followed by a loss. So we have:
    * $\frac{1}{p} = \frac{3}{8}W^2$
    * and sloving for W gives the max value $W = \sqrt{\frac{8}{3p}} = 2 \cdot \sqrt{\frac{2}{3p}}$
* The rate that data that is transmitted, i.e., throughput/bandwidth, BW, is computed as:
    * BW = data per cycle / time per cycle
* We got:
    * $BW = \frac{\text{data per cycle}}{\text{time per cycle}} = \frac{MSS \cdot \frac{3}{8} W^2}{RTT \cdot \frac{W}{2}} = \frac{\frac{MSS}{p}}{RTT \sqrt{\frac{2}{3p}}}$
* We can connect all of our constants into $C = \frac{3}{2}$, and compute the bandwidth:
    * $BW = \frac{MSS}{RTT} \cdot \frac{C}{\sqrt{p}}$
* In practice, because of additional parameters, such as small receiver windows, extra bandwidth availability, and TCP timeouts, our constant term C is usually less than 1. This means that bandwidth is bounded:
    * * $BW < \frac{MSS}{RTT} \cdot \frac{1}{\sqrt{p}}$

## TCP in Datacenter

* data center (DC) networks are other networks where new TCP congestion control algorithms have been proposed and implemented. There are mainly two differences that have led to this:
    1. The flow characteristics of DC networks are different from the public Internet. For example, there are many short flows that are sensitive to delay. Thus, the congestion control mechanisms are optimized for delay and throughput, not just the latter alone.
    2. A private entity often owns DC networks. This makes changing the transport layer easier since the new algorithms do not need to coexist with the older ones. 
* DCTCP and TIMELY are two popular examples of TCP designed for DC environments. DCTCP is based on a hybrid approach of using both implicit feedback, e.g., packet loss, and explicit feedback from the network using ECN for congestion control. TIMELY uses the gradient of RTT to adjust its window. 

## Terms

* **Round-trip time (RTT)** is the duration in milliseconds (ms) it takes for a network request to go from a starting point to a destination and back again to the starting point.
    * https://www.cloudflare.com/learning/cdn/glossary/round-trip-time-rtt/
