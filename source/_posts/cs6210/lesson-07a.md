# Lesson 7a: Distributed Subsystems L0- Global Memory Systems(GMS)

* How can we use peer memory for paging across LAN?

In a working set of multiple machines connected to LAN, some machines have more memory presure than the others. To utilize the memory from other machines to alleviate the busy ones is the main goal of GMS. The assumption is accessing the local disks take much more time than using the memory for paging accross the network. (Modern LANs can provide Gigabit or even 10 Gigabit connectivity between nodes, which can make it faster to access data from remote nodes than accessing data from a local disk.) In addition, we want to use idl cluster memory for other nodes in the network.

Comparing to tradition memory management: virtrual address -> physical address or disk, GMS trades network communication for disk I/O, changes the mapping to: virtrual address -> physical address or cluster memory or disk.

GMS only works for read across the network. The only pages that been paged out to the cluster memories are not dirty. GMS only serves as another level in the memory hierachy. The disk always has all of the copies of the pges.

## Basics

- In GSM, "cache" refers to physical memory, specifically dynamic random access memory (DRAM).
- Physical memory at each node is split into "local" (working set of currently executing processes) and "global" (community service for holding swapped out pages from fellow nodes).
- The split between local and global is dynamic and responds to memory pressure.
* Pages can be private or shared, and shared pages are the concern of the application for maintaining the **page coherence**.
	- The pages in "global" are always private to some processes.
	- The pages in "local" can be private or shared among multiple processes.
- GSM serves as a paging facility for remote paging and uses a page replacement algorithm (typically LRU) to manage memory.
- One of the key technical contributions of GSM is managing age information to pick the globally oldest page for replacement in the community service for handling page faults.

## Handling Page Faults 

### Case 1

