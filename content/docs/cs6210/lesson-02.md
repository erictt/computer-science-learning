---
weight: 1
title: "Lesson 02: OS Structure"
---

# Lesson 2: OS Structure

<!-- toc -->

The OS services:

1. Process/thread management and scheduling.
2. Memory management.
3. Inter-process communication.
4. File system.
5. Access to I/O devices.
6. Access to the network.

## Goal of OS Structure

- protection: isolation of user/system, avoid errors from each process disturb the others
- performance: OS requires minimum ops and offer the application maximum resources
- flexibility(extensibility): the OS can adapt to different requirements of the applications
- scalability: performance increase when hardware resources increase
- agility: OS adapts to changes of either application needs or resource availiability
- responsiveness: OS reacts to external events, e.g. I/O for video games.

## Typical structures

### Monolithic structure

- In a monolithic OS, all the OS services (Files system, CPU Scheduling, Virtual Memory Management, etc.) as well as the OS core functionalities (IPC, Address Space, etc.) are located **within** the kernel. Everything is under the same address space.
- Each application has its own address space, which is separate from the OS address space. This ensures that applications cannot affect each other, and a malfunction of a specific application cannot affect the OS itself -> **Higher protection**.
- Whenever an application needs a service from the OS, we have to switch between the application’s address space to the OS’s address space.
- A Monolithic OS is not customizable -> **Lower flexibility**.

### DOS-like structure

- Similar to monolithic structure, but less strict. The application and the OS share the same address space -> **higher performance**.
- The application can access the OS services directly -> **lower protection**.

### Microkernel structure

- No policies ingrained in the microkernel, only mechanisms for accessing hardware resources.
- All OS services are implemented as services on top of microkernel, running in their own address spaces that separated with OS address space.
- Offers inter-process communication for applications to request os services and talk to each other.
- Allow customization, aka different replicas of the same services -> **higher flexibility**.
- Applications have to go through kernel to make system calls(IPC), added costs of border crossings, in addition to copying data between address spaces -> **Lower performance**.

### Summary

| Feature       | Monolithic OS | DOS-like OS | MicroKernel OS |
|---------------|:--------------|:------------|----------------|
| Extensibility |               | X           | X              |
| Protection    | X             |             | X              |
| Performance   | X             | X           |                |

The question is, can we have all three in an OS?

## The SPIN Approach

### Introduction

- Both SPIN and ExoKernel approaches aim to achieve extensibility of the OS without compromising protection or performance. Both start with two premises:
  - microkernel-based design compromises on performance due to frequent border crossings
  - monolithic approach is not extensible.
- What are we shooting for in OS structure?
  - Thin OS(like µKernel): only mechanism should be ingrained in the kernel, not polices.
  - Access to resources without border crossing(like DOS).
  - Flexibility for resource management (like µKernel) without sacrificing protection and performance(like monolithic)

### Approaches to Extensibility

- Hydra OS (Capability-based):
  - Just mechanisms, no polices, for resource allocation in the kernel.
  - **Capability-based** resource access: Capabilities are essentially like keys that are presented to the OS during access requests to ensure resource security. Each time a capability is passed from one object to another, its validity must be checked (which introduces overhead).
  - Resource managers are implemented as coarse-grained objects (large components) to reduce border crossings (also reduces extensibility).

- Mach OS (µKernel-based):
  - Provides very limited mechanisms in the µKernel.
  - Implements all the OS services as normal processes that run above the kernel (extensible + portable).
  - Low performance was a disadvantage in this structure.

- SPIN approach:
  - Co-location a minimal kernel and its extensions in the same space to avoid border crossings between the components of the kernel and the extensions of the kernels.
  - Compiler-enforced modularity to maintain protection (strongly-typed programming language).
  - **Logical protection domains**: Data structures provided by the Modula-3 programming language to serve as containers for the OS extensions, which free us from relying on the HW address spaces for protection.
  - **Dynamic call binding**: Extensions execute in response to system events. Events are declared within interfaces and can be dispatched with the overhead of a procedure call.

### Logical Protection Domains in SPIN

#### Modula-3

- Strongly-typed language with built-in safety and encapsulation mechanisms.
- Supports **objects** (known entry points - unknown implementation), **threads** (executes in the context of an object), exception and generic **interfaces** (to expose the externally-visible methods inside objects).
- Modula-3 safety features allows implementing system services as objects with well-defined entry points.
- What you can do from outside the object is only what the entry point methods allow you to do.
  - Which means we get the safety advantages of a Monolithic kernel without having to put the system services in a separate HW address space. This facilitates both protection and performance.
