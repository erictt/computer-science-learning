#include <stdio.h>
#include <cs50.h>
#include <string.h>

bool isAlphabetaChar(char str);
bool isAlphabetaStr(string str);

int main(int argc, string argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./vigenere k\n");
        return 1;
    }
    
    string keyword = argv[1];
    int keywordLen = strlen(keyword);
    if(!isAlphabetaStr(keyword))
    {
        printf("Usage: ./vigenere k\n");
        return 1;
    }
    
    printf("plaintext: ");
    string input = get_string();
    int inputLen = strlen(input);
    
    printf("ciphertext: ");
    int keyIndex = 0;
    for(int i = 0; i < inputLen; i++)
    {
        if(keyIndex == keywordLen)
        {
            keyIndex = 0;
        }
        
        int offset = 0;
        offset = (keyword[keyIndex] - 'A') % 32;
        
        int output = input[i];
        if(isAlphabetaChar(input[i]))
        {
            output = input[i] + offset;
            if((output > 'Z' && input[i] <= 'Z') || (output > 'z' && input[i] <= 'z'))
            {
                output -= 26;
            }
            
            keyIndex ++;
        }
        
        printf("%c", output);
        
    }
    printf("\n");
}

bool isAlphabetaChar(char c)
{
        if(c >= 'a' && c <= 'z')
        {
            return true;
        }
        else if(c >= 'A' && c <= 'Z')
        {
            return true;
        }
        else
        {
            return false;
        }
}

bool isAlphabetaStr(string str)
{
    for(int i = 0, n = strlen(str); i < n; i++)
    {
        if(isAlphabetaChar(str[i]))
        {
            continue;
        }
        else
        {
            return false;
        }
    }
    return true;
}