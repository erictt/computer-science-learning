/**
 * Implements a dictionary's functionality.
 */

#include <stdbool.h>
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>

#include "dictionary.h"

const int INDICES_SIZE = 27;

typedef struct _trie
{
    struct _trie* trie[INDICES_SIZE];
    char* c;
}
Index;

struct _trie* root;

/**
 * Returns true if word is in dictionary else false.
 */
bool check(const char *word)
{
    printf("%s", word) ;
    return false;
}

/**
 * Loads dictionary into memory. Returns true if successful else false.
 */
bool load(const char *dictionary)
{
    FILE *fp = fopen(dictionary, "r");
    if (fp == NULL)
    {
        return false;
    }

    struct _trie* currentIndex = root;
    char *word = (char *)malloc(LENGTH);
    int i = 0;
    for (int c = fgetc(fp); c != EOF; c = fgetc(fp))
    {
        if(c == ' ' || c == '\n')
        {
            currentIndex->c = word;
            word = (char *)malloc(LENGTH);
            i = 0;
            currentIndex = root;
        }
        else if (isalpha(c) || c == '\'')
        {
            word[i++] = c;
            int indexNo = c - 'a';
            if(c == '\'') indexNo = c - 'z' + 1;
            struct _trie* tempIndex = NULL;
            currentIndex->trie[indexNo] = tempIndex;
            currentIndex = tempIndex;
        }
    }
    free(word);
    free(currentIndex);
    return false;
}

/**
 * Returns number of words in dictionary if loaded else 0 if not yet loaded.
 */
unsigned int size(void)
{
    // TODO
    return 0;
}

/**
 * Unloads dictionary from memory. Returns true if successful else false.
 */
bool unload(void)
{
    // TODO
    return false;
}