![](https://i.imgur.com/JADVQuh.png)
- Physical memory on each host is divided into local and global parts.
- Page fault handling in GMS involves finding if the page is in the global cache of another node in the cluster.
- If the page is found in another node's global cache, that node sends the page to the requesting node.
- The requesting node's local allocation of physical memory increases by one.
- To make space for the new page, the requesting node sends the oldest page from its global cache to the node that had the requested page in its cache.
- The global allocation (community service part) of the requesting node decreases by one, while the global allocation of the sending node remains unchanged.

### Case 2

![](https://i.imgur.com/XSHGtGw.png)

- In this case, there is no community service happening on host P due to high memory pressure.
- If there is another page fault, the only option is to throw out some page from its current working set to make room for the missing page.
- The victim candidate for the page is chosen from the local part of host P.
- The oldest page from the local part of host P is sent out as a victim.
- The distribution of local and global on host P remains unchanged, as global is already zero.
- There is no change on host Q in terms of the split between local and global.

### Case 3

![](https://i.imgur.com/30dNwHF.png)
- In this case, the faulting page is not available in the cluster memories and needs to be fetched from disk.
- The local allocation of physical memory on host P increases by one as the working set grows due to the page fault.
- To make room for the new page, the global allocation on host P decreases by one and the oldest page from the global cache is sent to a peer memory in the cluster.
- The peer memory that receives the replacement page could be either in the local or global part of the host.
- If the oldest page on the peer memory is in the global cache, it is discarded. If it is in the local part, it could be dirty and needs to be written back to disk.
- The local allocation of physical memory on the peer memory could decrease if the globally oldest page is in the local part and can be thrown out.
- The local and global allocation on host P changes as described above, while the allocation on the peer memory could remain unchanged or decrease depending on the globally oldest page.

### Case 4

![](https://i.imgur.com/ONGX0Ip.png)

- In this case, a page is actively shared between host P and host Q.
- When a page fault occurs on host P for page X, GMS finds that page X is in the local cache of host Q and makes a copy of it into the local cache of host P.
- The working set on host P increases, so the local allocation of physical memory on host P goes up by one and the global allocation goes down by one.
- GMS picks an arbitrary page from the global cache on host P to send to the host R that has the globally oldest page.
- The total memory pressure in the cluster goes up by one, so host R must pick an LRU candidate from its physical memory to send to the disk and make room for the incoming page from host P.
- If the LRU candidate comes from the local cache of host R, the working set on host R decreases and the local allocation goes down by one, while the global allocation goes up by one.
- The active sharing of page X between host P and host Q does not concern GMS for maintaining coherence between the copies on multiple nodes.

## Local and Global Boundary

![](https://i.imgur.com/PF6RiZy.png)

- In all cases except where the global part of the faulting node's cache is empty, the local part goes up by one and the global part comes down by one.
- When the faulting page is in the global cache of a different node, there is no change in the balance between local and global on either node.
- If the faulting page is on disk, we have to make space in the cluster memory by throwing out a page, and if the LRU page on the node with the globally oldest page is in the local cache, the local part goes down by one and the global part goes up by one.
- If the page is actively shared, there is no change in the balance between local and global on either node, but one of the node's global pages has to be sent to the node with the globally oldest page, and if the replacement candidate comes from the local cache, the local part shrinks by one and the global part increases by one to accommodate the new page.

## Behavior of Algorithm

- The behavior of GMS global memory management is dynamic, not static.
- The split between local and global cache changes based on the memory pressure at a particular node.
- Idle nodes with a decreasing working set can become memory servers for peers on the network.
- The algorithm does not handle coherence maintenance, which must be managed at a higher level of software.
- The global cache acts as a surrogate for the disk, providing faster access to pages than the disk itself.
- The algorithm optimizes memory usage by swapping pages between nodes in the LAN.

## Geriatrics!(Age management)

![](https://i.imgur.com/XAZXJfL.png)

- Age management is a critical part of the GMS system, as it determines which pages should be evicted and replaced with new pages.
- The age of a page represents how long it has been since it was last accessed, with smaller ages indicating more recently accessed pages.
- The GMS system breaks age management into epochs, which are time periods during which management work is done by a single node.
- The duration of an epoch is set by the parameter T, which is the maximum duration that an epoch can last.
- The epoch management work is either time-bound (limited by T) or space-bound (limited by M replacements). M is another parameter that represents the maximum number of page replacements that can occur in an epoch.
- At the beginning of each epoch, each node sends its age information to the initiator node. This includes the age of all local and global pages residing on the node.
- The initiator node calculates the minimum age of the M pages that will be replaced in the upcoming epoch. It also computes the weight for each node, which represents the fraction of replacements that will come from that node.
- The node with the highest weight becomes the initiator for the next epoch.
- When a page fault occurs, the node checks the age of the page that needs to be replaced. If the age is greater than the minimum age, the page is discarded. If it is less than the minimum age, the node sends the page to a peer node based on the weight distribution.
- By using age management to approximate a global LRU (Least Recently Used) algorithm, the GMS system ensures that older pages are evicted and replaced with newer pages, thus improving overall system performance.
- The GMS system also follows the principle of thinking globally but acting locally, where global information is used to make local decisions.

## Implementation in Unix

![](https://i.imgur.com/hD6Yv6m.png)

- In systems research, identifying a pain point and coming up with a clever solution is important.
- Implementing the solution, even if it's a simple idea, requires heavy lifting and technical details.
- Implementation tricks and techniques can be reusable knowledge for other systems research.
- The authors of GSM used the OSF/1 operating system by DEC(Digital Equipment Corporation) operating system as the base system for their memory management system.
- The OSF/1 memory system has two key components: the virtual memory system (VM) and the unified buffer cache (UBC).
- The virtual memory system (VM) is responsible for mapping process virtual address space to physical memory, and the unified buffer cache (UBC) is used by the file system to cache disk-resident files in physical memory.
- The GMS implementation required modifying both the VM and UBC components of the operating system to support the global memory system.
- Writing pages to disk remains unchanged in the GMS implementation, as only page faults are redirected to the cluster memory.
- Collecting age information for anonymous pages in the VM is challenging since the operating system doesn't see individual memory accesses made by a user process. To address this, the GMS implementation includes a daemon that periodically dumps the contents of the Translation Lookaside Buffer (TLB) to collect age information for anonymous pages.
- The GMS implementation also includes modifications to the pageout daemon and free list maintenance for allocating and freeing frames on each node.
- The technical details of how GMS integrates with the VM, UBC, and other components of the operating system are important and may be reusable knowledge for other systems research.

## Data Structures

![](https://i.imgur.com/UNrPfGS.png)

- GMS uses distributed data structures for virtual memory management across the cluster.
- The virtual address is converted into a universal ID (UID) to uniquely identify a virtual address.
- Three key data structures are used: PFD (Page frame Directory), GCD (Global Cache Directory), and POD (Page Ownership Directory).
- The **POD tells which node owns which pages**, and it is replicated on all nodes in the cluster. The **GCD maps UIDs (unique identifiers for virtual addresses) to the nodes that host the corresponding PFDs**. The **PFD contains the mapping between UIDs and page frame numbers (PFNs)** and is stored on the node that owns the page.
- When a **page fault occurs**, the node first converts the virtual address to a UID and uses the POD to determine the owner of the page. It then uses the GCD to find the node that hosts the PFD for that UID and sends the UID to that node. The node with the PFD retrieves the page and sends it back to the requesting node.
	- ![](https://i.imgur.com/FA1JAou.png)
	- Node A converts virtual address to UID and goes to page ownership directory (POD)
	- POD tells Node A who the owner of the page is (Node B), which has the Global Page Frame Directory (GCD)
	- Node B looks up its GCD and sends UID to node C, which has the Page Frame Directory (PFD) for that UID
	- Node C retrieves the page, sends it to Node A, which maps it and resumes the process
- Network communication occurs only when there is a page fault, and most page faults are for non-shared pages, meaning the POD and GCD are co-resident on the same node. In this case, there is no network communication to look up the GCD.
- There can be a **miss when requesting a page**, which can happen if the page has been evicted from the PFD or if the POD information is stale due to changes in the network. In these cases, the request can be retried after looking up the updated POD or GCD.
	- ![](https://i.imgur.com/Ie6o0Rf.png)
	- Misses are uncommon compared to page faults, and network communication is mostly local to the node
- To handle **page evictions**, each node has a paging daemon that puts evicted pages onto a candidate node based on weight information obtained from the geriatric management system (GMS). The paging daemon also coordinates with the GMS to update the GCD with the new PFD location for the corresponding UID. This happens in an aggregated manner when the free list falls below a threshold.
	- ![](https://i.imgur.com/e1KKUws.png)

## Conclusion

The concept of paging across a network is interesting but may not be feasible in certain environments such as individual-owned workstations. However, it may be feasible in large-scale clusters in data centers. The enduring aspects of this research are the techniques, distributed data structures, and algorithms for implementing the concept. The next lesson module will feature another thought experiment on using cluster memory.
