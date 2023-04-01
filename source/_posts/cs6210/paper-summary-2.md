# Paper Summary II

by Lei Yang(lyang423) @2023/04/01

```
Title: MapReduce: Simplified Data Processing on Large Clusters
Authors: Jeffrey Dean and Sanjay Ghemawat
```

## Introduction

Large-scale computational tasks often involve a two-step operation. The first step, the _map_ operation, calculates intermediate key/value pairs. The second step, the _reduce_ operation, aggregates the values of identical keys to produce the desired data combination. 

The primary goal of this paper is to utilize a simple yet powerful interface that facilitates automatic parallelization and distribution, thereby optimizing computation performance on large clusters of commodity personal computers (PCs). By leveraging this approach, the paper aims to achieve high efficiency and scalability in processing complex tasks on clusters of machines, ultimately enhancing the performance of large-scale computations.

## Programming Model

The model expresses the computation as two functions: **Map** and **Reduce**.
- **Map**: processes input pairs, producing intermediate key/value pairs, and forward them to the reduce function.
- **Reduce**: receive intermediate keys and associated set of values, aggragate the values to form a possibly smaller set of values.
The paper gives several examples, including distribute grep, count of URL access frequency, reverse web-link graph, etc.

## Implementation

![](https://i.imgur.com/BdYudrA.png)
- Overall workflow:
	1.  Input files are split into M pieces (typically 16-64 MB) and multiple program copies are initiated on a cluster.
	2.  One program copy acts as the master, assigning M map tasks and R reduce tasks to idle worker copies.
	3.  Assigned map tasks read input splits, parse key/value pairs, and pass them to the user-defined Map function. Intermediate pairs are buffered in memory.
	4.  Buffered pairs are periodically written to local disk, partitioned into R regions. The master forwards these locations to reduce workers.
	5.  Reduce workers read and sort the intermediate data, grouping occurrences of the same key together.
	6.  The reduce worker passes each unique key and corresponding values to the user’s Reduce function, appending output to the final output file.
	7.  Once all tasks are complete, the master signals the user program, and the MapReduce call returns to the user code.
- The master keeps several data strcutures such as the identity, task and state of each worker, and also conduit the intermediate file regoins for propagating map tasks to reduce tasks.
- MapReduce ensures fault tolerance through:
	1. Detecting and rescheduling failed tasks on idle workers.
	2. Write checkpoints of master to ensure fast recovery.
	3. Creating temporary output files and promoting them to final output files atomically to avoid inconsistencies.
- The master also take the location of input files into account to save network bandwidth.
- In practice, the pieces of map phase and reduce phase should be much larger than the number of workers to improve dynamic load balancing and failure recovery.
- To handle the problem of stragglers, MapReduce typically increase the computational resoruces by a few percent which significantly reduce the time to complete large operations.

## Reﬁnements

1.  **Partition Function**:  In addition to the default partitioning function, the user can provide a special functionto avoid imbalanced partitioning.
2. **Ordering Guarantees**: MapReduce guarantees the order of the intermediate key/value pairs within a given partition.
3.  **Combiner Function**: A user-specified function that aggregates intermediate key/value pairs on the map worker before transferring data to reduce workers, reducing network traffic and increasing efficiency.
4.  **Input and Output Types**: Allowing users to specify custom input and output types, enabling the system to handle various data formats and sources.
5. **Side-effects**: Tasks that produce multiple output ﬁles with cross-ﬁle consistency requirements should be deterministic.
6.  **Skipping Bad Records**: Implementing a mechanism to skip over problematic input records, enhancing fault tolerance and ensuring successful job completion despite occasional corrupt or ill-formatted data.
7. **Local Execution**: MapReduce offers an alternative implementation of the MapReduce library that sequentially executes all of the work for a MapReduce operation on the local machine for debugging, profiling, and small-scale testing.
8.  **Status Information**: Providing real-time status information about the ongoing computation, enabling users to monitor progress and diagnose issues.
9.  **Counters**: Offering user-defined counters to track global information during the MapReduce execution, facilitating debugging and optimization.

## Performance

The MapReduce paper evaluates the system using large-scale computations on clusters containing thousands of machines. Key insights include:

1.  **Scalability**: MapReduce efficiently distributes tasks, handling increasing workloads without performance degradation.
2.  **Fault Tolerance**: The system effectively handles worker failures by re-executing tasks, ensuring job completion.
3.  **Balancing and Stragglers**: MapReduce addresses stragglers with backup tasks, minimizing their impact on overall completion time.
4.  **Efficiency**: The system demonstrates competitive or superior performance compared to alternative solutions, attributed to its automatic parallelization and built-in optimizations.

## Experience

MapReduce has been used across a wide range od domains in Google. One of our most significant uses is the rewrite of the indexing system. The key benefits:

1. The code that deals with fault tolerance, distribution and parallelization is hidden by MapReduce.
2. Unrelated computations are separated.
3. Indexing proecss becomes eaiser to operate by leavraging MapReduce to handle the machine failures, networking hiccups, etc.

## Related Work

The paper compares MapReduce with variety of paarallel programming models such as Bulk Sysnchronous Programming, MPI, River, BAD-FS, TACC, etc. to emphise the key differences and similarities that MapReduce introduces, e.g. locality optimization and buckup taks mechanism.

## Conclusions

The MapReduce model is easy to use and can be adapted to a large variety of problems. In practise, restricting the model makes it easy to parallielize and distribute computations. Network bandwidth is a scarce resource with some optimization such as reading data from local disks. Redundant execution can be used to reduce the impact of slow machines.