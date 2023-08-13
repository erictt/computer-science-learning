---
weight: 1
title: "Lesson 03: Virtualization"
---

# Lesson 3: Virtualization

## Introduction to Virtualization

### Introduction

- Virtualization is the logical extension to the idea of extensibility of the entire operating system on top of HW.
- It facilitates sharing the same HW resources across multiple applications running on distinct OSs.

### Hypervisor

A **Hypervisor**(Virtual Machine Monitor - VMM) facilitates sharing the HW resources among the virtual machines(guest OSs)

- Native(bare metal) Hypervisor: Running directly on top of the HW.
- Hosted Hypervisor: Running as an application process on top of a host OS.

### Full virtualization

- Guest OSs running on top of the Hypervisor will be **full unchanged binaries**.
- When a guest OS tries to execute a privileged instruction, a trap will be generated and passed to the Hypervisor, which in turn will **emulate the intended functionality** of the OS (Trap & Emulate Strategy).
- This makes each guest OS think it’s running alone on the HW.
- <u>In some architectures, some privileged instructions may fail silently.</u> This is why the Hypervisor will use a **Binary Translation Strategy**. The Hypervisor looks into each guest OS binary for the specific instructions that might fail silently and edits the binary to ensure careful handling of these instructions.
  - Both Intel and AMD have since started adding virtualization support to the hardware, so that such problems don't exist any more.

### Para virtualization

- The binaries of the guest OSs will be **modified to avoid problematic instructions and utilize optimizations**.
- The Hypervisor will change only less than 2% of the guest OS code.
- For the user point of view, the OS is not changed.
- Ex.: Xen Hypervisor.

### What need to be done?

- Virtualize HW:
  - Memory hierarchy,
  - CPU,
  - HW devices.
- Effect data and control between guest OSs and hypervisor.

## Memory Virtualization

### Introduction

- Memory Hierarchy - a series of layers from small and fast to large and slow.
  - <img src="https://i.imgur.com/B9GTt1G.jpg" style="width: 800px" />
  - source: <https://computerscience.chemeketa.edu/cs160Reader/ComputerArchitecture/MemoryHeirarchy.html>
- **Memory hierarchy** is very important when it comes to virtualization.
- Handling memory while we have multiple OSs running on the same HW has a great effect on performance.
- Recall that each process lives in a separate HW address space, and the OS maintains a page table containing the mapping of the virtual and physical addresses. The virtual address space of a given process is not contiguous in physical memory.

### Memory Management

<img src="https://i.imgur.com/LvJiz5q.png" style="width: 800px" />

- There’re user processes running inside each OS running on top of the Hypervisor. **Each of these processes** has its own protection domain and a distinct page table.
- The Hypervisor doesn’t have any information about these page tables.
- Each guest OS thinks that its memory regions are located contiguously in the physical memory, where in fact it’s non-contiguous in the machine memory controlled by the Hypervisor.
- Even if these regions are contiguous, they can never start at the same address the OS thinks they start with.

#### Shadow page table

<img src="https://i.imgur.com/o3x2kYm.png" style="width: 800px" />

- The process’s page table, maintained by the guest OS, provides the mapping between the virtual page number and the physical page number.
- The shadow page table (S-PT), maintained by the Hypervisor, provides the mapping between the physical page number (PPN) to the real machine page number (MPN) of the HW memory.
  - Who keeps PPN->MPN mapping?
  - In full virtualization, the hypervisor since the guest OS has no knowledge of machine pages.
  - In para virtualization, the guest OS keeps since it's aware of hypervisor.
- This adds a redundant level of indirection between the virtual address and the memory address.
- How to make address translation **efficient** in a **full virtualization** setting? Here is how VMware ESX achieve this:

    <img src="https://i.imgur.com/COujgt2.png" style="width: 800px" />

    1. Whenever an OS tries to update its page table, a trap will be generated (Privileged operation).
    2. This trap is caught by the Hypervisor, which as a result updates the **shadow page table**.
    3. Now <u>whenever a process generates a virtual address, the Hypervisor will directly translate VPN to MPN into TLB and the hardware page table, without going through the guest OS</u>.
- In a **para virtualization** setting, the guest OS knows that its physical memory isn’t contiguous, so the translation process is shifted to it. For example, in Xen,
    1. it provides a set of **Hypercalls** for the guest OS to tell the Hypervisor about changes to the hardware page table.
    2. A guest OS can issue a “Hypercall” to the Hypervisor to **create** (allocate and initialize) a HW page frame and the guest OS can target this page frame to host a page table data structure.
    3. When a process starts to run, the guest OS issues another Hypercall to the Hypervisor to **switch** the page table to the previously given location.
    4. The guest OS can also **update** this page table.

