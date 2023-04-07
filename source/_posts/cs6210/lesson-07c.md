# Lesson 7: Distributed Subsystems - Distributed File Systems

How to use cluster memory for cooperate caching of files?

## Preliminaries (Striping a File to Multiple Disks)

<img src="https://i.imgur.com/JcOBi7z.png" style="width: 800px" />

- RAID stands for redundant array of inexpensive disks, and it allows multiple disks to be strung together in parallel to increase I/O bandwidth.
- A file can be striped across multiple disks to increase overall I/O bandwidth.
- Error-correcting codes are used to detect and correct errors in the data that is striped across multiple disks.
- The RAID technology can have a small write problem, which occurs when small files are written across multiple disks, making it inefficient to read.

## Preliminaries (Log Structured File System)

<img src="https://i.imgur.com/3EiWC14.png" style="width: 800px" />

- Log structured file systems write changes to files as log records rather than writing the file as-is.
- Changes to multiple files can be buffered in a contiguous log segment data structure and written out sequentially to the disk.
- The log segment can be striped across multiple disks using RAID technology.
- The log structured file system solves the small write problem by writing changes to multiple files in one log segment rather than writing small files across multiple disks.
- Latency may be associated with reading a file for the first time from the disk in a log structured file system.
- Logs must be cleaned periodically to remove old writes to parts of a file that are no longer relevant.

## Preliminaries Software (RAID)

<img src="https://i.imgur.com/67Rr4ds.png" style="width: 800px" />

- Software RAID is a solution to the problems of hardware RAID, which can be expensive and have difficulty handling small writes.
- The Zebra file system is an example of software RAID that combines log-structured file systems and RAID technology.
- The file system uses commodity hardware, such as nodes connected to disks in a local area network, to stripe log segments across multiple nodes.
- Log segments representing changes made to multiple files on a client node are striped across different nodes.
- The process of striping log segments in software RAID is similar to hardware RAID, with **the software performing the striping** on multiple nodes in a local area network.


## Putting Them All Together Plus More

- xFS is a distributed file system built at UC Berkeley.
- It builds on prior technologies, including log-based striping from the Zebra file system and co-operative caching.
- xFS aims to be truly scalable and move towards serverlessness, meaning no reliance on a central server.
- It introduces new techniques such as **dynamic management of data** and **metadata**, **subsetting of the storage servers**.
- Further details on these techniques will be discussed in the rest of the lecture.

## Dynamic Management

<img src="https://i.imgur.com/3FJGX02.png" style="width: 800px" />


- In a traditional centralized NFS server, data blocks reside on disks while metadata and file cache are stored in the memory of the server.
- The server keeps a client caching directory to track who is accessing its files.
- However, this centralized structure can result in hot spots and scalability issues.
- In xFS, metadata management is dynamically distributed and data structures like metadata, file cache, and caching information can be distributed among nodes.
- This allows for dynamic management of data and metadata to avoid hot spots.
- xFS also utilizes cooperative client caching to conserve memory and increase efficiency.

##  Log Based Striping and Stripe Groups

<img src="https://i.imgur.com/upizWO9.png" style="width: 800px" />

- xFS uses log based striping in software to avoid small write problems.
- Clients write changes made to files to an append only log, which is a data structure residing in the memory of the client.
- When the log segment fills up, it is written to disk and striped across storage servers.
- Storage servers keep log segments written by different clients.

<img src="https://i.imgur.com/ksP4NUx.png" style="width: 800px" />

- Stripe groups subset the storage servers and assign different groups for different log segments.
- This allows parallel client activities and increases availability and throughput.
- Efficient log cleaning is facilitated by stripe groups and allows for parallelism in management of the system.
- Subsetting the server group for striping increases availability and allows for incremental satisfaction of the user community in spite of failures.

## Cooperative Caching

<img src="https://i.imgur.com/cdl6Zj3.png" style="width: 800px" />


- xFS uses available memory in clients to cooperatively cache files and reduce stress on data file management.
- Unlike traditional Unix file systems, xFS worries about cache coherence and **maintains it at the file block level**.
- If a file is being read-shared by multiple clients, a write request results in a conflict, and the manager sends an invalidation message to the clients, revokes the token given to the requesting client, and distributes the file to a future requester.
- Using the fact that copies of the file exist in multiple clients, xFS exploits this to do cooperative caching and retrieve file content from a client's cache instead of going to the disk.

