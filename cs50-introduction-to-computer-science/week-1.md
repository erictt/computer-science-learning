# Week 1 - C

\[TOC\]

## Basic Linux Command

* `cd` for change directory, to move around to different folders
* `ls` which we’ve seen
* `mkdir` to make a directory
* `rm` to remove a file
* `rmdir` to remove a directory

## hello, C

* file `hello.c`

  ```c
   #include <stdio.h>

   int main(void)
   {
       printf("hello, world\n");
   }
  ```

* `~/workspace/ $ clang hello.c`
  * `clang` \(as in C language\) is a compiler, so we’re just asking it to compile our `hello.c` file.
  * `~/workspace/` just means that we’re in the folder called workspace in which `hello.c` lives
  * the default name for compiled programs is `a.out`, to run it with: `./a.out`
  * `~/workspace/ $ clang -o hello hello.c`, `-o` for `output` and specified it to be hello
* `~/workspace/ $ make hello`
  * This program will create a `hello` executable program from a source code file called `hello.c`

## The CS50 Libraries

* Libaries:
  * `get_char`
  * `get_double`
  * `get_float`
  * `get_int`
  * `get_long_long`
  * `get_string`
* `string.c` \(a string is just a sequence of characters\):

  ```c
    #include <cs50.h>
    #include <stdio.h>

    int main(void)
    {
        string name = get_string();
        printf("hello, %s\n", name);
    }
  ```

  * `cs50.h` contains the custom functions above,
  * `stdio.h` \(Standard Input and Output\) contains basic C functions like printf.

## Data Type

* There are lots of data types we’ll be using\(1 byte = 8 bits: 1 1 1 1 1 1 1 1\):
  * `bool` for a Boolean value \(true or false\), size: 1 byte
  * `char` for a single character, size: 1 byte
  * `double` for a large real number with more bits than a normal `float`, size: 8 bytes
  * `float`, size: 4 bytes
  * `int`, size: 4 bytes
  * `long` long for a large whole number with more bits than a normal `int`, size: 8 bytes
  * `string`, size: 8 bytes
* bugs
  * **overflow**: the number gets too big for the number of bits set aside for it.
  * **floating-point imprecision**: floats have a finite number of bits. But there are an infinite number of real numbers, so a computer has to round and represent some numbers inaccurately.

    ```c
      #include <stdio.h>

      int main(void)
      {
          printf("%.55f\n", 1.0 / 10.0);
      }
    ```

    * `%.55f`, just tells printf to print 55 digits after the decimal point.
    * when we run this, we get: `0.100000000000000000555111512312578...`

  * a few different data types that we can use, and also print with various symbols:

    ```text
      "%d";    // integer
      "%3d";   // integer with minimum of length 3 digits (right justifies text)
      "%s";    // string
      "%f";    // float
      "%ld";   // long
      "%3.2f"; // minimum 3 digits left and 2 digits right decimal float
      "%7.4s"; // (can do with strings too)
      "%c";    // char
      "%p";    // pointer
      "%x";    // hexadecimal
      "%o";    // octal
      "%%";    // prints %
    ```

  * escape sequences, symbols we can type, for printf to print tabs or quotes or others:

    ```text
      '\a'; // alert (bell) character
      '\n'; // newline character
      '\t'; // tab character (left justifies text)
      '\v'; // vertical tab
      '\f'; // new page (form feed)
      '\r'; // carriage return
      '\b'; // backspace character
      '\0'; // NULL character. Usually put at end of strings in C.
      //   hello\n\0. \0 used by convention to mark end of string.
      '\\'; // backslash
      '\?'; // question mark
      '\''; // single quote
      '\"'; // double quote
      '\xhh'; // hexadecimal number. Example: '\xb' = vertical tab character
      '\0oo'; // octal number. Example: '\013' = vertical tab character
    ```

## Some samples

* `if... else ...`:

  ```c
        #include <cs50.h>
        #include <stdio.h>

        int main(void)
        {
            char c = get_char();
            if (c == 'Y' || c == 'y')
            {
                printf("yes\n");
            }
            else if (c == 'N' || c == 'n')
            {
                printf("no\n");
            }
            else
            {
                printf("error\n");
            }
        }
  ```

* `switch case`:

  ```c
        #include <cs50.h>
        #include <stdio.h>

        int main(void)
        {
            char c = get_char();
            switch (c)
            {
                case 'Y':
                case 'y':
                    printf("yes\n");
                    break;
                case 'N':
                case 'n':
                    printf("no\n");
                    break;
                default:
                    printf("error\n");
                    break;
            }
        }
  ```

* `for` loop:

  ```c
        #include <cs50.h>
        #include <stdio.h>

        int main(void)
        {
            for (int i = 0; i < 3; i++)
            {
                printf("cough\n");
            }
        }
  ```

* **abstraction**:

  ```c
        #include <cs50.h>
        #include <stdio.h>

        void cough(int n);
        void say(string word, int n);
        void sneeze(int n);

        int main(void)
        {
            cough(3);
            sneeze(3);
        }

        void cough(int n)
        {
            say("cough", n);
        }

        void say(string word, int n)
        {
            for (int i = 0; i < n; i++)
            {
                printf("%s\n", word);
            }
        }

        void sneeze(int n)
        {
            say("achoo", n);
        }
  ```

### how the `make` command work

* preprocessing
  * Lines that start with `#`, like `#include`, are preprocessed. `#include` in particular makes our compiler look for the file somewhere on our computer and literally include them inside our files.
* compiling
  * We can run `clang -S hello.c` to see our C program compiled into another language called assembly language that has the very simple instructions that CPUs can understand.
* assembling
  * The intermediate assembly code is then translated into machine code, 0s and 1s, that the CPU can actually understand.
* linking
  * This final step takes the machine code of our program, and the machine code of all the libraries we included earlier and are using, and combines them so that the final program has all the pieces we need.

## Refers

* [http://docs.cs50.net/2016/fall/notes/1/week1.html](http://docs.cs50.net/2016/fall/notes/1/week1.html)

