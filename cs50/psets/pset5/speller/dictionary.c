/**
 * Implements a dictionary's functionality.
 */

#include <stdbool.h>
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "dictionary.h"

Node *root;
unsigned int numbersInDic;


int convertIndexFromChar(const char c) {
    int indexNo = c - 'a';
    if(c == '\'') {
        indexNo = 26;
        // indexNo = 'z' -'a' + 1;
        // printf("--------- %d\n", indexNo);
    }
    return indexNo;
}

/**
 * Returns true if word is in dictionary else false.
 */
bool check(const char *word)
{
    Node *currentNode = root;
    for(int i = 0; i < strlen(word); i++) 
    {
        int index = convertIndexFromChar(tolower(word[i]));
        if( currentNode->children[index] == NULL) 
            return false;
        else 
        {
            currentNode = currentNode->children[index];
        }
    }
    
    // printf("---------> dic size: %i\n", numbersInDic);    
    if(currentNode->is_word) 
    {
        return true;
    }
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
    
    root = malloc(sizeof(Node));
    root->is_word = false;
    memset(root, 0, sizeof(Node));

    Node *currentNode = root;
    
    for (int c = fgetc(fp); c != EOF; c = fgetc(fp))
    {
        if(c == ' ' || c == '\n')
        {
            numbersInDic++;
            currentNode->is_word = true;
            currentNode = root;
        }
        else if (isalpha(c) || c == '\'')
        {
            int indexNo = convertIndexFromChar(c);

            if (currentNode->children[indexNo] == NULL) 
            {
                currentNode->children[indexNo] = malloc(sizeof(Node));
                memset(currentNode->children[indexNo], 0, sizeof(Node));

                currentNode->children[indexNo]->is_word = false;
            } 
            currentNode = currentNode->children[indexNo];
            
        }
    }
    fclose(fp);

    return true;
}


/**
 * Returns number of words in dictionary if loaded else 0 if not yet loaded.
 */
unsigned int size(void)
{
    return numbersInDic;
}

/**
 * Unloads dictionary from memory. Returns true if successful else false.
 */
bool unload(void)
{
    unloadNode(root);
    
    return true;
}

void unloadNode(Node *node)
{
    int i = 0;
    while(i<INDICES_SIZE)
    {
        if(node->children[i] != NULL)
        {
            unloadNode(node->children[i]);
        }
        i++;
    }
    free(node);
}
