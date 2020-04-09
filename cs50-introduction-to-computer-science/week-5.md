# Week 5 - Data Structures

\[TOC\]

## Data Structure

### Linked Lists

#### Singly-Linked Lists

![](../.gitbook/assets/15032809637878%20%281%29.jpg)

* Structure

  ```c
    typedef struct sllist
    {
        VALUE val;
        struct sllist *next;
    }
    sllnode;
  ```

  * `VALUE` can be any type of data, `char`, `int`, etc.

* Create a linked list.
  * `sllnode* create(VALUE val);`
  * Steps
    * Dynamically allocate space for a new `sllnode`.
    * Check to make sure we didn't run out memory.
    * Initialize the node's `val` field.
    * Initialize the node's `next` field.
    * Return a pointer to the newly created `sllnode`.
* Search through a linked list to find an element.
  * `bool find(sllnode* head, VALUE val);`
  * Steps
    * Create a traversal pointer pointing to the list's head.
    * If the current node's val field is what we're looking for, report success.
    * If not, set the traversal pointer to the next pointer in the list and go back to step b.
    * If you've reached the end of the list, report failure.
  * The running time of this linear search will be `O(n)`, even if our list is sorted.
* Insert a new node into the linked list.
  * `sllnode* insert(sllnode* head, VALUE val);`
  * Steps
    * Dynamically allocate space for a new sllnode.
    * Check to make sure we didn't run out of memory.
    * Populate and insert the node **at the beginning of the linked list**.
    * Return a pointer to the new head of the linked list.
  * This would be `O(1)` if we didn’t want to keep the list sorted,
* Delete an entire linked list.
  * `void destroy(sllnode* head);`
  * Steps
    * If you've reach a null pointer, stop.
    * Delete the rest of the list.
    * Free the current node.
  * This will take `O(n)` since we’ll need to find the number want to delete first.

#### Doubly-Linked Lists

* A doubly-linked list, by contrast, allows us to move forward and backward through the list.
* Structure

  ```c
    typedef struct dllist
    {
        VALUE val;
        struct dllist *prev;
        struct dllist *next;        
    }
  ```

  * `VALUE` can be any type of data, `char`, `int`, etc.

* Insert a new node into the linked list.
  * `dllnode* insert(dllnode* head, VALUE val);`
  * Steps
    * Dynamically allocate space for a new dllnode.
    * Check to make sure we didn't run out of memory.
    * Populate and insert the node at the beginning of the linked list.
    * Fix the prev pointer of the old head of the linked list.
    * Return a pointer to the new head of the linked list.
  * This will take running time `O(n)`.
* Delete a node from a linked list.
  * `void delete (dllnode* target);`
  * Steps
    * Fix the pointers of the surrounding nodes to "skip over" target.
    * Free target.
  * This will take running time `O(1)`.
* Remember, we can never break the chain when rearranging the pointers.

### Stack

* A stack is a special type of structure that can eb used to maintain data in an organized way.
* This data structure is commonly implemented in one of two ways: as an **array** or as a **linked list**.
* In either case, if an element needs to be removed, the most recently added element is the only element that can legally be removed.
  * **Last in, first out** \(LIFO\).
* Operations
  * **push**: Add a new element to the top of the stack.
  * **pop**: Remove the most recently-added element from top.
* Structure 1
  * Array-based implementatoin

    ```c
      typedef struc _stack
      {
          VALUE array[CAPACITY];
          int top;
      }
      stack;
    ```

    * `VALUE` can be any type of data, `char`, `int`, etc.
    * `CAPACITY` is the maximum number of elements.
* **push**
  * `void push(stack* s, VALUE val);`
  * Steps
    * Accept a pointer to the stack.
    * Accept data of type VALUE to be added to the stack.
    * Add that data to the stack at the top of the stack.
    * Change the location of the top of the stack.
* **pop**
  * `VALUE pop(stack* s);`
  * Steps
    * Accept a pointer to the stack.
    * Change the location of the top of the stack.
    * Return the value that was removed from the stack.
* Structure 2
  * Linked-list based implementation

    ```c
    typedef struct _stack
    {
      VALUE val;
      struct _stack *next;
    }
    stack;
    ```
* **push**
  * Steps
    * dynamically allocate a new node, 
    * set its next pointer to point to the current head of the list,
    * then move the head pointer to he newly-created node.
* **pop**
  * Steps
    * traverse the linked list to its second element\(if it exists\), 
    * free the head of the list, 
    * then move the head pointer to the \(former\) second element.

### Queues

* data structure, same as stack.
* only different:
  * **First in, first out** \(FIFO\).
* Operations
  * **Enqueue**: Add a new element to the end of the queue.
  * **Dequeue**: Remove the oldest element from the front of the queue.
* Structure 1
  * Array-based implementation

    ```c
    typedef struct _queue
    {
      VALUE array[CAPACITY];
      int front;
      int size;
    }
    queue;
    ```
