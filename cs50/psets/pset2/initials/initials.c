#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>

int main(void)
{
    string str = get_string();
    if(str != NULL)
    {
        if(str[0] != ' ') 
        {
            printf("%c", toupper(str[0]));
        }
        
        int n = 0;
        while(str[n] != '\0')
        {
            if(str[n] == ' ' && str[n+1] != '\0' && str[n+1] != ' ')
            {
                printf("%c", toupper(str[n+1]));
            }
            n++;
        }
        printf("\n");
    }
}