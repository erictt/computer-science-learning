#define _XOPEN_SOURCE
#define ALPHABET_COUNT 52

#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <unistd.h>

void fillAlphabet(char alphabet[]);

int main(int argc, string argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./crack hash\n");
        return 1;
    }
    
    string hash = argv[1];
    
    char salt[2] = {hash[0], hash[1]};
    
    // get "A-Za-z"
    char alphabet[ALPHABET_COUNT];
    fillAlphabet(alphabet);
    
    int first = 0;
    int second = -1;
    int third = -1;
    int forth = -1;
    
    do {
        // crack in here
        // guess password length manipulation
        int guessLength = 2;
        if(second >= 0) {
            guessLength ++;
        }
        if(third >= 0) {
            guessLength ++;
        }
        if(forth >= 0) {
            guessLength ++;
        }
        
        // generate password
        char guessPwd[guessLength];
        
        guessPwd[guessLength-1] = '\0';
        guessPwd[guessLength-2] = alphabet[first];
        
        if(second >= 0) {
            guessPwd[guessLength-3] = alphabet[second];
        }
        if(third >= 0) {
            guessPwd[guessLength-4] = alphabet[third];
        }
        if(forth >= 0) {
            guessPwd[guessLength-5] = alphabet[forth];
        }
        
        string generatedHash = crypt(guessPwd, salt);
        // printf("guessed password: %s, and hashed: %s\n", guessPwd, generatedHash);
        
        // try to crack the password
        if(strcmp(hash, generatedHash) == 0)
        {
            printf("%s\n", guessPwd);
            return 0;
        }
        
        // set indices
        if(first == ALPHABET_COUNT - 1) 
        {
            first = 0;
            second ++;
        }
        else // first index always changes
        {
            first ++;
        }
        if(second == ALPHABET_COUNT - 1)
        {
            first = 0;
            second = 0;
            third ++;
        }
        if(third == ALPHABET_COUNT - 1)
        {
            first = 0;
            second = 0;
            third = 0;
            forth ++;
        }

    } while(forth <= ALPHABET_COUNT);
    
    printf("can't find the password\n");
    return 2;
}

void fillAlphabet(char alphabet[])
{
    int index = 0;
    
    for(char i = 'A'; i <= 'Z'; i++)
    {
        alphabet[index] = i;
        index++;
    }
    for(int i = 'a'; i <= 'z'; i++)
    {
        alphabet[index] = i;
        index++;
    }
}
