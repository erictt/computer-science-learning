# Lesson 6: Spring Operating System

## L06a. Introduction

* How to design for the continuous and incremental evolution for the complex distributed software systems (functionality + performance)?
    - Using **Distributed Object Technology**, we can design scalable OS services in a parallel system.
* How to innovate in the commercial OS space?
    - In a commercial space, the choice becomes <u>whether to build a new OS or to build a better implementation of an existing OS</u>. Due to the installed base of applications, moving to a new OS is not a good option. Sun, therefore, took the latter approach with Spring.
* The OS Sun was developing had to:
    - Run existing applications unchanged and yet allow for them to be scaled to larger capacities via clusters.
    - Allow for 3rd party vendors to use the APIs exposed optimally without breaking anything.

### Object-Based vs. Procedural Design

![|500](https://i.imgur.com/DcP7IoO.jpg)

* Procedural Design:
    - The code is written as a monolithic entity.
    - We have a **shared state** represented by the global variables, and **private states** represented by the function calls.
* Object-Based Design:
    - The **state is contained inside** the object.
    - Methods inside the object manipulate the state. Only the methods are visible externally.
* In Spring, Object Orientation is applied to build the OS Kernel.

### Spring Approach

![|500](https://i.imgur.com/LA1GcVB.jpg)

* Provide strong interfaces to each sub-system.
* The system is open and flexible. Thus, 3rd party vendors can integrate their software to the system.
* **IDL** (**Interface Definition Language**) is used to define the OS interfaces. This provided flexibility in terms of the programming language.
* The kernel in Spring is used to facilitate extensibility:
    - **Nucleus**: Threads + IPC.
    - **Virtual Memory Manager**: Memory management.
* Sun provided a “Network Proxy” node so that the OS can be used as a network OS.

### Nucleus

![](https://i.imgur.com/6hhzK8G.jpg)

* Nucleus is the microkernel of Spring OS. It manages only the threads abstractions and the IPC.
* Door:
    - A software capability to a target domain (a domain is container or an address space where threads can execute).
    - Threads can enter a target domain using the Door. It represents the entry point methods to the domain.
    - Every domain will have a **Door Table** containing the **IDs** of the Doors this domain can access.
    - Multiple client domains can have access to the same Door.
* How to make a **Protected Procedure Call**?
    - The client domain invokes the Door handle of the target domain.
    - The **Nucleus verifies this invocation**.
    - The Nucleus allocates a server thread to the target domain and executes the invocation that is indicated by this particular Door handle.
    - Since it’s a Protected Procedure Call, the client thread will be deactivated, and the thread is allocated to the target domain to execute the invocation.
    - On return, the thread is deactivated, and the client thread is reactivated to continue execution.
    - <u>Similar to LRPC</u> in terms of doing fast cross address space calls using the Door mechanism.
    - This ensures high performance.

### Object Invocation Across the Network

![](https://i.imgur.com/fqjELzn.jpg)

* Object invocation between client/server domains across the network is facilitated using the **Network Proxy**.
* <u>Each domain has **multiple Network Proxies**</u> to communicate with different nodes on the network. This facilitates specialization since these different proxies can represent different protocols.
* Network Proxies are invisible to the clients/servers.
* How to establish communication over the network?
    - A Network Proxy ($\text{𝑃𝑟𝑜𝑥𝑦}_𝑠$) will be instantiated on the server node and a Door will be created for communication between this Proxy and the server domain through the Nucleus.
    - $\text{𝑃𝑟𝑜𝑥𝑦}_𝑠$ will export the network handle embedding the Door created on the server domain to the Network Proxy of the client domain $\text{𝑃𝑟𝑜𝑥𝑦}_c$. These Proxies and the communication between them are outside the kernel.
    - $\text{𝑃𝑟𝑜𝑥𝑦}_c$ will use this network handle to establish a connection between the client’s Nucleus and the server’s Nucleus.
    - The client domain will then invoke the Door inside its Nucleus and the two Proxies will facilitate the invoking the server.

### Secure Object Invocation

![](https://i.imgur.com/pdKetTH.jpg)

* Spring OS facilitates providing different privilege levels for different clients using the “Front Object”.
* An underlying object may have a Front Object that is directly connected to it (without Doors).
* Whenever a client domain tries to access this protected domain, the Front Object will check the **Access Control List (ACL)** to see what privileges this client domain has for accessing the protected domain.
* Different instances of the Front Object can be created with different access policies to the same underlying object.
* **Doors are software capabilities**, which means they can be passed from client domain to another. When passing a Door, the client domain can determine whether to pass the same privileges or not.

![](https://i.imgur.com/NrkosOK.jpg)

### Virtual Memory Management

![](https://i.imgur.com/dNnZ6w1.jpg)

* Virtual memory management is part of the Spring OS kernel.
* The VMM is responsible for managing the linear address space of each process.
* The VMM breaks this linear address space into **memory regions** (sets of pages with different sizes).
* These memory regions are mapped to different **memory objects**.
* These memory objects are the mechanism by which parts of the address space <u>can be mapped into different **backing entities**</u> (e.g. desk, file system, etc.).

#### Pager Object

![](https://i.imgur.com/orpJYt3.jpg)

* The **Pager Object** is responsible for establishing the connection between virtual memory and physical memory. 
* The Pager Object makes sure that a memory object has a representation in the physical memory.
* The Pager Object will create a cache object representation for the memory object in the DRAM.
* The Pager Object gives the ability to have different regions of the linear address space of a given process by associating different pager objects with each of the regions that correspond to a particular memory object.
* These associations between region and memory objects can be dynamically created.
* The same memory object can have <u>distinct cache representations on different physical memory spaces</u>.
* The Pager Objects **maintains the coherence of these different cache objects** if needed.
    * Each pager objects within Pager ensure the consistency.

#### Summary

![|500](https://i.imgur.com/8XIwoK5.jpg)
* Object oriented kernel
    - nucleus -> threads + IPC
    - linedkie's microkernel -> nucleus + address space
    - door + doortable -> basis for cross domain calls
    - object invocation and cross machine calls
    - virtual memory management
        - Address space object, memory object, external pagers, cached object.
* Compare to Tornado. Tornado uses uses clustered object as an optimization for implementing kernel services. Spring's object technology permeates entire OS for structuring mechanism.

### Dynamic Client-Server Relationships

* The client-server interaction should be irrelative to the physical locations of the clients and the servers (Same machine – different nodes on a network).
* Scenario #1: We have several replica of the servers (to increase availability). The clients will be dynamically routed to different servers depending on the physical proximity of the client and the server, and also on the load distribution.
* Scenario #2: The servers are cached. The clients can dynamically access these cached copies instead of accessing the servers themselves.
* Then, we have two types of dynamic decisions:
    - In Scenario #1: Deciding which server replica the client should access.
    - In Scenario #2: Deciding which cached copy the client should access.
* Spring OS uses “Subcontracts” to manage these decisions.

### Subcontract

* As mentioned earlier, IDL is used to define the OS interfaces.
* The Subcontract is the implementation of the IDL interfaces, it hides the runtime behavior of an object from the actual interface.
    * For instance, there could be a singleton implementation of the server, or it could be a replicated implementation of the server. The client does not care.
* The client stub generation will be simple, since all the details about the server will be hidden in the Subcontract.

* IDL compiler is used to produce three pieces of source code: 
    1) A language specific form of the IDL interface 
    2) Client side stub code: Code meant to be dynamically linked into a client’s program to access an object that is implemented in another address space or on another machine 
    3) Server side stub code: Code to be linked into an object manager to translate incoming remote object invocations into the run-time environment of the object’s implementation.

* A **Subcontract can be changed dynamically** while the stub stays fixed. This facilitates adding functionalities to existing services using the Subcontract mechanism.
* Marshal/Un-marshal Interface: The Subcontract will marshal/unmarshal arguments when requested by the client. The Subcontract will do the appropriate steps to execute the request based on the location of the server (e.g. on the same machine, on the network, on a different processor, etc.).
* The Subcontract on the client side has an invocation mechanism.
* On the server side, the Subcontract has (create – revoke – process) mechanisms.

### Conclusion

* Spring OS uses object technology as a structuring mechanism in building a network OS.
    - Strong interfaces.
    - Flexibility.
    - Extensibility: Spring OS has a microkernel.
* Spring OS uses Network Proxies: The client and the servers don’t have to know the locations of each others.
* Subcontract mechanism allows the clients and the servers to dynamically change the relationships between each others without changing the client/server stubs.

## L06b. Java RMI

### Java Distributed Object Model

* Much of the hard work needed to build a client/server system using RPS (marshaling/unmarshaling, publishing the remote object on the network for the clients to access, etc.) are all managed undercover by the Java Distributed Object Model.
* Java Distributed Object Model concepts:
    - **Remote Object**: Accessible from different address spaces.
    - **Remote Interface**: Declarations for methods in a remote object.
    - **Failure Semantics**: Clients deal with RMI failure exceptions.
* **Similarities/differences between local objects and remote objects**:
    - In Local Object Model, the Object references passed as object invocation parameters, they are passed as a **pure reference** (i.e. if client changes the object, server will see the change).
    - In Distributed Object Model, the Object references passed as object invocation parameters, they are passed as **Value/Result** (i.e. if client changes the object, server will not see the change because <u>a copy of the object is actually sent</u> to the invoked method).

### Local vs. Remote Implementation

* Reuse of Local Implementation:
    - ![](https://i.imgur.com/JPuqF1f.jpg)

    - Extend a Local Implementation of the Account Class to implement Bank Account.
    - Use the Built-in Class called Remote Interface to make the methods in Bank Account visible remotely on the network.
    - Only the interface is visible to the client and not the actual implementation or the instantiated objects.
    - The actual location of the object is not visible to the client. Therefore, the implementer has to do the hard work of finding a way to make the location of the service visible to clients on the network (i.e. Instantiated Objects).
    - In this case, we used the Local Implementation and used only the Remote Interface to make the object instances remotely accessible. So, all the hard work of making the object instances remotely accessible needs to be done by the implementer. This is why this approach is **not preferable**. However, this approach has the advantage of providing fine-grained control on selective sharing of services.
* Reuse of Remote Object Class
    - ![](https://i.imgur.com/WST8BAh.jpg)

    - Extend the Remote Interface so that the Account Interface now becomes visible to any client that wants to access the Object.
    - Extend the Remote Object Class and Remote Server Class in order to get the Account Implementation Object.
    - Now, when we instantiate the Account Implementation Object, it becomes visible to the network clients through the Java Runtime System.
    - The Java RMI system is responsible for all the hard work of making the Server Object Instance visible to network clients and hence this is the more **preferred** way of building network services and making them available for remote clients anywhere on the network.

### How does Java RMI work?

* On Server side:
    - The server object is made visible on the network using the 3-step procedure:
        1. Instantiate the Object.
        2. Create a URL.
        3. Bind the URL to the Object Instance created.
    - ![](https://i.imgur.com/jyDPAJQ.jpg)
    - This allows the clients to be able to discover the existence of the new service on the network.
* On Client side:
    * Any arbitrary client can easily discover and access the server object on the network using the following procedure:
        1. Lookup the service provider URL by contacting a bootstrap name server in the Java RMI system and get a local access point for that remote object on the client-side.
        2. Use the local access point for the remote object on the client-side by simply calling the invocation methods, which look like normal procedure calls.
            - The Java Runtime System knows how to locate the server object in order to do the invocation.
            - The client does NOT know or care about the location of the server object.
        3. If there are failures in any of execution of the methods (functions), then Remote Exceptions will be issued by the server through the Java Runtime System back to the client.
        - A problem with Remote Exceptions is that the client may have no way of knowing at what point in the call invocation the failure happened.
    * ![](https://i.imgur.com/hjedUKR.jpg)

### RMI Implementation

![](https://i.imgur.com/FnHfGxI.jpg)

* The Java RMI functionality is implemented using the **Remote Reference Layer (RRL)**.
* The Client-side stub initiates the remote method invocation call, which causes RRL to marshal the arguments in order to send them over the network. When the server responds, the RRL unmarshals the results for the client.
* Similarly, the Server-side **skeleton**
    - Uses RRL to unmarshal the arguments from client message.
    - Makes the call to the server implementing the Remote Object.
    - Marshals the results from the server into a message to be sent to the client.
* Marshaling and unmarshaling are also called as **Serializing and De-serializing Java objects** and is done by the RRL layer.
* The RRL layer is similar to the Subcontract mechanism in the Spring Network OS. Java RMI derives a lot from the Subcontract mechanism.
* In summary:
    - RRL hides the details/location of the server (replica, singleton, etc.).
    - RRL supports different transport protocols.
    - RRL marshals/serializes information to be sent across the network.

### RMI Transport Layer

![](https://i.imgur.com/c5FFPXD.jpg)

The RMI Transport Layer provides the following four abstractions:

* **Endpoint**:
    - This is a **Protection Domain** or a **Sandbox** like **Java Virtual Machine** for execution of a server call or client call within the Sandbox.
    - The Endpoint has a table of Remote Objects that it can access (similar to Door Table in Spring OS).
* **Transport**:
    - The **connection management** of the transport layer is responsible for 
        - setting up connections, 
        - tearing down connections, 
        - listening for incoming connections, 
        - and establishing the connection.
    - The RRL layer decides which transport protocol to use (TCP or UDP Protocol) and it gives that command to the Transport Layer.
    - The Transport listens on channel for incoming connections.
    - The Transport is responsible for locating the dispatcher that invokes the remote method.
    - The Transport mechanism sits below the RRL layer and allows the object invocations to happen through the Transport Layer.
* **Channel**:
    - The type of the Transport decides the type of the Channel (TCP or UDP Channel).
    - Two Endpoints make a connection on the Channel and do I/O using the connection on the Channel.

## L06c. Enterprise Java Beans(EJB)

### N-Tier Applications

![](https://i.imgur.com/ezxgHld.jpg)

* Distributed Giant Scale Services are also called as N-tier applications because the software stack of an application comprises of several different layers:
    - **Presentation Layer**: Responsible for painting the browser screen and generating the web-page based on your request.
    - **Application Layer**: Responsible for the application logic that corresponds to what the service is providing.
    - **Business Logic Layer**: Corresponds to the way fees/prices are calculated.
    - **Database Layer**: Accesses the database that contains the information that is queried and updated based on the user request.

* N-tier applications must handle the following:
    - Persistence of data/actions.
    - Transaction properties.
    - Data caching.
    - Clustering related services/data.
    - Security.
    - Concurrency: Exploit parallelism across several simultaneous requests.
    - Reusing components: Portions of the application logic are reused in different components in order to serve simultaneous requests from several different clients.
* Also an opportunity to exploit parallelism, such as finding the availability of seats crossing airline companies, accepting requests simultaneously.

### Structuring N-Tier Applications

![](https://i.imgur.com/j6IdPcM.jpg)

* A Java Bean is a unit of reuse and contains a bundle of Java Objects to provide a specific functionality, e.g. a Java Bean may provide the shopping cart functionality.
* A Container is a Protection Domain implemented in a Java Virtual Machine (JVM) and it packages and hosts a related collection of Java Beans to provide higher-level functionality.
* An Application Service is constructed by using multiple Containers, typically present on different servers and used in a distributed manner.
* Mnemonic: Java Objects → Java Beans → Containers → Application Service.
* The **JEE (Java Enterprise Edition)** framework has 4 containers for constructing an application service:
    - **Client Container**: Resides on a web server and interacts with client browser.
    - **Applet Container**: Package the objects that constitute.
    - **Web Container**: Contains a Presentation Logic. Responsible for creating web pages to be sent back to the client browser.
    - **EJB Container**: Manages the Business Logic that decides what needs to be done to carry out the client browser requests. It also communicates with the Database server to read/write data corresponding to the client browser requests.

### What is a Java Bean?

* A Java Bean is a reusable software component that has many Java objects in a bundle so that the Java Bean can be passed around easily from one application to another application for reuse.
* Some of the challenges for different enterprises to provide together a common service are to maintain and evolve:
    - Service Interoperability and compatibility.
    - Service Scalability.
    - Service Reliability.
    - Service cost of operation.
* Such cross-enterprise services (e.g. airline reservation system, Gmail, internet search engine, etc.) are referred to as Giant Scale Services (GSS).
* The Object Technology facilitates the following:
    1. Structuring of an operating system at different levels
    2. Structuring of Distributed Services, providing customers various options based on cost, convenience, guarantees, etc.
    3. Handling resource conflicts that might occur between simultaneous requests across space and time coming from several different clients.


### Types of Java Beans

* **Entity Bean**: **Persistent Objects** with **Primary Keys** so that they can be easily retrieved from a database.
    - An Entity Bean may be a row of a database.
    - There are two types of persistence:
        1. **Bean-managed Persistence**: Persistence managed by the Bean.
        2. **Container-managed Persistence**: Persistence managed by Container.
* **Session Bean**: A Bean associated with client-server session.
    - There’re two types of Session Beans:
        1. **Stateful** Session Beans: Remember the state associated with the session across multiple sessions.
        2. **Stateless** Session Beans: The state is thrown away at the end of each session.
* **Message-driven Beans**: Useful **for asynchronous** behavior. An example would be receiving messages of interest that are typically event-driven (e.g. stock ticker information, newsfeed, RSS feed, etc.).

* Each Java Bean type denotes a particular functionality. Each Java Bean can be constructed into 2 forms, based on the granularity level:
    - **Fine-grained Java Beans**: Provide more concurrency in dealing with individual requests.
    - **Coarse-grained Java Beans**: Provide less concurrency, but keep the business logic simple.
    - Thus, the tradeoff in structuring N-tier applications is to choose either:
        1. Fine-grained granularity: More concurrency + complex business logic.
        2. Coarse-grained granularity: Less concurrency + simple business logic.

### Java Beans Design Alternatives

#### 1. Coarse grain session Beans

![](https://i.imgur.com/hU1aoxg.jpg)

* The Client Container and the Applet Container are in the Web-server so we will not consider them. Instead, we’ll only consider the **Web Container (Presentation Logic)** and **EJB Container (Business Logic)** in the several design alternatives below.
* A Servlet corresponds to an individual session with a particular client.
* Coarse-grained Session Bean:
    - A Coarse-grained Session Bean is **associated with each Servlet** and serves the needs of a Client.
    - **Each Client is associated with one Session**.
- Pros:
    1. Minimal Container services needed from the EJB Container: The EJB Container coordinates concurrent independent sessions.
    2. Business Logic is not exposed beyond the corporate network since the Business Logic is contained in the EJB Container and not in the Web Container.
- Cons:
    1. The Application Structure is similar to a **Monolithic** kernel.
    2. There is very **limited concurrency** for accessing different parts of a database in parallel. Hence, Coarse-grained Bean structure represents a lost opportunity in exploiting parallelism.

#### 2. Data Access Object(DAO)

fine-grained

![](https://i.imgur.com/Qe3HFmD.jpg)

- The **Business Logic is pushed to be in the Web Container** containing Servlet and Presentation Logic. Similar to having a 3-tier software structure of (Servlet – Presentation Logic – Business Logic).
- All Data Access happens through Entity Beans, which have Persistence characteristics. That is, Data Access Object (DAO) is implemented using Entity Beans.
- Entity Beans can have Container-Managed Persistence or Bean-Managed Persistence.
- An Entity Bean can represent the granularity of either one row of a database or a set of rows.
- Multiple Entity Beans can work in parallel for a single client-server session.
- The EJB Container contains these Entity Beans.
- Pros:
    1. There is an opportunity for the Entity Bean to cluster the requests from different clients and reduce accesses to the database server across several different client requests that are temporally happening at the same time.
    2. The granularity of the Data Access Object (DAO) determines the level of concurrency desired in constructing the application service. This provides reusability opportunities.
- Cons: **Business Logic is exposed outside the corporate network** because it was move from the EJB Container to the Web Container.

#### 3. Session Beans with Entity Beans

![](https://i.imgur.com/Z2H4qMi.jpg)

- The Web Container contains only the Servlet and the Presentation Logic associated with the Servlet.
- The Business Logic sits along with the Session Façade and Entity Bean in the EJB Container.
- A Session Façade is associated with each Client Session. The Session Façade handles all data access needs of its associated Business Logic.
- The DAOs are implemented using multiple Entity Beans (having CMP/BMP) so that we get Concurrency and can reduce data accesses across different client requests.
- The Session Bean communicates with the Entity Bean using Java RMI or local interfaces.
    1. Using local interface makes the communication faster since no network communication is used
    2. Using RMI makes the communication flexible enough to be used anywhere in network.

- Pros:
    1. No network communication between Business Logic and Entity Beans.
    2. Business Logic is not exposed beyond the corporate network.
    3. There is an opportunity for the Entity Bean to cluster the requests from different clients and reduce accesses to the database server across several different client requests that are temporally happening at the same time.
    4. The granularity of the Data Access Object (DAO) determines the level of concurrency desired in constructing the application service. This provides reusability opportunities.
- Cons: We’re causing **additional network access** to do the service we want for the data access and that can be mitigated by co-locating the Entity Bean and the Session Façade in the same EJB Container.