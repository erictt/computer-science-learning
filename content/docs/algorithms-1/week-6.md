---
weight: 1
title: "Week 6 - Hash Tables"
---

# Week 6 - Hash Tables

## Hashing

* Save items in a **key-indexed table** (index is a function of the key).
* **Hash function**. Method for computing array index from key.
* **Issues**.
  * Computing the hash function.
  * Equality test: Method for checking whether two keys are equal.
  * Collision resolution: Algorithm and data structure to handle two keys that hash to the same array index.

* Implementing hash code: strings

    ```java
    public final class String {
        private int hash = 0;
        private final char[] s;
        ...
        public int hashCode() {
            int h = hash;
            if(h != 0) return h;
            int hash = 0;
            for (int i = 0; i < length(); i++)
                hash = s[i] + (31 * hash);
            hash = h;
            return h;
        }
    }
    ```

* Modular hashing
  * An int between -2^31 and 2^31 - 1.
  * **Hash function.** An int between 0 and M - 1 (for use as array index).

        ```java
        private int hash(Key key) { return (key.hashCode() & 0x7fffffff) % M;}
        ```

### Collisions

* Two distinct keys hashing to same index.
* Solutions: **separate chaining** and **linear probing**.

#### Collision resolution: Separate chaining symbol table

* **Use an array of M < N linked lists.**
  * Hash: map key to integer i between 0 and M - 1.
  * Insert: put at front of i^th chain (if not already there).
  * Search: need to search only i^th chain.
* <img src="https://i.imgur.com/ubxBtRh.jpg" style="width:400px" />
* Typical choice: M ~ N / 5 ⇒ constant-time ops.

#### Collision resolution: Open addressing

* **When a new key collides, find next empty slot, and put it there.**
  * Hash. Map key to integer i between 0 and M-1.
  * Insert. Put at table index i if free; if not try i+1, i+2, etc.
  * Search. Search table index i; if occupied but no match, try i+1, i+2, etc.
  * Note. Array size M **must be** greater than number of key-value pairs N.
* <img src="https://i.imgur.com/Am6yr2b.jpg" style="width:300px" />
* Typical choice: α = N / M ~ ½.