- The generic interfaces allow for creating multiple instances of the same service.
- Fine-grained protection via capabilities:
  - A HW resource can be an object (e.g. page frame).
  - An interface can be an object (e.g. page allocation module).
  - A collection of interfaces can be an object (e.g. virtual memory).
- Different from Hydra OS, in Modula-3, pointers can serve as capabilities to the objects.
  - Entry point functions within an object that is representing a specific resource, is provided via capabilities that are simply language supported pointers.

### SPIN Mechanisms for Protection Domains

- **Create**:
  - Creating a logical protection domain.
  - This mechanism allows initiating an object file with the contents and export the names that are contained as entry point methods inside the object to be visible outside.
- **Resolve**:
  - Resolves the names that are implemented in one object file (source) and used in another one (target).
  - Similar to linking in any compiler.
- **Combine**:
  - Combining the source and target protection domain to create an aggregate domain.
  - These mechanisms facilitate extensibility through creating and managing different domains of the same services customized for each application and running concurrently on the same HW.

#### An example of customized OS with SPIN

    <img src="https://i.imgur.com/Gj3jLP8.png" style="width: 800px" />

- All services, such as file system, scheduler, memory manager, network, are logical extensions of SPIN.
- P1/P2 live on top of the same hardware concurrently.
- Memory manager 1/2 implement the same functionalities but very differently to cater the the needs of different applications.

#### Example Extensions with SPIN

<img src="https://i.imgur.com/QGSH6Jr.png" style="width: 800px" />

- Left: implement unix OS baes on the extensions of SPIN
- Right: Only implement the functions for display and store video, without an OS.

### Spin Mechanisms for Events

- External events include:
  - External interrupts.
  - Exceptions.
  - System calls.
- SPIN uses an event-based communication model.
- Services can implement event handlers that are managed by the SPIN Event Dispatcher.
- SPIN supports different mapping mechanisms between events and handlers:
  - One-to-one.
  - One-to-many.
  - Many-to-one.

#### Default Core Services in SPIN

- Any OS should provide **core OS services** (CPU scheduling, memory management, etc.). However, an extensible OS, like SPIN, should not dictate how these services should be implemented. SPIN provides interface procedures for implementing these services:
  - **Memory management**:
    - The following interfaces are provided by SPIN as header functions (interfaces) to the extension implementer, who in turn should write the actual code for these header functions:
      - Physical address interfaces.
      - Virtual address interfaces.
      - Translation: Create/destroy address space, add/remove mapping.
      - Event handlers: Page fault, access fault, bad address.
  - **CPU scheduling**:
    - SPIN only decides at a macro level, the amount of time, that is given to a particular extension. That's done through the SPIN global scheduler.
      - SPIN global scheduler: Interacts with the different extension threads package that are concurrently running on top of SPIN.
      - SPIN provides an abstraction called **strand** which is the unit of scheduling that SPIN's global scheduler uses, but the semantics of the strand is decided by the extension that is running on top of SPIN.
      - Event handlers: Block, unblock, checkpoint, resume.

#### Conclusion

- Some deep implications that may not be obvious. Core services are trusted services, since they provide access to hardware mechanisms. These services may need to step outside the language-enforced protection model to control the hardware resources.
- Extension to core services affects only the applications that use that extension. That means if something goes wrong with a particular extension, other extensions will not be affected.

## The Exokernel Approach

### Introduction

<img src="https://i.imgur.com/54Ai6Ta.png" style="width: 800px" />

- The name Exokernel itself comes from the fact that the kernel exposes hardware explicitly to the operating system extensions living above it. The basic idea in Exokernel, is to **decouple authorization of the hardware** from its actual use.

- Exokernel processing steps:
    1. A library OS asks for a HW resource.
    2. Exokernel validates this request and bind the request to the HW resource (secure binding).
    3. After establishing the **secure binding**, Exokernel returns an encrypted key for the HW resource to the library OS.
    4. In order for the library OS to use the HW, it must present the encrypted key to the Exokernel.
    5. The Exokernel checks if the key is valid and validates whether the presenting library OS is the same one that requested the key or not.
    6. If the key is valid, the library OS gets access to the HW resource.

- **Establishing the secure binding is expensive (needs the kernel intervention) but using the kernel afterwards can happen at HW speed**.

- Example of Candidate Resources - TLB entry:
    1. The virtual-to-physical address mapping is done by the library OS.
    2. “Secure Binding” is presented to the Exokernel along with capability of the key.
    3. Exokernel validates the key and puts the mapping into the HW TLB (privileged operation).
    4. Processes inside this library OS can use the TLB multiple times without Exokernel intervention.

