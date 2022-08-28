# Introduction

## What is an OS?

An operation system is a layer of systems software that:

- **directly** has privileges access to the underlying hardware;
    - e.g. **file eidtor** does not directly access hardware, but **file system** does
- manages hardware on behalf of the applications according to some predefined policies
- it ensures that applications are isolated and enforces fairness among them.

## OS Elements

* Abstractions
    * a layer above the hardware resources that allow application interactive with hardware indirectly. Such as process, thread, file, socket, memory page
    * Different from **Arbitration**, which is a method used for decide what/which hardware to use.
* Mechanisms
    * the implementation of the abstractions. For examples, threads are scheduled by the OS with some algorithms so application can run simultaneously. Other mechanisms like:  create, schedule, open, write, allocate

* Policies
    * the rules that all of the mechansms follow. for example, memory follow algorithems like least-recently used(LRU) to remove unused data from memory and only keey the recently used data.

## Design Principles

### Separation of mechanism and policy

* Implement flexible mechanisms to support many policies. Such as memory management, CPU scheduling. By providing a common interface for policies, it's easier to switch different policies without concerning the implemention.

### Optimize for the common case

* The design should be optimized for the way it’s most likely to be used. For example, the "interrupt as threads" design is beneficial to overall system performance because despite the fact that there is a cost incurred for interrupts, there are savings on every mutex lock/unlock operation. Because the latter occur much more frequently than the former (common case), it’s an overall performance gain. 

## User/Kernel Protection Boundary

* Kernel-mode: where OS resides, it's privileged, has direct access to the hardware
* User-mode: where application resides
* user-kernel mode crossing: this behavior is known as **trap**, a special **system call**, which is the way that user-mode process can interact with the system in a privileged way.
    * Whey a process want to gain privileged access, such as read files, the user-mode process will be set off a **trap**, and ask OS to review what caused the **trap**. The OS will either grant the user-mode process to the kernel-mode, or terminate the process.
* There are other system calls, e.g. `open(file)` - open a ﬁle, `send(socket)`, and `mmap(memory)` - request more memory.

### System Call Flowchart

* <img src="https://i.imgur.com/pn2aa0s.jpg" style="width:500px" />
* whey a process calls system call, the OS will flip the privilege bit so the process can execute system in the kernel mode, and return to user mode afterwards.

## Different OS

* Monolithc OS
    * Everything is included in the OS. This includes memory managers, device drivers, ﬁle management, processes/threads, scheduling, ﬁle systems for random and sequential access, etc.
    * Bebefits: compile time optimizations.
    * Disadvantages: large memory requirements; har to maintain/debugging/upgrading.
* Modular OS
    * Most modern OS, including Windows, macOS, Linux. This design contains basic services and APIs at OS level; everything else can be added as a module.
    * Bebefits: easier to maintain/upgrade.
    * Disadvantages: a performance impact due to the bigger call stack and more general-purpose code required.
* Microkernel OS
    * used in embeded systems. e.g. kernels like MINIX 3, Mach, QNX. It only includes the most basic primitives at the OS level, everything else, including file systems, device drivers, etc. are at user level.
    * Bebefits: small, better performanace for kernel code.
    * Disadvantages: usually written for very specialized harware; complex software development; can be costly.