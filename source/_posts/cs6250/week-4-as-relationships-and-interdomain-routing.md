# Week 4 - AS Relationships and Interdomain Routing

Summary:

* Protocol: BGP 
* The different types of interconnections 
* Internet Exchange Points, provide interconnection services for directly exchange traffic

## Autonomous Systems and Internet Interconnection

* The Internet is a complex ecosystem. It includes:
    * Internet Service Providers (ISPs), 
    * Internet Exchange Points (IXPs), 
    * Content Delivery Networks (CDNs). 
    * <img src="https://i.imgur.com/R8W0lp6.png" style="width: 600px" />

* ISP has three tiers: 
    * access ISPs (or Tier-3),
    * regional ISPs (or Tier-2),
    * large global scale ISPs (or Tier-1), e.g. AT&T, NTT, Level-3
* IXP: the physical infrastructure, where multiple networks (e.g., ISPs and CDNs) can interconnect and exchange traffic locally.
* CDNs: control of how the content is delivered to the end-users
* More interconnection options in the Internet ecosystem: Points of Presence (PoPs), multi-homing, and peering. 
    * PoPs are one (or more) routers in a provider's network, which a customer network can use to connect to that provider.
* Autonomous Systems(AS): a group of routers (including the links among them) that operate under the same administrative authority. An ISP, for example, may operate as a single AS, or it may operate through multiple ASes. Each AS implements its own set of policies, makes its own traffic engineering decisions and interconnection strategies, and determines how the traffic leaves and enters its network.
* Protocols for routing traffic between and within ASes:
    * The border routers of the ASes use the Border Gateway Protocol (BGP) to exchange routing information with one another.
    * In contrast, the Internal Gateway Protocols (IGPs) operate within an AS, and they are focused on "optimizing a path metric" within that network. Example IGPs include Open Shortest Paths First (OSPF), Intermediate System - Intermediate System (IS-IS), Routing Information Protocol (RIP), and E-IGRP. 

### AS Business Relationships
 
* business relationships between ASes:
    * **Provider-Customer relationship (or transit)**: Based on a financial settlement that determines how much the customer will pay the provider. The provider forwards the customer's traffic to destinations found in the provider's routing table (including the opposite direction of the traffic). 
    * **Peering relationship**: In a peering relationship, two ASes share access to a subset of each other's routing tables. Peering relationships are formed between Tier-1 ISPs but also between smaller ISPs. 
        * In the case of Tier-1 ISPs, the two peers need to be of similar size and handle proportional amounts of traffic. Otherwise, the larger ISP would lack the incentive to enter a peering relationship with a smaller size ISP. 
        * When two small ISPs peer, they both save the money they would otherwise pay to their providers by directly forwarding traffic between themselves instead of through their providers.
        * Quiz: In a peering relationship, the traffic exchanged between the two peers must be highly asymmetric so that there is enough incentive for both parties to peer with each other.
* <img src="https://i.imgur.com/FJ31KZS.jpg" style="width: 600px" />

* How do providers charge customers? A fixed price or the bandwidth used.
    
## BGP

### BGP Routing Policies: Importing and Exporting Routes

