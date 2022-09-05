# P1 Preparation

## C

### Basic Input/Output

```c
int main() {
    int x = 50;
    char hello[5] = "Hello";
    printf("%s World %d\n", hello, x); // Hello World 50
    printf("%3s World %d\n", hello, x); // llo World 50
    printf("%.*s World %d\n", 3, hello, x); // llo World 50
    int val;
    scanf("%d", &val); // read an interger from stdin, &val: the address of operator (pointer)
    printf("The val you intput: %d\n", val);
}
``` 

### String

* Different ways to declare a String

```c
char first_name[15] = "ANTHONY";
char first_name[15] = {'A','N','T','H','O','N','Y','\0'}; // NULL character '\0' is required at end in this declaration
char string1 [6] = "hello";/* string size = 'h'+'e'+'l'+'l'+'o'+"NULL" = 6 */
char string2 [ ] = "world";  /* string size = 'w'+'o'+'r'+'l'+'d'+"NULL" = 6 */
char string3[6] = {'h', 'e', 'l', 'l', 'o', '\0'} ; /*Declaration as set of characters ,Size 6*/
```

* `unsign long strlen()` return the size of string, use `\0` to identify the end.
* compare string: `if (strcmp(val, "Hello") == 0) {}`
* copy string: `int val[] = "hello"; char copy[20]; strcpy(copy, val);` copy from val to copy
* append string: `strcat(str, appendVal)`

### Pointer

```c
// some basic operations
int main() {
    int a = 1;
    int *b = &a; // create a pointer that store the location of a's value;
    
    printf("a=%d\n", a); 
    printf("b=%d\n", *b); // dereference the pointer *b;
    
    // change the value of a
    a = 2;
    *b = 2; // inderect update
    
    int c = 3;
    *b = &c; // b points to c now
}
```

```c
// change the value inside of function
void square(int *val) { // pass the pointer
    *val *= *val;
}

int main() {
    int i = 2;
    square(&i);
    printf("%d\n", i); // 4
    return 0;
}
```

```c
// array is different, when it passes to function, it automatically decay as a pointer.
void maxVal(int vals[], int size) { 
    // if you run sizeof(vals), it will return the size of the pointer not array.
    int max = vals[0];
    for (int i = 1; i < size; i++) {
        if (vals[i] > max) max = val[i];
    }
    return max;
}

int main() {
    int vals[] = {1, 2, 3, 4}; // vals is a pointer automatically
    int max = maxVal(vals, 4);
    printf("%d\n", max);
    return 0;
}
```

### Structs

```c

struct rectangle1 {
    int length;
    int width;
}

// equivelent to the firstone
typedef struct {
    int length;
    int width;
} rectangle2;

typedef struct {
    char[] owner;
    int pos;
    rectrangle2 rec;
} house;

int main() {
    struct rectangle1 firstRec = {5 ,10};
    rectangle2 secondRec = {5, 10}; // no need to write struct
    printf("Len: %d, width: %d\n", firstRec.length, firstRec.width);
    
    house mine = {"Eric", 1, {5, 10}};
    printf("%s's house: Len: %d, width: %d\n", mine.owner, mine.rec.length, mine.rec.width);
    
    house *structPointer = &mine; // use -> to access the attributes when you use pointers
    printf("%s's house: Len: %d, width: %d\n", structPointer->owner, structPointer->rec.length, structPointer->rec.width);    
    return 0;
}
```

### malloc / calloc / realloc / free

* malloc():  used to allocate a block of memory dynamically. It reserves memory space of specified size and returns the null pointer pointing to the memory location.
* calloc(): used to allocate multiple blocks of memory having the same size. 
* realloc(): for adding more memory size to already allocated memory blocks.
* free(): release or deallocate the memory blocks which are previously allocated by calloc(), malloc() or realloc() functions.

```c

typedef struct {
    char name[30];
    int age;
    bool verifed;
} user;
    
user *createUser(char name[], int age, bool verified) {
    user *newUser = malloc(sizeof(user));
    strcpy(newUser->name, name);
    newUser->age = age;
    newUser->verified = verified;
}

int main() {
    int size;
    printf("How many int elements u need? ");
    scanf("%d", &size); // prompt to user to input
    
    int *arr = malloc(size * sizeof(int)); // manually allocated memory need to be free manually as well.
    
    if (arr == 0) {
        printf("Invalid pointer. Error allocating memory\n");
        return -1; // exit the program;
    } else {
        printf("Good to go\n");
    }
    
    for (int i = 0; i < size; i++) {
        scanf("%d", &arr[i]); // prompt to user to input
    }
    printf("Array: \n");
    for (int i = 0; i < size; i++) {
        printf("arr[%d] = %d\n", i, arr[i]);
    }
    
    free(arr); // free the memory manually.
    
    user *me = createUser("Eric", 100, false);
    printf("Eric: %d\n", me->age);
    free(me);
}
```