##  Log Cleaning

<img src="https://i.imgur.com/CGkOb6X.png" style="width: 800px" />


- As client activities progress, log segments evolve on the disk, and log cleaning is required to clean up the disk and get rid of unnecessary data.
- Log cleaning involves finding the utilization status of old log segments, picking some log segments to clean, reading all the live blocks in the chosen log segments, and writing them into a new log segment before garbage collecting the old segments.
- xFS makes clients responsible for log cleaning and stripe groups responsible for cleaning activities in their set of servers.
- The leader of each stripe group assigns cleaning services to the members of the group, and conflicts between client updates and cleaner functions are resolved by the manager.

## Unix File System

https://cs.ericy.me/cs6200/p3l5-io-management/index.html#ext2-second-extended-filesystem

##  xFS Data Structures

![](https://i.imgur.com/1OqtNsL.png)

<img src="https://i.imgur.com/TK2zEGg.png" style="width: 800px" />


- Metadata management in a distributed file system is not static.
- Every client node has a replicated data structure called **manager map** that tells who the metadata manager is for a particular file name.
- The manager node uses a **file directory** data structure to map the file name to an i-number and an i-map data structure to get the i-node address for that file.
- The **stripe group map** tells how the file is striped and which storage server contains the log segment ID associated with that file.
- The manager has to go through multiple data structures to go from the file name to the data blocks associated with that file, but caching helps reduce the long path for file access.

## Client Reading a File Own Cache

In the xFS distributed file system, caching plays a significant role in improving file access performance. When a client node receives a file name and offset, it looks up the directory to obtain an index and offset. If the file has been accessed before and is in the client's cache, then the data block can be obtained from the local cache, bypassing the need for network communication and disk access. This provides the fastest path for file access and is the common case.
- <img src="https://i.imgur.com/6WR5Wcx.png" style="width: 800px" />

However, if the file is not in the client's cache, then the client has to consult the manager map data structure to determine the metadata manager for the file. This may involve a network hop to the manager node. If the manager node determines that the file is currently in another client's cache, then the data can be obtained from that client's cache, which is still faster than disk access. This is the second-best path for file access and may involve multiple network hops.
- <img src="https://i.imgur.com/OFQ9JcV.png" style="width: 800px" />
In the worst-case scenario, the file is not in any cache and has to be retrieved from disk. This involves a longer path, with multiple data structures involved. The client node consults the manager map data structure to determine the metadata manager for the file and obtains the index and offset from the directory. The manager node then looks up its imap data structure and stripe group map data structure to determine the location of the i-node that corresponds to the log segment for the requested data block. The manager then contacts the storage server to obtain the index node of the log segment ID and uses the stripe group map to determine which storage servers have the log segment striped and which one to contact for the requested portion of the file.
- <img src="https://i.imgur.com/L504Bqd.png" style="width: 800px" />

This long path involves network hops and accessing storage servers to retrieve the data blocks. However, if the index node for the log segment ID associated with the file has been previously accessed by the manager, it may be present in the manager's cache, allowing the manager to bypass some of the network hops. Overall, caching helps minimize the number of network hops and disk access needed for file access, improving performance in the xFS distributed file system.

### The whole picture

![](https://i.imgur.com/NZySsHc.png)


## Client Writing a File

<img src="https://i.imgur.com/YNgl6e8.png" style="width: 800px" />

- Writing to a file involves aggregating writes into a Log Segment Data Structure in the client's memory.
- The client flushes the Log Segment to the disk, striping it on the Storage Servers that are part of the Stripe Group.
- The manager is notified of the Log Segments being flushed to the disk.
- Technical Innovations of xFS include **Log-based Striping**, **Cooperative Caching with Dynamic Management of Data and Metadata**, and **Distributive Log Cleaning**.

## Distributed File Systems Conclusion

- Network file systems are essential in any computing environment.
- Companies like NetApp have developed scalable NFS products.
- Lessons learned from the design and implementation of distributed file systems can be applied to other distributed subsystems.
- Creative techniques were used to fully utilize memory available in local area network nodes in the studied papers on GSM, DSM, and DFS.