### Dynamically Increasing Memory

- If a guest OS starts running an application that needs more memory, the Hypervisor can take back a memory region from another guest OS and provide it to the requesting OS.
- This concept can lead to unexpected and anomalous behavior of applications running on the guest operating system.
- A standard approach is to coach one of the guest OS to give up some physical memory voluntarily to satisfy the needs of a peer.

#### Ballooning

<img src="https://i.imgur.com/CMrwXMy.png" style="width: 800px" />

- A Balloon is a device driver that the Hypervisor installs inside the guest OS to manage memory pressures.
- Whenever a guest OS requires more memory, the Hypervisor will contact the Balloon inside any guest OS that is not using the whole memory given to it through a private communication channel and tells it to inflate.
- This means the Balloon will start requesting more memory from the guest OS. The guest OS will page out to disk to free extra memory for the Balloon driver.
- Once the Balloon driver gets the memory, it returns it back to the Hypervisor, which in turn gives it to the guest OS requiring more memory.
- Whenever the memory pressure situation is fixed, the Hypervisor instructs the Balloon to deflate, giving out more memory to the guest OS that provided the memory in the first place.
- The Ballooning technique is <u>applicable to both full and para virtualization</u>.

### Sharing Memory Across Virtual Machines

- Sharing memory between VMs can facilitate maximum utilization of the physical resources, but on the other hand, it might affect protection.
- If we’re having different instances of the same application running on different guest OSs, the **core pages** of these instance can share the same physical memory page.
  - Solution #1: The guest OS has hooks that allows the Hypervisor to mark pages as **copy-on-write** and have the physical page numbers point to the same machine page.
  - Solution #2(used in VMWare ESX):

        <img src="https://i.imgur.com/oNL1N6n.png" style="width: 800px" />
        <img src="https://i.imgur.com/wU4P7Ff.png" style="width: 800px" />

        1. The Hypervisor has a data structure (hash table). This hash table contains a content hash of the **machine pages**.
        2. For each physical page (on the guest OS), the Hypervisor creates a **content hash** and searches the hash table for a match.
        3. If a match found, the Hypervisor performs full comparison between the contents of the matching pages.
            - The reason that we do a full comparison after a match is because the hash match is only a hint, the actually page might have been modified.
        4. If the two pages have the exact same content, the Hypervisor modifies the PPN to MPN mapping of the guest OSs to point to a single machine page.
        5. This machine page will be marked as **copy-on-write**.
        6. A **reference count** in the hash table is maintained to indicate how many guest OSs are using the same machine page.
        7. This approach requires no modification to the guest OSs.

### Memory Allocation Policies

- **Pure share-based approach**: You have control over the resources whether you’re using it or not.
  - problem: holing
- **Working-set based approach**: You get as much resources as you need.
- **Dynamic idle-adjusted shares approach**: If you’re not using some of the resources you have, a percentage of these resources will be taken away from you.
  - Tax on idle memory
    - charge more for idle page than active page
    - idle-adjusted shares-per-page ratio
  - Tax rate on idle pages:
    - explicit administrative parameter
    - 0% = plutocracy(富豪统治) ... 100% = socialism
      - 0% = pure share-based approach. you have the whole control
      - 100% meaning if you got resources but not using it, it will taken away.
      - Making this “tax percentage” less than 100% **allows for sudden working set surges**.
        - e.g. 50% meaning there are 50% of chances the idle memory will be taken away. You can get it back when you need it.
    - High default rate
      - Reclaim most idle memory
      - Some buffer against rapid working-set increases

## CPU & Device Virtualization

### Introduction

- In addition to memory virtualization, the CPU and devices need also to be virtualized.
- Virtualizing the CPU and devices will be more challenging since that they’re more explicit to the guest OSs living on top of the HW.

### CPU Virtualization

- The Hypervisor must give the illusion to each guest OS that it owns the CPU:
  - The Hypervisor allocates a certain amount of CPU time to each VM.
  - The Hypervisor doesn’t care about how each VM uses the CPU during its allocated time.
  - Similar to memory allocation, the Hypervisor can use different policies for CPU allocation:
        1. Proportional share: Each VM has a share of the CPU proportional to the processes running inside it.
        2. Fair share: An equal share to each VM.
  - The Hypervisor shall reward the guest OS for any CPU time taken from its share to serve another guest OS (e.g. interrupt coming for a VM other than the one owning the CPU at the moment).
