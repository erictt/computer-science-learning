#define _XOPEN_SOURCE

#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <unistd.h>
#include <stdlib.h>

int calSizeOfPass(char tests[]);
void convertTestsToPassword(char tests[], char generatedPass[]);
int increaseTest(char tests[]);

int main(int argc, string argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./crack hash\n");
        return 1;
    }
    
    string hash = argv[1];
    char salt[2] = {hash[0], hash[1]};

    // initial the tests array
    char tests[] = "@@@A"; // {'A'-1, 'A'-1, 'A'-1, 'A'};
    
    int hitWall = 0;
    do {
        // calculate the new generated password's length
        int sizeOfPass = 2;
        sizeOfPass = calSizeOfPass(tests);
        // get the new password
        char generatedPass[sizeOfPass];
        convertTestsToPassword(tests, generatedPass);
        generatedPass[sizeOfPass-1]  = '\0';
        
        // try to crack the password
        string generatedHash = crypt(generatedPass, salt);
        // printf("size: %i, guess: %s, and hash: %s\n", sizeOfPass, generatedPass, generatedHash);
        if(strcmp(hash, generatedHash) == 0)
        {
            printf("%s\n", generatedPass);
            return 0;
        }
        
        hitWall = increaseTest(tests);

    } while(hitWall == 0);
    
    printf("can't find the password\n");
    return 2;
}

int calSizeOfPass(char tests[])
{
    int size = 0;
    for(int i = 0, n = strlen(tests); i < n; i++)
    {
        if(tests[i] >= 'A') {
            size ++;
        }
    }
    size ++;
    return size;
}

void convertTestsToPassword(char tests[], char generatedPass[])
{
    int index = 0;
    for(int i = 0, n = strlen(tests); i < n; i++)
    {
        if(tests[i] >= 'A') {
            generatedPass[index] = tests[i];
            index ++;
        }
    }
}

int increaseTest(char tests[])
{
    for(int n = strlen(tests), i = n - 1; i >= 0; i--)
    {
        if(tests[i] == 'Z') 
        {
            tests[i] = 'a';
            return 0;
        }
        else if(tests[i] < 'z') 
        {
            tests[i] ++;
            return 0;
        } else {
            tests[i] = 'A';
        }
    }
    return 0;
}
