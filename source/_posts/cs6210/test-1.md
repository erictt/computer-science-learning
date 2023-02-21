# Test 1

## OS Structure

### I. SPIN

1. [3 points] [True/False with justification] Distinct protection domains require distinct hardware address spaces.
    - False. Small protection domains can share one hardware address space, separated by the boundary of segment registers.
2. [4 points] SPIN promotes implementing an entire OS in a strongly typed high level language like Modula-3. Give 2 examples scenarios in which the OS may have to go outside the boundaries of language enforced protection model.
    - The core services that need to control the hardware resources will go out of the boundaries, such as the services like CPU scheduler and memory management.
    - When CPU schedulier switch processes, it needs to store process's PCB into memory and load the next PCB for the next process.
    - Memory management. e.g. create and destroy the address spaces. 
3. [4 points] Give any two techniques that underlie SPIN’s ability to achieve their goals of extensibility, safety, and good performance.
    - co-location of the extensions within the kernel allows efficient communication between the kernel and the extension (good performance).
    - SPIN offers the concept of generic interfaces and allow developers to implement the OS services such as file system, network protocols (extensibility).

### II. Exokernel

1. [6 points] A library OS implements a paged virtual memory on top of Exokernel. An application running in this OS encounters a page fault. List the steps from the time the page fault occurs to the resumption of this application. For this problem assume the following:
    * The processor architecture has only a TLB for address translation (i.e., a TLB miss triggers a page fault)
    * The library OS has already acquired all the necessary capabilities from Exokernel (writing to the memory mapped device controller registers to start the DMA from the disk to a memory buffer)
    * The library OS has a pool of free page frames already preallocated to it by Exokernel.
        1. Exokernel will upcall the page fault to the library OS through a “Registered Handler”.
        2. The library OS serves the page fault and performs the required mapping.
        4. This mapping is then presented to the Exokernel with the TLB entry.
        5. The Exokernel will validate the key and install the mapping into the HW TLB (privileged operations).
2. [2 points] [True/False with justification] When exokernel receives an interrupt and the library OS to which the interrupt is to be delivered is not currently running, exokernel ignores the interrupt.
    1. False. Exokernel buffers the interrupt and delivers it to the lib OS when it's scheduled.
3. [3 points] Give ONE similarity and ONE difference between the approaches to extensibility of SPIN and Exokernel
    1. Similar: To reduce the impact of boarder crossing, Exokernel allows downloading code into the kernel. SPIN co-locate the extension and the kernel to the kernel address space.
    2. Diff: Exokernel allow downloading arbitrary code into kernel, less secure. SPIN's extension are created at compile time and follow the rules enforced by the programming language.

### III. L3 Microkernel

1. [2 points] [True/False with justification] In designing the L3 microkernel, Liedtke further strengthens the conclusions of SPIN/Exokernel.
    - False, Liedtke approved that microkernel can be efficient.
2. [2 points] [True/False with justification] If a CPU architecture does not support address-space tagged TLB, a TLB flush is unavoidable when moving from one user-level protection domain to another.
    - False. We can use segment registers to specify the range of virtual addresses that a process can legally access. Since each process have it's own protection domain, the process will not clash when querying the TLB. therefore, there is no need to flush the TLB.
3. [2 points] [True/False with justification] To implement a high-performance microkernel, the microkernel abstractions should be architecture independent. 
    - False. It should be processor-specific, and take advantage of the processor architecture offers such as segment register.
    
## Virtualization

### IV. Para virtualization

An architecture supports a TLB that is entirely software-managed in kernel mode. The size of the TLB is an architectural parameter that is published and known to the system software. The ISA of the processor provides the following instructions:
• Set-AS(AS-ID): Stores the AS-ID in a register called Address Space Register (ASR) that can be accessed only in kernel mode.
• Enter(AS-ID, VPN, PFN): Stores the tuple <AS-ID, VPN, PFN> in the TLB. If the TLB is full, this instruction will fail silently.
• Delete(AS-ID, VPN, PFN): Deletes the tuple <AS-ID, VPN, PFN> from the TLB. If the entry is non-existent the instruction is a NOP.

