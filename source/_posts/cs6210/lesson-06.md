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

<img src="https://i.imgur.com/DcP7IoO.jpg" style="width: 800px" />

* Procedural Design:
    - The code is written as a monolithic entity.
    - We have a **shared state** represented by the global variables, and **private states** represented by the function calls.
* Object-Based Design:
    - The **state is contained inside** the object.
    - Methods inside the object manipulate the state. Only the methods are visible externally.
* In Spring, Object Orientation is applied to build the OS Kernel.

### Spring Approach

<img src="https://i.imgur.com/LA1GcVB.jpg" style="width: 800px" />

* Provide strong interfaces to each sub-system.
* The system is open and flexible. Thus, 3rd party vendors can integrate their software to the system.
* **IDL** (**Interface Definition Language**) is used to define the OS interfaces. This provided flexibility in terms of the programming language.
* The kernel in Spring is used to facilitate extensibility:
    - **Nucleus**: Threads + IPC.
    - **Virtual Memory Manager**: Memory management.
* Sun provided a “Network Proxy” node so that the OS can be used as a network OS.

### Nucleus

<img src="https://i.imgur.com/6hhzK8G.jpg" style="width: 800px" />

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

<img src="https://i.imgur.com/fqjELzn.jpg" style="width: 800px" />

* Object invocation between client/server domains across the network is facilitated using the **Network Proxy**.
* Each domain has **multiple Network Proxies** to communicate with different nodes on the network. This facilitates specialization since these different proxies can represent different protocols.
* Network Proxies are invisible to the clients/servers.
* How to establish communication over the network?
    - A Network Proxy ($\text{𝑃𝑟𝑜𝑥𝑦}_𝑠$) will be instantiated on the server node and a Door will be created for communication between this proxy and the server domain through the Nucleus.
    - $\text{𝑃𝑟𝑜𝑥𝑦}_𝑠$ will export the network handle embedding the Door created on the server domain to the Network Proxy of the client domain $\text{𝑃𝑟𝑜𝑥𝑦}_c$. These Proxies and the communication between them are outside the kernel.
    - $\text{𝑃𝑟𝑜𝑥𝑦}_c$ will use this network handle to establish a connection between the client’s Nucleus and the server’s Nucleus.
    - The client domain will then invoke the Door inside its Nucleus and the two proxies will facilitate the invoking the server.

### Secure Object Invocation

<img src="https://i.imgur.com/pdKetTH.jpg" style="width: 800px" />

- A server object may need to provide different privilege levels to different clients. In Spring, the security model uses a **Front Object** to provide different privilege levels for different clients.
* An underlying object may have a Front Object that is directly connected to it (without Doors).
* Whenever a client domain tries to access this protected domain, the Front Object will check the **Access Control List (ACL)** to see what privileges this client domain has for accessing the protected domain.
* Different instances of the Front Object can be created with different access policies to the same underlying object.
* **Doors as software capabilities**, can be passed from client domain to other domains, and the policies can be implemented through the front object. 
	* e.g. the Front Object can reduce the privilege level of the capability provided to the printer object as a one-time capability.

<img src="https://i.imgur.com/NrkosOK.jpg" style="width: 800px" />

### Virtual Memory Management

<img src="https://i.imgur.com/dNnZ6w1.jpg" style="width: 800px" />

* **Virtual Memory Manager (VMM)**: The VMM is responsible for managing the linear address space of a process by dividing it into regions and mapping those **memory regions** to specific **memory objects**.
	* The abstraction of a memory object allows a region of virtual memory to be associated with a backing file, or swap space on the disk.
	* allows a region of virtual memory to be associated with a backing file, or the swap space on the disk
	* allow different regions of the same address space are mapped to the same memory object

#### Pager Object

<img src="https://i.imgur.com/orpJYt3.jpg" style="width: 800px" />

* **Pager objects**: Pager objects establish the connection between virtual memory (memory objects) and physical memory (cached object representations in DRAM). They are responsible for ensuring that memory objects are brought into physical memory when the process needs to access a particular region of its address space.
* **Cached object representations**: When a pager object maps a memory object to a region of the address space, it creates a cached object representation in DRAM. This allows the process to access that portion of its address space.
- **Shared memory objects**: It is possible for a memory object to be shared between two different address spaces. In this case, distinct pager objects are responsible for managing the coherence of the cached representations of the shared memory object in the two address spaces.

### Comparison to other OSes

* Object oriented kernel
    - nucleus -> threads + IPC
    - linedkie's microkernel -> nucleus + address space
    - door + doortable -> basis for cross domain calls
    - object invocation and cross machine calls
    - virtual memory management
        - Address space object, memory object, external pagers, cached object.
* Compare to Tornado. Tornado uses uses clustered object as an optimization for implementing kernel services. Spring's object technology permeates entire OS for structuring mechanism.

### Dynamic Client-Server Relationships