- Implementing Secure Bindings:
    1. **Hardware mechanisms** (e.g. TLB entry).
    2. **Software caching on behalf of each library OS.** Specifically the shadow TLB in the software data structure that is associated with each library OS, is to avoid the context switch penalty when switching library OS.
    3. **Downloading code into kernel** to avoid border crossing by inserting specific code that an operating system once executed on behalf of it.
        - This is similar to SPIN extension, and it compromises protection. This is more dangerous than the SPIN approach, since in SPIN extensions are created at compile time and follow the rules enforced by the programming language. On the other hand, in Exokernel we’re downloading arbitrary code into the kernel itself.

### Default Core Services in Exokernel

- **Memory management**:
  - What happens if a running process incurred a page fault?

        <img src="https://i.imgur.com/ufUVxDj.png" style="width: 800px" />

        1. Exokernel will upcall the page fault to the library OS through a “Registered Handler”.
        2. The library OS serves the page fault.
        3. The library OS performs the required mapping.
        4. This mapping is then presented to the Exokernel with the TLB entry.
        5. The Exokernel will validate the key and install the mapping into the HW TLB (privileged operations).

- **Secure Binding**:
  - **The library OS is given the ability to drop code into the kernel** itself.
  - This is intended to avoid border crossings and improve performance.
  - This greatly compromises protection.
  - The ability to create these extensions are restricted to only a trusted set of users to ensure protection.

- **Memory management using Soft-TLB**:

    <img src="https://i.imgur.com/HduE7g0.png" style="width: 800px" />

  - A method used by the Exokernel to implement Secure Bindings.
    - Since the address spaces occupied by two different library OSs are completely separate, a context switch requires flushing the TLB.
    - This produces a huge overhead for the new library OS to execute, because it will not find any of its addresses in the TLB.
  - The Exokernel creates a software TLB for each library OS to save **a snapshot of the HW TLB of this library OS**.
  - When a context switch happens, the Exokernel will **dump the contents of the HW TLP to the SW TLP** of the switched-from library TLB.
  - Then the Exokernel will **pre-load the HW TLP with the contents of the SW TLB** of the switched-to library OS.
  - This ensures that the library OS will find “some” of its mappings in the HW TLB.

- **CPU scheduling**:

    <img src="https://i.imgur.com/kkMSOG9.png" style="width: 800px" />

  - The Exokernel maintains a linear vector of “time slots”, where each library OS gets a time quantum.
  - Each library OS should mark its time quantum at startup.
  - The Exokernel is scheduling the CPU according to this time vector.
  - There's a penalty associated with exceeding the time quantum when the OS library misbehaves.
  - The Exokernel doesn’t interfere with a library OS during its time quantum, unless a process is running on behalf of the OS incurs a page fault.

### Revoking Resources

- The Exokernel keeps track of which HW resources have been allocated to the different library OS’s.
- The Exokernel provides a “repossession vector” to each library OS to describe the HW resources it’s revoking.
- The library OS takes the **corrective actions** to clean up these resources before giving them back to the kernel.
- These **corrective actions** can also be done by the kernel if the library OS indicated this by “seeding” the kernel for “autosave” beforehand.

### Conclusion

- The Exokernel maintains a boundary between the different library OS’s running on top of the kernel and the kernel itself, and also between the library OS’s.
- To improve performance, the Exokernel <u>provides the ability to “inject” code securely directly to the kernel</u>.
- If the running threads performed any operation out of its normal scope (e.g. system call, page fault, exception, etc.), or an external interrupt stopped the thread, a trap happens, and the Exokernel informs the library OS that the thread is to be discontinued. After that, the Exokernel runs another library OS according to the time vector.
- To facilitate the above scenario, the Exokernel maintains a state of each library OS living on top of it (**PE**(Portable Executable) Data Structure).
  - <img src="https://i.imgur.com/oEc6aXo.png" style="width: 800px" />
  - The PE data structure contains the entry points in the library operating system for dealing with the different kinds of program discontinuities. For example, **exceptions** that are thrown by the currently executing process has a specific entry point in the library operating system.
  - Per wiki, The PE format is a data structure that encapsulates the information necessary for the Windows OS loader to manage the wrapped executable code. This includes **dynamic library references for linking**, **API export and import tables**, **resource management data** and **thread-local storage (TLS) data**.

## The L3 Microkernel Approach

### Introduction

- The SPIN and Exokernel approaches originated from the assumption that microkernel-based systems are inherently inefficient and has poor performance. That’s because the popular microkernel-based OS back then, Mach-OS, was designed with portability as its most important goal.
- L3 microkernel approach was introduced to prove that performance is achievable with a microkernel-based OS.

- **Microkernel-based OS structure**:
  - The microkernel provides only core abstractions and has its own address space.
  - Many traditional OS services are implemented as processes on top of the microkernel. Each service has its own address space. These services run at the same privilege level as the user-level applications.
  - Communication between system services and user-level applications are done through the **Inter-process communication (IPC)**, which is provided by the microkernel.

