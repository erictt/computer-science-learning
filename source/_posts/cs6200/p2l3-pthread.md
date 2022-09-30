# P2L2: PThread - Case Study

<!-- toc -->
----

## PThread Creation

```c
/* PThread Creation */ 

#include <stdio.h>
#include <pthread.h>

void *foo (void *arg) {		/* thread main */
	printf("Foobar!\n");
	pthread_exit(NULL);
}

int main (void) {

	int i;
	pthread_t tid;
	
	pthread_attr_t attr;
	pthread_attr_init(&attr); // Required!!!
	pthread_attr_setdetachstate(&attr, PTHREAD_CREATE_DETACHED);
	pthread_attr_setscope(&attr, PTHREAD_SCOPE_SYSTEM);
	pthread_create(&tid, &attr, foo, NULL);

	return 0;
}
```

* `int pthread_create(pthread_t *thread, const pthread_attr_t *attr, void * (*start_routine)(void *), void *arg);` = Fork(proc, args) in Birrell's design
    * `pthread_t *thread` the thread pointer
    * `onst pthread_attr_t *attr` the configuration options
    * `void * (*start_routine)(void *)` the run function
    * `void *arg` the config for the run function
    * return `int` whether creation success or not
* `int pthread_join(pthread_t thread, void **status);` = Join(thread) in Birrell's design
    * join a child thread 
* `pthread_attr_t` data structure allows to define features for the thread, such as:
    * stack size
    * scheduling policy
    * priority
    * system/process scope
    * inheritance
    * joinable
* passing `NULL` means take all default values for the attributes
* functions for managing attributes:
    
    ```
    int pthread_attr_init(pthread_attr_t *attr);
    int pthread_attr_destroy(pthread_attr_t *attr);
    pthread_attr_{set/get}{attribute};
    ```

* One mechanism not considered by Birrell is **detachable threads**. In pthreads, the default behavior for thread creation is joinable threads. For a joinable (child) thread, the parent will not terminate until the child has completed their execution. If the parent thread exits early, the child threads may turn into zombies.
* In Pthread, the child thread is allowed to be detached and continue to exist even parent exit.

    ```
    // two ways to detach:
    // 1.
    int pthread_detach(pthread_t thread);
      
    // 2.
    pthread_attr_setdetachstate(attr, PTHREAD_CREATE_DETACHED);
        
    // ...
        
    pthread_create(..., attr, ...);
    
    // to exit
    void pthread_exit(void *status);
    ```

### Example 1

```c
#define NUM_THREADS 4

void *hello (void *arg) { /* thread main */
	printf("Hello Thread\n");
	return 0;
}

int main (void) {
	int i;
	pthread_t tid[NUM_THREADS];
	
	for (i = 0; i < NUM_THREADS; i++) { /* create/fork threads */
		pthread_create(&tid[i], NULL, hello, NULL);
	}
	
	for (i = 0; i < NUM_THREADS; i++) { /* wait/join threads */
		pthread_join(tid[i], NULL);
	}
	return 0;
}
```

* simply create 4 threads and join them

### Example 2

```c
#define NUM_THREADS 4

void *threadFunc(void *pArg) { /* thread main */
	int *p = (int*)pArg;
	int myNum = *p;
	printf("Thread number %d\n", myNum);
	return 0;
}

int main(void) {
	int i;
	pthread_t tid[NUM_THREADS];
	
	for(i = 0; i < NUM_THREADS; i++) { /* create/fork threads */
		pthread_create(&tid[i], NULL, threadFunc, &i);
	}
	
	for(i = 0; i < NUM_THREADS; i++) { /* wait/join threads */
		pthread_join(tid[i], NULL);
	}
	return 0;
}
```

* L6 may output any number, because i is globally visible, all other threads see the new value. This situation is called **data race** or **race condition**. 

### Example 3

```c
#define NUM_THREADS 4

void *threadFunc(void *pArg) { /* thread main */
	int myNum = *((int*)pArg);
	printf("Thread number %d\n", myNum);
	return 0;
}

int main(void) {

	int i;
	int tNum[NUM_THREADS];
	pthread_t tid[NUM_THREADS];
	
	for(i = 0; i < NUM_THREADS; i++) { /* create/fork threads */
		tNum[i] = i;
		pthread_create(&tid[i], NULL, threadFunc, &tNum[i]);
	}
	
	for(i = 0; i < NUM_THREADS; i++) { /* wait/join threads */
		pthread_join(tid[i], NULL);
	}

	return 0;
}
```

* To solve the problem in example 2, in this example, we created an array to store a copy of i's value. This way, each thread will only access the `i`th value in the tNum array.

## PThread Mutexes

