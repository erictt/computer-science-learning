# Introduction

## What is an OS?

An operation system is a layer of systems software that:

- **directly** has privileges access to the underlying hardware;
    - e.g. **file eidtor** does not directly access hardware, but **file system** does
- hide hardware complexity
- manages hardware on behalf of one of more applications according to some predefined policies
- in addition, it ensures that applications are isolated and protected from one another

### OS Elements

Abstractions

- process, thread, file, socket, memory page

Mechanisms

- create, schedule, open, write, allocate

Policies

- least-recently used(LRU), earliest deadline first(EDF)

Lesson review

I learned:

1. what elements that an OS offers.

1.1. **Abstraction**: abstract a layer upon all of the hardwares.

1.2. **Arbitration**: Decide what hardware to use

1.3. **Mechanism**: methods to manage the resources, such as open/write/allocate

1.4. **Policies**: Algorithms to manage resources, such as LRU, EDF

2. How application use **System Calls** to manipulate the hardware. The concept of user/kernel mode. Applications run in user mode(unprivileged), and switch to Kernel model(privileged) via trap to call the System Call methods and then return to user mode.

3. Differnet design of OS, and some examples such as Linix and Mac.