You are designing a hypervisor for supporting para-virtualized guest OSes on top of this architecture.

1) [2 points] What advantage does this architecture have over x86-style architecture (that has a page-table plus hardware managed TLB) for implementing a para-virtualized guest OS?
    - The fact that TLB is AS-tagged allow guest OSes and the hypervisor coexist in separate address spaces, and we can switch between guest OS and hypervisor without flushing the TLB.
2) [2 points] How would you provide memory isolation/independence/integrity for each guest OS?
    - Each guest OS has its own software-based TLB space. The hypervisor will install the software TLB for the guest when running it.
3) [6 points] How can each guest-OS provide memory isolation/independence/integrity for processes created within it?
    - The guest OS creates AS-ID qprocess and call `Set-AS` to allocate it to the CPU, then use both `Enter` and `Delete` instructions to manage the hardware space for the process.

    - The guest OS allocates a page frame as the page table data structure for the newly created process
    - It initializes the page table
    - It uses an API provided by the hypervisor to give the page frame address to the hypervisor.
    - The hypervisor records this address as one of the valid page table pointers for this guest OS
    - Whenever the guest OS wishes to schedule this process it will use an API provided by the hypervisor (e.g., "Switch PT") to tell the hypervisor to load the PTBR with the address of the page table it has registered with the hypervisor earlier
    - When a process has a page fault, the hypervisor upcalls the guest OS which resolves the page fault and presents a valid mapping (VPN to MPN) to the hypervisor using an API (e.g., "Install Mapping") which is entered into the page table named by the API call.
    - Since each process has its own page table and thus its own address space, it has the guarantees of isolation and protection.

    2. A guest OS can issue a “Hypercall” to the Hypervisor to **create** (allocate and initialize) a HW page frame and the guest OS can target this page frame to host a page table data structure.
    3. When a process starts to run, the guest OS issues another Hypercall to the Hypervisor to **switch** the page table to the previously given location.
    4. The guest OS can also **update** this page table.

### V. Full virtualization

1. [2 points] [True/False with justification] A fully virtualized environment with multiple Guest OSes has a single shadow page table.
    - False. The s-PT is per guest OS. 
2. Assume that a fully virtualized OS is running on top of x86 processor that has a page table and TLB. The guest-OS maps a process’s virtual page number (VPN) to a physical page number (PPN). However, PPN is an illusion of the guest-OS which must be translated to the machine page number (MPN).
    1) [2 points] How is this illusion of physical memory being contiguous for the guest-OS not result in inefficiency in a fully virtualized setting?
        - When the guest os tries to update the page table, it will trap to the hypervisor. 
        - The hypervisor updates the shadow PT to map the PPN to MPN, and set VPN -> MPN in the guest OS's TLB.
        - Then we have a hardware-accessible page table that translate virtual-to-machine pages at hardware speed.
    2) [2 points] How does the processor translate the virtual page number generated by the currently running process to its corresponding machine page number in memory?
        - Every time a process generates a virtual address, we won't go through the guest OS to do the translation, since the translation has already ben installed in TLB and the hardware page table.
3. [2 points] State the difference between fully virtualized and para virtualized environments when it comes to updating the process page table after servicing a page fault. 
    - In full, the guest OS try to execute a privileged instruction to update the mapping, which will trap to the hypervisor. The hypervisor will update the shadow page table along with the TLB and hardware address space.
    - In para, the guest OS makes hypercall to explicitly ask the hypervisor to update the page table.

### VI. Memory Management [Y]

1. [2 points] Explain concisely, how can the ballooning mechanism be used with a fully virtualized OS?
    - Hypervisor installs the ballon device driver in every guest OS
    - When any guest OS asking for more memory, the hypervisor will inflate the balloon driver on other guest OS to force them page out unused pages.
    - The balloon driver give back the memory to the hypervisor to reallocate.
    - Conversely, the hypervisor can deflate the balloon driver to give the guest OS more memory to page in the pages from disk.