* Exporting Routes
    * Different types of routes that an AS (let's call it X) decides whether to export.
        * Routes learned from customers: These are the routes X receives as advertisements from its customers. Since provider X is getting paid to provide reachability to a customer AS, it makes sense that X wants to advertise these customer routes to as many other neighboring ASes as possible. 
        * Routes learned from providers: These are the routes X receives as advertisements from its providers. Advertising these routes does not make sense since X does not have the financial incentive to carry traffic for its provider's routes.  
        * Routes learned from peers: These are routes that X receives as advertisements from its peers. As we saw earlier, it does not make sense for X to advertise to provider A the routes it receives from provider B.
* Importing Routes 
    * When an AS receives multiple route advertisements towards the same destination from multiple ASes, it needs to rank the routes before selecting which one to import. In order of preference, the imported routes are **the customer routes, then the peer routes, and finally the provider routes**(Quiz). The reasoning behind this ranking is that an AS...
        * wants to ensure that routes towards its customers do not traverse other ASes unnecessarily generating costs,
        * uses routes learned from peers since these are usually "free" (under the peering agreement),
        * and finally resorts to importing routes learned from providers as these will add to costs.

### BGP and Design Goals

* **Scalability**: to manage the complications of this growth while achieving convergence in reasonable timescales and providing loop-free paths. 
* **Express routing policies**: BGP has defined route attributes that allow ASes to implement policies (which routes to import and export) through route filtering and route ranking. Each ASes routing decisions can be kept confidential, and each AS can implement them independently of one another. 
* **Allow cooperation among ASes**: Each individual AS can still make local decisions (which routes to import and export) while keeping these decisions confidential from other ASes. 
* **Security**: Originally, the design goals for BGP did not include security. However, the increase in size and complexity of the Internet demands security measures to be implemented. We need protection and early detection for malicious attacks, misconfiguration, and faults. There have been several efforts to enhance BGP security ranging from protocols (e.g., S-BGP), additional infrastructure (e.g., registries to maintain up-to-date information about which ASes own which prefixes ASes), public keys for ASes, etc. Also, there has been extensive research work to develop machine learning based approaches and systems. But these solutions have not been widely deployed or adopted for multiple reasons that include difficulties in transitioning to new protocols and lack of incentives.

### BGP Protocol Basics

* A pair of routers, known as **BGP peers**, exchange routing information over a semi-permanent TCP port connection called a **BGP session**. In order to begin a BGP session, a router will send an OPEN message to another router. Then the sending and receiving routers will send each other announcements from their routing tables. The time it takes to exchange routes varies from a few seconds to several minutes, depending on the number of routes exchanged.

* A BGP session between a pair of routers in two different ASes is called an **external BGP (eBGP)** session, and a BGP session between routers that belong to the same AS is called an **internal BGP (iBGP)** session. 

* In the following diagram, we can see three different ASes along with iBGP (e.g., between 3c and 3a) and eBGP (e.g., between 3a and 1c ) sessions between their border routers.

* <img src="https://i.imgur.com/H8TylTW.png" style="width: 600px" />


* **BGP messages**: After BGP peers establish a session,  they can exchange BGP messages to provide reachability information and enforce routing policies. We have two types of BGP messages: 

    1. The **UPDATE** messages contain information about the routes that have changed since the previous update. There are two kinds of updates:
        * Announcements are messages that advertise new routes and updates to existing routes. They include several standardized attributes. 
        * Withdrawals messages inform that receive that a previously announced route is no longer available. The removal could be due to some failure or a change in the routing policy.
    1. The **KEEPALIVE** messages are exchanged between peers to keep a current session going.

* **BGP Prefix Reachability**: In the BGP protocol, destinations are represented by IP prefixes. Each prefix represents a subnet or a collection of subnets that an AS can reach. Gateway routers running eBGP advertise the IP prefixes they can reach according to the AS's specific export policy to routers in neighboring ASes. Then, using separate iBGP sessions, the gateway routers disseminate these routes for external destinations to other internal routers according to the AS's import policy. Internal routers run iBGP to propagate the external routes to other internal iBGP speaking routers.  

* **Path Attributes and BGP Routes**: In addition to the reachable IP prefix field, advertised **BGP routes** consist of several **BGP attributes**. Two notable attributes are AS-PATH and NEXT-HOP.
    * **ASPATH**: Each AS is identified by its **autonomous system number (ASN)**. As an announcement passes through various ASes, their identifiers are included in the ASPATH attribute. This attribute prevents loops and is used to choose between multiple routes to the same destination, the route with the shortest path.
    * **NEXT HOP**: This attribute refers to the next-hop router's IP address (interface) along the path towards the destination. Internal routers use the field to store the IP address of the border router. Internal BGP routers will forward all traffic bound for external destinations through the border router. Suppose there is more than one such router on the network, and each advertises a path to the same external destination. In that case, NEXT HOP allows the internal router to store in the forwarding table the best path according to the AS routing policy.

### iBGP and eBGP

* In the previous topic, we saw that we have two flavors of BGP: eBGP (for sessions are between border routers of neighboring ASes) and iBGP (for sessions between internal routers of the same AS). 

* Both protocols are used to disseminate routes for external destinations.

* The eBGP speaking routers learn routes to external prefixes and disseminate them to all routers within the AS. This dissemination is happening with iBGP sessions. For example, as the figure below shows, the border routers of AS1, AS2, and AS3 establish eBGP sessions to learn external routes. Inside AS2, these routes are disseminated using iBGP sessions.

* <img src="https://i.imgur.com/K6Wh3Qc.png" style="width: 600px" />

* The dissemination of routes within the AS is done by establishing a full mesh of iBGP sessions between the internal routers. Each eBGP speaking router has an iBGP session with every other BGP router in the AS to send updates about the routes it learns (over eBGP).

* <img src="https://i.imgur.com/OVJqXFC.png" style="width: 600px" />

* [Quiz] Finally, we note that iBGP is not another IGP-like protocol (e.g., RIP or OSPF). IGP-like protocols are used to establish paths between the internal routers of an AS based on specific costs within the AS. In contrast, iBGP is only used to disseminate external routes within the AS.
    * IGP-like protocols are used to establish paths between the internal routes of an AS based on specific osts within AS. iBGP is used for disseminaing **external** routes within the AS
* [Quiz] Diff between iBGP and eBGP: both for disseminating **external** routes. eBGP session is  established between two **border routes** that belong to different ASes. An iBGP session is established between routers that belong to the same AS.

### BGP Decision Process: Selecting Routes at a Router

* Let's zoom into what is happening as the routers exchange BGP messages to select routes.
* <img src="https://i.imgur.com/6maGQw8.png" style="width: 600px" />
* A router receives incoming BGP messages and processes them. When a router receives advertisements
    1. It first <u>applies the import policies to exclude routes from further consideration</u>. 
    2. Then the router <u>implements the decision process to select the best routes</u> that reflect the policy in place. 
    3. Next, the newly <u>selected routes are installed</u> in the forwarding table. 
    4. Finally, the router <u>decides which neighbors to export</u> the route to by applying the export policy. 

#### The Router's Decision Process

*  Suppose that a router receives multiple route advertisements to the same destination. How does the router choose which route to import? 
    *  In a nutshell, the decision process is how the router compares routes. It goes through the list of attributes in the route advertisements. In the simplest scenario, the router uses the attribute of the path length to select the route with the fewest number of hops. Rarely occurs in practice, though.
    *  A router compares a pair of routes by going through the list of attributes, as shown in the figure below:
        *  <img src="https://i.imgur.com/VvFYozj.png" style="width: 600px" />
*  Let's focus on two attributes, **LocalPref** and **MED (Multi-Exit Discriminator)**.
    * The **LocalPref** attribute is used to prefer routes learned through a specific AS over other ASes. For example, suppose AS B learns of a route to the same destination x via A and C. If B prefers to route its traffic through A, due to peering or business, it can assign a higher LocalPref value to routes it learns from A. And therefore, by using LocalPref, AS B can control where the traffic exits the AS. In other words, **it will influence which routers will be selected as exit points for the traffic that leaves the AS** **(outbound traffic)**. 
        * <img src="https://i.imgur.com/jsmj3oP.png" style="width: 600px" />
    * An AS ranks the routes it learns by preferring first the routes learned from its customers, then the routes learned from its peers, and finally, the routes learned from its providers. An operator can assign a non-overlapping range of values to the LocalPref attribute according to the type of relationship. So assigning different LocalPref ranges will influence which routes are imported. The following image shows a scheme that can be used to reflect the business relationships:
        * <img src="https://i.imgur.com/if7w7W2.png" style="width: 600px" />
    * The **MED (Multi-Exit Discriminator)** value is used by ASes connected by multiple links to designate which links are preferred for **inbound traffic**. For example, the network operator of AS B will assign different MED values to its routes advertised to AS A through R1 and different MED values to its routes advertised through R2. As a result of different MED values for the same routes, AS A will be influenced to choose R1 to forward traffic to AS B, if R1 has a lower MED value, and if all other attributes are equal.  

    * We have seen in the previous topics that an AS does not have an economic incentive to export routes that it learns from providers or peers to other providers or peers. An AS can reflect this by tagging routes with a MED value to "staple" the type of business relationship. Also, an AS filters routes with specific MED values before exporting them to other ASes. Finally, we note that influencing the route exports will also affect how the traffic enters an AS (the routers that are entry points for the traffic that enters the AS).

* So, where/how are the attributes controlled? The attributes are set either 
    a. locally by the AS (e.g., LocalPref), 
    b. by the neighboring AS (e.g., MED), 
    c. or by the protocol (e.g., if a route is learned through eBGP or iBGP).

### Challenges with BGP

#### Scalability and Misconfigurations

* the BGP protocol in practice can suffer from two significant limitations: **misconfigurations** and **faults**.
    * A possible misconfiguration or an error can result in an excessively large number of updates, resulting in route instability, router processor and memory overloading, outages, and router failures.
    * One way that ASes can help reduce the risk that these events will happen is by **limiting the routing table size** and **limiting the number of route changes**. 
* An AS can **limit the routing table size using filtering**. For example, long, specific prefixes can be filtered to encourage route aggregation. In addition, routers can limit the number of prefixes advertised from a single source on a per-session basis. Some small ASes also have the option to configure default routes into their forwarding tables. ASes can likewise protect other ASes by using route aggregation and exporting less specific prefixes where possible. 
* Also, an AS can **limit the number of routing changes**, explicitly limiting the propagation of unstable routes by using a mechanism known as **flap damping**. To apply this technique, an AS will track the number of updates to a specific prefix over a certain amount of time. <u>If the tracked value reaches a configurable value, the AS can suppress that route until a later time.</u> Because this can affect reachability, an AS can be strategic about how it uses this technique for certain prefixes. For example, more specific prefixes could be more aggressively suppressed (lower thresholds), while routes to known destinations that require high availability could be allowed higher thresholds. 

### Peering at Internet Exchange Points(IXPs)

* What are IXPs?
    * IXPs are physical infrastructures that provide the means for ASes to interconnect and directly exchange traffic with one another. The ASes that interconnect at an IXP are called participant ASes. The physical infrastructure of an IXP is usually a network of switches located either in the same physical location or distributed over a region or even at a global scale. Typically, the infrastructure has a fully redundant switching fabric that provides fault tolerance. The equipment is usually located in facilities such as data centers, which provide reliability, sufficient power, and physical security. 
    * For example, in the figure below we see an IXP infrastructure (2012), called DE-CIX that is located in Frankfurt, Germany. The figure shows the core of the infrastructure (noted as 3 and 6) and additional sites (1-4 and 7) that are located at different colocation facilities in the area.
    * <img src="https://i.imgur.com/qARL3wh.png" style="width: 600px" />
* Why have IXPs become increasingly popular, and  why are they important to study?
    1. **IXPs are interconnection hubs handling large traffic volumes.**
    2. **An important role in mitigating DDoS attacks**: As IXPs have become increasingly popular interconnection hubs, they can observe the traffic to/from an increasing number of participant ASes. In this role, IXPs can play the role of a “shield” to mitigate DDoS attacks and stop the DDoS traffic before it hits a participant AS. As a result, there are many DDoS events that IXPs have mitigated. 
    3. **“Real-world” infrastructures with a plethora of research opportunities**: IXPs play an important role in today’s Internet infrastructure. Studying this peering ecosystem, the end-to-end flow of network traffic, and the traffic that traverses these facilities can help us understand how the Internet landscape is changing. For example, BGP blackholing for DDoS mitigation or applications for Software Defined Networking. 
    4. **IXPs are active marketplaces and technology innovation hubs**: IXPs are active marketplaces, especially in North America and Europe. They provide an expanding list of services that go beyond interconnection. Most notably are DDoS mitigation and SDN-based services. As a result, IXPs have been evolving from interconnection hubs to technology innovation hubs.   
* What are the steps for an AS to peer at an IXP?
    * Each participating network must have a public Autonomous System Number (ASN). Each participant brings a router to the IXP facility (or one of its locations if the IXP has an infrastructure distributed across multiple data centers) and connects one of its ports to the IXP switch. The router of each participant must be able to run BGP since the exchange of routes across the IXP is via BGP only. In addition, each participant must agree to the IXP’s General Terms and Conditions (GTC).
    * Two networks may publicly peer at IXP by using the IXP infrastructure to establish a connection for exchanging traffic according to their own requirements and business relationships. But, first, each network incurs a one-time cost to establish a circuit from the premises to the IXP. Then, there is a monthly charge for using a chosen IXP port, where higher port speeds are more expensive. The entity that owns and operates the IXP might also charge an annual membership fee. In particular, exchanging traffic over an established public peering link at an IXP is in principle “settlement-free” (i.e., involves no form of payment between the two parties) as IXPs typically do not charge for exchanged traffic volume. Moreover, IXPs usually do not interfere with the bilateral relationships between the IXP’s participants unless they violate the GTC. For example, the two parties of an existing IXP peering link are free to use that link in ways that involve paid peering. Other networks may even offer transit across an IXP’s switching fabric. Depending on the IXP, the time it takes to establish a public peering link can range from a few days to a couple of weeks.
* Why do networks choose to peer at IXPs? 
    * Keep local traffic local. 
    * Lower costs. Typically peering at an IXP is offered at a lower cost than relying on third parties to transfer the traffic, which is charged based on volume. 
    * Network performance is improved due to reduced delay. 
    * Incentives. Critical players in today’s Internet ecosystem often “incentivize” other networks to connect at IXPs. For example, a prominent content provider may require another network to be present at a specific IXP or IXPS in order to peer with them. 
* What services are offered at IXPs? 
    * **Public peering**: The most well-known use of IXPs is public peering service, in which two networks use the IXP’s network infrastructure to establish a connection to exchange traffic based on their bilateral relations and traffic requirements. The costs required to set up this connection are a one-time cost for establishing the connection, the monthly charge for using the chosen IXP port (those with higher speeds are more expensive), and perhaps an annual fee of membership in the entity owning and operating the IXP. However, the IXPs do not usually charge based on the amount of exchanged volume. They also do not usually interfere with bilateral relations between the participants unless there is a violation of the GTC. Even with the set-up costs, IXPs are generally cheaper than other conventional methods of exchanging traffic (such as relying on third parties which charge based on the volume of exchanged traffic). IXP participants also often experience better network performance and Quality-of-Service (QoS) because of reduced delays and routing efficiencies. In addition, many companies that are significant players in the Internet space (such as Google) incentivize other networks to connect at IXPs by making it a requirement to peering with them. 
    * **Private peering**: Most operational IXPs also provide a private peering service (Private Interconnects, or PIs) that allows direct traffic exchange between the two parties, and <u>doesn’t use the IXP’s public peering infrastructure</u>(Quiz). This is commonly used when the participants want a well-provisioned, dedicated link capable of handling high-volume, bidirectional, and relatively stable traffic.
    * **Route servers and Service level agreements**: Many IXPs also include service level agreements (SLAs) and <u>free use of the IXP’s route servers</u>(Quiz) for participants. This allows participants to arrange instant peering with many co-located participant networks using essentially a single agreement/BGP session.
    * **Remote peering through resellers**: Another popular service is IXP reseller/partner programs. Third parties resell IXP ports wherever they have infrastructure connected to the IXP. These third parties can offer the IXP’s service remotely, which will enable networks that have little traffic also to use the IXP. This also enables remote peering, where networks in distant geographic areas can use the IXP. 
    * **Mobile peering**: Some IXPs also provide support for mobile peering, which is a scalable solution for the interconnection of mobile GPRS/3G networks.
    * **DDoS blackholing**: A few IXPs support customer-triggered blackholing, which allows users to alleviate the effects of DDoS attacks against their network.
    * **Free value-added services**: In the interest of ‘good of the Internet’, a few IXPs such as Scandinavian IXP Netnod offer free value-added services like Internet Routing Registry (IRR), consumer broadband speed tests9, DNS root name servers, country-code top-level domain (ccTLD) nameservers, as well as distribution of the official local time through NTP.

### Peering at IXPs: How Does a Route Server Work?

* two ASes exchange traffic through the switching fabric utilize a two-way BGP session, called a **bilateral BGP session**. which does not scale with many participants. To mitigate this, some IXPs operate a route server, which helps to make peering more manageable. In summary, a **Route Server (RS)** does the following:
    * It collects and shares routing information from its peers or participants of the IXP that connect to the RS.
    * It executes its own BGP decision process and re-advertises the resulting information (e.g., best route selection) to all RS's peer routers.
* The figure below shows a **multi-lateral BGP peering session**, an RS that facilitates and manages how multiple ASes can "talk" on the control plane simultaneously. 
* <img src="https://i.imgur.com/9qiOFQL.png" style="width: 600px" />
* How does a route server (RS) maintain multi-lateral peering sessions?
    * Let's look at a modern route server architecture in the figure below to understand how it works. A typical routing daemon maintains a Routing Information Base (RIB), which contains all BGP paths that it receives from its peers - the Master RIB. In addition, the route server also maintains AS-specific RIBs to keep track of the individual BGP sessions they maintain with each participant AS. 
    * Route servers maintain two types of route filters. **Import filters** are applied to ensure that each member AS only advertises routes that it should advertise(Quiz). And **export filters** are typically triggered by the IXP members themselves to restrict the set of other IXP member ASes that receive their routes. Let's look at an example where AS X and AS Z exchange routes through a multi-lateral peering session that the route server holds. The steps are as follows:
        1. In the first step, AS X advertises a prefix p1 to the RS, which is added to the route server's RIB specific to AS X. 
        2. The route server uses the peer-specific import filter to check whether AS X is allowed to advertise p1. If it passes the filter, the prefix p1 is added to the Master RIB. 
        3. The route server applies the peer-specific export filter to check if AS X allows AS Z to receive p1, and if true, it adds that route to the AS Z-specific RIB.
        4. Lastly, the route server advertises p1 to AS Z with AS X as the next hop.
    * <img src="https://i.imgur.com/sr3spll.png" style="width: 600px" />

### Remote Peering [Optional] 

* What is remote peering?
    * Remote peering (RP) is peering at the peering point without the necessary physical presence. The remote peering provider is an entity that sells access to IXPs through their own infrastructure. RP removes the barrier to connecting to IXPs around the world, which in itself can be a more cost-effective solution for localized or regional network operators. 

* How to detect remote peering? 
    * <img src="https://i.imgur.com/mSk7Qkl.png" style="width: 600px" />
* The primary method of identifying remote peering is to measure the round-trip time (RTT) between a vantage point (VP) inside the IXP and the IXP peering interface of a member. However, this method fails to account for the changing landscape of IXPs today and even misinfers latencies of remote members as local and local members as being remote. Instead, a combination of methods can achieve detection of remote peering in a more tractable way, some of which include:
    * **Information about the port capacity**: One way to find reseller customers is via port capacities. The capacity of the peering port for each IXP member can be obtained through the IXP website or PeeringDB. IXPs offer ASes connectivity to ports with capacity typically between 1 and 100 Gbit/s. But resellers usually offer connectivity through their virtual ports with smaller capacities and lower prices. 
    * **Gathering colocation information**: An AS needs to be physically present (i.e., actually deploy routing equipment) in at least one colocation facility where the IXP has deployed switching equipment. It should be easy to locate the colocation facilities where both AS and IXPs are colocated, though this information is imperfect in practice.  
    * **Multi-IXP router inference**: An AS can operate a multi-IXP router, which is a router connected to multiple IXPs to reduce operational costs. Suppose a router is connected to multiple IXPs, and say, we infer the AS as local or remote to one of these IXPs from a previous step. In that case, we can extend the inference to the rest of the involved IXPs based on whether they share colocation facilities or not.
    * **Private connectivity with multiple existing AS participants**: If an AS has private peers over the same router that connects it to an IXP, and the private peers are physically colocated to the same IXP facilities, it can be inferred that the AS is also local to the IXP. 

### BGP Configuration Verification [Optional]

* Control of BGP configuration is complex and easily misconfigured. Two main aspects of persistent routing define BGP correctness. They are **path visibility** and **route validity**.
    * **Path visibility** means that route destinations are correctly propagated through the available links in the network.
    * **Route validity** means that the traffic meant for a given destination reaches it.
* **The router configuration checker, or rcc**, is a tool researchers propose that detects BGP configuration faults. rcc uses static analysis to check for correctness before running the configuration on an operational network before deployment. The rcc analyzes router configuration settings and outputs a list of configuration faults. 
* In order to analyze a single router or a network-wide BGP configuration, the rcc will first “factor” the configuration to a normalized model by focusing on how the configuration is set to handle route dissemination, route filtering, and route ranking.
* Although rcc is designed to be used before running a live BGP configuration, it can be used to analyze the configuration of live systems and potentially detect live faults. While analyzing real-world configurations, it was found that most Path Visibility Faults were the result of:
    1. problems with “full mesh” and route reflector configurations in iBGP settings leading to signaling partitions
    2. Route reflector cluster problems 
    3. Incomplete iBGP sessions where an iBGP session is active on one router but not the other
* Route Validity Faults were determined to stem from filtering and dissemination problems. The specific filtering behaviors included legacy filtering policies not being fully removed when changes occur, inconsistent export to peer behavior, inconsistent import policies, undefined references in policy definitions, or non-existent or inadequate filtering. Dissemination problems included unorthodox AS prepending practices and iBGP sessions with “next-hop self”. These issues suggest that routing might be less prone to faults if there were improvements to iBGP protocols when it comes to making updates and scaling.
* Because rcc is intended to run prior to deployment, it may help network operators detect issues before they become major problems in a live setting, which often go undetected right away. rcc is implemented as static analysis and does not offer either completeness or soundness; it may generate false positives, and it may not detect all faults.