- Spring is a network OS. The clients and servers interact seamlessly, regardless of their physical location in the network. 
* Scenario #1: We have several replicas of the servers (to increase availability). The clients will be dynamically routed to different servers depending on the physical proximity of the client and the server, and also on the load distribution.
* Scenario #2: The servers are cached. The clients can dynamically access these cached copies instead of accessing the servers themselves.
* Then, we have two types of dynamic decisions:
    - In Scenario #1: Deciding which server replica the client should access.
    - In Scenario #2: Deciding which cached copy the client should access.
* Spring OS uses “Subcontracts” to manage these decisions.

#### Subcontract

* As mentioned earlier, IDL is used to define the OS interfaces.
* The **Subcontract is the implementation of the IDL interfaces**, it hides the runtime behavior of an object from the actual interface.
    - For instance, there could be a singleton implementation of the server, or it could be a replicated implementation of the server. The client does not care.
* The client stub generation will be simple, since all the details about the server will be hidden in the Subcontract.

* IDL compiler is used to produce three pieces of source code: 
    1) A language specific form of the IDL interface 
    2) Client side stub code: Code meant to be dynamically linked into a client’s program to access an object that is implemented in another address space or on another machine 
    3) Server side stub code: Code to be linked into an object manager to translate incoming remote object invocations into the run-time environment of the object’s implementation.

* **Dynamic loading of subcontracts**: Subcontracts can be discovered and installed at runtime, allowing for seamless addition of functionality to existing services. For example, if a singleton server becomes replicated, a new subcontract can be introduced to handle the replicated servers without any changes to the client stub.
* Marshal/Unmarshal Interface: The Subcontract will marshal/unmarshal arguments when requested by the client. The Subcontract will do the appropriate steps to execute the request based on the location of the server (e.g. on the same machine, on the network, on a different processor, etc.).

### Conclusion

* Spring OS uses object technology as a structuring mechanism in building a network OS.
    - Strong interfaces.
    - Flexibility.
    - Extensibility: Spring OS has a microkernel.
* Spring OS uses Network Proxies: The client and the servers don’t have to know the locations of each others.
* Subcontract mechanism allows the clients and the servers to dynamically change the relationships between each others without changing the client/server stubs.

## L06b. Java RMI

### Java Distributed Object Model

* The Java Distributed Object Model, also known as Java Remote Method Invocation (RMI), simplifies the process of creating client-server systems by handling aspects like marshaling, unmarshaling, and publishing remote objects for clients. It shares some similarities with the Spring system's subcontract mechanism.
* Here's an overview of the Java Distributed Object Model:
    - **Remote Object**: Accessible from different address spaces.
    - **Remote Interface**: A remote interface defines the method declarations for a remote object that clients can access from anywhere.
    - **Failure Semantics**: Clients in the Java distributed object model must handle RMI exceptions, which represent failure scenarios when invoking remote methods.
* **Similarities/differences between local objects and remote objects**:
	- **Similarity**: Both local and remote objects in Java allow passing object references as parameters when making an object invocation. 
	- **Difference**: The passing mechanism for remote objects is **value/result**, meaning a **copy of the object** is sent to the invoked method. In contrast, local objects pass a **pure reference**, allowing modifications made by the invoked method to be reflected in the original object. This difference means that any changes made by the client to an object after passing its reference to the server will not be visible to the server.

### Local vs. Remote Implementation

In this example, we'll construct a bank account server using Java's distributed object model. The server provides APIs for deposit, withdrawal, and balance inquiries. We'll consider two possibilities for implementing this service as a distributed object accessible from clients anywhere in the network below. Before divng into details. Here are some definitions
1. Remote Interface(`java.rmi.Remote`): This interface is completely abstract and has no methods.
	- `interface Remote {}`
2. Remote interface: `BandAccount` for a bank account extends `Remote`.

	```Java
	import java.rmi.*;
	
	public interface BankAccount extends Remote {
		public void deposit(float amount) throws RemoteException;
		public void withdraw(float amount) throws OverdrawnException, RemoteException;
		public float balance() throws RemoteException;
	}
    ```

4. Reuse of Local Implementation:
	- <img src="https://i.imgur.com/2OUnyDd.png" style="width: 400px" />
	- The developer starts with a local class called `Account` and extends it to create a `BankAcctImpl` class with public API methods.
	- Using Java's built-in `Remote` Interface, the server makes the `BankAccount` methods visible on the network.
	- In this approach, the developer has to do some extra work (the "heavy lifting") to make the location of the instantiated `BankAccount` object visible to clients on the network. This typically involves setting up a registry service that maps the `BankAccountInterface` to the actual location of the `BankAccount` object.
5. Reuse of Remote Object Class
	- <img src="https://i.imgur.com/6yNF0sO.png" style="width: 400px" />
	- Similar to the last implementation, the developer writes the `BankAccount` interface and publishes its methods using the `Remote` Interface. 
	- The difference is, the `BankAcctImpl` extends `RemoteServer` classes and implements `BankAccount` Interface.

		```Java
		package myPackage;
		
		import java.rmi.RemoteException; 
		import java.rmi.server.RemoteServer;
		
		public class BankAcctImpl extends RemoteServer implements BankAccount {
			public void deposit(float amount) throws RemoteException {...};
			public void withdraw(float amount) throws OverdrawnException, RemoteException {...};
			public float balance() throws RemoteException {...};
		}
		```

	- When the BankAccount object is instantiated, it becomes instantly visible to network clients. This is because it **inherits the built-in classes** from the Java distributed object model.
	- Now, when we instantiate the BankAccount object, it becomes visible to the network clients through the Java Runtime System.
	- The Java RMI system is responsible for all the hard work of making the Server Object Instance visible to network clients and hence this is the more **preferred** way of building network services and making them available for remote clients anywhere on the network.