2. [2 points] [True/False with justification] In VM oblivious page sharing, if there is a hash match between the page (call it incoming page) being brought in from the disk and an existing hash entry in the hypervisor’s hash table, then the machine page associated with the incoming page can be safely discarded.
    - False. A hash match only hints that there could be a possible match. The content might have been updated since then. A full comparison is require before discarding the page.
3. [2 points] [True/False with justification] Inflating the balloon driver of a Guest OS will result in more machine memory being allocated to that OS.
    - False. inflate results more memory goes to the ballon drive, hence less memory for the guest OS.

## Parallel systems

### VII. Atomicity

1. [4 points] Consider a SMP with invalidation-based CC and whose Instruction-set Architecture (ISA) provides instructions for atomic read and atomic write. The OS supports multi-threaded applications and implements scheduling at the level of individual threads at available CPU cores. You have implemented the mutual exclusion algorithm as below:

```c
// L is a shared variable 
Lock(L):
    back:
    if (L == 0) L = 1; // success
    else
        While (L == 1); // spin go back;
Unlock(L):
    L = 0;
```

- Will this lock algorithm work? If not, why not?
    - No. it's possible that two threads encounter the `if(L==0)` situation, and they both acquired the lock. We need RMW instruction for this.
2. [2 points] [True/False with justification] An atomic read-modify-write instruction is not a necessity in the processor’s ISA for implementing Anderson’s mutual exclusion lock algorithm.
    - False. A processor needs to use the `fetch_and_inc` instruction to mark itself in the queue. If `fetch_and_inc` is not provided, we need to implement it with `test_and_set`.
3. [2 points] [True/False with justification] An atomic read-modify-write instruction is a necessity in the processor’s ISA for implementing any barrier synchronization algorithm. 
    - False. E.g. the MCS barrier only rely on atomic read and write.

### VIII. Barriers

[3 points] Consider the sense reversing barrier implementation in C as follows where count, sense are shared variables across threads which are initialized to N and False respectively. Will this code work? If yes explain why, if no, give brief reasoning and an example!

```c
// global variables visible to all threads 
bool sense = false; 
int count = N;

// thread specific static variable 
bool local_sense = false;

void barrier(){
    count--; 
    if(count == 0){ 
        sense = !local_sense;
        count = N;
    } else {
        while(local_sense == sense);
    } 
    local_sense = !local_sense;
}
```

- No. There are several race problems. 
- One is, multiple threads try to decrease count at the same time, resulting count never reach 0. 
- Another one is, any threads can go to the next barrier and decrease the count before the count reset to N. Then after the count reset to N, it will never reach 0 since one thread decrease it before the reset.

### IX. Potpourri

1. [2 points][True/False with justification] Each position in the array of flags defined in Anderson’s queue lock is statically allocated to a designated processor to ensure fairness.
    - False. The fairness is given from the fact that the processors are sequenced and processed who gets in line first. In fact the threads are dynamically allocated.
2. [2 points] [True/False with justification] MCS mutual exclusion lock can be implemented on a multi-processor that supports **only a globally atomic T&S** primitive.
    - True. There are two instructions that been used in MCS. One is `fetch_and_store`, the other is `compare_and_swap`. Both can be implemented with `test_and_set`.
3. [3 points] Explain why the MCS barrier algorithm will work even on an NCC NUMA machine.
    - A NUMA machine consists of a set of nodes connected through an interconnection network.
    - The parent spins on a memory location in its NUMA piece of the memory. The child will reach across the ICN to modify the memory location. The change will be seen by the parent since there is a hardware cache coherence within each node of the NCC NUMA architecture.
4. [2 points] [True/False with justification] In Tornado parallel OS, the representation of clustered object – namely, replication, partitioning across the processors – is decided at the design time of a given subsystem and does not change.
    - False. E.g. Tornado can monitor the use of the regions over time and potentially carve them up into smaller regions if it would be advantageous. 
5. [4 points] Explain why in a vanilla client/server RPC package there are 4 message copies between the client’s invocation and the server procedure starting to execute.
    1. A client stub will copy the data from the client stack to a serialized RPC packet.
    2. The kernel copies the RPC packet to kernel buffer.
    3. The kernel copies the packet from its buffer to the server's domain.
    4. The server de-serialize the packet and copy it to its working stack.