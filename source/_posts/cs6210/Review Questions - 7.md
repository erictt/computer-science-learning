Giant Scale services
--------------------
1) Discuss the pros and cons of load management at different levels in
   giant scale services.

2) Discuss the tradeoffs between replication and partitioning in architecting
   the data repositories of giant scale services.

3) Define the availability metrics: "uptime", "yield", and "harvest".

4) Explain the DQ principle and how it helps in handling graceful
   degradation of giant scale services.

5) Discuss the pros and cons of the three approaches to online evolution of
   giant-scale services: "fast reboot", "rolling upgrade", and "big flip".

Map-Reduce
----------
1) Write a Map-Reduce solution for ranking the pages of web pages.  Be explicit
   in identifying the <key, value> of the map and reduce functions both for
   input and output.

2) What "heavy lifting" is involved in large-scale distributed implementation
   of the map-reduce paradigm.

3) What is the work done by the "Reduce" worker thread in the implementation
   of the Map-Reduce paradigm.

4) How does the implementation deal with redundant Map and Reduce workers that
   could potentially be working on the same "split" of the data set for the
   map and reduce operations, respectively?

5) Describe the difference between public and private clouds.

CoralCDN
----------
1) Distinguish between the storage and retrieval mechanisms in
   traditional DHT and DSHT. [Use the link for DHT
   from the class presentation powerpoint if you need more
   information on traditional DHT.]

2) A Coral node comes to life.  Step through the process by which
   it becomes a member of the Coral CDN.

3) A Coral node makes a web page request for a coralized URL through its
   web browser.  Step through the process by which it gets the page it
   is requesting to appear on the browser.

4) Enumerate and discuss the differentiating factors between the
   design spaces of Coral CDN and traditional CDNs (such as Akamai).

5) Explain tree saturation.  How is that experienced in CDNs?

6) Explain how the key-based routing layer of Coral mitigates the
   slashdot effect.

7) Why is Coral called "sloppy" DHT?

8) Let Li be a given level of the Coral CDN cache hierarchy.  Let Lj, Lk, Lm
   be levels higher than Li to which members of Li belong.

   Li contains all the content of Lj, Lk, and Lm.

   Explain if this is True or False with justification.

9) Why are traditional methods of evaluating CDNs or Web servers not
   appropriate for evaluating Coral CDN?

Web Technologies (not for exam)
-------------------------------
1) Explain how SOAP enables RPC across different programming
   languages and implementation platforms.

2) Distinguish between abstract binding and concrete binding in WSDL.

3) Explain the power of the tmodel mechanism in UDDI for future evolution
   of services.

4) Discuss the need for implementing security measures at the SOAP level.

5) Bring out the analogy between traditional distributed system building
   components (processes, parallelism, ordering, transactions, etc.)
   and the service compostion framework of Web Services.
