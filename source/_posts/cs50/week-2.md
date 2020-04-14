# Week 2

## Cryptography

### String

* a sequence of characters, in an array (a list of things right next to each other) in memory.
* Sample with `string.h`:

    ```c
    #include <cs50.h>
    #include <stdio.h>
    #include <string.h>
    
    int main(void)
    {
        // ask user for input
        string s = get_string();
    
        // make sure get_string returned a string
        if (s != NULL)
        {
            // iterate over the characters in s one at a time
            for (int i = 0, n = strlen(s); i < n; i++)
            {
                // print i'th character in s
                printf("%c\n", s[i]);
            }
        }
    }
    ```
    
### Typecasting

* ASCII is a standrad for mapping characters to letters. Here are some sample ones:
       
    ``` 
    A   B   C   D   E   F   G   H   I  ...
    65  66  67  68  69  70  71  72  73  ...
     
    a   b   c   d   e   f   g   h   i   ...
    97  98  99  100 101 102 103 104 105 ...
    ```
    
    * We can experiment with this program:

        ```c
        #include <stdio.h>
        
        int main(void)
        {
            //  treat numbers like characters:
            for (int i = 65; i < 65 + 26; i++)
            {
                printf("%c is %i\n", (char) i, i);
            }
            
            //  we can also treat characters like numbers:
            for (char c = 'A'; c <= 'Z'; c++)
            {
                printf("%c is %i\n", c, c);
            }
        }
        ```
        
    * `toupper` in `<ctype.h>`, implements:

        ```c
        #include <cs50.h>
        #include <stdio.h>
        #include <string.h>
        
        int main(void)
        {
            string s = get_string();
            if (s != NULL)
            {
                for (int i = 0, n = strlen(s); i < n; i++)
                {
                    if (s[i] >= 'a' && s[i] <= 'z')
                    {
                        // ('a' - 'A') = 32
                        printf("%c", s[i] - ('a' - 'A'));
                    }
                    else
                    {
                        printf("%c", s[i]);
                    }
                }
                printf("\n");
            }
        }
        ```
        
### String in Memory

* `strlen`:

    ```c
    #include <cs50.h>
    #include <stdio.h>
    
    int main(void)
    {
        string s = get_string();
        int n = 0;
        while (s[n] != '\0') # \0 is end of the string, NOT space
        {
            n++;
        }
        printf("%i\n", n);
    }
    ```

* a string in C is just the location of the first character in memory, which are stored with a character at the end marking the end of a string, since there’s no predetermined length, so a string in memory really looks like:
        
    ```
    ------------------------------
    | Z | a | m | y | l | a | \0 |
    ------------------------------
    ```
    
    * And with `\0`, C indicates the end of our string.
    
* We can represent more of our computer’s memory as a grid:

    ```
    -----------------------------------
    | Z | a | m | y  | l | a | \0 | A |
    -----------------------------------
    | n | d | i | \0 |   |   |    |   |
    -----------------------------------
    |   |   |   |    |   |   |    |   |
    -----------------------------------
    |   |   |   |    |   |   |    |   |
    -----------------------------------
    ```
    
    * We can imagine each byte (each box in this grid) of memory as labeled from `0` to `31`, since there are 32 bytes total. In the sample, `Zamyla` start with `0`, and `Andi` start with `7`.

## Command-Line Arguments

```c
#include <cs50.h>
#include <stdio.h>

int main(int argc, string argv[])
{
    if (argc == 2)
    {
        printf("hello, %s\n", argv[1]);
    }
    else
    {
        printf("hello, world\n");
    }
}
```

```bash
~/workspace/ $ ./argv0 hello
hello, hello
```

* `argc` : argument count
* `argv` : argument vector, a list of strings
*  `argv[0]` is always the name of the program itself.

### `main`'s output

* `main` return a number `0` to indicate a program exists successfully. A non-zero number is used to present an error.:

    ```c
    #include <cs50.h>
    #include <stdio.h>
    
    int main(int argc, string argv[])
    {
        if (argc != 2)
        {
           printf("missing command-line argument\n");
           return 1;
        }
        printf("hello, %s\n", argv[1]);
        return 0;
    }
    ```
    
* We can use command `$?` to see the exit code in terminal, like this:

    ```
    ~/workspace/ $ ./exit
    missing command-line argument
    ~/workspace/ $ echo $?
    1
    ```

## Refers

* [http://docs.cs50.net/2016/fall/notes/2/week2.html](http://docs.cs50.net/2016/fall/notes/2/week2.html)