- **Potential of performance loss**:
  - <img src="https://i.imgur.com/XiYe41O.png" style="width: 800px" />
  - border crossing has both explicit and implicit costs.
    - explicit: applications from user protection level slips into the microkernel at different privilege level.
    - implicit: several processes that involved in accomplishing the particular service.
  - Consulting services such as storage module requires **protected procedure calls**. Protected procedure calls are 100x times of normal procedure calls.
    - Because these services are in a micro-kernel based design are implemented in their own addresses. And we lose locality both in terms of address translations contains in the TLB and the content cache the processor uses to access memory.

### L3 Microkernel

- The L3 Microkernel provides the core OS abstractions (Address space - Threads - IPC - UID).
- The basic argument behind L3 is that we can achieve an efficient microkernel OS if we maintained proper implementation.
- The difference in L3 Microkernel is that it enforces that each of the system services has to be in its own “protection domain” not necessarily in its own distinct address space.
- L3's argument is, it's all about **efficient implementation of the microkernel** and not the principle of a microkernel based operating system structure.

- **The strikes against microkernel**:
    1. **Kernel-user switches**[explicitly]: The **border crossing cost** related to the communication between the user-level applications and the system services.
    2. **Address space switches**[explicitly]: The cost of Protected Procedure Calls between system services across protection domains.
    3. **Thread switches and IPC**[explicitly]: The thread switches happen with Protected Procedure Calls need the intervention of the kernel, which adds also the cost of inter-process communication.
    4. **Memory effects**[implicitly]: These different calls move between different address spaces, so with each call we need to switch address space, so we lose the TLB contents and the cache contents (locality loss), which make them very expensive.

- **L3 Microkernel improvements**:
    1. **border crossing**:
        1. L3 can perform a border crossing, including TLB and Cache misses, in only 123 processor cycles. Opposed to the 900 processor cycles that Mach-OS takes on the same HW (mainly because <u>Mach doesn’t take performance as its first priority</u>).
            - it's not that L3 improve anything, but simply put that it's equally the same as the other two design.
        2. The process actually takes 107 processor cycle to execute the machine instruction themselves, which makes the 123 cycles that the L3 takes very close to the minimum time.

    2. **Address space switches**:
        1. Whenever we switch from a specific address space to another, we might need to load the mappings of the new process to the TLB (perform TLB flush).
        2. This depends on whether the TLB has address space tags in addition to the normal virtual address tags. These TLBs are called “Address Space Tagged TLBs”.
        3. In an Address Space Tagged TLB, whenever we create a TLB entry, we not only save the tag of the virtual space address, but also the PID of the process for which this entry is being created.
        4. In an Address Space Tagged TLB, we don’t need to flush the TLB when we perform a context switch.
        5. This depends on the HW support. If the HW doesn’t support address space TLB tagging, some suggestions can work:
            - -> x86 - PowerPC: These architectures provide segment registers to bound the range of virtual addresses that can be legally accessed by a running process. We can use these segment registers to provide protection domains.
            - -> This way we’ll not need to flush TLB in case of context switch.
        6. If the protection domains are too large, and the HW doesn’t support address space TLB tagging, then a TLB flushing is inevitable.
        7. If we’re switching between large protection domains, the switching cost itself is not important, the cache and TLB costs (locality loss) will be dominant.

    3. **Thread switches and IPC**: // TODO don't get it.
        1. The explicit costs of the thread switching include saving all the volatile state of the processor in the thread context block.
        2. By construction, L3 shows that a microkernel is as competitive as SPIN and Exokernel in this area.

    4. **Memory effects**:
        1. L3 suggests that if we have small protection domains, we should pack them together in the same HW space and enforce protection using segment registers.
        2. If the protection domains are large, the cost cannot be mitigated.

### Mach-OS Border Crossings

- Mach-OS focus mainly on portability, and it doesn’t tailor any parts of the code to a specific HW. This results in a **large footprint for the code base**, which means **less locality and more cache misses**. This is the reason behind longer latency in border crossing.
- Portability and performance cannot be achieved together.

### L3 Thesis for OS Structuring

- **Minimal abstractions in the microkernel**: The microkernel should only include the basic OS abstractions (**Address space** - **Threads** - **IPC** - **UID**). These abstractions are needed by any subsystem running above the microkernel.
- Microkernels are **processor-specific in implementation**: You should take advantage of whatever the underlying HW is providing. This will **result in non-portability**.
- **L3 Microkernel** is **based on building processor-specific kernel** and **processor-independent abstractions** at the higher layer of the OS stack.
