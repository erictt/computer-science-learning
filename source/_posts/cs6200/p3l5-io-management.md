# P3L5: I/O Management

<!-- toc -->
----

## I/O Devices

An input/output(I/O) device is any hardware used by a human operator or other systems to communicate with a computer.

<img src="https://i.imgur.com/GoPPub4.jpg" style="width: 400px" />

The picture shows a single CPU attached to the main memory of the system via some kind of **memory bus** or interconnect. Some devices are connected to the system via a general **I/O bus**, which in many modern systems would be **PCI** (or one of its many derivatives); graphics and some other higher-performance I/O devices might be found here. Finally, even lower down are one or more of what we call a **peripheral bus**, such as **SCSI**, **SATA**, or **USB**. These connect slow devices to the system, including **disks**, **mice**, and **keyboards**.

### I/O Device Features

A canonical device has two important components:
- The ﬁrst is the **hardware interface** it presents to the rest of the system. Just like a piece of software, hardware must also present some kind of interface that allows the system software to control its operation.
- The second part of any device is its **internal structure**. This part of the device is **implementation speciﬁc and is responsible for implementing the abstraction the device presents to the system**. Very simple devices will have one or a few hardware chips to implement their functionality; more complex devices will include a simple *CPU*, some *general purpose memory*, and other *device-speciﬁc chips* to get their job done.

<img src="https://i.imgur.com/cjg9fSk.jpg" style="width: 500px" />
In the picture above, the (simpliﬁed) device interface is comprised of three registers: 
- a **status** register, which can be read to see the current status of the device; 
- a **command** register, to tell the device to perform a certain task; 
- a **data** register to pass data to the device, or get data from the device. 
By reading and writing these registers, the operating system can control device behavior.

## CPU Device Interconnect

A device communicates with a computer system by sending signals over a cable or even through the air. The device communicates with the machine via a connection point, or **port**. If devices share a common set of wires, the connection is called a **bus**. A **bus**, like the PCI bus used in most computers today, is a set of wires and a rigidly defined protocol that specifies a set of messages that can be sent on the wires.

<img src="https://i.imgur.com/TOHsnsR.jpg" style="width: 600px" />

In the figure, a **PCIe bus** (the common PC system bus) connects the processor–memory subsystem to fast devices, and an **expansion bus** connects relatively slow devices, such as the keyboard and serial and USB ports. In the lower-left portion of the figure, four disks are connected together on a **serial-attached SCSI (SAS)** bus plugged into an SAS controller. PCIe is a flexible bus that sends data over one or more “lanes.” A lane is composed of two signaling pairs, one pair for receiving data and the other for transmitting.
* PCI: Peripheral Component Interconnect

## Device Drivers

Device Driver Layer
- hide the differences among device controllers from the I/O subsystem of the kernel,
- making the I/O subsystem **independent** of the hardware simplifies the job of the operating-system developer.

<img src="https://i.imgur.com/b9vgHN3.jpg" style="width: 600px" />
### Types of Devices

- **Block**: disk
    - read/write blocks of data
    - direct access to arbitrary block
- **Character**: keyboard
    - get() or put() one character.
- **Network devices**
    - One interface available in many operating systems, including UNIX and Windows, is the network **socket** interface.

OS represents device as special device files. On UNIX-like systems, all devices appear as files under the **/dev** directory. They are treated by the filesystems **tmpfs** and **devfs**.

## CPU/Device Interactions

The device registers appear to the CPU as memory locations at a specific physical address. When the CPU writes to these locations, the integrated PCI controller realizes that these accesses should be routed to the appropriate device.

This means that a portion of the physical memory on the system is dedicated for device interactions. We call this **memory-mapped I/O.** The portion of the memory that is reserved for these interactions is controlled by the **Base Address Registers** (BAR). These registers get configured during the boot process in accordance to the PCI protocol.

In addition, the CPU can access devices via special instructions. x86 platforms specify certain in/out instructions that are used for accessing devices. Each instruction needs to specify the target device - the I/O port - as well as some value that will be passed to the device. This model is called the **I/O Port Model**.

The path from the device to the CPU complex can take two routes. Devices can generate **interrupts** to the CPU. CPUs can **poll** devices by reading their status registers to determine if they have some response/data for the CPU.
* **interrupts**
    - upside: can be triggered by the device as soon as the device has info for the CPU
    - downside: multiple steps involved in the interrupt handler that cost CPU cycles
