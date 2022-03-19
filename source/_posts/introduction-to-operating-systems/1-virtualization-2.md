# Virtualizing The Memory

## Memory Types

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
        
            * int *x: the complier make room for the pointer
            * malloc(): requests spcae for an integer on the **heap**, return either the address of the integer or NULL if fails.
                * notice if you print out the size of x: `printf("%d\n", sizeof(x));`, it's gonna be the size of pointer, not the integer.
            * free(): free the heap memory.