- The Hypervisor must also handle program discontinuities:
  - These discontinuities include external interrupts, exceptions, system calls, page faults, etc.
  - The Hypervisor packs these discontinuities as software interrupts and deliver them to the corresponding guest OS.
  - The guest OS may require privileged access to handle some of these events.
  - Whenever a guest OS tries to execute a privileged instruction, it will produce a trap, which will be handled by the Hypervisor.
  - The problem occurs in a full virtualized setting if the privileged instruction that the guest OS is trying to execute failed silently.
    - To deal with this problem, the Hypervisor should search the guest OS’s unchanged binary for such silently-failing instructions and do binary rewriting to avoid such issues.
  - In a para virtualized system, the Hypervisor provides APIs to the guest OSs to facilitate communication between the guest OS and the Hypervisor.

### Device Virtualization

- Similar to CPU virtualization, the Hypervisor must give the illusion to each guest OS that it owns the I/O devices.
- The two things we need to worry about are:
  - Data transfer.
  - Control transfer.
- Full virtualization: The guest OS already thinks that it owns the devices.
  - Control transfer from the guest OS to the Hypervisor: When the guest OS tries to access the devices, a trap will be issued to the Hypervisor.
  - Control transfer from the Hypervisor to the guest OS: The Hypervisor will emulate the functionality that the guest OS intends for the device.
  - Data transfer: The data transfer happens implicitly through the Hypervisor.
- Para virtualization: The guest OS in fact can see the exact same I/O devices that are available to the Hypervisor.
  - Control transfer from the guest OS to the Hypervisor: When the guest OS needs to access the devices, it issues a Hypercall to the Hypervisor.
  - Control transfer from the Hypervisor to the guest OS: The Hypervisor serves these Hypercalls trough software interrupts.
    - NOTE: The guest OS has control (via Hypercalls) on when event notifications (SW interrupts) should be delivered.
  - Data transfer:
        1. The Hypervisor exposes shared buffers to the guest OS to facilitate passing data from the guest OS to the I/O devices without the overhead of copying these data between different address spaces.
        2. The Hypervisor must account for the CPU time needed for demultiplexing the interrupts and managing the buffers for the guest OSs.
- Data transfer in Xen(Para):
  - Xen provides an **Asynchronous** **I/O rings**(a set of descriptors) that are shared with the guest OSs.
  - Each I/O ring with be populated with the I/O requests with the guest OS owning the ring.
    - Echo guest OS has its own I/O ring.
      - <img src="https://i.imgur.com/12m3kDA.png" style="width: 800px" />

    - There is no need for mutex since read and write are separated.
  - Xen checks the ring pointer and picks the I/O request to be processed in a FIFO manner.
  - Xen will then place the responses to these requests in the same ring.
- Network (and disk I/O) virtualization in Xen:
    1. Each guest OS has two I/O rings, one for transmission and one for reception.
        1. <img src="https://i.imgur.com/U1ZLBHI.png" style="width: 800px" />

    2. The guest OS transmit packets by enqueuing **packet descriptors** in the transmission ring through **Hypercalls**.
    3. These requests in the ring data structure will be **pointers** to the guest OS buffers to avoid copying the packets themselves. The buffers than contain the packets are in guest OS.
        1. There's no copying of the package themselves from the guest operating system buffers into Xen. Because the pointers to the guest operating system buffers have been embedded in these descriptors.
        2. And for the duration of the transmission, the pages associated with these network packets are pinned so that Xen can complete the transmission of the packets.
    4. Xen uses a round robin scheduler to provide transmission services to all the guest OSs in order to transmit packets from different virtual machines.
    5. Packet reception works in the same way. But in addition to the buffer/pointer method. To make the process efficient, there are two tricks Xen do:
        1. What a guest operating system will do is pre-allocate network buffers which are pages owned by the guest operating system. So when a package comes in, Xen can directly put the network package into the buffer that is owned by the guest operating system.
        2. When Xen receives a packet into a machine page, it simply exchange that machine page with some other page that belongs to the guest operating system.

## Measuring Time

For billing purpose

- CPU usage
- Memory usage
- Storage usage
- Network usage

## Xen and VMware

The main difference of virtualization technology from **extensible** OS is, virtualization(para virtualization - Xen, full virtualization - VMware) focus on **protection** and **flexibility**.