### How does Java RMI work?

* On Server side:
    - The server object is made visible on the network using the 3-step procedure:
        1. Instantiate the Object.
        2. Create a URL.
        3. Bind the URL to the Object Instance created.

	```Java
	BankAccount acct = new BankAcctImpl(); 
	URL url = new URL(“rmi://zaphod/account”); // bind url to remote object 
	java.rmi.Naming.bind(url, acct);
	```

    - This allows the clients to be able to discover the existence of the new service on the network.
* On Client side:
    - Any arbitrary client can easily discover and access the server object on the network using the following procedure:
        1. Lookup the service provider URL by contacting a bootstrap name server in the Java RMI system and get a local access point for that remote object on the client-side.
        2. Use the local access point for the remote object on the client-side by simply calling the invocation methods, which look like normal procedure calls.
            - The Java Runtime System knows how to locate the server object in order to do the invocation.
            - The client does NOT know or care about the location of the server object.
        3. If there are failures in any of execution of the methods (functions), then Remote Exceptions will be issued by the server through the Java Runtime System back to the client.
        - A problem with Remote Exceptions is that the client may have no way of knowing at what point in the call invocation the failure happened.

	```java
	BankAccount acct = java.rmi.Naming.lookup(url);// lookup account 
	float balance; 
	acct.deposit(243.50); 
	acct.withdraw(100.00); 
	balance = acct.balance();
	```

### RMI Implementation

<img src="https://i.imgur.com/vqPJnap.png" style="width: 400px" />

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

<img src="https://i.imgur.com/c5FFPXD.jpg" style="width: 800px" />

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

<img src="https://i.imgur.com/ezxgHld.jpg" style="width: 800px" />

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

![](https://i.imgur.com/dK29co9.png)

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

<img src="https://i.imgur.com/l8m6s1X.png" style="width: 800px" />

In this approach, **business logic** and **data access** are combined in a single **session bean**. The session bean acts as a "facade" and provides a **simplified interface for clients**. Clients interact with the session bean, which, in turn, manages the underlying data and enforces business rules. This approach is suitable for simple applications with limited data access requirements. However, it can lead to a **tight coupling** between business logic and data access, making the application less modular and harder to maintain.

- Pros:
    1. Minimal container services needed from the EJB container: The EJB container coordinates concurrent independent sessions.
    2. Business logic not exposed to the outside world since the Business logic is contained in the EJB container and not in the Web container.
- Cons:
    1. The application structure is similar to a **monolithic** kernel.
    2. Limited concurrency for database access, missed opportunity for parallel data retrieval.

#### 2. Data Access Object(DAO)

fine-grained

<img src="https://i.imgur.com/EJ5MxT2.png" style="width: 800px" />

The DAO pattern is a way to separate **data access logic** from **business logic**. DAOs are responsible for accessing and manipulating the data in the underlying data storage, while the business logic is encapsulated in session beans. Clients interact with session beans, which delegate data access operations to DAOs. This separation of concerns makes the application more modular and easier to maintain. The DAO pattern can be combined with other patterns, such as the Value Object pattern, to improve the efficiency of data transfer between the application tiers.

- Pros:
	1. Exploits concurrency for data access, allows parallel requests to share data access.
	2. The granularity of the Data Access Object (DAO) determines the level of concurrency desired in constructing the application service. This provides reusability opportunities.
- Cons: 
	1. **Business Logic is exposed outside the corporate network** because it was move from the EJB container to the Web container.

#### 3. Session Beans with Entity Beans

<img src="https://i.imgur.com/mhP3do6.png" style="width: 800px" />

In this approach, business logic is encapsulated in session beans, while data access is handled by entity beans. Entity beans are designed to represent persistent data and manage the relationships between data entities. Clients interact with session beans, which, in turn, interact with entity beans to perform data operations. This approach helps separate business logic from data access and can provide better performance and scalability when dealing with complex data models. However, it can be more complex to implement and maintain, as it involves additional components and interactions.

- Pros:
	1. No network communication between Business Logic and Entity Beans.
	2. Business logic is not exposed beyond the corporate network.
	3. There is an opportunity for the Entity Bean to cluster the requests from different clients and reduce accesses to the database server across several different client requests that are temporally happening at the same time.
	4. The granularity of the Data Access Object (DAO) determines the level of concurrency desired in constructing the application service. This provides reusability opportunities.
- Cons: 
	1. May incur **additional network access** for data access service which can be mitigated by co-locating the Entity Bean and the Session Façade in the same EJB Container.