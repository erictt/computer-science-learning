# Week 4

## Memory

* take memory as a rectangle:

    <img src="https://i.imgur.com/9aNd320.jpg" style="width:200px" />
            
    * "text": machine code
    * "data": variables
    * "stack": used for functions. Like the `main` function in C. When then next function called, will have its own chunk of memory. Each block is individually addressed.

## String

* `C` doesn't have `string` type data, it's the first char's address of the string in memory, ends with `\0`.
* So, `string s = get_string();` equals with `char *t = get_string();`. `s` and `t` are just the address of first character in memory. 
* compare two string ?
    
    ```c    
    #include <cs50.h>
    #include <stdio.h>
    #include <string.h>
    
    int main(void)
    {
        printf("s: ");
        char *s = get_string();
    
        printf("t: ");
        char *t = get_string();
    
        if (s != NULL && t != NULL)
        {
            // `strcmp` probably does that 
            // with a loop looking at the `i`th character in each string, 
            // comparing them one at a time.
            if (strcmp(s, t) == 0)
            {
                printf("same\n");
            }
            else
            {
                printf("different\n");
            }
        }
    }
    ```

* copy strings, don't forget to free the memory

    ```c
    #include <cs50.h>
    #include <ctype.h>
    #include <stdio.h>
    #include <string.h>
    
    int main(void)
    {
        printf("s: ");
        char *s = get_string();
        if (s == NULL)
        {
            return 1;
        }
    
        // malloc : allocates some memory. 
        // strlen(s)+1 : the plus one is for \0
        // sizeof(char): 1 byte, in case you forgot, refer to week 1's lecture for more details.
        char *t = malloc((strlen(s) + 1) * sizeof(char));
        if (t == NULL)
        {
            return 1;
        }
    
        for (int i = 0, n = strlen(s); i <= n; i++)
        {
            t[i] = s[i];
        }
    
        if (strlen(t) > 0)
        {
            t[0] = toupper(t[0]);
        }
    
        printf("s: %s\n", s);
        printf("t: %s\n", t);
    
        // make the habit of calling free on our manually allocated memory, 
        // which marks it as usable again.
        free(t);
    
        return 0;
    }
    ```

## Pointers

* a `swap` function to sway ints:

    ```c
    #include <stdio.h>

    void swap(int *a, int *b);
    
    int main(void)
    {
        int x = 1;
        int y = 2;
    
        printf("x is %i\n", x);
        printf("y is %i\n", y);
        printf("Swapping...\n");
        
        // & is pass the pointer to swap function, not the value.
        swap(&x, &y);
        printf("Swapped!\n");
        printf("x is %i\n", x);
        printf("y is %i\n", y);
    }
    
    // now to swap
    void swap(int *a, int *b)
    {
        // 1. set tmp to a's pointer
        int tmp = *a;
        // a pointer start to point to b's value
        *a = *b;
        // b pointer start to point to a's value
        *b = tmp;
        // so the fact is they just swap the pointer to each other's value
    }
    ```
    
## Memory Leaks

* `valgrind` is another command-line tool for checking memory leaks.
    * `valgrind --leak-check=full ./memory` // `./memory` is our commnd
* "Stack Overflow" is the term for stack that has grown too large, perhaps if we have a recursive function that calls itself too many times.
* "Heap Overflow" is the term for a heap that is too large, perhaps if we called `malloc` for large chunks of memory without ever calling `free`.
* "Buffer Overflow" is the overarching term for when too much data is placed into a finite amount of allocated space.
* For example:

    ```c   
    #include <string.h>

    void foo(char *bar)
    {
        char c[12];
        // copy from bar into c, for as many bytes as strlen(bar).
        memcpy(c, bar, strlen(bar));
    }
    
    int main(int argc, char *argv[])
    {
        foo(argv[1]);
    }
    ```
    
    <img src="https://i.imgur.com/8uXBoDh.jpg" style="width:260px" />

    * With a short string less than 12, it will be still ok. But if large than 12, it will overwritten with the address of the beginning of the string, even rewrite the main function:
    
        <img src="https://i.imgur.com/1SDa825.jpg" style="width:260px" />

## Images

* Each grid is a pixel, since an image has a finite size and thus finite information in it.
* JPEG 
    * JPEG files all start with the same three bytes, `255`, `216`, `255` as a standard, to indicate its filetype.
    * `255` in decimal is `1111 1111`, and `216` is `1101 1000`. Each of those four bits, since they can hold 16 values, map perfectly to hexadecimal. `1111` is `f`, `1101` is `d`, and `1000` is `8`. So `255` is the same as `ff`, and `216` is the same as `d8`. And it’s convention to write hexadecimal as `0xff` and `0xd8`.
* BMP

    <img src="https://i.imgur.com/rJGcuXe.jpg" style="width:360px" />

    * Files are just a sequence of bits, and if we think of each byte as having some offset from the beginning, we can specify exactly what should be in a file for it to be valid.

## Struct

* sample code:

    ```c
    typedef struct
    {
        string name;
        string dorm;
    }
    student;
    ```
    
    ```c
    #include <cs50.h>
    #include <stdio.h>
    #include <string.h>
    
    #include "structs.h"
    
    #define STUDENTS 3
    
    int main(void)
    {
        student students[STUDENTS];
    
        for (int i = 0; i < STUDENTS; i++)
        {
            printf("name: ");
            // to access the student's name   
            students[i].name = get_string();
    
            printf("dorm: ");
            students[i].dorm = get_string();
        }
    
        for (int i = 0; i < STUDENTS; i++)
        {
            printf("%s is in %s.\n", students[i].name, students[i].dorm);
        }
    }
    ```
    
* FILE, write into files

    ```c
    #include <cs50.h>
    #include <stdio.h>
    #include <stdlib.h>
    #include <string.h>
    
    #include "structs.h"
    
    #define STUDENTS 3
    
    int main(void)
    {
        student students[STUDENTS];
    
        for (int i = 0; i < STUDENTS; i++)
        {
            printf("name: ");
            students[i].name = get_string();
    
            printf("dorm: ");
            students[i].dorm = get_string();
        }
    
        FILE *file = fopen("students.csv", "w");
        if (file != NULL)
        {
            for (int i = 0; i < STUDENTS; i++)
            {
                fprintf(file, "%s,%s\n", students[i].name, students[i].dorm);
            }
            fclose(file);
        }
    }
    ```


