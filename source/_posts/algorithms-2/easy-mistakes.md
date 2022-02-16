# Easy Mistakes

## Condition Error

* In a while condition like `while (!qW.isEmpty() || !qV.isEmpty())`, make sure you need match both or just one.
* Make sure whether the question is asking for throw exception or return -1 like values
    * sometimes, the question require to return -1 if the parameter given is empty, and throw expection if the parameter is null.
* edge cases are really complicated, make sure check triple times and think of some different approaches to test the code.
    * for example, short path for `e.g. 1 0, 1 2, 2 3, 3 4, 4 5, 5 0 and check 3 and 1 (digraph2.txt)`
        * if start looping and return the first result we get, the distance will be 4 which is wrong.