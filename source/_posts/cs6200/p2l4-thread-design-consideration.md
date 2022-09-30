# P2L4: Thread Design Considerations

<!-- toc -->
----

## Kernel Vs. User Level Threads



Thread Related Data Structures: Single CPU
Thread Data Structures: At Scale
Hard and Light Process State
Rationale For Data Structures
User Level Structures in Solaris 2.0
SunOS paper
Lightweight Threads paper
Kernel Level Structures in Solaris 2.0
Basic Thread Management Interaction
Thread Management Visibility and Design
Issue On Multiple CPUs
Synchronization Related Issues
Interrupts and Signals Intro
Interrupts
Signals
Signal/Interrupt Similarities
Interrupt Handling
Signal Handling
Why Disable Interrupts or Signals?
More on Signal Masks
Interrupts on Multicore Systems
Types of Signals
Interrupts as Threads
Interrupts: Top Vs. Bottom Half
Performance of Threads as Interrupts
Threads and Signal Handling
Tasks in Linux
