# Lesson 7c: Distributed Subsystems - Distributed File Systems

How to use cluster memory for cooperate caching of files?

## Preliminaries (Striping a File to Multiple Disks)

![](https://i.imgur.com/JcOBi7z.png)

- RAID stands for redundant array of inexpensive disks, and it allows multiple disks to be strung together in parallel to increase I/O bandwidth.
- A file can be striped across multiple disks to increase overall I/O bandwidth.
- Error-correcting codes are used to detect and correct errors in the data that is striped across multiple disks.
- The RAID technology can have a small write problem, which occurs when small files are written across multiple disks, making it inefficient to read.

## Preliminaries (Log Structured File System)

![](https://i.imgur.com/3EiWC14.png)

- Log structured file systems write changes to files as log records rather than writing the file as-is.
- Changes to multiple files can be buffered in a contiguous log segment data structure and written out sequentially to the disk.
- The log segment can be striped across multiple disks using RAID technology.
- The log structured file system solves the small write problem by writing changes to multiple files in one log segment rather than writing small files across multiple disks.
- Latency may be associated with reading a file for the first time from the disk in a log structured file system.
- Logs must be cleaned periodically to remove old writes to parts of a file that are no longer relevant.

## Preliminaries Software (RAID)

![](https://i.imgur.com/67Rr4ds.png)

- Software RAID combines log structured file system and RAID technology.
- Log segments are written to nodes connected to disks on a local area network rather than data files.
- The log segment can be striped across multiple nodes using software RAID technology.
- The software RAID technology solves the problem of using expensive hardware in hardware RAID technology.


## Putting Them All Together Plus More

https://github.com/audrey617/CS6210-Advanced-Operating-Systems-Notes/blob/main/img/l7/54.JPG?raw=true
![](https://i.imgur.com/GrrASy9.png)

- xFS is a distributed file system built at UC Berkeley.
- It builds on prior technologies, including log-based striping from the Zebra file system and co-operative caching.
- xFS aims to be truly scalable and move towards serverlessness, meaning no reliance on a central server.
- It introduces new techniques such as dynamic management of data and metadata, subsetting of the storage servers.
- Further details on these techniques will be discussed in the rest of the lecture.

## Dynamic Management

![](https://i.imgur.com/3FJGX02.png)


- In a traditional centralized NFS server, data blocks reside on disks while metadata and file cache are stored in the memory of the server.
- The server keeps a client caching directory to track who is accessing its files.
- However, this centralized structure can result in hot spots and scalability issues.
- In xFS, metadata management is dynamically distributed and data structures like metadata, file cache, and caching information can be distributed among nodes.
- This allows for dynamic management of data and metadata to avoid hot spots.
- xFS also utilizes cooperative client caching to conserve memory and increase efficiency.

##  Log Based Striping and Stripe Groups

![](https://i.imgur.com/wCHkmcB.png)


![](https://i.imgur.com/ksP4NUx.png)


- xFS uses log based striping in software to avoid small write problems.
- Clients write changes made to files to an append only log, which is a data structure residing in the memory of the client.
- When the log segment fills up, it is written to disk and striped across storage servers.
- Storage servers keep log segments written by different clients.
- Stripe groups subset the storage servers and assign different groups for different log segments.
- This allows parallel client activities and increases availability and throughput.
- Efficient log cleaning is facilitated by stripe groups and allows for parallelism in management of the system.
- Subsetting the server group for striping increases availability and allows for incremental satisfaction of the user community in spite of failures.

## Cooperative Caching

![](https://i.imgur.com/cdl6Zj3.png)


- xFS uses available memory in clients to cooperatively cache files and reduce stress on data file management.
- Unlike traditional Unix file systems, xFS worries about cache coherence and maintains it at the file block level.
- If a file is being read-shared by multiple clients, a write request results in a conflict, and the manager sends an invalidation message to the clients, revokes the token given to the requesting client, and distributes the file to a future requester.
- Using the fact that copies of the file exist in multiple clients, xFS exploits this to do cooperative caching and retrieve file content from a client's cache instead of going to the disk.

##  Log Cleaning

![](https://i.imgur.com/CGkOb6X.png)


- As client activities progress, log segments evolve on the disk, and log cleaning is required to clean up the disk and get rid of unnecessary data.
- Log cleaning involves finding the utilization status of old log segments, picking some log segments to clean, reading all the live blocks in the chosen log segments, and writing them into a new log segment before garbage collecting the old segments.
- xFS makes clients responsible for log cleaning and stripe groups responsible for cleaning activities in their set of servers.
- The leader of each stripe group assigns cleaning services to the members of the group, and conflicts between client updates and cleaner functions are resolved by the manager.

## Unix File System

![](https://i.imgur.com/eoWPhnl.png)
![](https://i.imgur.com/3cBvZg4.png)


- xFS implementation details are being discussed.
- Unix file systems have i-node data structures.
- i-nodes map file names to data blocks on the disk.
- The file system can use the i-node to determine where the data blocks are located based on a file name and offset.
- This is a standard feature of Unix file systems.

##  xFS Data Structures

![](https://i.imgur.com/TK2zEGg.png)


- Metadata management in a distributed file system is not static.
- Every client node has a replicated data structure called manager map that tells who the metadata manager is for a particular file name.
- The manager node uses a file directory data structure to map the file name to an i-number and an i-map data structure to get the i-node address for that file.
- The stripe group map tells how the file is striped and which storage server contains the log segment ID associated with that file.
- The manager has to go through multiple data structures to go from the file name to the data blocks associated with that file, but caching helps reduce the long path for file access.

## Client Reading a File Own Cache

![](https://i.imgur.com/6WR5Wcx.png)


![](https://i.imgur.com/OFQ9JcV.png)


![](https://i.imgur.com/L504Bqd.png)


- Local caching of files in a client's memory helps speed up file access.
- If a file is not in the local cache, the client consults the manager map data structure to know who's the manager for that file.
- The manager may tell the client that another peer has a copy of the file in their cache, and the data can be obtained from there.
- If the data is not available in any cache, the manager has to go through multiple data structures to find the data blocks on a storage server, and there could be multiple network hops involved.
- The worst-case scenario involves accessing all the data structures in the manager, going through network hops and storage lookups to get the data blocks for the requested file.

## Client Writing a File

![](https://i.imgur.com/YNgl6e8.png)

- Writing to a file involves aggregating writes into a Log Segment Data Structure in the client's memory.
- The client flushes the Log Segment to the disk, striping it on the Storage Servers that are part of the Stripe Group.
- The manager is notified of the Log Segments being flushed to the disk.
- Technical Innovations of xFS include Log-based Striping, Cooperative Caching with Dynamic Management of Data and Metadata, and Distributive Log Cleaning.

## Distributed File Systems Conclusion

- Network file systems are essential in any computing environment.
- Companies like NetApp have developed scalable NFS products.
- Lessons learned from the design and implementation of distributed file systems can be applied to other distributed subsystems.
- Creative techniques were used to fully utilize memory available in local area network nodes in the studied papers on GSM, DSM, and DFS.