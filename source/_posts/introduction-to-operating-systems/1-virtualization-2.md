# Virtualizing The Memory

## Address Space

* The abstraction of physical memory, used for storing variables, code, stack, heap, etc. In C, when printing a pointer, the output is a virtual address. The OS has some instructions to map the virtual address to physical address in memory. The key of understanding memory is to understand how the address was mapped or **translated**.

* Some explanations about memory types:
    * Stack
        * is allocated and deallocated by the compiler **implicitly**, also called automatic memory. it's used to keep track of where the program is
            * e.g. `void func() { int x; }` // declares an integer on the desk, will be deallocated when function returns.
    * Heap
        * all allocations and deallocations are explicitly handled by programmers.
            * e.g. 
            
                ```
                void func() {
                    int *x = (int *) malloc(sizeof(int));
                    ...
                    free(x);
                }
                ```
            
                * **int *x**: the complier make room for the pointer
                * **malloc()**: requests spcae for an integer on the **heap**, return either the address of the integer or NULL if fails.
                    * notice if you print out the size of x: `printf("%d\n", sizeof(x));`, it's gonna be the size of pointer, not the integer.
                * **free()**: free the heap memory.

## Address Translation

* Short for **hardware-based address translation**, changing the virtual address provided by the instruction to a physical address. The OS was involved to **set up the hardware so that the correct translations** take place.

* The first approach of the translation management is called **Dynamic Reloation**. It requires two hardware registers within each CPU: `base` register, `bounds` register. Then the translation by the processer is: `physical address = virtual address + base`
    * the bounds register ensures that such addresses are within the conﬁnes of the address space.
    * the base and bounds registers are **hardware structures** kept on the chip (one pair per CPU) which is called **memory management unit(MMU)**.

* The second appoach is called **Segmentation**. Dynamic Relocation has two issues: 1. waste memory; 2. not flexible. Segmentation was born to solve these issues.
    * A segment is a contiguous portion of the address space of a particular length. Code, stack and heap all have different logically-different segments.