```c
// must be initialized before using it
int pthread_mutex_init(pthread_mutex_t *mutex, const pthread_mutexattr_t *attr);

// to lock and unlock
int pthread_mutex_lock(pthread_mutex_t *mutex);
int pthread_mutex_unlock(pthread_mutex_t *mutex);

// some interesting functions
// return immediately if the mutex cannot be acquired.
int pthread_mutex_trylock(pthread_mutex_t *mutex);

// free the pthread
int pthread_mutex_destroy(pthread_mutex_t *mutex);
```

### Mutex Safety Tips

* shared data should always be accessed through single mutex
* mutex scope must be global
* globally order locks - lock mutexes in order (to prevent deadlocks)
* always unlock the (correct) mutex

## PThread Condition Variables

```c
// When a thread enters this function, it immediately releases the mutex and 
// places itself on the wait queue associated with the condition variable. 
// When the thread is woken up, it will automatically reacquire the mutex before 
// exiting the wait operation.
int pthread_cond_wait(pthread_cond_t *cond, pthread_mutex_t *mutex);

// signal one waiting thread
int pthread_cond_signal(pthread_cond_t *cond);
// signal all waiting threads, but only one thread execute at a time.
int pthread_cond_broadcast(pthread_cont *cond);

int pthread_cond_init(pthread_cond_t *cond, const pthread_condattr_t *attr);
int pthread_cond_destroy(pthread_cond_t *cond);
```

### Condition Variable Safety Tips

* Don't forget to notify waiting threads!
    * When a condition changes, make sure to signal/broadcast the correct condition variable
* When in doubt use broadcast! 
    * Using broadcast incorrectly can incur a performance loss, but using signal incorrectly make cause your program to execute incorrectly.
* You don't need a mutex to signal/broadcast 
    * May be best to notify after unlocking mutex to prevent spurious wake ups.


## Producer and Consumer Example

```c
#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>

#define BUF_SIZE 3		/* Size of shared buffer */

int buffer[BUF_SIZE];  	/* shared buffer */
int add = 0;  			/* place to add next element */
int rem = 0;  			/* place to remove next element */
int num = 0;  			/* number elements in buffer */

pthread_mutex_t m = PTHREAD_MUTEX_INITIALIZER;  	/* mutex lock for buffer */
pthread_cond_t c_cons = PTHREAD_COND_INITIALIZER; /* consumer waits on this cond var */
pthread_cond_t c_prod = PTHREAD_COND_INITIALIZER; /* producer waits on this cond var */

void *producer (void *param);
void *consumer (void *param);

int main(int argc, char *argv[]) {

	pthread_t tid1, tid2;  /* thread identifiers */
	int i;

	/* create the threads; may be any number, in general */
	if(pthread_create(&tid1, NULL, producer, NULL) != 0) {
		fprintf(stderr, "Unable to create producer thread\n");
		exit(1);
	}

	if(pthread_create(&tid2, NULL, consumer, NULL) != 0) {
		fprintf(stderr, "Unable to create consumer thread\n");
		exit(1);
	}

	/* wait for created thread to exit */
	pthread_join(tid1, NULL);
	pthread_join(tid2, NULL);
	printf("Parent quiting\n");

	return 0;
}

/* Produce value(s) */
void *producer(void *param) {

	int i;
	for (i=1; i<=20; i++) {
		
		/* Insert into buffer */
		pthread_mutex_lock (&m);	
			if (num > BUF_SIZE) {
				exit(1);  /* overflow */
			}

			while (num == BUF_SIZE) {  /* block if buffer is full */
				pthread_cond_wait (&c_prod, &m);
			}
			
			/* if executing here, buffer not full so add element */
			buffer[add] = i;
			add = (add+1) % BUF_SIZE;
			num++;
		pthread_mutex_unlock (&m);

		pthread_cond_signal (&c_cons);
		printf ("producer: inserted %d\n", i);
		fflush (stdout);
	}

	printf("producer quiting\n");
	fflush(stdout);
	return 0;
}

/* Consume value(s); Note the consumer never terminates */
void *consumer(void *param) {

	int i;

	while(1) {

		pthread_mutex_lock (&m);
			if (num < 0) {
				exit(1);
			} /* underflow */

			while (num == 0) {  /* block if buffer empty */
				pthread_cond_wait (&c_cons, &m);
			}

			/* if executing here, buffer not empty so remove element */
			i = buffer[rem];
			rem = (rem+1) % BUF_SIZE;
			num--;
		pthread_mutex_unlock (&m);

		pthread_cond_signal (&c_prod);
		printf ("Consume value %d\n", i);  fflush(stdout);

	}
	return 0;
}
```