* **enqueue**
  * `void enqueue(queue* q, VALUE data);`
  * Steps
    * Accept a pointer to the queue.
    * Accept data of type VALUE to be added to the queue.
    * Add that data to the queue at the end of the queue.
    * Change the size of the queue.
* **dequeue**
  * `VALUE dequeue(queue* q);`
  * Steps
    * Accept a pointer to the queue.
    * Change the location of the front of the queue.
    * Decrease the size of the queue.
    * Return the value that was removed from the queue.
* Structure 2
  * Linked list-based implementation

    ```c
    typedef struct _queue
    {
      VALUE val;
      struct _queue *prev;
      struct _queue *next;        
    }
    queue;
    ```
* **enqueue**
  * `void enqueue(queue* q, VALUE data);`
  * Steps
    * Dynamically allocate a new node.
    * Set its next pointer to NULL, set its prev pointer to the tail.
    * Set the tail's next pointer to the new node.
    * Move the tail pointer to the newly-created node.
* **dequeue**
  * `VALUE dequeue(queue* q);`
  * Steps
    * Traverse the linked list to its second element\(if it exists\);
    * Free the head of the list;
    * Move the head pointer to the \(former\) second element;
    * Make that node's prev pointer point to NULL.

### Binary Search Tree

* ![](../.gitbook/assets/15032894082395%20%281%29.jpg)
  * Each node can only have a maximum of 2 children,
  * we can simply add new nodes by allocating memory for them and changing pointers to point to them.
* Structure

  ```c
    typedef struct node
    {
        int n;
        struct node *left;
        struct node *right;
    }
    node;
  ```

* use recursion to search:

  ```c
    bool search(int n, node* tree)
    {
        if (tree == NULL)
        {
            return false;
        }
        else if (n < tree->n)
        {
            return search(n, tree->left);
        }
        else if (n > tree->n)
        {
            return search(n, tree->right);
        }
        else
        {
            return true;
        }
    }
  ```

### Hash Tables

* ![](../.gitbook/assets/15032895917805.jpg)
* A hash table amounts to a combination of two things:
  * First, a **hash function**, which returns an nonnegative integer value called a **hash code**.

    ```text
      hash = hashfunc(key)
      index = hash % array_size
    ```

  * Second, an **array** capable of storing data of the type we with to place into the data structure.
* most hash table designs employ an imperfect hash function, which might cause hash **collisions** where the hash function generates the same index for more than one key. Such collisions must be accommodated in some way.

#### Collision resolution

* Linear probing
  * It is subject to a problem called **clustering**. Once there's a miss, two adjacent cells will contain data, making it more likely in the future that the cluster will grow.
* Separate chaining
  * Each bucket is independent, and has linked list of entries with the same index. 
    * The time for hash table operations is the time to find the bucket \(which is constant\) plus the time for the list operation.

### Tries

![](../.gitbook/assets/15033015224683.jpg)

```c
typedef struct _trie
{
    char name[45];
    struct _trie* paths[45];
}
trie;
```

* the struct of dictionary.

  ```c
    typedef struct Node
    {
        struct Node *children[INDICES_SIZE];
        bool is_word;
    }
    Node;
  ```

* the key program of load dictionary.

  ```c
    if (currentNode->children[indexNo] == NULL) 
    {
        // calloc = malloc + memset
        // calloc() zero-initializes the buffer, 
        // malloc() leaves the memory uninitialized. 
        // currentNode->children equals (*currentNode).children
        currentNode->children[indexNo] = calloc(1, sizeof(Node));
        currentNode->children[indexNo]->is_word = false;
    } 
    currentNode = currentNode->children[indexNo];
  ```

* Tries combine structures and pointers together to store data.
* Each array contains pointers to the next layer of arrays.
* The data to be searched for in the trie is now a roadmap.
* A trie has running time of `O(1)`, since we just need to look up words based on the letters in them, and that’s not affected by the number of other words in the trie. Inserting and removing a word, too, is also a constant time operation.

### Some Syntax of Pointers Supplement

```c
int x = 0;
int *px;
px = &x; // Stores the address of x in px
printf("%d\n", *px); // => Prints 0, the value of x
(*px)++; // Increment the value px is pointing to by 1

struct rectangle {
  int width;
  int height;
};

void function_1()
{
  struct rectangle my_rec;

  // Access struct members with .
  my_rec.width = 10;
  my_rec.height = 20;

  // You can declare pointers to structs
  struct rectangle *my_rec_ptr = &my_rec;

  // Use dereferencing to set struct pointer members...
  (*my_rec_ptr).width = 30;

  // ... or even better: prefer the -> shorthand for the sake of readability
  my_rec_ptr->height = 10; // Same as (*my_rec_ptr).height = 10;
}
```

## Refers

[https://en.wikipedia.org/wiki/Hash\_table](https://en.wikipedia.org/wiki/Hash_table) [http://docs.cs50.net/2016/fall/notes/5/week5.html](http://docs.cs50.net/2016/fall/notes/5/week5.html) [https://learnxinyminutes.com/docs/c/](https://learnxinyminutes.com/docs/c/)

