# P1 Preparation

## C

### String

* Different ways to declare a String

```c
char first_name[15] = "ANTHONY";
char first_name[15] = {'A','N','T','H','O','N','Y','\0'}; // NULL character '\0' is required at end in this declaration
char string1 [6] = "hello";/* string size = 'h'+'e'+'l'+'l'+'o'+"NULL" = 6 */
char string2 [ ] = "world";  /* string size = 'w'+'o'+'r'+'l'+'d'+"NULL" = 6 */
char string3[6] = {'h', 'e', 'l', 'l', 'o', '\0'} ; /*Declaration as set of characters ,Size 6*/
```

### malloc / calloc / realloc / free

* malloc():  used to allocate a block of memory dynamically. It reserves memory space of specified size and returns the null pointer pointing to the memory location.
* calloc(): used to allocate multiple blocks of memory having the same size. 
* realloc(): for adding more memory size to already allocated memory blocks.
* free(): release or deallocate the memory blocks which are previously allocated by calloc(), malloc() or realloc() functions.

```c
#include <stdio.h>
#include <stdlib.h>
int main() {
  int i, *ptr, sum = 0;
  ptr = malloc(100);
  if (ptr == NULL) {
    printf("Error! memory not allocated.");
    exit(0);
  }

  ptr = realloc(ptr, 500);
  if (ptr != NULL)
    printf("Memory created successfully\n");

  free(ptr);

  return 0;
}
```

```c
#include <stdio.h>
#include <stdlib.h>

int main() {
  int i, *ptr, sum = 0;
  ptr = calloc(10, sizeof(int));
  if (ptr == NULL) {
    printf("Error! memory not allocated.");
    exit(0);
  }
  printf("Building and calculating the sequence sum of the first 10 terms n ");
  for (i = 0; i < 10; ++i) {
    *(ptr + i) = i;
    sum += *(ptr + i);
  }
  printf("Sum = %d", sum);
  free(ptr);
  return 0;
}
```

### Pointer