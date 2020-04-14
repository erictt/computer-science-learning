#include <stdio.h>
#include <cs50.h>

int main(void)
{
    int height;
    do {
         printf("Height: ");
        height = get_int();    
    } while (height > 23 || height < 0);
    
    for(int i = 1; i <= height; i++)
    {
        for(int j = 1; j <= height - i; j++)
        {
            printf(" ");
        }
        int k = 2;
        do{
            for(int j = 1; j <= i; j++)
            {
                printf("#");
                
            }
            if(k == 2) printf("  ");
            k--;
        } while(k > 0);

        printf("\n");
    }

    
}