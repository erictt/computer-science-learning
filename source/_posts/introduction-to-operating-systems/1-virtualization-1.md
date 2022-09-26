# Virtualizing the CPU

[TOC]

* What are the goals for virtualization?
    * Efficiency
    * Security
        * processes should be isolated from each other

## The Abstraction: The Process

* What changes when a program runs?
    * registers (program counter, general purpose) // [what are registers?](https://www.learncomputerscienceonline.com/what-are-cpu-registers/)
    * I/O (disk, network)
    * memory(address space)
        * techincally, it's virtual memory.

## How to virtualize CPUs?

* The goal is to run N processes "at once" even we have M CPUs(N > M)

* Two key concepts:
    * Mechanisms: low-level methods or protocols that ensure processes running alternatively. e.g. **context switch**, which gives the OS the ability to stop one program and run another.
        * **Time sharing** is a basic technique used by an OS to share a resource. By allowing the resource to be used for a little while by one entity, and then a little while by another, and so forth.
    * Policies: on top of the mechanisms, policies are algorithms for making some kind of decision of which program to run within the OS.

* One example to explain the details: Assume we have one CPU and one process, then the procedure will be: 1) OS boot up; 2) Switch to program P; 3) program P exit and switch to OS;
    * The problems are:
        1. what if P wants to do something restricted? e.g. reading a file that it's not supposed to read.
        2. what if OS wants to stop P and run another program?
        3. what if P does something slow? e.g. disk I/O or network I/O
    * Solotions:
        * Problme 1: use a bit(0 and 1) to indicate the `mode of operation` (user mode or kernel mode)
            * application runs on user mode with limited access, and OS runs on kernel mode with no restriction. The mode switching procedure is called **trap instruction**.
            * There are lots of **system calls** like open(), read() and close() which require the CPU to switch to kernel mode to perform.
                * C has the same functions like open(), read(), but they are hidden inside the system call.
            * A complete example of the switching is:
                1) OS boot up and set up the **trap handler** and then switch to user mode to run program(this is called **return-from-trap**)
                2) The program runs in user mode and switch to kernel mode(this is called **trap**) to utilize system calls, and **return-from-trap** later on, then **exit()** eventually.
            * this whole mechanism is called **limited direct execution**
        * Problem 2: a **timer interrupt** is programmed in the CPU that interrupt processes every x ms, and a pre-conﬁgured **interrupt handler** in the OS runs.
            * The OS has a **scheduler** to decide what's the next step and execute a **context switch**. 
                * A context switch is conceptually simple: all the OS has to do is save a few register values for the currently-executing process (onto its kernel stack, for example) and restore a few for the soon-to-be-executing process (from its kernel stack).
        * Problem 3: Use process states. e.g. when a process initiated an I/O request to a disk, it becomes **blocked** and thus some other process can use the processor. Here are the other states:
            * <img src="https://i.imgur.com/tgM8fmf.jpg" style="width:300px" />
        * Running: a process is running
        * Ready: a process is ready, but OS has chosen not to run it at the moment
        * Blocked: waiting for other events to be finished. e.g. I/O request to disk or network.