* **polling**
    - upside: the OS can choose to poll when convenient
    - downside: delay in how events are observed or handled; and too much polling cause CPU overhead

### Programmed I/O

**programmed I/O (PIO)** is a method of data transmission, via input/output (I/O), between a central processing unit (CPU) and a peripheral device. -- [Wikipedia](https://en.wikipedia.org/wiki/Programmed_input%E2%80%93output)

With PIO, the CPU issues instructions by writing into the command registers of the device. And the CPU controls data movement to/from the device by reading/writing into the data registers for the device.

However, when using programmed I/O (PIO) to transfer a large chunk of data to a device, the CPU is overburdened with a rather trivial task(simply transfer the data back and forth), and thus wastes a lot of time and effort that could better be spent running other processes.

Let's consider how a process running on the CPU transmits a network packet via a **network interface card (NIC)** device. There is a 1500B packet that we wish to transmit using 8 byte data registers. The whole operation will take 1 CPU access to the command register and then 188 = 1500/8 rounded up - accesses to the data register. In total, 189 CPU accesses are needed to transmit the packet.

### Direct Memory Access(DMA)

 The solution to this the overburden issue from PIO is **Direct Memory Access (DMA)**. A DMA engine is essentially a very specific device within a system that can orchestrate transfers between devices and main memory without much CPU intervention.

DMA works as follows. To transfer data to the device, for example, the OS would program the DMA engine by telling it where the data lives in memory, how much data to copy, and which device to send it to. At that point, the OS is done with the transfer and can proceed with other work. When the DMA is complete, the DMA controller raises an **interrupt**, and the OS thus knows the transfer is complete.

However, DMA configuration is not a trivial operation! It takes many more cycles than a memory access. For smaller transfers, PIO will still be more efficient.

In order for DMA to work, the data buffer must be in physical memory until the transfer completes. It cannot be swapped out to disk, since the DMA controller only has access to physical memory. This means that the memory regions involved in DMA are **pinned**. <u>They are non-swappable.</u>

## Typical Device Access

<img src="https://i.imgur.com/KyKcypm.jpg" style="width: 400px" />

### OS Bypass

For some devices, it's possible to configure them to be accessible directly from user level. This is called **operating system bypass**. In OS bypass, any memory/registers assigned for use by the device is directly available to a user process.

The OS is involved in making the device registers available to the user process on create, but then is out of the way.

Since we don't want to interact with the kernel in order to control the device, we need a **user-level driver** - basically a library - that the user process links in order to interact with the device. These libraries, like the kernel-level drivers, will usually be provided by the device manufacturers. 

The OS has to retain some coarse-grain(粗鲁的) control. For example, the OS can still enable/disable a device or add permissions to add more processes to use the device. The device must have enough registers so that the OS can map some of them into one or more user processes while still retaining access to a few registers itself so it can interact with the device at a high-level.

When the device needs to pass some data to one of the processes interacting with it, the device must figure out which process the data belongs to. The device must perform some protocol functionality in order to **demultiplex** different chunks of data that belong to different processes. Normally, the kernel performs the demultiplexing, but in OS bypass that responsibility is left to the device itself.

### Sync vs. Async Access

When an I/O request is made, the user process typically requires some type of response from the device, even if it just an acknowledgement.

What happens to a user thread once an I/O request is made depends on whether the request was synchronous or asynchronous:
- For synchronous operations, the calling thread will block. The OS kernel will place the thread on the corresponding wait queue associated with the device, and thread will eventually become runnable again when the response to its request becomes available.
- For asynchronous operations, the thread is allowed to continue as soon as it issues the request. At some later time, the user process can be allowed to check if the response is available. Alternatively, the kernel can notify the process that the operation is complete and that the results are available.

<img src="https://i.imgur.com/8eORTCM.jpg" style="width: 600px" />


### Block Device Stack

<img src="https://i.imgur.com/h9fnjgv.jpg" style="width: 300px" />

Block devices, like disks, are typically used for storage, and the typical storage-related abstraction used by applications is the file. A file is a logical storage unit which maps to some underlying physical storage location. At the level of the user process we don't think about interacting with blocks of storage, but files.

Below the file-based interface used by applications is the **file system**. The file system will receive read/write operations from a user process for a given file, and will have the information to find the file, determine if the user process can access it and which portion to access. The operating system can then actually perform the access.

Operating systems allow for a filesystem to be modified or completely replaced with a different filesystem. To make this easy, operating systems standardize the filesystem interface that is exposed to a user process. The standardized API is the POSIX API, which includes the system calls for read and write. The result is that filesystems can be swapped out without breaking user applications.

If the files are stored on block devices, the filesystem will need to interact with these devices via their device drivers. Different types of block devices can be used for the physical storage and the actual interaction with them will require certain protocol-specific APIs. Even though the devices may all be block devices, there can and often will be differences among their APIs.

In order to mask these device-specific differences, the block device stack introduces another layer: **the generic block layer**. The intent of this layer is to <u>provide a standard for a particular operating system to all types of block devices</u>. The full device features are still available and accessible through the device driver, but are abstracted away from the filesystem itself.

Thus, in the same way that the filesystem provides a consistent file API to user processes, the operating system provides a consistent block API to the filesystem.

## Virtual File System

Operating systems like Linux include a **virtual filesystem (VFS)** layer. This layer hides all details regarding the underlying filesystem(s) from the higher level consumers.

<img src="https://i.imgur.com/lmIb9Rn.jpg" style="width: 600px" />

The VFS layer serves two important functions:
1. **It separates file-system-generic operations from their implementation by defining a clean VFS interface**. Several implementations for the VFS interface may coexist on the same machine, allowing transparent access to different types of file systems mounted locally.
2. **It provides a mechanism for uniquely representing a file throughout a network**. The VFS is based on a file-representation structure, called a **vnode**, that contains a numerical designator for a network-wide unique file. (UNIX inodes are unique within only a single file system.) This networkwide uniqueness is required for support of network file systems. The kernel maintains one vnode structure for each active node (file or directory).

### Virtual File system Abstractions

The **file** abstraction represent the elements on which the VFS operates.

The OS abstracts files via **file descriptors**. A file descriptor is an integer that is created when a file is first opened. There are many operations that can be supported on files using a file descriptor, such as read, write and close.

For each file the VFS maintains a persistent data structure called an **inode**. The inode maintains a list of all of data blocks corresponding to the file. In this way, the inode is the "index node" for a file. The inode also contains other information for that file, like permissions associated with the file, the size of the file, and other metadata. inodes are important because file do not need to be stored contiguously on disk. Blocks for a file may exist all over the storage media, making it important to maintain this index.

To help with certain operations on directories, Linux maintains a data structure called a **dentry (directory entry)**. Each dentry object corresponds to a single path component that is being traversed as we are trying to reach a particular file. For instance, if we are trying to access a file in `/users/ada`, the filesystem will create a dentry for every path component - for `/` , `/users` and `/users/ada`.

This is useful because when we need to find another file in `/users/ada`, we don't need to go through the entire path and re-read the files that correspond to all of the directories in order to get to the `/users/ada` directory. The filesystem will maintain a **dentry cache** containing all of the directories that we have previously visited. Note that dentry objects live only in memory; they are not persisted.

Finally, the **superblock** abstraction provides information about how a particular filesystem is laid out on some storage device. The data structure maintains a map that the filesystem uses so it can figure out how it has organized the persistent data elements like inodes and the data blocks that belong to different files.

Each file system maintains some additional metadata in the superblock. Different file systems store different metadata

### VFS on Disk

The virtual file system data structures are software entities. They are created and maintained by the operating system file system component.

Other than the dentries, the remaining components of the filesystem will correspond to blocks that are present on disk. The files are written to disk as blocks. The **inodes** - which track all of the blocks that correspond to a file - are persisted as well in a block.

To make sense of all of this - that is, to understand which blocks hold data, which blocks hold inodes and which blocks are free - the superblock maintains an overall map of all of the disks on a particular device. This map is used both for allocation and lookup.

### ext2: Second Extended Filesystem

The ext2 filesystem was the default filesystem in Linux until it was replaced by ext3 and ext4.

A disk partition that is used as a ext2 Linux filesystem looks as follows:

<img src="https://i.imgur.com/BW4m5ug.jpg" style="width: 800px" />

The first block is not used by Linux and is often used to **boot** the system.

The rest of the partition is divided into **block groups**. The size of these block groups have **no correlation to the physics** of the actual disk these group abstract.

Each block group contains several blocks.

**The first block is the super block**, which contains information about the overall block group:
- number of inodes
- number of disk blocks
- start of free blocks

The overall state of the block group is further described by the group descriptor, which contains information about:
- bitmaps
- number of free nodes
- number of directories

Bitmaps are used to quickly find free blocks and inodes. Higher level allocators can read the bitmaps to easily determine which blocks and inodes are free and which are in use.

The **inodes are numbered from 1 to some maximum value**. Every inode in ext2 is a 128B data structure that **describes exactly one file**. The inode will contain information about file ownership as well as pointers to the actual data blocks that hold the data.

Finally, the block group contains the actual data blocks themselves that hold the data.

#### inodes

A file is uniquely identified by its inode. The inode contains a list of all of the blocks that correspond to the actual file. In addition to the list of blocks, an inode also contains additional metadata information.

<img src="https://i.imgur.com/6uu5eRp.jpg" style="width: 400px" />

The file shown above has 5 blocks allocated to it. If we need more storage for the file, the filesystem can allocate a free block, and simply update the inode to contain a sixth entry, pointing to the newly allocated block.

The benefit of this approach is that it is easy to perform both **sequential** and **random** accesses to the file.

The downside of this approach is that there is a limit on the file size for files that can be indexed using this data structure. For example, if we have a 128B inode containing 4B block pointers, we can only address 32 blocks. If each block can store 1Kb of information, our file size limit is 32Kb, which is too restrictive.

One way to solve the issue of file size limits is to use **indirect pointers**.

<img src="https://i.imgur.com/Bx2fsXu.jpg" style="width: 600px" />

The first section of blocks contain blocks that point directly to data. The direct pointers will point to 1kb per entry.

To extend the number a disk blocks that can be addressed via a single inode element, while also keeping the size of the inode small, we can use indirect pointers.

An indirect pointer will point to a block of pointers, where each pointer points to data. Given that a block contains 1kB of space, and a pointer is 4B large, a single indirect pointer can point to 256KB of file content.

A double indirect pointer will point to a block of single indirect pointers, while will point to pointers to data. This means that a single double indirect pointer can point to 2562561KB = 64MB of file content.

The benefits of indirect pointers is that it allows us to use relatively small inodes while being able to address larger and large files.

The downside of indirect pointers is that file access is slowed down. Without any indirect pointers, we have at most two disk accesses to get a block of content: one access for the inode, one access for the block. With double indirect pointers, we double the number of accesses we need to make: inode + block + two pointers.

Quiz: An inode has the following structure: Each block pointer is 4B. If a block on disk is 1KB, what is the maximum file size that can be supported by this structure(nearest GB)? And what is the maximum file size if a block on disk is 8KB(nearest TB)?
- 1KB: 1KB -> 256 pointers (12 + 256 + 256^2 + 256^3) x 1KB ~= 16GB
- 8KB: 8KB blocks / 4B pointers size = 2k pointers / block
    - (12 + 2K + 2K^2 + 2k^3) x 8KB ~= 64TB

### Disk Access Optimizations

Filesystems use several techniques to try to minimize the accesses to disk and to improve the file access overheads.

For example, filesystems rely on **buffer caches** in main memory to reduce the number of disk accesses. Content will be written to and read from these caches, and periodically will be flushed to disk. File systems support this operation via the fsync system call.

Another component that helps reduce the file access overhead is **I/O scheduling**. A main goal of I/O scheduling is to reduce the disk head movement, which is a slow operation. I/O schedulers can achieve this by maximizing sequential accesses over random accesses.

For example, if a disk head is at block 7, and a request to write at block 25 comes in, followed by a request to write at block 17, the I/O scheduler may re-order the requests so it can write to block 17 on its way to block 25 instead of having to backtrack.

Another useful technique is **prefetching**. Since there is often a lot of locality in how a file is accessed, cache hits can be increased by fetching nearby blocks during a request.

For example, if a read request comes in for block 17, the filesystem may also read block 18 and 19 into its cache. It prefetches these blocks because it is likely that they will also be read.

This does use more disk bandwidth to move more data from disk into main memory, but it can significantly reduce the access latency by increasing the cache hit rate.

A final useful technique is **journaling**. I/O scheduling reduces random access, but it still keeps the data in memory. Blocks 17 and 25 are still in memory waiting for the I/O scheduler to interleave them in the right way. That means that if the system crashes these data blocks will be lost.

As opposed to writing out the data in the proper disk location, which would require a lot of random disk access, in journaling we write updates to a log. The log will contain some description of the write that needs to take place, such as the block, the offset, and the content to be written. The writes described in the log are periodically applied to proper disk locations.