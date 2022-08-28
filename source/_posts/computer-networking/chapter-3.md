# The Transport Layer

## Port & Socket

* **Port** is logical construct that **identifies** a specific process at the software level. it's ranging 0 - 65535 (2^16). The ports from 0-1023 are used by system processes, such as SSH, FTP, SMTP, etc. 
    * The full list of ports: https://en.wikipedia.org/wiki/List_of_TCP_and_UDP_port_numbers
* **Socket** is used for transfering data between two endpoints over ports.
* Frankly speaking, there are lots of applications running on our computers. The OS needs to identify which application should get the data that the computer received via the network. IP and Port are used to identify that.

## Multiplexing and Demultiplexing

* multiplexing and demultiplexing happen at not just transport layer but all layers.
* On the **transport layer**, **demultiplexing** sorts out which **application** should gets the data. In reverse, **multiplexing** encapsulating the message with the identity info so the destination knows which application the data should be sent to.
* So what the transport layer uses as identity in demultiplexing and multiplexing?
    * With **UDP**, it only requires the **destination port**. The **source port** is only needed when the client needs responding messages from the server. e.g. an DNS query:
        * ![](/images/16482338327285.jpg)
    * With TCP, it uses 4-tuple: source/destination IP address and port numbers, because the server supports simuptanous TCP connections with different sockets. Each sockets is associated with a different client.

## User Datagram Protocol(UDP)

* Segment structure
    * ![](/images/16485020244376.jpg)
    * Length, in bytes of UDP segment, including header
    * The **UDP checksum** is used to determine whether bits within the UDP segment have been altered.
