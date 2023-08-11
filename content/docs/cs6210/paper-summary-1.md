---
weight: 1
title: "Paper Summary I"
---

# Paper Summary I

by Lei Yang(lyang423) @2023/03/26

```
Title: Xen and the Art of Virtualization
Authors: Paul Barham, Boris Dragovic, Keir Fraser, Steven Hand, Tim Harris, Alex Ho, Rolf Neugebauer, Ian Pratt, and Andrew Warfield
```

## Introduction

- Xen is a high-performance, resource-managed virtual machine monitor (VMM) that facilitates various applications, including server consolidation, colocated hosting environments, distributed web services, secure computing platforms, and application portability.
- The motivation is to overcome the limitations of full virtualization, which often suffers from **performance overhead** and **increased complexity** due to the emulation of an entire hardware platform.

## Approach towards Virtualization

- Xen requires modifications to the guest operating systems to work cooperatively with the VMM. This approach results in reduced complexity and improved performance compared to full virtualization.
- Comparing to Denali's implementation, Xen focuses on supporting popular general-purpose operating systems like Linux, Windows, and NetBSD and intends to scale approximately 100 virtual machines.
* Xen's design principles:
	* Support for unmodified application binaries, aka no changes to application binary interface(ABI)
	* Support full multi-application operating system
	* Obtain high performance and strong resource isolation
	* Do not hide the effects of resource virtualization from guest OSes.

### The Virtual Machine Interface

- **Memory**: Guest OSes are responsible for allocating and managing the hardware page tables. Xen allocates 64MB at the top of every address space to avoid TLB flushing when entering and leaving hypervisor.
- **CPU**: 
	1. To protect the hypervisor, Xen utilizes the privilege rings and keeps the hypervisor at ring 0, and the guest OS and applications at a lower privilege level. The privileged instructions require to be validated and executed within Xen. 
	2. To handle the two types of exceptions: system calls and page faults, Xen allows guest OS to register a 'fast' exception handler which can be accessed directly by the processor without in directing via ring 0.
- **Device I/O**: I/O data is transferred to and from each domain via Xen, using shared-memory, asynchronous buffer-descriptor rings.

### Control and Management

![](https://i.imgur.com/zPBBYOl.png)

## Detailed Design

### Control Transfer: Hypercalls and Events

- **Hypercalls** are used by guest operating systems running in virtual machines to request privileged operations from the hypervisor, such as requesting a set of page-table updates. When a hypercall is made, Xen validates and applies the requested updates and then returns control to the calling domain when this is completed.
- Communication from Xen to a domain is provided through an **asynchronous event mechanism**, which replaces the usual delivery mechanisms for device interrupts and allows lightweight notiﬁcations of important events such as domain-termination requests.

### Data Transfer: I/O Rings

-   Xen provides an **asynchronous** **I/O descriptor ring** that is a circular queue of descriptors allocated by a domain but accessible from within Xen. Each ring has two pairs of producer-consumer pointers: domains place requests and Xen remove the requests for handling; Xen place responses and the domains consume the responses.

### Subsystem Virtualization

- **CPU Scheduling**: Xen uses the Borrowed Virtual Time(BVT) scheduling algorithm, which provides low-latency dispatch by using virtual-time warping.
- **Time and timers**: Xen offers guest OSes real time, virtual time and wall-clock time. 
	- Real time is the accurate time synced with external source. 
	- Virtual time is typically used for timeslice sharing. 
	- Wall-clock time is a measure of the real time that takes into account any adjustments made to the clock due to factors such as daylight saving time or changes in timezone.
- **Virtual address translation**: The guest OSes are restricted to read-only access to their page tables. All updates to the page table will be trapped to the Hypervisor to validate the updates and propagate the changes to the shadow page tables.
- **Physical memory**: Memory is statically partitioned at creation. To adjust the usage of each domain, Xen implements a balloon driver by passing the memory pages between the Xen and the guest OSes.
- **Network**: 
	- Similar to disk I/O, Xen offers two network I/O rings of buffer descriptors, one for transmit and one for receive. To transmit a packet, the guest OS enqueue a buffer descriptor onto the transmit ring. Xen copies it and applies the filter rules.
	- For efficiency, guest OS exchanges an unused page frame for each packet it receives to avoid the packet copying between Xen and guest OS.
- **Disk**: All domains except Domain0 access disk via the abstraction of virtual block devices(VBDs).

### Building a New Domain

- This task is mostly delegated to *Domain0* which uses its privileged control interfaces to access the new domain’s memory and inform Xen of initial register state.

## Performance Evaluation

- Xen achieves near-native performance for guest OSes, with minimal overhead compared to running on bare hardware. The paper presents several benchmarks and case studies demonstrating that Xen's ability to efficiently manage numerous of virtual CPUs and its effectiveness in a multiprocessor environment.

## Related Work

- Virtualization has evolved over the decades, with early systems like IBM VM/370 and VMware using full virtualization, which has performance drawbacks. Xen employs paravirtualization, improving performance by presenting a modified interface to guest OSes. It offers a more general solution without constraints on safety, termination, or language, and can support language-level virtual machines running over a guest OS, highlighting its flexibility and efficiency.

## Future Work and Conclusion

- The future work of Xen will be focusing on virtual block devices, physical memory performance, Internet-scale computing infrastructure, and better support for management and administration. 
- In conclusion, Xen simplifies transient server hosting and offers near-equivalent performance to baseline Linux, showcasing its potential for broad applicability.